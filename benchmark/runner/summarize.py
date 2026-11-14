#!/usr/bin/env python3
"""Summarize the run folders of one benchmark round into one analysis: benchmark/results/README.md.

The numbers come from the run folders (answers.csv, config.json, traces.jsonl) through report.py, the same code as each
run's report.md. The sentences under "Reading" are generated from the numbers by fixed rules, so a reader can check each
one against a table. Nothing is typed in by hand.

  python3 benchmark/runner/summarize.py                       # every run folder in benchmark/results
  python3 benchmark/runner/summarize.py --folders a b c d     # these folders only
"""
import argparse
import csv
import glob
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'harness'))
import report as R  # noqa: E402

REPO = 'https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/results'
E2 = 'agent-e2'
MODE_ORDER = {'baseline': 0, E2: 1, 'web': 2}
LEVEL_KEYS = [f'level:{x}' for x in R.LEVELS]


def _pts(x):
    return '-' if x is None or math.isnan(x) else f'{100 * x:+.0f}'


def load(folders):
    """Return rows of all folders (valid answers only), and the info of each folder."""
    rows, info = [], []
    for f in folders:
        cfg = json.load(open(os.path.join(f, 'config.json')))
        allrows = list(csv.DictReader(open(os.path.join(f, 'answers.csv'))))
        ok = [r for r in allrows if not r['error']]
        times = sorted(r['time'] for r in allrows if r.get('time'))
        judge_cost = _judge_cost(f, cfg, ok)
        info.append({'folder': os.path.basename(f), 'cfg': cfg, 'answers': len(ok), 'failed': len(allrows) - len(ok),
                     'first': times[0] if times else '', 'last': times[-1] if times else '',
                     'cost': sum(float(r['cost_usd'] or 0) for r in ok) + judge_cost, 'judge_cost': judge_cost,
                     'truncated': sum(1 for r in ok if str(r.get('truncated') or '0') == '1'),
                     'unparsed': sum(1 for r in ok if r['answer_type'] == 'deterministic' and str(r['parse_ok']) == '0')})
        rows += ok
    return rows, info


def _judge_cost(folder, cfg, ok):
    """Judge cost of one run: judge tokens from traces.jsonl when present, else the measured average per judged answer."""
    p = cfg.get('judge_pricing') or {}
    try:
        pin, pout = float(p['input']), float(p['output'])
    except (KeyError, TypeError, ValueError):
        return 0.0
    tin = tout = n = 0
    path = os.path.join(folder, 'traces.jsonl')
    if os.path.exists(path):
        for line in open(path):
            for s in json.loads(line)['trace']:
                if s['action'] == 'judge':
                    n += 1
                    tin += s.get('prompt_tokens') or 0
                    tout += s.get('completion_tokens') or 0
    if not n:
        n = sum(1 for r in ok if r['answer_type'] == 'judged')
        tin, tout = n * 1800, n * 340
    return tin * pin + tout * pout


def _minutes(i):
    import datetime as dt
    if not i['first']:
        return float('nan')
    return (dt.datetime.fromisoformat(i['last']) - dt.datetime.fromisoformat(i['first'])).total_seconds() / 60


def _lift(fin, model, a, b):
    """Score points of mode b over mode a for a model, with the margin of the difference (both margins combined)."""
    if (model, a) not in fin or (model, b) not in fin:
        return None, None
    d = fin[(model, b)]['final'] - fin[(model, a)]['final']
    m = math.hypot(fin[(model, a)]['margin'], fin[(model, b)]['margin'])
    return d, m


def reading(fin, rows, info, ref):
    """Sentences generated from the numbers. Each can be checked against a table."""
    out = []
    locals_ = sorted({m for m, _ in fin if m != ref[0]})
    for m in locals_:
        s = lambda mode: fin.get((m, mode), {}).get('final')      # noqa: E731
        parts = [f'{mode} {s(mode):.0%}' for mode in ('baseline', E2) if s(mode) is not None]
        line = f'{m}: ' + ', '.join(parts) + '.'
        d, mg = _lift(fin, m, 'baseline', E2)
        if d is not None:
            line += f' Agent E2 is {_pts(d)} points over the model alone ({"outside" if abs(d) > mg else "inside"} the margin of {100 * mg:.0f} points).'
        out.append(line)
    if ref in fin:
        best = max(locals_, key=lambda m: fin.get((m, E2), {}).get('final', -1), default=None)
        if best and (best, E2) in fin:
            gap = fin[(best, E2)]['final'] - fin[ref]['final']
            out.append(f'Best local model with Agent E2: {best}, {fin[(best, E2)]["final"]:.0%}; the frontier model without the knowledge base '
                       f'scores {fin[ref]["final"]:.0%}, a gap of {_pts(gap)} points (an outcome, not a gate).')
    passed = [m for m in locals_ if (m, E2) in fin and all(g[3] for g in R.gate(fin, rows, m, E2, ref)[:3])]
    out.append('Release gate on Agent E2 (final score, Level 400, confident wrong): ' +
               (f'passed by {", ".join(passed)}.' if passed else 'passed by no model.'))
    bad = [i for i in info if i['failed'] or i['truncated'] or i['unparsed']]
    for i in bad:
        out.append(f'Check {i["folder"]}: {i["failed"]} failed answers, {i["truncated"]} cut off at max_tokens, {i["unparsed"]} with no readable letter.')
    return out


def build(folders, today=None):
    rows, info = load(folders)
    fin = R.final(rows)
    ref = R.REFERENCE
    dates = sorted({i['folder'][:8] for i in info})
    cfg0 = info[0]['cfg']
    n_q = len(cfg0.get('questions') or [])
    L = [f'# Benchmark results: round of {dates[0][:4]}-{dates[0][4:6]}-{dates[0][6:]}', '',
         f'- {len(info)} runs, {n_q} questions, {cfg0.get("runs")} runs per question, sampling {json.dumps(cfg0.get("sampling")) if cfg0.get("sampling") else cfg0.get("temperature")}. '
         f'Judge: {cfg0.get("judge_model")}. Written by `benchmark/runner/summarize.py` from the run folders; every number below comes from them.',
         '- How to read a score: the exact value is read at plus or minus 5 points. The benchmark is a proof: Agent E2 against the release gate and the frontier reference. '
         'Method and scoring: [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md). '
         'Scores are not comparable with scores graded by another judge.', '']
    L += ['## Runs', '', '| Run folder | Model | Modes | Request settings | Answers | Failed | Cut off | First to last answer | Cost US$ (judge) |', '|---|---|---|---|---|---|---|---|---|']
    for i in info:
        c = i['cfg']
        m = list(c['models'])[0] if len(c['models']) == 1 else ', '.join(c['models'])
        prm = '; '.join(json.dumps(v) for v in (c.get('model_params') or {}).values()) or 'default'
        L.append(f'| [{i["folder"]}]({REPO}/{i["folder"]}/report.md) | {m} | {", ".join(c["modes"])} | `{prm}` | {i["answers"]} | {i["failed"]} | '
                 f'{i["truncated"]} | {_minutes(i):.0f} min | {i["cost"]:.2f} ({i["judge_cost"]:.2f}) |')
    L += ['', f'- Total cost US$ {sum(i["cost"] for i in info):.2f}. Agent E2: up-front blocks '
              f'{", ".join(k for k, v in (cfg0.get("primer") or {}).items() if v) or "none"}; case read by the model: {"on" if cfg0.get("case_model", True) else "off"}; '
              f'gap follow-up: {"on" if cfg0.get("gap_followup", True) else "off"}.', '']
    L += ['## Final score', '', '| Model | Mode | Final | ± margin | Level 100 | Level 200 | Level 300 | Level 400 | Confident wrong |', '|---|---|---|---|---|---|---|---|---|']
    for (m, mode), s in sorted(fin.items(), key=lambda x: (x[0][0] == ref[0], x[0][0], MODE_ORDER.get(x[0][1], 9))):
        L.append(f'| {m} | {mode} | **{s["final"]:.0%}** | {100 * s["margin"]:.0f} | ' + ' | '.join(R._pct(s[k]) for k in LEVEL_KEYS) + f' | {R._pct(s["confident_wrong"])} |')
    L += ['', 'Final = mean over the questions of the mean credit over the runs. Levels: the same mean within one level. The worst-run score is in each run folder\'s report.md (consistency; not a gate).', '']
    L += ['## Lift', '', 'Points of the final score. A difference is outside the margin when it is larger than the two margins combined.', '',
          '| Model | Agent E2 over the model alone |', '|---|---|']
    for m in sorted({m for m, _ in fin if m != ref[0]}):
        cells = []
        for a, b in (('baseline', E2),):
            d, mg = _lift(fin, m, a, b)
            cells.append('-' if d is None else f'{_pts(d)} ({"outside" if abs(d) > mg else "inside"} ±{100 * mg:.0f})')
        L.append(f'| {m} | ' + ' | '.join(cells) + ' |')
    L.append('')
    if ref in fin:
        L += ['## Release gate (Agent E2)', '', f'Reference: {ref[0]}, {ref[1]} mode. Limits: benchmark/design.md, section 7.5.', '', '| Model | Gate | Value | Limit | Pass |', '|---|---|---|---|---|']
        for m in sorted({m for m, mode in fin if mode == E2 and m != ref[0]}):
            for name, v, limit, ok in R.gate(fin, rows, m, E2, ref):
                L.append(f'| {m} | {name} | {v:.0%} | {limit} | {"-" if ok is None else "yes" if ok else "no"} |' if not name.startswith('Paired') else
                         f'| {m} | {name} | p {v:.3f} | {limit} | {"-" if ok is None else "yes" if ok else "no"} |')
        L += ['', 'Not read here: no up-front misconception (lines marked `up_front`) stated as true (author check of the answers), and the held-out set at most 11 points below the development set (a separate run).', '']
    if (cfg0.get('consensus_samples') or 1) <= 1 and (cfg0.get('runs') or 0) >= 3:
        L += R.consensus_table(fin, R.consensus(rows))[1:] + ['']
    L += ['## Reading', ''] + [f'- {x}' for x in reading(fin, rows, info, ref)] + ['']
    L += ['## Time and tokens', '', '| Model | Mode | Mean latency s | Mean model calls | Mean tokens |', '|---|---|---|---|---|']
    agg = R.aggregate(rows)
    best = {}
    for (m, mode, tr), a in agg.items():
        best.setdefault((m, mode), []).append(a)
    for (m, mode), xs in sorted(best.items(), key=lambda x: (x[0][0], MODE_ORDER.get(x[0][1], 9))):
        a = xs[0]
        L.append(f'| {m} | {mode} | {a["latency"]:.1f} | {a["steps"]:.1f} | {a["tokens"]:.0f} |')
    L += ['', 'Latency is the sum of the model calls of one answer (the judge is not in it). Per-run detail, hardest questions and consistency: the report.md of each run folder.', '']
    return '\n'.join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results')
    ap.add_argument('--folders', nargs='+', help='run folders (default: every folder of benchmark/results with a config.json)')
    ap.add_argument('--out', default=os.path.join(root, 'README.md'))
    a = ap.parse_args()
    folders = a.folders or sorted(os.path.dirname(p) for p in glob.glob(os.path.join(root, '*', 'config.json')))
    if not folders:
        sys.exit('No run folders.')
    text = build(folders)
    open(a.out, 'w').write(text)
    print(f'Wrote {a.out} ({len(folders)} runs)')


if __name__ == '__main__':
    main()
