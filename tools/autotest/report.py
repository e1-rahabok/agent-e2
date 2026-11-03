"""Aggregate answers.csv into report.md, and append one summary row per case to results.csv."""
import csv
import json
import math
import os
from collections import Counter, defaultdict


def _rows(run_dir):
    return [r for r in csv.DictReader(open(os.path.join(run_dir, 'answers.csv'))) if not r['error']]


def _mean(xs):
    xs = [float(x) for x in xs if x not in ('', None)]
    return sum(xs) / len(xs) if xs else float('nan')


def _pct(x):
    return '-' if math.isnan(x) else f'{100 * x:.0f}%'


def _margin(p, n):
    return 1.96 * math.sqrt(p * (1 - p) / n) if n and not math.isnan(p) else float('nan')


def aggregate(rows):
    """Per (model, mode, track): measures from the design doc."""
    groups = defaultdict(list)
    for r in rows:
        groups[(r['model'], r['mode'], r['track'])].append(r)
    out = {}
    for key, rs in groups.items():
        by_case = defaultdict(list)
        for r in rs:
            by_case[r['case_id']].append(r)
        majority, consistent, stable, luck, stable_unsure = [], [], [], [], []
        for cid, crs in by_case.items():
            answers = Counter(r['answer_letters'] for r in crs)
            top, _ = answers.most_common(1)[0]
            majority.append(int(top == crs[0]['correct']))
            consistent.append(int(len(answers) == 1))
            ex = [int(r['exact']) for r in crs]
            stable.append(int(all(ex)))                      # correct in every run: known, not guessed
            luck.append(int(any(ex) and not all(ex)))        # correct in some runs only: luck
            stable_unsure.append(int(all(int(r.get('unsure') or 0) for r in crs)))
        answered = [r for r in rs if not int(r.get('unsure') or 0)]
        n_cases = len(by_case)
        maj = _mean(majority)
        out[key] = {
            'answers': len(rs), 'cases': n_cases,
            'exact': _mean(r['exact'] for r in rs), 'partial': _mean(r['partial'] for r in rs),
            'majority': maj, 'margin': _margin(maj, n_cases), 'consistency': _mean(consistent),
            'stable': _mean(stable), 'stable_margin': _margin(_mean(stable), n_cases), 'luck': _mean(luck),
            'stable_unsure': _mean(stable_unsure), 'points': _mean(r.get('points') for r in rs),
            'unsure': _mean(r.get('unsure') for r in rs), 'answered_accuracy': _mean(r['exact'] for r in answered),
            'trap': _mean(r['trap'] for r in rs), 'not_covered': _mean(r['not_covered'] for r in rs),
            'parse_fail': 1 - _mean(r['parse_ok'] for r in rs),
            'recall': _mean(r['retrieval_recall'] for r in rs),
            'fallback': _mean(r['fallback'] for r in rs), 'steps': _mean(r['steps'] for r in rs),
            'tokens': _mean(int(r['prompt_tokens'] or 0) + int(r['completion_tokens'] or 0) for r in rs),
            'latency': _mean(r['latency'] for r in rs), 'cost': sum(float(r['cost_usd'] or 0) for r in rs),
        }
    return out


def write(run_dir):
    rows = _rows(run_dir)
    all_rows = list(csv.DictReader(open(os.path.join(run_dir, 'answers.csv'))))
    cfg = json.load(open(os.path.join(run_dir, 'config.json')))
    agg = aggregate(rows)
    L = [f'# Auto Test report: {cfg["run_id"]}', '',
         f'- Index version: `{cfg["index_version"][:12]}`. Retrieval: {cfg["retrieval"]}. Temperature: {cfg["temperature"]}. Runs: {cfg["runs"]}.',
         f'- Cases: {len(cfg["cases"])} multiple-choice. Skipped (not multiple-choice): {", ".join(cfg["skipped_cases"]) or "none"}.',
         f'- Answers: {len(rows)} scored, {len(all_rows) - len(rows)} failed.' + (' Mock run: scores are random.' if cfg.get('mock') else ''),
         '', '## Luck-free scores', '',
         '| Model | Mode | Track | Stable correct | ± margin | Luck | Stable unsure | Net points | Unsure | Accuracy when answered |',
         '|---|---|---|---|---|---|---|---|---|---|']
    for (m, mode, tr), s in sorted(agg.items(), key=lambda x: (x[0][2], -x[1]['stable'])):
        L.append(f'| {m} | {mode} | {tr} | {_pct(s["stable"])} | {_pct(s["stable_margin"])} | {_pct(s["luck"])} | '
                 f'{_pct(s["stable_unsure"])} | {_pct(s["points"])} | {_pct(s["unsure"])} | {_pct(s["answered_accuracy"])} |')
    L += ['', '- Stable correct: share of questions answered correctly in every run. The headline score: a known answer, not a guess.',
          '- Luck: share of questions correct in some runs but not all. Counted as not known.',
          '- Stable unsure: share of questions where the model chose Unsure in every run.',
          '- Net points: mean of +1 (exact), 0 (Unsure alone), -1 (anything else, including unparsed). Range -100% to +100%. Guessing does not raise it.',
          '- Accuracy when answered: exact share among answers that were not Unsure.', '',
         '## Scores', '',
         '| Model | Mode | Track | Exact | Partial | Majority | ± margin | Consistency | Trap | Parse fail | Recall | Fallback | Steps | Tokens | Latency s | Cost US$ |',
         '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for (m, mode, tr), s in sorted(agg.items(), key=lambda x: (x[0][2], -x[1]['majority'])):
        L.append(f'| {m} | {mode} | {tr} | {_pct(s["exact"])} | {_pct(s["partial"])} | {_pct(s["majority"])} | {_pct(s["margin"])} | '
                 f'{_pct(s["consistency"])} | {_pct(s["trap"])} | {_pct(s["parse_fail"])} | {_pct(s["recall"])} | {_pct(s["fallback"])} | '
                 f'{"-" if math.isnan(s["steps"]) else round(s["steps"], 1)} | {int(s["tokens"]) if not math.isnan(s["tokens"]) else "-"} | '
                 f'{"-" if math.isnan(s["latency"]) else round(s["latency"], 1)} | {s["cost"]:.3f} |')
    L += ['', '- Exact and Partial: mean over all runs. Majority: most common answer per question. Margin: 95% interval on Majority from the number of questions.',
          '- Consistency: share of questions answered identically in every run. Recall: share of the case `knowledge` ids the mode retrieved or read.', '']

    # per area and level, kb modes
    for dim in ('area', 'level'):
        vals = sorted({r[dim] for r in rows if r[dim]})
        if not vals:
            continue
        L += [f'## Exact score by {dim}', '', '| Model | Mode | ' + ' | '.join(vals) + ' |', '|---|---|' + '---|' * len(vals)]
        g = defaultdict(list)
        for r in rows:
            if r['track'] == 'text':
                g[(r['model'], r['mode'], r[dim])].append(r['exact'])
        for m, mode in sorted({(r['model'], r['mode']) for r in rows}):
            L.append(f'| {m} | {mode} | ' + ' | '.join(_pct(_mean(g[(m, mode, v)])) for v in vals) + ' |')
        L.append('')

    # worst questions
    per_case = defaultdict(list)
    for r in rows:
        if r['mode'] != 'baseline':
            per_case[r['case_id']].append(int(r['exact']))
    worst = sorted(per_case.items(), key=lambda x: _mean(x[1]))[:10]
    L += ['## Hardest questions (knowledge base modes)', '', '| Case | Exact | Common wrong answers |', '|---|---|---|']
    for cid, xs in worst:
        wrong = Counter(r['answer_letters'] or '(unparsed)' for r in rows if r['case_id'] == cid and r['mode'] != 'baseline' and r['exact'] == '0')
        L.append(f'| {cid} | {_pct(_mean(xs))} | ' + ', '.join(f'{k} ×{v}' for k, v in wrong.most_common(3)) + ' |')
    L += ['', 'Traces: `traces.jsonl` in this folder (one line per answer).', '']
    path = os.path.join(run_dir, 'report.md')
    open(path, 'w').write('\n'.join(L))
    return path


def append_summary(run_dir, results_csv):
    """One row per model, mode, track and case: mean exact score over the runs."""
    rows = _rows(run_dir)
    cfg = json.load(open(os.path.join(run_dir, 'config.json')))
    g = defaultdict(list)
    for r in rows:
        g[(r['model'], r['mode'], r['track'], r['case_id'])].append(r)
    exists = os.path.exists(results_csv)
    header = next(csv.reader(open(results_csv))) if exists else ['date', 'model', 'effort', 'mode', 'case_id', 'score', 'notes']
    with open(results_csv, 'a', newline='') as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(header)
        for (m, mode, tr, cid), rs in sorted(g.items()):
            score = _mean(r['exact'] for r in rs)
            d = cfg['run_id'][:8]
            w.writerow([f'{d[:4]}-{d[4:6]}-{d[6:8]}', m, 'n/a', f'{mode}-{tr}' if tr != 'text' else mode, cid, f'{score:.2f}',
                        f'autotest {cfg["run_id"]}; score = exact-match mean 0-1 over {len(rs)} runs; temp {cfg["temperature"]}'])
