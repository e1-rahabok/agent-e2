#!/usr/bin/env python3
"""Auto Test runner.

Examples:
  python3 tools/autotest/run.py --dry-run
  python3 tools/autotest/run.py --mock --runs 2
  AI_GATEWAY_API_KEY=... python3 tools/autotest/run.py --models openai/gpt-oss-20b --modes classic --runs 1 --cases cpu-004
  AI_GATEWAY_API_KEY=... python3 tools/autotest/run.py              # full matrix from config.yaml
  python3 tools/autotest/run.py --resume evaluation/results/autotest/<run-id>
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
import cases as C  # noqa: E402
import kb  # noqa: E402
import modes  # noqa: E402
import report  # noqa: E402
from llm import GatewayClient, LLMError, MockClient  # noqa: E402
from retrieval import Retriever  # noqa: E402

FIELDS = ['run_id', 'time', 'model', 'provider', 'mode', 'track', 'case_id', 'area', 'level', 'run', 'temperature',
          'options_order', 'answer_letters', 'correct', 'exact', 'partial', 'trap', 'not_covered', 'parse_ok',
          'retrieval_recall', 'ids_used', 'steps', 'tool_errors', 'fallback', 'prompt_tokens', 'completion_tokens',
          'latency', 'cost_usd', 'index_version', 'error', 'reason']


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--config', default=os.path.join(os.path.dirname(__file__), 'config.yaml'))
    ap.add_argument('--models', help='comma-separated model ids (default: config)')
    ap.add_argument('--modes', help='comma-separated: baseline,classic,agentic')
    ap.add_argument('--runs', type=int)
    ap.add_argument('--cases', help='comma-separated id fragments, e.g. cpu-004,memory')
    ap.add_argument('--temperature', type=float)
    ap.add_argument('--concurrency', type=int)
    ap.add_argument('--no-embeddings', action='store_true', help='BM25 only')
    ap.add_argument('--mock', action='store_true', help='offline: random answers, no API calls')
    ap.add_argument('--dry-run', action='store_true', help='print the matrix and cost estimate, then stop')
    ap.add_argument('--resume', help='existing run folder to continue')
    ap.add_argument('--out', default=os.path.join(kb.ROOT, 'evaluation', 'results', 'autotest'))
    ap.add_argument('--no-summary-csv', action='store_true', help='do not append to evaluation/results/results.csv')
    a = ap.parse_args()

    cfg = yaml.safe_load(open(a.config))
    for k in ('runs', 'temperature', 'concurrency'):
        if getattr(a, k) is not None:
            cfg[k] = getattr(a, k)
    models_ = a.models.split(',') if a.models else cfg['models']
    modes_ = a.modes.split(',') if a.modes else cfg['modes']

    all_cases = C.load(a.cases)
    skipped = [c.id for c in all_cases if not c.scorable]
    cases_ = [c for c in all_cases if c.scorable]
    if not cases_:
        sys.exit('No multiple-choice cases matched.')

    client = MockClient() if a.mock else GatewayClient(cfg['gateway'])
    meta = _model_meta(client, models_, a.mock)
    tasks = []
    for m in models_:
        vision = 'vision' in meta.get(m, {}).get('tags', [])
        for mode in modes_:
            for c in cases_:
                tracks = ['text'] + (['vision'] if c.has_images and vision else [])
                for tr in tracks:
                    for r in range(1, cfg['runs'] + 1):
                        tasks.append((m, mode, c, tr, r))

    print(f'Cases: {len(cases_)} multiple-choice (skipped {len(skipped)} not multiple-choice: {", ".join(skipped)})')
    print(f'Models: {len(models_)}  Modes: {", ".join(modes_)}  Runs: {cfg["runs"]}  Answers: {len(tasks)}')
    est = _estimate(tasks, meta)
    print(f'Estimated cost: US$ {est:.2f} (rough; agentic counted at 3x classic tokens)')
    if a.dry_run:
        return

    run_dir = a.resume or os.path.join(a.out, dt.datetime.now().strftime('%Y%m%d-%H%M%S') + ('-mock' if a.mock else ''))
    os.makedirs(run_dir, exist_ok=True)
    run_id = os.path.basename(run_dir)
    answers_path = os.path.join(run_dir, 'answers.csv')
    done = set()
    if os.path.exists(answers_path):
        for row in csv.DictReader(open(answers_path)):
            if not row['error']:
                done.add((row['model'], row['mode'], row['case_id'], row['track'], int(row['run'])))
    tasks = [t for t in tasks if (t[0], t[1], t[2].id, t[3], t[4]) not in done]

    docs, chunks = kb.load()
    embed = None if (a.no_embeddings or a.mock or not cfg.get('embedding_model')) else cfg['embedding_model']
    try:
        retriever = Retriever(docs, chunks, client if embed else None, embed)
    except LLMError as e:
        print(f'Embeddings unavailable ({e}); using BM25 only.')
        embed, retriever = None, Retriever(docs, chunks)
    sha = kb.git_sha()
    json.dump({'run_id': run_id, 'started': dt.datetime.now().isoformat(timespec='seconds'), 'index_version': sha,
               'models': {m: {k: meta.get(m, {}).get(k) for k in ('tags', 'context_window', 'pricing')} for m in models_},
               'modes': modes_, 'runs': cfg['runs'], 'temperature': cfg['temperature'], 'cases': [c.id for c in cases_],
               'skipped_cases': skipped, 'retrieval': 'hybrid' if embed else 'bm25', 'embedding_model': embed,
               'mock': a.mock, 'config': cfg}, open(os.path.join(run_dir, 'config.json'), 'w'), indent=2)

    lock = threading.Lock()
    new = not os.path.exists(answers_path)
    fa = open(answers_path, 'a', newline='')
    w = csv.DictWriter(fa, fieldnames=FIELDS)
    if new:
        w.writeheader()
    ft = open(os.path.join(run_dir, 'traces.jsonl'), 'a')
    print(f'Run folder: {run_dir}  ({len(tasks)} answers to go)')

    def one(task):
        m, mode, c, track, r = task
        rng = random.Random(f'{c.id}-{r}')  # same option order for every model and mode in run r
        question, mapping = c.render(rng)
        images = c.image_parts() if track == 'vision' else []
        row = {'run_id': run_id, 'time': dt.datetime.now().isoformat(timespec='seconds'), 'model': m, 'mode': mode,
               'track': track, 'case_id': c.id, 'area': c.area, 'level': c.level, 'run': r,
               'temperature': cfg['temperature'], 'options_order': ''.join(v if v != 'NC' else '*' for v in mapping.values()),
               'correct': ','.join(c.answer), 'index_version': sha[:12]}
        try:
            res, used, trace, fb = modes.answer(mode, client, m, question, images, cfg, retriever)
            picked = C.parse(res['content'], mapping)
            row.update(C.score(c, picked))
            row['answer_letters'] = ','.join(picked) if picked else ''
            row['reason'] = _reason(res['content'])
            row['provider'] = res.get('provider', '')
            row['prompt_tokens'] = sum(s.get('prompt_tokens') or 0 for s in trace)
            row['completion_tokens'] = sum(s.get('completion_tokens') or 0 for s in trace)
            row['latency'] = round(sum(s.get('latency') or 0 for s in trace), 2)
            row['steps'] = sum(1 for s in trace if s['action'] in ('search', 'read_file', 'follow_links', 'get_images'))
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
            ft.write(json.dumps({'case_id': c.id, 'model': m, 'mode': mode, 'track': track, 'run': r,
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
        report.append_summary(run_dir, os.path.join(kb.ROOT, 'evaluation', 'results', 'results.csv'))


def _reason(text):
    for line in (text or '').split('\n'):
        if line.strip().upper().startswith('REASON:'):
            return line.split(':', 1)[1].strip()[:300]
    return ''


def _model_meta(client, models_, mock):
    if mock:
        return {m: {'tags': ['tool-use', 'vision'] if 'gemma' in m or 'mistral' in m else ['tool-use'], 'pricing': {}} for m in models_}
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


def _estimate(tasks, meta):
    total = 0.0
    for m, mode, c, tr, r in tasks:
        pin, pout = {'baseline': (600, 300), 'classic': (8000, 300), 'agentic': (24000, 900)}[mode]
        total += _cost(meta.get(m, {}), pin, pout) or 0
    return total


if __name__ == '__main__':
    main()
