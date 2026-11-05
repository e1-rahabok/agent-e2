"""Aggregate answers.csv into report.md, and append one summary row per question to results.csv."""
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


KINDS = ['multiple-choice', 'screenshot', 'conversation']


def _kind(r):
    return r.get('kind') or ('screenshot' if r['track'] == 'vision' else 'multiple-choice')


def _credit(r):
    """Credit of one answer, 0-1: exact letters (1 or 0), or judge score / 3."""
    v = r.get('credit')
    return float(v) if v not in ('', None) else float(r['exact'])


def _choice(r):
    return (r.get('format') or 'multiple-choice') == 'multiple-choice'


def final(rows):
    """Per (model, mode): final score and sub-scores, 0-1.

    Question credit = the lowest credit over its runs (the worst run counts, as Stable correct does for letters).
    Final = mean question credit over all questions; each question weighs the same. Sub-score = the same mean within one kind.
    A question with a vision track is scored on that track only.
    """
    g = defaultdict(lambda: defaultdict(list))
    for r in rows:
        g[(r['model'], r['mode'])][r['question_id']].append(r)
    out = {}
    for key, by_question in g.items():
        credit, kinds, luck, cw = {}, {}, [], []
        for cid, crs in by_question.items():
            if any(r['track'] == 'vision' for r in crs):
                crs = [r for r in crs if r['track'] == 'vision']
            cs = [_credit(r) for r in crs]
            credit[cid], kinds[cid] = min(cs), _kind(crs[0])
            luck.append(int(max(cs) > min(cs)))
            for r in crs:
                v = r.get('confident_wrong')
                cw.append(int(v) if v not in ('', None) else int(not int(r['exact']) and not int(r.get('unsure') or 0)))
        n = len(credit)
        f = sum(credit.values()) / n
        s = {'final': f, 'margin': _margin(f, n), 'questions': n, 'luck': sum(luck) / n, 'confident_wrong': _mean(cw),
             'override': override([r for crs in by_question.values() for r in crs])}
        for k in KINDS:
            xs = [credit[c] for c in credit if kinds[c] == k]
            s[k] = sum(xs) / len(xs) if xs else float('nan')
            s[k + '_n'] = len(xs)
        out[key] = s
    return out


def override(rows):
    """Share of answers that state the trap although every needed knowledge file was in the context.

    The knowledge base gave the correct reading, and the model answered from its own (Level 300) belief instead.
    Knowledge base modes only; nan when no answer had full retrieval recall.
    """
    full = [r for r in rows if r['mode'] != 'baseline' and r.get('retrieval_recall') not in ('', None)
            and float(r['retrieval_recall']) >= 1]
    return _mean(int(r.get('trap') or 0) for r in full) if full else float('nan')


def aggregate(rows):
    """Per (model, mode, track): measures from the design doc."""
    groups = defaultdict(list)
    for r in rows:
        groups[(r['model'], r['mode'], r['track'])].append(r)
    out = {}
    for key, rs in groups.items():
        by_question = defaultdict(list)
        for r in rs:
            by_question[r['question_id']].append(r)
        majority, consistent, stable, luck, stable_unsure = [], [], [], [], []
        for cid, crs in by_question.items():
            answers = Counter(r['answer_letters'] for r in crs)
            top, _ = answers.most_common(1)[0]
            majority.append(int(top == crs[0]['correct']))
            consistent.append(int(len(answers) == 1))
            ex = [int(r['exact']) for r in crs]
            stable.append(int(all(ex)))                      # correct in every run: known, not guessed
            luck.append(int(any(ex) and not all(ex)))        # correct in some runs only: luck
            stable_unsure.append(int(all(int(r.get('unsure') or 0) for r in crs)))
        answered = [r for r in rs if not int(r.get('unsure') or 0)]
        n_questions = len(by_question)
        maj = _mean(majority)
        out[key] = {
            'answers': len(rs), 'questions': n_questions,
            'exact': _mean(r['exact'] for r in rs), 'partial': _mean(r['partial'] for r in rs),
            'majority': maj, 'margin': _margin(maj, n_questions), 'consistency': _mean(consistent),
            'stable': _mean(stable), 'stable_margin': _margin(_mean(stable), n_questions), 'luck': _mean(luck),
            'stable_unsure': _mean(stable_unsure),
            'confident_wrong': _mean(int(not int(r['exact']) and not int(r.get('unsure') or 0)) for r in rs),
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
    all_scored = _rows(run_dir)
    all_rows = list(csv.DictReader(open(os.path.join(run_dir, 'answers.csv'))))
    cfg = json.load(open(os.path.join(run_dir, 'config.json')))
    fin = final(all_scored)
    rows = [r for r in all_scored if _choice(r)]  # letter-scored answers, for the multiple-choice tables
    agg = aggregate(rows)
    sample = next(iter(fin.values()), {})
    L = [f'# Benchmark report: {cfg["benchmark_id"]}', '',
         f'- Index version: `{cfg["index_version"][:12]}`. Retrieval: {cfg["retrieval"]}. Temperature: {cfg["temperature"]}. Runs: {cfg["runs"]}.',
         f'- Questions: {len(cfg["questions"])} (' + ', '.join(f'{k} {sample.get(k + "_n", 0)}' for k in KINDS) + ').'
         f' Skipped: {", ".join(cfg["skipped_questions"]) or "none"}. Judge: {cfg.get("judge_model") or "none"}.',
         f'- Answers: {len(all_scored)} scored, {len(all_rows) - len(all_scored)} failed.' + (' Mock run: scores are random.' if cfg.get('mock') else ''),
         '', '## Final score', '',
         '| Model | Mode | Final | ± margin | Multiple choice | Screenshot | Conversation | Luck | Confident wrong | Override |',
         '|---|---|---|---|---|---|---|---|---|---|']
    for (m, mode), s in sorted(fin.items(), key=lambda x: -x[1]['final']):
        L.append(f'| {m} | {mode} | {_pct(s["final"])} | {_pct(s["margin"])} | {_pct(s["multiple-choice"])} | '
                 f'{_pct(s["screenshot"])} | {_pct(s["conversation"])} | {_pct(s["luck"])} | {_pct(s["confident_wrong"])} | {_pct(s["override"])} |')
    L += ['', '- Final: mean question credit over all questions, 0-100%. Every question weighs the same.',
          '- Question credit = the worst of its runs. Multiple choice: 1 if exact in every run, else 0. Free text: lowest judge score / 3.',
          '- Sub-scores: the same mean within one kind. Screenshot = every question with an image, whatever its format. Conversation = free-text and compound questions without images.',
          '- Luck: share of questions whose credit differs between runs. Confident wrong: share of answers that are wrong and not Unsure (free text: judge score 0, not unsure).',
          '- Override: share of answers in knowledge base modes that state the trap although every needed file was in the context: the model kept its own belief over the knowledge base. Target: 0. See `benchmark/models.md`, section 1.',
          '- Method: `benchmark/design.md`, section 7.4.', '']
    conv = [r for r in all_scored if not _choice(r)]
    if conv:
        L += ['## Free-text answers (judge)', '', '| Model | Mode | Mean score 0-3 | Score 3 | Score 0 | Trap | Unsure |', '|---|---|---|---|---|---|---|']
        g = defaultdict(list)
        for r in conv:
            g[(r['model'], r['mode'])].append(r)
        for (m, mode), rs in sorted(g.items()):
            sc = [int(r['judge_score']) for r in rs]
            L.append(f'| {m} | {mode} | {sum(sc) / len(sc):.2f} | {_pct(_mean(int(x == 3) for x in sc))} | '
                     f'{_pct(_mean(int(x == 0) for x in sc))} | {_pct(_mean(r["trap"] for r in rs))} | {_pct(_mean(r["unsure"] for r in rs))} |')
        L.append('')
    L += ['## Multiple choice: luck-free scores', '',
         '| Model | Mode | Track | Stable correct | ± margin | Luck | Stable unsure | Confident wrong | Unsure | Accuracy when answered |',
         '|---|---|---|---|---|---|---|---|---|---|']
    for (m, mode, tr), s in sorted(agg.items(), key=lambda x: (x[0][2], -x[1]['stable'])):
        L.append(f'| {m} | {mode} | {tr} | {_pct(s["stable"])} | {_pct(s["stable_margin"])} | {_pct(s["luck"])} | '
                 f'{_pct(s["stable_unsure"])} | {_pct(s["confident_wrong"])} | {_pct(s["unsure"])} | {_pct(s["answered_accuracy"])} |')
    L += ['', '- Stable correct: share of questions answered correctly in every run. The headline score: a known answer, not a guess.',
          '- Luck: share of questions correct in some runs but not all. Counted as not known.',
          '- Stable unsure: share of questions where the model chose Unsure in every run.',
          '- Confident wrong: share of answers that are wrong and not Unsure (wrong letters, partly right, Unsure mixed with other letters, unparseable). The answers that mislead an operator. Target: near 0.',
          '- Accuracy when answered: exact share among answers that were not Unsure.', '',
         '## Multiple choice: scores', '',
         '| Model | Mode | Track | Exact | Partial | Majority | ± margin | Consistency | Trap | Parse fail | Recall | Fallback | Steps | Tokens | Latency s | Cost US$ |',
         '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for (m, mode, tr), s in sorted(agg.items(), key=lambda x: (x[0][2], -x[1]['majority'])):
        L.append(f'| {m} | {mode} | {tr} | {_pct(s["exact"])} | {_pct(s["partial"])} | {_pct(s["majority"])} | {_pct(s["margin"])} | '
                 f'{_pct(s["consistency"])} | {_pct(s["trap"])} | {_pct(s["parse_fail"])} | {_pct(s["recall"])} | {_pct(s["fallback"])} | '
                 f'{"-" if math.isnan(s["steps"]) else round(s["steps"], 1)} | {int(s["tokens"]) if not math.isnan(s["tokens"]) else "-"} | '
                 f'{"-" if math.isnan(s["latency"]) else round(s["latency"], 1)} | {s["cost"]:.3f} |')
    L += ['', '- Exact and Partial: mean over all runs. Majority: most common answer per question. Margin: 95% interval on Majority from the number of questions.',
          '- Consistency: share of questions answered identically in every run. Recall: share of the question `knowledge` ids the mode retrieved or read.', '']

    # per area and level, kb modes
    for dim in ('area', 'level'):
        vals = sorted({r[dim] for r in rows if r[dim]})
        if not vals:
            continue
        L += [f'## Multiple choice: exact score by {dim}', '', '| Model | Mode | ' + ' | '.join(vals) + ' |', '|---|---|' + '---|' * len(vals)]
        g = defaultdict(list)
        for r in rows:
            g[(r['model'], r['mode'], r[dim])].append(r['exact'])
        for m, mode in sorted({(r['model'], r['mode']) for r in rows}):
            L.append(f'| {m} | {mode} | ' + ' | '.join(_pct(_mean(g[(m, mode, v)])) for v in vals) + ' |')
        L.append('')

    # worst questions
    per_question = defaultdict(list)
    for r in all_scored:
        if r['mode'] != 'baseline':
            per_question[r['question_id']].append(_credit(r))
    worst = sorted(per_question.items(), key=lambda x: _mean(x[1]))[:10]
    L += ['## Hardest questions (knowledge base modes)', '', '| Question | Mean credit | Common wrong answers or missed points |', '|---|---|---|']
    for cid, xs in worst:
        wrong = Counter((r['answer_letters'] or '(unparsed)') if _choice(r) else (r.get('judge_missed') or f'score {r.get("judge_score")}')
                        for r in all_scored if r['question_id'] == cid and r['mode'] != 'baseline' and _credit(r) < 1)
        L.append(f'| {cid} | {_pct(_mean(xs))} | ' + ', '.join(f'{k} ×{v}' for k, v in wrong.most_common(3)).replace('|', '/') + ' |')
    L += ['', 'Traces: `traces.jsonl` in this folder (one line per answer).', '']
    path = os.path.join(run_dir, 'report.md')
    open(path, 'w').write('\n'.join(L))
    return path


def append_summary(run_dir, results_csv):
    """One row per model, mode, track and question: mean exact score over the runs."""
    rows = _rows(run_dir)
    cfg = json.load(open(os.path.join(run_dir, 'config.json')))
    g = defaultdict(list)
    for r in rows:
        g[(r['model'], r['mode'], r['track'], r['question_id'])].append(r)
    exists = os.path.exists(results_csv)
    header = next(csv.reader(open(results_csv))) if exists else ['date', 'model', 'effort', 'mode', 'question_id', 'score', 'notes']
    with open(results_csv, 'a', newline='') as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(header)
        for (m, mode, tr, cid), rs in sorted(g.items()):
            score = _mean(_credit(r) for r in rs)
            d = cfg['benchmark_id'][:8]
            w.writerow([f'{d[:4]}-{d[4:6]}-{d[6:8]}', m, 'n/a', f'{mode}-{tr}' if tr != 'text' else mode, cid, f'{score:.2f}',
                        f'benchmark {cfg["benchmark_id"]}; score = mean credit 0-1 (exact letters, or judge score / 3) over {len(rs)} runs; temp {cfg["temperature"]}'])
