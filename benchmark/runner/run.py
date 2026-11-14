#!/usr/bin/env python3
"""Benchmark runner.

Examples:
  python3 benchmark/runner/run.py --dry-run
  python3 benchmark/runner/run.py --mock --runs 2
  AI_GATEWAY_API_KEY=... python3 benchmark/runner/run.py --models google/gemma-4-31b-it --modes agent-e2 --runs 1 --questions L4-04
  AI_GATEWAY_API_KEY=... python3 benchmark/runner/run.py              # full matrix from config.yaml
  python3 benchmark/runner/run.py --resume benchmark/results/<benchmark-id>   # models, modes, runs, questions and judge come from the folder
  python3 benchmark/runner/run.py --models <id> --max-minutes 110            # stops cleanly after 110 minutes (exit code 3)
Exit codes: benchmark/runner/exitcodes.py. A whole benchmark round: benchmark/RUN.md.
"""
import argparse
import csv
import datetime as dt
import json
import os
import random
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import yaml

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'harness'))
import exitcodes as X  # noqa: E402
import questions as C  # noqa: E402
import judge as J  # noqa: E402
import kb  # noqa: E402
import modes  # noqa: E402
import report  # noqa: E402
from governor import Governor  # noqa: E402
from health import Health  # noqa: E402
from llm import GatewayClient, LLMError, MockClient, ParamClient  # noqa: E402
from naming import run_name  # noqa: E402
from retrieval import Retriever  # noqa: E402

AGENT_ACTIONS = ('compute', 'gap', 'repair', 'consensus', 'context_over')
FIELDS = ['benchmark_id', 'time', 'model', 'provider', 'mode', 'track', 'question_id', 'answer_type', 'input', 'technology', 'task', 'level', 'run', 'temperature',
          'options_order', 'answer_letters', 'correct', 'exact', 'partial', 'misconception', 'unsure', 'parse_ok',
          'retrieval_recall', 'ids_used', 'steps', 'prompt_tokens', 'completion_tokens',
          'latency', 'cost_usd', 'index_version', 'error', 'reason', 'tools_used', 'verify_flags', 'repaired',
          'credit', 'confident_wrong', 'judge_model', 'judge_score', 'judge_missed', 'answer_text', 'truncated']


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--config', default=os.path.join(os.path.dirname(__file__), 'config.yaml'))
    ap.add_argument('--models', help='comma-separated model ids (default: config)')
    ap.add_argument('--modes', help='comma-separated: baseline, agent-e2 (candidates); web (the frontier reference)')
    ap.add_argument('--runs', type=int)
    ap.add_argument('--questions', help='comma-separated: an id or a file-name fragment, e.g. L4-04,L1-,esxtop')
    ap.add_argument('--temperature', type=float)
    ap.add_argument('--concurrency', type=int, help='proven parallel requests for every model (overrides concurrency and concurrency_by_model)')
    ap.add_argument('--no-adaptive', action='store_true', help='keep every model at its proven concurrency: no probing upward')
    ap.add_argument('--no-embeddings', action='store_true', help='BM25 only')
    ap.add_argument('--mock', action='store_true', help='offline: random answers, no API calls')
    ap.add_argument('--judge', help='judge model id (default: config judge_model)')
    ap.add_argument('--primer', help='up-front blocks of the answer prompt to switch on, comma-separated: rules,terms, or all (default: config primer)')
    ap.add_argument('--dry-run', action='store_true', help='print the matrix and cost estimate, then stop')
    ap.add_argument('--resume', help='existing run folder to continue; models, modes, runs, temperature, questions, judge and primer are read from its config.json unless you pass them')
    ap.add_argument('--max-minutes', type=float, help='stop starting new answers after this many minutes, let the running ones finish, '
                    'print the resume command and exit with code 3 (default: config max_minutes, or no limit)')
    ap.add_argument('--out', default=os.path.join(kb.ROOT, 'benchmark', 'results'))
    ap.add_argument('--name', help='folder name inside --out (default: <date>-<model>, naming.py)')
    ap.add_argument('--params', help='JSON {model: {"reasoning": {...}, "max_tokens": N}}: settings sent with every request of that model. '
                    'Default: the first entry of the model\'s list in config model_params (benchmark/runner/preflight.py picks the entry that works)')
    ap.add_argument('--no-health', action='store_true', help='do not stop a run whose answers are cut off, unparsable or failing')
    a = ap.parse_args()

    cfg = yaml.safe_load(open(a.config))
    # A resumed run continues with its own settings: a resume without --models once ran every model of the config into the folder.
    saved = {}
    if a.resume and os.path.exists(os.path.join(a.resume, 'config.json')):
        saved = json.load(open(os.path.join(a.resume, 'config.json')))
        for k in ('runs', 'temperature'):
            if getattr(a, k) is None and saved.get(k) is not None:
                cfg[k] = saved[k]
        if saved.get('sampling') is not None:
            cfg['sampling'] = saved['sampling']
        if not a.primer and saved.get('primer') is not None:
            cfg['primer'] = saved['primer']
        if not a.questions and saved.get('questions'):
            a.questions = ','.join(saved['questions'])
        print(f'Resuming {a.resume}: settings from its config.json.')
    for k in ('runs', 'temperature', 'concurrency'):
        if getattr(a, k) is not None:
            cfg[k] = getattr(a, k)
    models_ = a.models.split(',') if a.models else (list(saved['models']) if saved.get('models') else cfg['models'])
    modes_ = a.modes.split(',') if a.modes else (saved.get('modes') or cfg['modes'])
    limit = a.max_minutes if a.max_minutes is not None else cfg.get('max_minutes')
    deadline = time.monotonic() + limit * 60 if limit is not None else None
    # Concurrency per model: the proven value is the floor; the governor probes above it (governor.py).
    by_model = {} if a.concurrency is not None else (cfg.get('concurrency_by_model') or {})
    ac = cfg.get('adaptive_concurrency') or {}
    gov = Governor({m: by_model.get(m, cfg['concurrency']) for m in models_},
                   adaptive=bool(ac.get('enabled')) and not a.no_adaptive and not a.mock,
                   step=ac.get('step', 2), max_probes=ac.get('max_probes', 2), window=ac.get('window', 40),
                   gain_fraction=ac.get('gain_fraction', 0.5), log=lambda s: print(f'  {s}', flush=True))

    all_questions = C.load(a.questions)
    skipped = [c.id for c in all_questions if not c.scorable]
    questions_ = [c for c in all_questions if c.scorable]
    if not questions_:
        sys.exit('No scorable questions matched.')

    params = _model_params(cfg, models_, a.params, saved)
    # Sampling: each model's own card settings; --temperature replaces them for every model (an experiment, not the release run).
    sampling = {m: (cfg.get('sampling') or {}).get(m, {'temperature': cfg.get('temperature')}) for m in models_}
    if a.temperature is not None:
        sampling = {m: {'temperature': a.temperature} for m in models_}
    client = ParamClient(MockClient() if a.mock else GatewayClient(cfg['gateway']), params, sampling)
    if a.primer:
        on = {'rules', 'terms'} if a.primer == 'all' else {x.strip() for x in a.primer.split(',')}
        cfg['primer'] = {b: b in on for b in ('rules', 'terms')}
    unknown = [m for m in modes_ if m not in modes.MODES]
    if unknown:
        sys.exit(f'Unknown modes {unknown}: {", ".join(modes.MODES)}. Classic and agentic were removed on 2026-11-14 (harness/AGENT.md).')
    judge_model = a.judge or saved.get('judge_model') or cfg.get('judge_model')   # a resume never switches the judge
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
    print(f'Estimated cost: US$ {est:.2f} (rough; Agent E2 counted as the case call plus one answer)')
    if a.dry_run:
        return

    run_dir = a.resume or os.path.join(a.out, a.name or run_name(models_, a.out, a.mock))
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
        retriever = Retriever(docs, chunks, client if embed else None, embed, expand=cfg.get('query_expansion', False))
    except LLMError as e:
        print(f'Embeddings unavailable ({e}); using BM25 only.')
        embed, retriever = None, Retriever(docs, chunks, expand=cfg.get('query_expansion', False))
    sha = kb.git_sha()
    now_s = dt.datetime.now().isoformat(timespec='seconds')
    json.dump({'benchmark_id': benchmark_id, 'started': saved.get('started', now_s), 'resumed': (saved.get('resumed') or []) + ([now_s] if saved else []),
               'index_version': sha,
               'primer': cfg.get('primer'), 'case_model': cfg.get('case_model', True), 'gap_followup': cfg.get('gap_followup', True), 'model_params': params, 'sampling': sampling,
               'models': {m: {k: meta.get(m, {}).get(k) for k in ('tags', 'context_window', 'pricing')} for m in models_},
               'modes': modes_, 'runs': cfg['runs'], 'temperature': cfg['temperature'], 'questions': [c.id for c in questions_],
               'skipped_questions': skipped, 'judge_model': judge.model if judge else None,
               'judge_pricing': {k: ((meta.get(judge.model) or {}).get('pricing') or {}).get(k) for k in ('input', 'output')} if judge and not a.mock else None,
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

    def answer_one(task):
        m, mode, c, track, r = task
        rng = random.Random(f'{c.id}-{r}')  # same option order for every model and mode in run r
        if c.choice:
            question, mapping = c.render(rng)
        else:
            question, mapping = c.open_text(), {}
        images = c.image_parts() if track == 'vision' else []
        row = {'benchmark_id': benchmark_id, 'time': dt.datetime.now().isoformat(timespec='seconds'), 'model': m, 'mode': mode,
               'track': track, 'question_id': c.id, 'answer_type': c.answer_type, 'input': ' '.join(c.input_types), 'technology': ' '.join(c.technology), 'task': c.task, 'level': c.level, 'run': r,
               'temperature': sampling.get(m, {}).get('temperature', ''), 'options_order': ''.join({'UN': '?'}.get(v, v) for v in mapping.values()),
               'correct': ','.join(c.answer), 'index_version': sha[:12]}
        try:
            res, used, trace = modes.answer(mode, client, m, question, images, cfg, retriever,
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
                            'reason': v['reason'], 'misconception': int(v['misconception']), 'unsure': int(v['unsure']),
                            'exact': int(v['score'] == 3), 'credit': round(v['score'] / 3, 3),
                            'confident_wrong': int(v['score'] == 0 and not v['unsure']), 'parse_ok': 1,
                            'answer_text': (res['content'] or '')[:2000]})
            row['provider'] = res.get('provider', '')
            row['truncated'] = int(res.get('finish_reason') == 'length')
            row['prompt_tokens'] = sum(s.get('prompt_tokens') or 0 for s in trace if s['action'] != 'judge')
            row['completion_tokens'] = sum(s.get('completion_tokens') or 0 for s in trace if s['action'] != 'judge')
            row['latency'] = round(sum(s.get('latency') or 0 for s in trace), 2)
            row['steps'] = sum(1 for s in trace if s.get('prompt_tokens') is not None and s['action'] != 'judge')   # model calls
            # Tools of the web reference, and the stages of Agent E2 that acted (compute, gap follow-up, repair, consensus)
            row['tools_used'] = ' '.join(sorted({s['action'] for s in trace if s['action'] in modes.TOOL_NAMES + list(AGENT_ACTIONS)}))
            row['verify_flags'] = ' | '.join(f for s in trace if s['action'] == 'verify' for f in s['output'])[:300]
            row['repaired'] = int(any(s['action'] == 'repair' for s in trace))
            row['ids_used'] = ' '.join(used)
            # needed files whose text reached the model (the reading set and any gap follow-up). Agent E2 only:
            # baseline and web read no knowledge base
            row['retrieval_recall'] = round(len(set(used) & set(c.knowledge)) / len(c.knowledge), 3) if (c.knowledge and mode == modes.AGENT) else ''
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

    health = None if (a.no_health or a.mock) else Health()

    def late():
        return (deadline is not None and time.monotonic() >= deadline) or bool(health and health.reason)

    def one(task):
        if late():
            return None             # past --max-minutes: do not start it; it stays for the resume
        gov.acquire(task[0])    # at most gov.limit_of(model) answers of one model at a time
        try:
            if late():
                return None
            row = answer_one(task)
        finally:
            gov.release(task[0])
        gov.record(task[0], task[1], row['error'])
        if health and health.record(row):
            print(f'  STOP: {health.reason}', flush=True)
        return row

    n, errors, left = 0, 0, 0
    with ThreadPoolExecutor(max_workers=gov.max_workers) as ex:
        for f in as_completed([ex.submit(one, t) for t in tasks]):
            row = f.result()
            n += 1
            if row is None:
                left += 1
                continue
            errors += bool(row['error'])
            if n % 25 == 0 or n == len(tasks):
                print(f'  {n - left}/{len(tasks)} done, {errors} errors, concurrency {gov.summary()}')
    fa.close()
    ft.close()
    if health and health.reason:
        # Invalid answers or a refused key: no report, which would score them. The answers stay in the folder.
        print(f'Run stopped: {health.reason}')
        print(f'{len(tasks) - left} answers done, {left} not started, {errors} errors. Folder: {run_dir}')
        sys.exit(health.code)
    if left:
        # Not a finished run: no report, which would score a partial run.
        print(f'Stopped at the {limit:g}-minute limit: {len(tasks) - left} answers done, {left} to go, {errors} errors.')
        print(f'Resume: python3 benchmark/runner/run.py --resume {run_dir}')
        sys.exit(X.STOPPED)

    path = report.write(run_dir)
    print(f'Report: {path}')
    if errors:
        print(f'{errors} answers failed. Re-run with --resume {run_dir} to retry them.')


def _model_params(cfg, models_, given, saved):
    """Request settings per model: --params, else the ones a resumed folder started with, else the first entry of the
    model's list in config model_params (preflight.py tries the entries in order and picks the first that answers cleanly)."""
    if given:
        return json.loads(given)
    if saved.get('model_params'):
        return saved['model_params']
    out = {}
    for m in models_:
        ladder = (cfg.get('model_params') or {}).get(m) or []
        if ladder and ladder[0]:
            out[m] = ladder[0]
    return out


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
        pin, pout = {'baseline': (600, 300), 'agent-e2': (12000, 600), 'web': (2500, 600)}[mode]   # agent-e2: case call + answer
        if not c.choice:
            pout *= 2  # a free-text answer is longer than two lines
        total += _cost(meta.get(m, {}), pin, pout) or 0
        if not c.choice and judge_model:
            total += _cost(meta.get(judge_model, {}), 1500, 300) or 0
    return total


if __name__ == '__main__':
    main()
