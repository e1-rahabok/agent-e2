"""Aggregate answers.csv into report.md (one run folder)."""
import csv
import itertools
import json
import math
import os
from collections import Counter, defaultdict


def _mc(r):
    """The misconception flag of one answer row; results before 2026-11-11 call the column trap."""
    v = r.get('misconception', r.get('trap'))
    return float(v) if v not in (None, '') else 0


def _rows(run_dir):
    return [r for r in csv.DictReader(open(os.path.join(run_dir, 'answers.csv'))) if not r['error']]


def _mean(xs):
    xs = [float(x) for x in xs if x not in ('', None)]
    return sum(xs) / len(xs) if xs else float('nan')


def _pct(x):
    return '-' if math.isnan(x) else f'{100 * x:.0f}%'


def _margin(p, n):
    return 1.96 * math.sqrt(p * (1 - p) / n) if n and not math.isnan(p) else float('nan')


# Sub-score groups (benchmark/design.md, section 3). A question counts once per group; for input type it counts
# for every input it includes (a level 400 question with a table and a screenshot counts for both).
ANSWER_TYPES = ['deterministic', 'judged']
INPUT_TYPES = ['text', 'table', 'screenshot']
LEVELS = ['100', '200', '300', '400']


def _groups(r):
    """Sub-score keys of one answer row: answer type, input types, level."""
    at = r.get('answer_type') or ('deterministic' if (r.get('format') or 'multiple-choice') == 'multiple-choice' else 'judged')
    inputs = [x for x in (r.get('input') or '').split(' ') if x] or (['screenshot'] if r['track'] == 'vision' else ['text'])
    lv = str(r.get('level') or '')
    return [f'answer:{at}'] + [f'input:{x}' for x in inputs] + ([f'level:{lv}'] if lv in LEVELS else [])


def _credit(r):
    """Credit of one answer, 0-1: exact letters (1 or 0), or judge score / 3."""
    v = r.get('credit')
    return float(v) if v not in ('', None) else float(r['exact'])


def _choice(r):
    at = r.get('answer_type')
    return at == 'deterministic' if at else (r.get('format') or 'multiple-choice') == 'multiple-choice'


def final(rows):
    """Per (model, mode): final score and sub-scores, 0-1.

    Question credit = the mean credit over its runs: what one ask gets, on average, as a user asks once (author, 2026-11-13).
    Final = mean question credit over all questions; each question weighs the same.
    Worst run = the same mean with each question on its lowest credit over the runs: consistency, reported, not a gate.
    Sub-score = the same mean within one group: answer type, input type, level.
    A question with a vision track is scored on that track only.
    """
    g = defaultdict(lambda: defaultdict(list))
    for r in rows:
        g[(r['model'], r['mode'])][r['question_id']].append(r)
    out = {}
    for key, by_question in g.items():
        credit, worst, groups, luck, cw = {}, {}, {}, [], []
        for cid, crs in by_question.items():
            if any(r['track'] == 'vision' for r in crs):
                crs = [r for r in crs if r['track'] == 'vision']
            cs = [_credit(r) for r in crs]
            credit[cid], worst[cid], groups[cid] = sum(cs) / len(cs), min(cs), _groups(crs[0])
            luck.append(int(max(cs) > min(cs)))
            for r in crs:
                v = r.get('confident_wrong')
                cw.append(int(v) if v not in ('', None) else int(not int(r['exact']) and not int(r.get('unsure') or 0)))
        n = len(credit)
        f = sum(credit.values()) / n
        s = {'final': f, 'margin': _margin(f, n), 'questions': n, 'worst': sum(worst.values()) / n, 'luck': sum(luck) / n, 'confident_wrong': _mean(cw),
             'override': override([r for crs in by_question.values() for r in crs])}
        for k in [f'answer:{x}' for x in ANSWER_TYPES] + [f'input:{x}' for x in INPUT_TYPES] + [f'level:{x}' for x in LEVELS]:
            xs = [credit[c] for c in credit if k in groups[c]]
            s[k] = sum(xs) / len(xs) if xs else float('nan')
            s[k + '_n'] = len(xs)
        out[key] = s
    return out


def consensus(rows, k=3, modes=('agent-e2',)):
    """Per (model, mode): the scores the harness would get with consensus of k samples (cfg consensus_samples), projected
    from the recorded runs. Multiple choice: every draw of k runs out of the recorded ones; unanimous letters stand,
    anything else (disagreement, Unsure, unreadable) is Unsure: no credit, not confident wrong. Judged answers are kept
    as recorded: consensus applies to letters only (harness/modes.py, _consensus).
    The projection is the exact mean over all draws of the recorded runs, so it needs no new model call. It assumes the
    samples of one question are independent, as the runs of one question are.
    Returns {(model, mode): {final, confident_wrong, choice_confident_wrong, choice_unsure, k}}; questions with fewer
    than k runs are left out.
    """
    g = defaultdict(lambda: defaultdict(list))
    for r in rows:
        if r['mode'] in modes:
            g[(r['model'], r['mode'])][r['question_id']].append(r)
    out = {}
    for key, by_question in g.items():
        credit, cw, n_ans, c_cw, c_un, c_n = [], 0.0, 0, 0.0, 0.0, 0
        for crs in by_question.values():
            if any(r['track'] == 'vision' for r in crs):
                crs = [r for r in crs if r['track'] == 'vision']
            if len(crs) < k:
                continue
            if not _choice(crs[0]):
                credit.append(sum(_credit(r) for r in crs) / len(crs))
                cw += sum(int(r.get('confident_wrong') or 0) for r in crs)
                n_ans += len(crs)
                continue
            draws = list(itertools.combinations(crs, k))
            ok = wrong = 0
            for d in draws:
                letters = {r['answer_letters'] for r in d}
                if len(letters) == 1 and d[0]['answer_letters'] and not int(d[0].get('unsure') or 0):
                    ok += int(d[0]['exact'])
                    wrong += 1 - int(d[0]['exact'])
            credit.append(ok / len(draws))
            cw += wrong / len(draws) * len(crs)
            n_ans += len(crs)
            c_cw += wrong / len(draws)
            c_un += 1 - (ok + wrong) / len(draws)
            c_n += 1
        if credit and c_n:
            out[key] = {'final': sum(credit) / len(credit), 'confident_wrong': cw / n_ans, 'choice_confident_wrong': c_cw / c_n,
                        'choice_unsure': c_un / c_n, 'k': k}
    return out


# Release gate (benchmark/design.md, section 7.5; author, Q130, 2026-11-12). Read on Agent E2 (mode agent-e2, 2026-11-14).
# Not computed here: no up-front misconception (lines marked up_front) stated as true (author check of each answer),
# and the held-out set at most 11 points below the development set (a separate run).
GATE = {'final': 0.85, 'level:400': 0.80, 'confident_wrong': 0.03}
ALPHA = 0.05  # paired test against the frontier model: reported as an outcome, not a gate (author, 2026-11-13)
REFERENCE = ('anthropic/claude-opus-5.5', 'web')  # frontier model as a user meets it: web search available, its own choice to use it; no knowledge base (Q164, 2026-11-13)


def mcnemar(rows, model, mode, ref=REFERENCE):
    """Paired one-sided exact McNemar test of (model, mode) against the reference, on the questions both answered.

    A question is correct when its credit is 1 (exact in every run; judged: score 3 in every run).
    b = questions only the model gets right, c = questions only the reference gets right.
    Returns (b, c, p): p = P(X >= b) for X ~ Binomial(b + c, 0.5). nan when there is no discordant question.
    """
    credit = defaultdict(lambda: defaultdict(list))
    for r in rows:
        credit[(r['model'], r['mode'])][r['question_id']].append(_credit(r))
    a, z = credit.get((model, mode), {}), credit.get(ref, {})
    common = set(a) & set(z)
    b = sum(min(a[q]) == 1 and min(z[q]) < 1 for q in common)
    c = sum(min(a[q]) < 1 and min(z[q]) == 1 for q in common)
    n = b + c
    p = sum(math.comb(n, k) for k in range(b, n + 1)) / 2 ** n if n else float('nan')
    return b, c, p


def gate(fin, rows, model, mode='agent-e2', ref=REFERENCE):
    """Release gate rows for (model, mode): (name, value, limit, passed).

    The gap to the reference and its paired test follow as outcome rows: passed is None, they gate nothing.
    """
    s = fin[(model, mode)]
    out = [('Final score', s['final'], f'at least {GATE["final"]:.0%}', s['final'] >= GATE['final']),
           ('Level 400', s['level:400'], f'at least {GATE["level:400"]:.0%}',
            not math.isnan(s['level:400']) and s['level:400'] >= GATE['level:400']),
           ('Confident wrong', s['confident_wrong'], f'at most {GATE["confident_wrong"]:.0%}',
            not math.isnan(s['confident_wrong']) and s['confident_wrong'] <= GATE['confident_wrong'])]
    if ref in fin:
        gap = s['final'] - fin[ref]['final']
        b, c, p = mcnemar(rows, model, mode, ref)
        out += [('Gap to the frontier model', gap, 'outcome, not a gate', None),
                (f'Paired test (b {b}, c {c})', p, f'significant if p below {ALPHA}', None)]
    return out


def consensus_table(fin, proj):
    """Report lines: recorded scores next to the consensus projection (report and results summary)."""
    if not proj:
        return []
    k = next(iter(proj.values()))['k']
    L = ['', f'## Consensus of {k}, projected', '',
         f'What the shipped setting `consensus_samples: {k}` would give: multiple-choice letters stand only when {k} samples agree; '
         'otherwise Unsure. Projected from the recorded runs, no new model call (`report.py`, function `consensus`). Judged answers unchanged.', '',
         '| Model | Mode | Final | Final, consensus | Confident wrong | Confident wrong, consensus | Multiple choice: confident wrong, consensus | Multiple choice: Unsure, consensus |',
         '|---|---|---|---|---|---|---|---|']
    for key, p in sorted(proj.items()):
        s = fin.get(key, {})
        L.append(f'| {key[0]} | {key[1]} | {_pct(s.get("final", float("nan")))} | {_pct(p["final"])} | {_pct(s.get("confident_wrong", float("nan")))} | '
                 f'{_pct(p["confident_wrong"])} | {_pct(p["choice_confident_wrong"])} | {_pct(p["choice_unsure"])} |')
    return L


def override(rows):
    """Share of answers that state the misconception although every needed knowledge file was in the context.

    The knowledge base gave the correct reading, and the model answered from its own (Level 300) belief instead.
    Knowledge base modes only; nan when no answer had full retrieval recall.
    """
    full = [r for r in rows if r['mode'] != 'baseline' and r.get('retrieval_recall') not in ('', None)
            and float(r['retrieval_recall']) >= 1]
    return _mean(int(_mc(r) or 0) for r in full) if full else float('nan')


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
            'misconception': _mean(int(_mc(r) or 0) for r in rs),
            'parse_fail': 1 - _mean(r['parse_ok'] for r in rs),
            'recall': _mean(r['retrieval_recall'] for r in rs), 'steps': _mean(r['steps'] for r in rs),
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
         f'- Index version: `{cfg["index_version"][:12]}`. Retrieval: {cfg["retrieval"]}. Sampling: {json.dumps(cfg.get("sampling")) if cfg.get("sampling") else cfg["temperature"]}. Runs: {cfg["runs"]}.',
         f'- Questions: {len(cfg["questions"])} (' + ', '.join(f'{k} {sample.get("answer:" + k + "_n", 0)}' for k in ANSWER_TYPES) + '; '
         + ', '.join(f'{k} {sample.get("input:" + k + "_n", 0)}' for k in INPUT_TYPES) + '; '
         + ', '.join(f'level {k}: {sample.get("level:" + k + "_n", 0)}' for k in LEVELS) + ').'
         f' Skipped: {", ".join(cfg["skipped_questions"]) or "none"}. Judge: {cfg.get("judge_model") or "none"}.',
         f'- Answers: {len(all_scored)} scored, {len(all_rows) - len(all_scored)} failed.' + (' Mock run: scores are random.' if cfg.get('mock') else ''),
         '', '## Final score', '',
         '| Model | Mode | Final | ± margin | Worst run | Luck | Confident wrong | Override |',
         '|---|---|---|---|---|---|---|---|']
    for (m, mode), s in sorted(fin.items(), key=lambda x: -x[1]['final']):
        L.append(f'| {m} | {mode} | {_pct(s["final"])} | {_pct(s["margin"])} | {_pct(s["worst"])} | {_pct(s["luck"])} | '
                 f'{_pct(s["confident_wrong"])} | {_pct(s["override"])} |')
    if (cfg.get('consensus_samples') or 1) <= 1 and (cfg.get('runs') or 0) >= 3:
        L += consensus_table(fin, consensus(all_scored))
    cands = [k for k in fin if k[1] == 'agent-e2' and k != REFERENCE]
    if cands:
        L += ['', '## Release gate', '', f'Agent E2. Reference: {REFERENCE[0]}, {REFERENCE[1]} mode'
              + ('' if REFERENCE in fin else ' (not in this benchmark: gap not read)') + '.', '',
              '| Model | Gate | Value | Limit | Pass |', '|---|---|---|---|---|']
        for m, mode in sorted(cands):
            for name, v, lim, ok in gate(fin, all_scored, m, mode):
                val = f'{v:.3f}' if name.startswith('Paired') and not math.isnan(v) else _pct(v)
                L.append(f'| {m} | {name} | {val} | {lim} | {"-" if ok is None else "yes" if ok else "no"} |')
        L += ['', '- Not read here: no up-front misconception (lines marked `up_front`) stated as true (author check), and the held-out set at most 11 points below the development set (separate run). Method: `benchmark/design.md`, section 7.5.']
    L += ['', '## Sub-scores', '',
          '| Model | Mode | Deterministic | Judged | Text | Table | Screenshot | Level 100 | Level 200 | Level 300 | Level 400 |',
          '|---|---|---|---|---|---|---|---|---|---|---|']
    for (m, mode), s in sorted(fin.items(), key=lambda x: -x[1]['final']):
        keys = [f'answer:{x}' for x in ANSWER_TYPES] + [f'input:{x}' for x in INPUT_TYPES] + [f'level:{x}' for x in LEVELS]
        L.append(f'| {m} | {mode} | ' + ' | '.join(_pct(s[k]) for k in keys) + ' |')
    L += ['', '- Final: mean question credit over all questions, 0-100%. Every question weighs the same.',
          '- Question credit = the mean of its runs. Deterministic: share of runs with the exact letters. Judged: mean judge score / 3. Worst run: the same score with each question on its lowest run (consistency; not a gate).',
          '- Sub-scores: the same mean within one group. By answer type, by input type (a question counts for every input it includes), by level.',
          '- Luck: share of questions whose credit differs between runs. Confident wrong: share of answers that are wrong and not Unsure (judged: score 0, not unsure).',
          '- Override: share of Agent E2 answers that state the misconception although every needed file was in the context: the model kept its own belief over the knowledge base. Target: 0. See `benchmark/models.md`, section 1.',
          '- Method: `benchmark/design.md`, sections 3 and 7.4.', '']
    conv = [r for r in all_scored if not _choice(r)]
    if conv:
        L += ['## Judged answers', '', '| Model | Mode | Mean score 0-3 | Score 3 | Score 0 | Misconception | Unsure |', '|---|---|---|---|---|---|---|']
        g = defaultdict(list)
        for r in conv:
            g[(r['model'], r['mode'])].append(r)
        for (m, mode), rs in sorted(g.items()):
            sc = [int(r['judge_score']) for r in rs]
            L.append(f'| {m} | {mode} | {sum(sc) / len(sc):.2f} | {_pct(_mean(int(x == 3) for x in sc))} | '
                     f'{_pct(_mean(int(x == 0) for x in sc))} | {_pct(_mean(int(_mc(r) or 0) for r in rs))} | {_pct(_mean(r["unsure"] for r in rs))} |')
        L.append('')
    L += ['## Deterministic answers: luck-free scores', '',
         '| Model | Mode | Track | Stable correct | ± margin | Luck | Stable unsure | Confident wrong | Unsure | Accuracy when answered |',
         '|---|---|---|---|---|---|---|---|---|---|']
    for (m, mode, tr), s in sorted(agg.items(), key=lambda x: (x[0][2], -x[1]['stable'])):
        L.append(f'| {m} | {mode} | {tr} | {_pct(s["stable"])} | {_pct(s["stable_margin"])} | {_pct(s["luck"])} | '
                 f'{_pct(s["stable_unsure"])} | {_pct(s["confident_wrong"])} | {_pct(s["unsure"])} | {_pct(s["answered_accuracy"])} |')
    L += ['', '- Stable correct: share of questions answered correctly in every run: a known answer, not a guess. Consistency, not the final score (the final score is the mean of the runs).',
          '- Luck: share of questions correct in some runs but not all. Counted as not known.',
          '- Stable unsure: share of questions where the model chose Unsure in every run.',
          '- Confident wrong: share of answers that are wrong and not Unsure (wrong letters, partly right, Unsure mixed with other letters, unparseable). The answers that mislead an operator. Target: near 0.',
          '- Accuracy when answered: exact share among answers that were not Unsure.', '',
         '## Deterministic answers: scores', '',
         '| Model | Mode | Track | Exact | Partial | Majority | ± margin | Consistency | Misconception | Parse fail | Recall | Steps | Tokens | Latency s | Cost US$ |',
         '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for (m, mode, tr), s in sorted(agg.items(), key=lambda x: (x[0][2], -x[1]['majority'])):
        L.append(f'| {m} | {mode} | {tr} | {_pct(s["exact"])} | {_pct(s["partial"])} | {_pct(s["majority"])} | {_pct(s["margin"])} | '
                 f'{_pct(s["consistency"])} | {_pct(s["misconception"])} | {_pct(s["parse_fail"])} | {_pct(s["recall"])} | '
                 f'{"-" if math.isnan(s["steps"]) else round(s["steps"], 1)} | {int(s["tokens"]) if not math.isnan(s["tokens"]) else "-"} | '
                 f'{"-" if math.isnan(s["latency"]) else round(s["latency"], 1)} | {s["cost"]:.3f} |')
    L += ['', '- Exact and Partial: mean over all runs. Majority: most common answer per question. Margin: 95% interval on Majority from the number of questions.',
          '- Consistency: share of questions answered identically in every run. Recall: share of the question `knowledge` ids whose text reached the model (Agent E2 only: the reading set and any gap follow-up). Steps: model calls per answer.', '']

    # per technology and task (a question counts for every technology it lists), deterministic answers
    for dim in ('technology', 'task'):
        vals = sorted({v for r in rows for v in (r.get(dim) or '').split()})
        if not vals:
            continue
        L += [f'## Deterministic answers: exact score by {dim}', '', '| Model | Mode | ' + ' | '.join(vals) + ' |', '|---|---|' + '---|' * len(vals)]
        g = defaultdict(list)
        for r in rows:
            for v in (r.get(dim) or '').split():
                g[(r['model'], r['mode'], v)].append(r['exact'])
        for m, mode in sorted({(r['model'], r['mode']) for r in rows}):
            L.append(f'| {m} | {mode} | ' + ' | '.join(_pct(_mean(g[(m, mode, v)])) for v in vals) + ' |')
        L.append('')

    # worst questions
    per_question = defaultdict(list)
    for r in all_scored:
        if r['mode'] != 'baseline':
            per_question[r['question_id']].append(_credit(r))
    worst = sorted(per_question.items(), key=lambda x: _mean(x[1]))[:10]
    L += ['## Hardest questions (Agent E2, or web for the frontier reference)', '', '| Question | Mean credit | Common wrong answers or missed points |', '|---|---|---|']
    for cid, xs in worst:
        wrong = Counter((r['answer_letters'] or '(unparsed)') if _choice(r) else (r.get('judge_missed') or f'score {r.get("judge_score")}')
                        for r in all_scored if r['question_id'] == cid and r['mode'] != 'baseline' and _credit(r) < 1)
        L.append(f'| {cid} | {_pct(_mean(xs))} | ' + ', '.join(f'{k} ×{v}' for k, v in wrong.most_common(3)).replace('|', '/') + ' |')
    L += ['', 'Traces: `traces.jsonl` in this folder (one line per answer).', '']
    path = os.path.join(run_dir, 'report.md')
    open(path, 'w').write('\n'.join(L))
    return path
