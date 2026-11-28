"""The answer set of release 1.0 and its automated grader (R-E2-004, R-E2-005, R-E2-006 in project/requirements/answer-service.md).

    python3 benchmark/runner/answer_grader.py --check          # the set is complete and its keys are checked: no model call
    python3 benchmark/runner/answer_grader.py                  # answer every question 3 times, grade, write the report

The set is one YAML file per question in benchmark/answer-set/ (fields: id, kind, question, key_points, likely_wrong, knowledge,
and as needed facts, role, page, history, attachments, min_score, clarify_reply). Each question is answered by the service
(harness/answer_service.py, its shipped service_config.yaml). Claude Opus 5.5 grades each answer 0 to 3 by the rubric in
benchmark/free-text-rubric.md. A grade is reused when the answer, the question with its key points, the rubric and the grader
model are the same; an answer is reused when the question, the run number and every file of knowledge/ and harness/ are the same.
The report is benchmark/results/answer-set-<date>/report.md; the exit code is 1 when a limit is missed.
"""
import argparse
import base64
import datetime
import json
import os
import re
import sys
import time

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'harness'))
import answer_attachments  # noqa: E402
import answer_reuse  # noqa: E402
import spending_stop  # noqa: E402

SET_DIR = os.path.join(ROOT, 'benchmark', 'answer-set')
QUESTIONS_DIR = os.path.join(ROOT, 'benchmark', 'questions')
RUBRIC_FILE = os.path.join(ROOT, 'benchmark', 'free-text-rubric.md')
RESULTS_DIR = os.path.join(ROOT, 'benchmark', 'results')
KEY_CHECK = 'key-check.md'
LIMITS_FILE = 'limits.json'          # written by the first run when its mean credit is below FIRST_RUN_FLOOR (R-E2-006)
GRADER_MODEL = 'anthropic/claude-opus-5.5'
MIN_KINDS = {'acme': 3, 'reader': 5, 'csv': 2, 'screenshot': 2, 'conversation': 1, 'design': 1}
REQUIRED = ('id', 'kind', 'question', 'key_points', 'likely_wrong', 'knowledge')
RUNS = 3
SPAN = 12                            # words: a shared run this long is a copy (T-E2-004b)
LIMITS = {'mean_credit': 0.75, 'confident_wrong': 0.05, 'misconceptions': 0}
FIRST_RUN_FLOOR = 0.5
CLARIFY_REPLY = 'Use what is shown and what I have told you. I have nothing more to add.'
STATUS_WORDS = re.compile(r'\b(draft|reviewed|review status)\b', re.I)     # T-E2-002b
SYSTEM = ('You grade answers to VMware vSphere and VCF operations questions against an expert answer key.\n'
          'Reply with one JSON object and nothing else:\n'
          '{"score": 0-3, "misconception": true|false, "unsure": true|false, "missed": "<key point missed, or empty>", '
          '"reason": "<one sentence>"}\n'
          'misconception = the answer states the likely wrong answer (the Level 300 misconception).')


class GradingError(Exception):
    pass


# ---------------------------------------------------------------- the set

def load_set(folder=SET_DIR):
    """Every question of the set, by file name. Each gets `dir`, the folder its facts and attachments are relative to."""
    out = []
    for name in sorted(os.listdir(folder)):
        if name.endswith('.yaml'):
            with open(os.path.join(folder, name), encoding='utf-8') as f:
                q = yaml.safe_load(f)
            q['dir'], q['file'] = folder, name
            out.append(q)
    return out


def words(text):
    return re.findall(r"[a-z0-9']+", str(text).lower())


def spans(text, n=SPAN):
    w = words(text)
    return {' '.join(w[i:i + n]) for i in range(len(w) - n + 1)}


def benchmark_spans(folder=QUESTIONS_DIR):
    """Every run of SPAN words in the multiple-choice questions' files, with the file it comes from."""
    found = {}
    for dirpath, _, names in os.walk(folder):
        for name in names:
            if name.endswith('.md'):
                with open(os.path.join(dirpath, name), encoding='utf-8') as f:
                    for s in spans(f.read()):
                        found.setdefault(s, name)
    return found


def question_text(q):
    """Everything an answer-set question says in its own words: the question, the history and the key points."""
    parts = [q.get('question', '')] + [t for h in q.get('history') or [] for t in (h.get('question'), h.get('answer'))]
    return '\n'.join(str(p) for p in parts + list(q.get('key_points') or []) + [q.get('likely_wrong', '')])


def check_set(questions, knowledge_ids, benchmark=None, key_rows=None):
    """The problems of the set, one string each (T-E2-004a, T-E2-004b, T-E2-004c). [] when the set is complete."""
    problems, counts, seen = [], {}, set()
    for q in questions:
        qid = q.get('id') or q.get('file')
        counts[q.get('kind')] = counts.get(q.get('kind'), 0) + 1
        if qid in seen:
            problems.append(f'{qid}: the id is used twice')
        seen.add(qid)
        for field in REQUIRED:
            if not q.get(field):
                problems.append(f'{qid}: no {field}')
        for k in q.get('knowledge') or []:
            if k not in knowledge_ids:
                problems.append(f'{qid}: knowledge file {k} does not exist')
        for rel in ([q['facts']] if q.get('facts') else []) + list(q.get('attachments') or []):
            if not os.path.isfile(os.path.join(q['dir'], rel)):
                problems.append(f'{qid}: file {rel} does not exist')
        if q.get('kind') in ('csv', 'screenshot') and not q.get('attachments'):
            problems.append(f'{qid}: a {q["kind"]} question has no attachment')
        if q.get('kind') == 'conversation' and len(q.get('history') or []) < 1:
            problems.append(f'{qid}: a conversation question has no history')
        if benchmark is not None:
            copied = sorted({benchmark[s] for s in spans(question_text(q)) if s in benchmark})
            if copied:
                problems.append(f'{qid}: shares a run of {SPAN} words with {", ".join(copied[:3])}')
        if key_rows is not None and qid not in key_rows:
            problems.append(f'{qid}: no row in {KEY_CHECK}')
    for kind, n in MIN_KINDS.items():
        if counts.get(kind, 0) < n:
            problems.append(f'kind {kind}: {counts.get(kind, 0)} questions, at least {n} needed')
    return problems


def knowledge_ids(root=ROOT):
    base = os.path.join(root, 'knowledge')
    return {os.path.relpath(os.path.join(d, n), base)[:-3].replace(os.sep, '/')
            for d, _, names in os.walk(base) for n in names if n.endswith('.md')}


def key_check_rows(path):
    """{question id: 'agrees' | 'uncertain'} from the table of key-check.md. {} when the file is missing."""
    if not os.path.isfile(path):
        return {}
    rows = {}
    for line in open(path, encoding='utf-8'):
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) >= 2 and cells[1].lower() in ('agrees', 'uncertain'):
            rows[cells[0].strip('`')] = cells[1].lower()
    return rows


# ---------------------------------------------------------------- what a question sends

def attachment_items(q):
    items = []
    for rel in q.get('attachments') or []:
        with open(os.path.join(q['dir'], rel), 'rb') as f:
            items.append({'name': os.path.basename(rel), 'data': base64.b64encode(f.read()).decode()})
    return items


def load_facts(q):
    if not q.get('facts'):
        return None
    with open(os.path.join(q['dir'], q['facts']), encoding='utf-8') as f:
        return json.load(f)


def request_body(q):
    """The body of POST /v1/answer for a question."""
    body = {'question': q['question']}
    for key in ('role', 'page', 'history'):
        if q.get(key):
            body[key] = q[key]
    if q.get('facts'):
        body['facts'] = load_facts(q)
    if q.get('attachments'):
        body['attachments'] = attachment_items(q)
    return body


def fingerprint(q):
    """What a grade and an answer depend on in the question: its request, its key points and its likely wrong answer."""
    return answer_reuse.digest('question-1', request_body(q), q['key_points'], q['likely_wrong'], q.get('min_score'))


def rubric():
    """The rubric text: the first fenced block under the heading Rubric in free-text-rubric.md."""
    text = open(RUBRIC_FILE, encoding='utf-8').read()
    m = re.search(r'## Rubric\s+```text\n(.*?)```', text, re.S)
    if not m:
        raise GradingError('free-text-rubric.md has no Rubric block')
    return m.group(1).strip()


# ---------------------------------------------------------------- the grader

def grader_messages(q, answer, rubric_text, exchange=None):
    """The grader's request: the key and the answer, then what Agent E2 saw (facts, history, CSV text, screenshots)."""
    lines = ['Question:', q['question']]
    if q.get('history'):
        lines += ['', 'Earlier turns of the conversation:'] + [f'- Q: {h["question"]}\n  A: {h["answer"]}' for h in q['history']]
    if q.get('facts'):
        lines += ['', 'Facts the page sent with the question (JSON):', json.dumps(load_facts(q))]
    if exchange:
        lines += ['', "The answer first asked these questions, and the person's scripted reply followed:"] + [f'- {t}' for t in exchange]
    lines += ['', 'Expected key points (the answer key):'] + [f'- {k}' for k in q['key_points']]
    lines += ['', 'Likely wrong answer:', q.get('likely_wrong') or '(none given)', '', 'Answer to grade:', answer or '(empty)']
    parts = [{'type': 'text', 'text': '\n'.join(lines)}]
    for a in answer_attachments.parse(attachment_items(q)):
        parts.append(a.part())
    return [{'role': 'system', 'content': SYSTEM + '\n\n' + rubric_text}, {'role': 'user', 'content': parts}]


def parse_reply(text):
    """The grade in a reply, or None when the reply is not valid."""
    m = re.search(r'\{.*\}', text or '', re.S)
    try:
        g = json.loads(m.group(0)) if m else None
    except ValueError:
        return None
    if not isinstance(g, dict) or g.get('score') not in (0, 1, 2, 3):
        return None
    return {'score': g['score'], 'misconception': bool(g.get('misconception')), 'unsure': bool(g.get('unsure')),
            'missed': str(g.get('missed') or ''), 'reason': str(g.get('reason') or '')}


def grade(client, q, answer, rubric_text, cache=None, model=GRADER_MODEL, exchange=None):
    """Grade one answer (T-E2-005a, T-E2-005b, T-E2-005d). A reply that is not valid JSON gets one retry, then the grading fails
    with the reply's first 200 characters. Returns the grade with `reused` (true when the cache held it) and `tokens`."""
    key = answer_reuse.digest('grade-1', answer, fingerprint(q), rubric_text, model, exchange or [])
    if cache is not None and key in cache:
        return {**cache[key], 'reused': True}
    messages = grader_messages(q, answer, rubric_text, exchange)
    tokens = 0
    for attempt in range(2):
        res = client.chat(model, messages, temperature=0, max_tokens=800)
        tokens += res.get('prompt_tokens', 0) + res.get('completion_tokens', 0)
        g = parse_reply(res.get('content'))
        if g:
            g['tokens'] = tokens
            if cache is not None:
                cache[key] = g
            return {**g, 'reused': False}
        messages = messages + [{'role': 'assistant', 'content': res.get('content') or ''},
                               {'role': 'user', 'content': 'Reply with the JSON object only.'}]
    raise GradingError(f'{q["id"]}: the grader did not reply with valid JSON: {(res.get("content") or "")[:200]}')


# ---------------------------------------------------------------- answering

def answer_question(service, q, run, cache=None, service_hash=''):
    """One answer of the service. A clarifying question is answered by the scripted reply (the question's `clarify_reply`, else
    CLARIFY_REPLY), and the final answer counts. Returns {'content', 'exchange', 'model', 'commit', 'elapsed_s', 'tokens', 'reused'}."""
    key = answer_reuse.digest('answer-1', fingerprint(q), run, service_hash)
    if cache is not None and key in cache:
        return {**cache[key], 'reused': True}
    body = request_body(q)
    out = service.answer(body)
    exchange, tokens, elapsed = [], 0, 0.0
    usage = lambda o: (o.get('usage') or {}).get('prompt_tokens', 0) + (o.get('usage') or {}).get('completion_tokens', 0)  # noqa: E731
    tokens, elapsed = usage(out), out.get('elapsed_s', 0)
    if out.get('type') == 'clarify':
        reply = q.get('clarify_reply') or CLARIFY_REPLY
        exchange = list(out.get('questions') or []) + [reply]
        out = service.answer({**body, 'turns': [q['question'], '\n'.join(out.get('questions') or []), reply]})
        tokens, elapsed = tokens + usage(out), elapsed + out.get('elapsed_s', 0)
    res = {'content': out.get('content', ''), 'exchange': exchange, 'model': out.get('model', ''),
           'commit': out.get('knowledge_commit') or '', 'elapsed_s': elapsed, 'tokens': tokens}
    if cache is not None:
        cache[key] = res
    return {**res, 'reused': False}


# ---------------------------------------------------------------- limits and report

def evaluate(rows, questions, limits=None):
    """(figures, misses) for the rows of a run: mean credit, the share of confident wrong answers, misconceptions, the status
    words of T-E2-002b and the per-question minimum score (T-E2-021a). `misses` lists each limit that is missed."""
    limits = limits or LIMITS
    n = len(rows) or 1
    mean = sum(r['score'] for r in rows) / 3 / n
    wrong = sum(1 for r in rows if r['score'] == 0 and not r['unsure'])
    figures = {'answers': len(rows), 'mean_credit': round(mean, 3), 'confident_wrong': round(wrong / n, 3),
               'misconceptions': sum(1 for r in rows if r['misconception']),
               'status_words': sum(1 for r in rows if STATUS_WORDS.search(r['answer']))}
    low = {q['id']: q['min_score'] for q in questions if q.get('min_score')}
    figures['below_minimum'] = sorted({r['id'] for r in rows if r['id'] in low and r['score'] < low[r['id']]})
    misses = []
    if figures['mean_credit'] < limits['mean_credit']:
        misses.append(f'mean credit {figures["mean_credit"]} is below {limits["mean_credit"]}')
    if figures['confident_wrong'] > limits['confident_wrong']:
        misses.append(f'confidently wrong answers {figures["confident_wrong"]:.1%} are above {limits["confident_wrong"]:.0%}')
    if figures['misconceptions'] > limits['misconceptions']:
        misses.append(f'{figures["misconceptions"]} answers state a misconception')
    if figures['status_words']:
        misses.append(f'{figures["status_words"]} answers contain "draft", "reviewed" or "review status"')
    if figures['below_minimum']:
        misses.append('below the minimum score: ' + ', '.join(figures['below_minimum']))
    return figures, misses


def report_text(rows, figures, misses, meta, limits, note=''):
    out = [f'# Answer set report, {meta["date"]}', '',
           f'- Model: {meta["model"]}. Knowledge commit: {meta["commit"]}. Grader: {GRADER_MODEL}.',
           f'- Answers: {figures["answers"]} ({meta["reused_answers"]} reused, {meta["reused_grades"]} grades reused). '
           f'Tokens used: {meta["tokens"]}.',
           f'- Mean credit: {figures["mean_credit"]} (limit {limits["mean_credit"]}). '
           f'Confidently wrong: {figures["confident_wrong"]:.1%} (limit {limits["confident_wrong"]:.0%}). '
           f'Misconceptions: {figures["misconceptions"]} (limit {limits["misconceptions"]}).',
           f'- Result: {"PASS" if not misses else "FAIL: " + "; ".join(misses)}']
    if note:
        out.append(f'- {note}')
    out += ['', '| Question | Run | Score | Misconception | Unsure | Seconds | Tokens | Missed |', '|---|---|---|---|---|---|---|---|']
    for r in rows:
        out.append(f'| {r["id"]} | {r["run"]} | {r["score"]} | {"yes" if r["misconception"] else "no"} | '
                   f'{"yes" if r["unsure"] else "no"} | {round(r["elapsed_s"], 1)} | {r["tokens"]} | {r["missed"] or ""} |'.replace('\n', ' '))
    out += ['', '## Answers and reasons', '']
    for r in rows:
        out += [f'### {r["id"]}, run {r["run"]}, score {r["score"]}', '', f'Grader: {r["reason"]}', '', r['answer'].strip(), '']
    return '\n'.join(out)


def load_limits(folder=SET_DIR):
    path = os.path.join(folder, LIMITS_FILE)
    return (json.load(open(path)), True) if os.path.isfile(path) else (dict(LIMITS), False)


def run(service, client, questions, rubric_text, out_dir, runs=RUNS, cache_dir=None, stop=None, set_dir=SET_DIR, date=None):
    """Answer and grade the set. Returns (figures, misses, report path)."""
    cache_dir = cache_dir or os.path.join(RESULTS_DIR, 'answer-set-cache')
    os.makedirs(cache_dir, exist_ok=True)
    caches = {}
    for name in ('answers', 'grades'):
        path = os.path.join(cache_dir, f'{name}.json')
        caches[name] = json.load(open(path)) if os.path.isfile(path) else {}
    service_hash = answer_reuse.digest(answer_reuse.tree_hash(ROOT, ['knowledge', 'harness']), service.cfg)
    rows, reused_a, reused_g, tokens = [], 0, 0, 0
    for q in questions:
        for n in range(1, runs + 1):
            if stop is not None and stop():
                raise RuntimeError('the spending limit is reached: stop and tell the author')
            a = answer_question(service, q, n, caches['answers'], service_hash)
            g = grade(client, q, a['content'], rubric_text, caches['grades'], exchange=a['exchange'])
            reused_a += a['reused']
            reused_g += g['reused']
            tokens += a['tokens'] if not a['reused'] else 0
            rows.append({'id': q['id'], 'run': n, 'answer': a['content'], 'model': a['model'], 'commit': a['commit'],
                         'elapsed_s': a['elapsed_s'], 'tokens': a['tokens'], **{k: g[k] for k in
                         ('score', 'misconception', 'unsure', 'missed', 'reason')}})
            for name in caches:     # saved at every answer: a stopped run resumes where it ended
                json.dump(caches[name], open(os.path.join(cache_dir, f'{name}.json'), 'w'))
    limits, fixed = load_limits(set_dir)
    figures, misses = evaluate(rows, questions, limits)
    note = ''
    if not fixed and figures['mean_credit'] < FIRST_RUN_FLOOR:
        limits = {'mean_credit': figures['mean_credit'], 'confident_wrong': figures['confident_wrong'],
                  'misconceptions': figures['misconceptions']}
        json.dump(limits, open(os.path.join(set_dir, LIMITS_FILE), 'w'), indent=1)
        figures, misses = evaluate(rows, questions, limits)
        note = (f'First run below {FIRST_RUN_FLOOR}: the limits are now this run\'s own values and no later run may fall below them '
                f'(R-E2-006). Record them in the requirement.')
    meta = {'date': date or datetime.date.today().isoformat(), 'model': rows[0]['model'] if rows else '',
            'commit': rows[0]['commit'] if rows else '', 'reused_answers': reused_a, 'reused_grades': reused_g, 'tokens': tokens}
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, 'report.md')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(report_text(rows, figures, misses, meta, limits, note))
    return figures, misses, path


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--check', action='store_true', help='check the set only: no model call')
    ap.add_argument('--runs', type=int, default=RUNS)
    ap.add_argument('--config', default=os.path.join(ROOT, 'harness', 'service_config.yaml'))
    ap.add_argument('--max-cost-usd', type=float, default=100, help='stop at this much gateway spending (CONSTRAINT-1)')
    ap.add_argument('--only', help='answer only the questions whose id starts with this')
    a = ap.parse_args(argv)
    questions = load_set()
    problems = check_set(questions, knowledge_ids(), benchmark_spans(), key_check_rows(os.path.join(SET_DIR, KEY_CHECK)))
    uncertain = [i for i, v in key_check_rows(os.path.join(SET_DIR, KEY_CHECK)).items() if v == 'uncertain']
    for p in problems:
        print('PROBLEM:', p)
    print(f'{len(questions)} questions, {len(problems)} problems, {len(uncertain)} keys uncertain (for the author)')
    if problems or a.check:
        return 1 if problems else 0
    if not os.environ.get('AI_GATEWAY_API_KEY'):
        print('NOT RUN: AI_GATEWAY_API_KEY is not set')
        return 4
    import answer_service
    from model_client import GatewayClient
    cfg = yaml.safe_load(open(a.config))
    service = answer_service.Service(cfg)
    grader = GatewayClient(cfg['gateway'], retry_seconds=cfg.get('gateway_retry_minutes', 1) * 60)
    stopper = spending_stop.SpendingStop(a.max_cost_usd, lambda: 0, grader.credits(), grader.credits)
    chosen = [q for q in questions if not a.only or q['id'].startswith(a.only)]
    day = datetime.date.today().isoformat()
    try:
        figures, misses, path = run(service, grader, chosen, rubric(), os.path.join(RESULTS_DIR, f'answer-set-{day}'), a.runs,
                                    stop=lambda: stopper.spent() >= a.max_cost_usd)
    except RuntimeError as e:
        print(e)
        return 9
    print(json.dumps(figures))
    print('report:', path)
    for m in misses:
        print('MISSED:', m)
    return 1 if misses else 0


if __name__ == '__main__':
    sys.exit(main())
