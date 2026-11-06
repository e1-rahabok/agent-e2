#!/usr/bin/env python3
"""Benchmark runner.

Examples:
  python3 benchmark/runner/run.py --dry-run
  python3 benchmark/runner/run.py --mock --runs 2
  AI_GATEWAY_API_KEY=... python3 benchmark/runner/run.py --models openai/gpt-oss-20b --modes classic --runs 1 --questions L4-04
  AI_GATEWAY_API_KEY=... python3 benchmark/runner/run.py              # full matrix from config.yaml
  python3 benchmark/runner/run.py --resume benchmark/results/<benchmark-id>
"""
import argparse
import csv
import datetime as dt
import json
import os
import random
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

import yaml

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'harness'))
import questions as C  # noqa: E402
import judge as J  # noqa: E402
import kb  # noqa: E402
import modes  # noqa: E402
import report  # noqa: E402
from llm import GatewayClient, LLMError, MockClient  # noqa: E402
from retrieval import Retriever  # noqa: E402

FIELDS = ['benchmark_id', 'time', 'model', 'provider', 'mode', 'track', 'question_id', 'answer_type', 'input', 'technology', 'task', 'level', 'run', 'temperature',
          'options_order', 'answer_letters', 'correct', 'exact', 'partial', 'trap', 'not_covered', 'unsure', 'points', 'parse_ok',
          'retrieval_recall', 'ids_used', 'steps', 'tool_errors', 'fallback', 'prompt_tokens', 'completion_tokens',
          'latency', 'cost_usd', 'index_version', 'error', 'reason', 'tools_used', 'verify_flags', 'repaired',
          'credit', 'confident_wrong', 'judge_model', 'judge_score', 'judge_missed', 'answer_text']


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--config', default=os.path.join(os.path.dirname(__file__), 'config.yaml'))
    ap.add_argument('--models', help='comma-separated model ids (default: config)')
    ap.add_argument('--modes', help='comma-separated: baseline,classic,agentic')
    ap.add_argument('--runs', type=int)
    ap.add_argument('--questions', help='comma-separated: an id or a file-name fragment, e.g. L4-04,L1-,esxtop')
    ap.add_argument('--temperature', type=float)
    ap.add_argument('--concurrency', type=int)
    ap.add_argument('--no-embeddings', action='store_true', help='BM25 only')
    ap.add_argument('--mock', action='store_true', help='offline: random answers, no API calls')
    ap.add_argument('--judge', help='judge model id (default: config judge_model)')
    ap.add_argument('--primer', help='agent up-front blocks to switch on, comma-separated: map,rules,terms,flows,procedure, or all (default: config agent_primer)')
    ap.add_argument('--dry-run', action='store_true', help='print the matrix and cost estimate, then stop')
    ap.add_argument('--resume', help='existing run folder to continue')
    ap.add_argument('--out', default=os.path.join(kb.ROOT, 'benchmark', 'results'))
    ap.add_argument('--no-summary-csv', action='store_true', help='do not append to benchmark/results/results.csv')
    a = ap.parse_args()

    cfg = yaml.safe_load(open(a.config))
    for k in ('runs', 'temperature', 'concurrency'):
        if getattr(a, k) is not None:
            cfg[k] = getattr(a, k)
    models_ = a.models.split(',') if a.models else cfg['models']
    modes_ = a.modes.split(',') if a.modes else cfg['modes']

    all_questions = C.load(a.questions)
    skipped = [c.id for c in all_questions if not c.scorable]
    questions_ = [c for c in all_questions if c.scorable]
    if not questions_:
        sys.exit('No scorable questions matched.')

    client = MockClient() if a.mock else GatewayClient(cfg['gateway'])
    if a.primer:
        on = {'map', 'rules', 'terms', 'flows', 'procedure'} if a.primer == 'all' else {x.strip() for x in a.primer.split(',')}
        cfg['agent_primer'] = {b: b in on for b in ('map', 'rules', 'terms', 'flows', 'procedure')}
    judge_model = a.judge or cfg.get('judge_model')
    needs_judge = any(not c.choice for c in questions_)
    if needs_judge and judge_model in models_:
        sys.exit(f'The judge {judge_model} is also a candidate. The judge must never grade its own answers.')
    if needs_judge and not (judge_model or a.mock):
        sys.exit('Judged questions need a judge: set judge_model in config.yaml or pass --judge.')
    judge = J.MockJudge() if a.mock else J.Judge(client, judge_model, cfg) if needs_judge else None
    meta = _model_meta(client, models_ + ([judge_model] if needs_judge and not a.mock else []), a.mock)
    # Reading screenshots is a basic requirement (benchmark/models.md): a model without vision is not a candidate.
    blind = [m for m in models_ if 'vision' not in meta.get(m, {}).get('tags', [])]
    if meta and blind and any(c.has_images for c in questions_):
        sys.exit(f'Models without vision cannot take the screenshot questions: {", ".join(blind)}. '
                 'Remove them (benchmark/models.md) or pass --questions without screenshot questions.')
    tasks = []
    for m in models_:
        for mode in modes_:
            for c in questions_:
                tr = 'vision' if c.has_images else 'text'
                for r in range(1, cfg['runs'] + 1):
                    tasks.append((m, mode, c, tr, r))

    answer_types = ', '.join(f'{k} {sum(1 for c in questions_ if c.answer_type == k)}' for k in ('deterministic', 'judged'))
    print(f'Questions: {len(questions_)} ({answer_types}). Skipped (no key, awaiting input or retired): {", ".join(skipped) or "none"}')
    if needs_judge:
        print(f'Judge: {judge.model}')
    print(f'Models: {len(models_)}  Modes: {", ".join(modes_)}  Runs: {cfg["runs"]}  Answers: {len(tasks)}')
    est = _estimate(tasks, meta, judge_model if needs_judge else None)
    print(f'Estimated cost: US$ {est:.2f} (rough; agentic counted at 3x classic tokens)')
    if a.dry_run:
        return

    run_dir = a.resume or os.path.join(a.out, dt.datetime.now().strftime('%Y%m%d-%H%M%S') + ('-mock' if a.mock else ''))
    os.makedirs(run_dir, exist_ok=True)
    benchmark_id = os.path.basename(run_dir)
    answers_path = os.path.join(run_dir, 'answers.csv')
    done = set()
    if os.path.exists(answers_path):
        for row in csv.DictReader(open(answers_path)):
            if not row['error']:
                done.add((row['model'], row['mode'], row['question_id'], row['track'], int(row['run'])))
    tasks = [t for t in tasks if (t[0], t[1], t[2].id, t[3], t[4]) not in done]

    docs, chunks = kb.load()
    embed = None if (a.no_embeddings or a.mock or not cfg.get('embedding_model')) else cfg['embedding_model']
    try:
        retriever = Retriever(docs, chunks, client if embed else None, embed)
    except LLMError as e:
        print(f'Embeddings unavailable ({e}); using BM25 only.')
        embed, retriever = None, Retriever(docs, chunks)
    sha = kb.git_sha()
    json.dump({'benchmark_id': benchmark_id, 'started': dt.datetime.now().isoformat(timespec='seconds'), 'index_version': sha,
               'agent_primer': cfg.get('agent_primer'),
               'models': {m: {k: meta.get(m, {}).get(k) for k in ('tags', 'context_window', 'pricing')} for m in models_},
               'modes': modes_, 'runs': cfg['runs'], 'temperature': cfg['temperature'], 'questions': [c.id for c in questions_],
               'skipped_questions': skipped, 'judge_model': judge.model if judge else None,
               'groups': {c.id: {'answer_type': c.answer_type, 'input': c.input_types, 'level': c.level} for c in questions_}, 'retrieval': 'hybrid' if embed else 'bm25', 'embedding_model': embed,
               'mock': a.mock, 'config': cfg}, open(os.path.join(run_dir, 'config.json'), 'w'), indent=2)

    lock = threading.Lock()
    new = not os.path.exists(answers_path) or os.path.getsize(answers_path) == 0
    fa = open(answers_path, 'a', newline='')
    # A resumed run keeps the header it started with (older runs lack the newer columns).
    fields = FIELDS if new else next(csv.reader(open(answers_path)))
    w = csv.DictWriter(fa, fieldnames=fields, extrasaction='ignore')
    if new:
        w.writeheader()
    ft = open(os.path.join(run_dir, 'traces.jsonl'), 'a')
    print(f'Benchmark folder: {run_dir}  ({len(tasks)} answers to go)')

    def one(task):
        m, mode, c, track, r = task
        rng = random.Random(f'{c.id}-{r}')  # same option order for every model and mode in run r
        if c.choice:
            question, mapping = c.render(rng)
        else:
            question, mapping = c.prompt, {}
        images = c.image_parts() if track == 'vision' else []
        row = {'benchmark_id': benchmark_id, 'time': dt.datetime.now().isoformat(timespec='seconds'), 'model': m, 'mode': mode,
               'track': track, 'question_id': c.id, 'answer_type': c.answer_type, 'input': ' '.join(c.input_types), 'technology': ' '.join(c.technology), 'task': c.task, 'level': c.level, 'run': r,
               'temperature': cfg['temperature'], 'options_order': ''.join({'NC': '*', 'UN': '?'}.get(v, v) for v in mapping.values()),
               'correct': ','.join(c.answer), 'index_version': sha[:12]}
        try:
            res, used, trace, fb = modes.answer(mode, client, m, question, images, cfg, retriever,
                                                'choice' if c.choice else 'open')
            if c.choice:
                picked = C.parse(res['content'], mapping)
                row.update(C.score(c, picked))
                row['answer_letters'] = ','.join(picked) if picked else ''
                row['reason'] = _reason(res['content'])
                row['credit'] = row['exact']
                row['confident_wrong'] = int(not row['exact'] and not row['unsure'])
            else:
                v, jres = judge.grade(c, res['content'], images)
                trace.append({'step': len(trace) + 1, 'action': 'judge', 'input': judge.model, 'output': v,
                              'prompt_tokens': jres.get('prompt_tokens'), 'completion_tokens': jres.get('completion_tokens')})
                row.update({'judge_model': judge.model, 'judge_score': v['score'], 'judge_missed': v['missed'],
                            'reason': v['reason'], 'trap': int(v['trap']), 'unsure': int(v['unsure']),
                            'exact': int(v['score'] == 3), 'credit': round(v['score'] / 3, 3),
                            'confident_wrong': int(v['score'] == 0 and not v['unsure']), 'parse_ok': 1,
                            'answer_text': (res['content'] or '')[:2000]})
            row['provider'] = res.get('provider', '')
            row['prompt_tokens'] = sum(s.get('prompt_tokens') or 0 for s in trace if s['action'] != 'judge')
            row['completion_tokens'] = sum(s.get('completion_tokens') or 0 for s in trace if s['action'] != 'judge')
            row['latency'] = round(sum(s.get('latency') or 0 for s in trace), 2)
            row['steps'] = sum(1 for s in trace if s['action'] in modes.TOOL_NAMES)
            row['tools_used'] = ' '.join(sorted({s['action'] for s in trace if s['action'] in modes.TOOL_NAMES}))
            row['verify_flags'] = ' | '.join(f for s in trace if s['action'] == 'verify' for f in s['output'])[:300]
            row['repaired'] = int(any(s['action'] == 'repair' for s in trace))
            row['tool_errors'] = sum(1 for s in trace if s['action'] in ('tool_error', 'refused'))
            row['fallback'] = int(fb)
            row['ids_used'] = ' '.join(used)
            row['retrieval_recall'] = round(len(set(used) & set(c.knowledge)) / len(c.knowledge), 3) if (c.knowledge and mode != 'baseline') else ''
            row['cost_usd'] = _cost(meta.get(m, {}), row['prompt_tokens'], row['completion_tokens'])
            row['error'] = ''
        except LLMError as e:
            trace, row['error'] = [], str(e)[:300]
        with lock:
            w.writerow(row)
            fa.flush()
            ft.write(json.dumps({'question_id': c.id, 'model': m, 'mode': mode, 'track': track, 'run': r,
                                 'question': question, 'trace': trace}, default=str) + '\n')
            ft.flush()
        return row

    n, errors = 0, 0
    with ThreadPoolExecutor(max_workers=cfg['concurrency']) as ex:
        for f in as_completed([ex.submit(one, t) for t in tasks]):
            row = f.result()
            n += 1
            errors += bool(row['error'])
            if n % 25 == 0 or n == len(tasks):
                print(f'  {n}/{len(tasks)} done, {errors} errors')
    fa.close()
    ft.close()

    path = report.write(run_dir)
    print(f'Report: {path}')
    if errors:
        print(f'{errors} answers failed. Re-run with --resume {run_dir} to retry them.')
    if not a.no_summary_csv and not a.mock:
        report.append_summary(run_dir, os.path.join(kb.ROOT, 'benchmark', 'results', 'results.csv'))


def _reason(text):
    for line in (text or '').split('\n'):
        if line.strip().upper().startswith('REASON:'):
            return line.split(':', 1)[1].strip()[:300]
    return ''


def _model_meta(client, models_, mock):
    if mock:
        return {m: {'tags': ['tool-use', 'vision'], 'pricing': {}} for m in models_}
    try:
        allm = client.models()
    except Exception as e:  # listing is public; failure is not fatal
        print(f'Could not read model list: {e}')
        return {}
    missing = [m for m in models_ if m not in allm]
    if missing:
        sys.exit(f'Unknown model ids on the gateway: {", ".join(missing)}')
    return {m: allm[m] for m in models_}


def _cost(m, pin, pout):
    p = m.get('pricing') or {}
    try:
        return round(pin * float(p.get('input', 0)) + pout * float(p.get('output', 0)), 6)
    except (TypeError, ValueError):
        return ''


def _estimate(tasks, meta, judge_model=None):
    total = 0.0
    for m, mode, c, tr, r in tasks:
        pin, pout = {'baseline': (600, 300), 'classic': (8000, 300), 'agentic': (24000, 900)}[mode]
        if not c.choice:
            pout *= 2  # a free-text answer is longer than two lines
        total += _cost(meta.get(m, {}), pin, pout) or 0
        if not c.choice and judge_model:
            total += _cost(meta.get(judge_model, {}), 1500, 300) or 0
    return total


if __name__ == '__main__':
    main()
