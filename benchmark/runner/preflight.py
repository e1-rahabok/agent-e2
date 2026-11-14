#!/usr/bin/env python3
"""Preflight: prove on a small sample that a round will produce valid answers, before it runs for hours.

The first full benchmark found out after 2 hours that a reasoning model was cut off at the token cap on 85% of its
answers. Every check here would have caught that in two minutes. For each run of the round (model and modes) it:
  1. reads the account credits;
  2. answers a sample (4 multiple-choice, 2 judged, 1 screenshot question) in each mode, once per entry of the model's
     list `model_params` in config.yaml, in order, until one entry answers cleanly;
  3. checks the sample: no API error, readable letters, no answer cut off at max_tokens, completion tokens well under
     max_tokens, every mode answered;
  4. projects time and cost of the whole run from the sample (a small sample: the cost carries a safety factor).
A run that fails is not started. The sample runs through run.py, the code of the real run, with the real harness settings.

  python3 benchmark/runner/preflight.py                      # the release runs of config.yaml
  python3 benchmark/runner/preflight.py --models alibaba/qwen3.8-27b --json out.json
Exit code 0: every run passed. 4: at least one failed, or the credits do not cover the round. 6: the gateway refused (402, 401, 403).
"""
import argparse
import concurrent.futures as cf
import csv
import glob
import json
import os
import subprocess
import sys
import tempfile

import yaml

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'harness'))
import exitcodes as X  # noqa: E402
import questions as C  # noqa: E402

JUDGE_TOKENS = (1800, 340)      # judge prompt and reply tokens per judged answer, measured on 3,109 judge calls (2026-11-13)
JUDGE_SECONDS = 5.0             # judge latency per judged answer


def pick_sample(questions, n=7):
    """Evenly spaced questions so the sample is the same every time: 4 multiple-choice, 2 judged, the rest screenshot.
    With no judged question in the set (every question multiple choice since Q199, 2026-11-14), 6 multiple-choice."""
    ok = [c for c in questions if c.scorable]

    def spaced(items, k):
        if not items or k <= 0:
            return []
        step = max(len(items) // k, 1)
        return items[::step][:k]
    choice = [c for c in ok if c.choice and not c.has_images]
    judged = [c for c in ok if not c.choice and not c.has_images]
    vision = [c for c in ok if c.has_images]
    out = spaced(choice, 4 if judged else 6) + spaced(judged, 2) + spaced(vision, max(n - 6, 1))
    return out[:n]


def evaluate(rows, max_tokens, modes, min_parse_rate=0.95, max_token_share=0.5):
    """Judge one sample (the answers.csv rows). Return (problems, stats). No problem = the settings are good."""
    problems = []
    if not rows:
        return ['no answer was written'], {}
    errors = [r for r in rows if r.get('error')]
    if errors:
        problems.append(f'{len(errors)} of {len(rows)} answers failed: {errors[0]["error"][:160]}')
    got = {r['mode'] for r in rows if not r.get('error')}
    for m in modes:
        if m not in got:
            problems.append(f'mode {m}: no valid answer')
    good = [r for r in rows if not r.get('error')]
    mc = [r for r in good if r['answer_type'] == 'deterministic']
    if mc:
        rate = sum(1 for r in mc if str(r.get('parse_ok')) == '1') / len(mc)
        if rate < min_parse_rate:
            problems.append(f'only {rate:.0%} of multiple-choice answers have a readable letter (need {min_parse_rate:.0%})')
    cut = [r for r in good if str(r.get('truncated') or '0') == '1']
    if cut:
        problems.append(f'{len(cut)} of {len(good)} answers were cut off at max_tokens ({max_tokens})')
    stats = {}
    for m in modes:
        rs = [r for r in good if r['mode'] == m]
        if not rs:
            continue
        mean = lambda k: sum(float(r.get(k) or 0) for r in rs) / len(rs)       # noqa: E731
        stats[m] = {'n': len(rs), 'latency': mean('latency'), 'completion_tokens': mean('completion_tokens'),
                    'prompt_tokens': mean('prompt_tokens'), 'cost': mean('cost_usd'), 'steps': mean('steps')}
        if stats[m]['completion_tokens'] > max_token_share * max_tokens:
            problems.append(f'mode {m}: mean {stats[m]["completion_tokens"]:.0f} completion tokens, over {max_token_share:.0%} of max_tokens ({max_tokens})')
    return problems, stats


def project(stats, n_questions, runs, judged_share, concurrency, judge_cost):
    """Time (minutes) and cost (US$) of the whole run from the sample's per-mode means."""
    seconds = cost = 0.0
    for m, s in stats.items():
        n = n_questions * runs
        seconds += n * (s['latency'] + judged_share * JUDGE_SECONDS) / max(concurrency, 1)
        cost += n * (s['cost'] + judged_share * judge_cost)
    return seconds / 60, cost


def _judge_cost(meta, judge_model):
    p = (meta.get(judge_model) or {}).get('pricing') or {}
    try:
        return JUDGE_TOKENS[0] * float(p['input']) + JUDGE_TOKENS[1] * float(p['output'])
    except (KeyError, TypeError, ValueError):
        return 0.0


def run_sample(model, modes, ids, params, cfg_path, log):
    """Answer the sample through run.py. Return the answers.csv rows and the folder's log tail."""
    with tempfile.TemporaryDirectory(prefix='preflight-') as tmp:
        cmd = [sys.executable, os.path.join(os.path.dirname(__file__), 'run.py'), '--config', cfg_path, '--models', model,
               '--modes', ','.join(modes), '--runs', '1', '--questions', ','.join(ids), '--out', tmp,
               '--params', json.dumps({model: params} if params else {}), '--concurrency', '4', '--no-adaptive', '--no-health']
        p = subprocess.run(cmd, capture_output=True, text=True)
        files = glob.glob(os.path.join(tmp, '*', 'answers.csv'))
        rows = list(csv.DictReader(open(files[0]))) if files else []
        return rows, (p.stdout + p.stderr)[-600:]


def check_model(model, modes, ladder, cfg, cfg_path, sample, meta, pf, log):
    """Try the model's settings in order. Return the verdict dict."""
    ids = [c.id for c in sample]
    attempts = []
    for params in (ladder or [{}]):
        rows, tail = run_sample(model, modes, ids, params, cfg_path, log)
        max_tokens = (params or {}).get('max_tokens', cfg['max_tokens'])
        problems, stats = evaluate(rows, max_tokens, modes, pf['min_parse_rate'], pf['max_token_share'])
        attempts.append({'params': params, 'problems': problems})
        log(f'  {model} {json.dumps(params)}: ' + ('ok' if not problems else '; '.join(problems)))
        if any('HTTP 402' in p or 'HTTP 401' in p or 'HTTP 403' in p for p in problems):
            return {'model': model, 'ok': False, 'refused': True, 'params': params, 'problems': problems, 'attempts': attempts}
        if not problems:
            questions = [q for q in C.load() if q.scorable]
            judged_share = sum(1 for q in questions if not q.choice) / len(questions)
            return {'model': model, 'ok': True, 'params': params, 'stats': stats, 'attempts': attempts,
                    'n_questions': len(questions), 'judged_share': judged_share, 'max_tokens': max_tokens}
    return {'model': model, 'ok': False, 'problems': attempts[-1]['problems'], 'attempts': attempts}


def run_preflight(cfg, cfg_path, plan, client, log=print, only=None):
    """plan: [{model, modes}, ...]. Return the report dict: ok, refused, credits, runs{model: verdict}, projected cost and hours."""
    pf = cfg['release']['preflight']
    rel = cfg['release']
    meta = client.models()
    sample = pick_sample(C.load(), pf['questions'])
    log(f'Sample: {len(sample)} questions ({", ".join(c.id for c in sample)})')
    report = {'ok': True, 'refused': False, 'runs': {}, 'problems': []}
    try:
        report['credits'] = client.credits()
        log(f'Credits: US$ {report["credits"]:.2f}')
    except Exception as e:      # noqa: BLE001  credits is a courtesy check; the sample proves the key works
        report['credits'] = None
        log(f'Credits not readable ({e})')
    items = [p for p in plan if not only or p['model'] in only]
    with cf.ThreadPoolExecutor(max_workers=len(items) or 1) as ex:
        futs = {ex.submit(check_model, p['model'], p['modes'], (cfg.get('model_params') or {}).get(p['model']),
                          cfg, cfg_path, sample, meta, pf, log): p for p in items}
        for f in cf.as_completed(futs):
            p = futs[f]
            v = f.result()
            v['modes'] = p['modes']
            if v['ok']:
                conc = (cfg.get('concurrency_by_model') or {}).get(p['model'], cfg['concurrency'])
                v['minutes'], v['cost'] = project(v['stats'], v['n_questions'], cfg['runs'], v['judged_share'], conc,
                                                  _judge_cost(meta, cfg['judge_model']))
            report['runs'][p['model']] = v
            report['ok'] &= v['ok']
            report['refused'] |= bool(v.get('refused'))
    good = [v for v in report['runs'].values() if v['ok']]
    report['cost'] = sum(v['cost'] for v in good)
    report['cost_with_margin'] = report['cost'] * rel['cost_safety']
    report['hours'] = max([v['minutes'] for v in good] or [0]) / 60
    if report['credits'] is not None and report['cost_with_margin'] > report['credits']:
        report['ok'] = False
        report['problems'].append(f'credits US$ {report["credits"]:.2f} do not cover the projected US$ {report["cost_with_margin"]:.2f} '
                                  f'(US$ {report["cost"]:.2f} x {rel["cost_safety"]}): top up to at least US$ {report["cost_with_margin"]:.0f}')
    if report['cost_with_margin'] > rel['max_cost_usd']:
        report['ok'] = False
        report['problems'].append(f'projected cost US$ {report["cost_with_margin"]:.0f} is over max_cost_usd {rel["max_cost_usd"]}')
    if report['hours'] > rel['max_hours']:
        report['ok'] = False
        report['problems'].append(f'projected {report["hours"]:.1f} hours is over max_hours {rel["max_hours"]}')
    return report


def show(report, log=print):
    log('')
    log('| Model | Settings | Result | Projected time | Projected cost |')
    log('|---|---|---|---|---|')
    for m, v in sorted(report['runs'].items()):
        if v['ok']:
            log(f'| {m} | {json.dumps(v["params"])} | ok | {v["minutes"]:.0f} min | US$ {v["cost"]:.2f} |')
        else:
            log(f'| {m} | - | FAILED: {"; ".join(v["problems"])[:200]} | - | - |')
    log(f'Total projected: US$ {report["cost"]:.2f} (US$ {report["cost_with_margin"]:.2f} with the safety factor); slowest run {report["hours"]:.1f} h '
        f'(runs go in parallel; rough: the sample is small).')
    for p in report['problems']:
        log(f'PROBLEM: {p}')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--config', default=os.path.join(os.path.dirname(__file__), 'config.yaml'))
    ap.add_argument('--models', help='comma-separated: only these runs of the release plan')
    ap.add_argument('--json', help='write the report here')
    a = ap.parse_args()
    cfg = yaml.safe_load(open(a.config))
    from llm import GatewayClient
    client = GatewayClient(cfg['gateway'])
    report = run_preflight(cfg, a.config, cfg['release']['runs'], client, only=a.models.split(',') if a.models else None)
    show(report)
    if a.json:
        json.dump(report, open(a.json, 'w'), indent=2)
    sys.exit(X.OK if report['ok'] else X.BUDGET if report['refused'] else X.PREFLIGHT)


if __name__ == '__main__':
    main()
