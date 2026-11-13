#!/usr/bin/env python3
"""Run a whole benchmark round without anyone at the keyboard: preflight, all runs in parallel, recovery, summary.

  python3 benchmark/runner/run_all.py --max-minutes 110      # start the round (stops cleanly after 110 minutes: exit 3)
  python3 benchmark/runner/run_all.py --resume --max-minutes 110   # continue after exit 3 (or after a top-up, exit 6)
  python3 benchmark/runner/run_all.py --dry-run               # print the plan; no API call

Steps (benchmark/RUN.md has the full playbook):
  1. Preflight (preflight.py): credits, a sample answered per model and mode, request settings chosen per model, time and cost projected.
     A run that fails the sample is not started. Nothing is spent on the long run before this passes.
  2. One run.py per entry of config `release.runs`, all at once, each in its own folder `<date>-<model>`.
  3. Recovery: a crashed run is relaunched with --resume (config `release.retries` times); answers that failed are retried the same way;
     a run stopped by the time limit is relaunched by you with --resume. A run whose answers are invalid, or a refused key, is not retried.
  4. When every run is complete: summarize.py writes benchmark/results/README.md, earlier run folders move to project/archive/.
Exit codes: exitcodes.py. 0 = the round is complete; 3 = relaunch with --resume; 6 = top up credits or key budget, then --resume;
4, 5, 7 = a run failed: read the printed list.
"""
import argparse
import csv
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'harness'))
import exitcodes as X  # noqa: E402
from naming import run_name  # noqa: E402

ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
RESULTS = os.path.join(ROOT, 'benchmark', 'results')
STATE = '.round.json'
PROGRESS = '.progress.txt'
PREFLIGHT = '.preflight.json'


# ---------- pure helpers (tested) ----------

def classify(code):
    """What the exit code of one run.py means for the orchestrator."""
    return {X.OK: 'complete', X.STOPPED: 'stopped', X.UNHEALTHY: 'invalid', X.BUDGET: 'refused'}.get(code, 'crashed')


def unresolved(folder):
    """Answers in a run folder that failed and were never answered later: (model, mode, question, track, run) keys."""
    path = os.path.join(folder, 'answers.csv')
    if not os.path.exists(path):
        return set()
    bad, good = set(), set()
    for r in csv.DictReader(open(path)):
        k = (r['model'], r['mode'], r['question_id'], r['track'], r['run'])
        (bad if r['error'] else good).add(k)
    return bad - good


def total_answers(entry, cfg, n_questions):
    return len(entry['modes']) * n_questions * cfg['runs']


def count_valid(folder):
    path = os.path.join(folder, 'answers.csv')
    if not os.path.exists(path):
        return 0, 0
    ok = bad = 0
    for r in csv.DictReader(open(path)):
        ok += not r['error']
        bad += bool(r['error'])
    return ok, bad


def child_cmd(entry, out_dir, minutes_left, resume, extra=''):
    cmd = [sys.executable, os.environ.get('RUN_ALL_CHILD') or os.path.join(HERE, 'run.py'), '--out', out_dir, '--max-minutes', f'{minutes_left:.1f}'] + extra.split()
    if resume:
        cmd += ['--resume', os.path.join(out_dir, entry['folder'])]
    else:
        cmd += ['--models', entry['model'], '--modes', ','.join(entry['modes']), '--name', entry['folder'],
                '--params', json.dumps({entry['model']: entry['params']} if entry.get('params') else {})]
    return cmd


def archive_old(results_dir, keep, archive_dir):
    """Move run folders that are not part of this round into archive_dir. Return their names."""
    moved = []
    for name in sorted(os.listdir(results_dir)):
        p = os.path.join(results_dir, name)
        if name in keep or not os.path.isdir(p) or not os.path.exists(os.path.join(p, 'config.json')):
            continue
        os.makedirs(archive_dir, exist_ok=True)
        shutil.move(p, os.path.join(archive_dir, name))
        moved.append(name)
    return moved


# ---------- state ----------

def load_state(out_dir):
    p = os.path.join(out_dir, STATE)
    return json.load(open(p)) if os.path.exists(p) else None


def save_state(out_dir, state, lock):
    with lock:
        json.dump(state, open(os.path.join(out_dir, STATE), 'w'), indent=2)


# ---------- the round ----------

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--config', default=os.path.join(HERE, 'config.yaml'))
    ap.add_argument('--out', default=RESULTS)
    ap.add_argument('--max-minutes', type=float, help='stop cleanly after this many minutes (exit 3); a Claude Code cloud background command lives 120: use 110')
    ap.add_argument('--resume', action='store_true', help='continue the round in progress (benchmark/results/.round.json)')
    ap.add_argument('--new', action='store_true', help='discard a round in progress and start again')
    ap.add_argument('--skip-preflight', action='store_true', help='start without the sample (not for the real round)')
    ap.add_argument('--only', help='comma-separated models: run only these entries of release.runs')
    ap.add_argument('--dry-run', action='store_true', help='print the plan and stop')
    ap.add_argument('--child-args', default='', help='test only: extra flags for every run.py, e.g. "--mock --runs 1 --questions L4-0"')
    ap.add_argument('--archive-dir', help='test only: where earlier run folders go (default project/archive/benchmark-results-before-<date>)')
    a = ap.parse_args()
    cfg = yaml.safe_load(open(a.config))
    rel = cfg['release']
    started = time.monotonic()
    deadline = started + a.max_minutes * 60 if a.max_minutes else None
    lock = threading.Lock()

    state = load_state(a.out)
    if state and not (a.resume or a.new or a.dry_run):
        sys.exit(f'A round is in progress ({os.path.join(a.out, STATE)}). Continue it with --resume, or discard it with --new.')
    if a.new:
        state = None
    if a.resume and not state:
        sys.exit('No round in progress: nothing to resume. Start one without --resume.')
    only = set(a.only.split(',')) if a.only else None
    plan = [p for p in rel['runs'] if not only or p['model'] in only]

    if a.dry_run:
        print(f'Round plan: {len(plan)} runs, {cfg["runs"]} runs per question, judge {cfg["judge_model"]}.')
        for p in plan:
            print(f'  {p["model"]}: {", ".join(p["modes"])}  settings {json.dumps((cfg.get("model_params") or {}).get(p["model"]) or [{}])}')
        print(f'  folders: {a.out}/<date>-<model>; limit {rel["max_cost_usd"]} US$, {rel["max_hours"]} h')
        return

    if not os.environ.get('AI_GATEWAY_API_KEY'):
        sys.exit('AI_GATEWAY_API_KEY is not set.')

    # 1. preflight (a fresh round only: a resume keeps the settings its folders started with)
    if not state:
        state = {'started': dt.datetime.now().isoformat(timespec='seconds'), 'runs': []}
        if not a.skip_preflight:
            import preflight
            from llm import GatewayClient
            print('Preflight: a sample per model and mode (about 3 minutes, under US$ 1).', flush=True)
            rep = preflight.run_preflight(cfg, a.config, plan, GatewayClient(cfg['gateway']), log=lambda s: print(s, flush=True), only=only)
            preflight.show(rep, log=lambda s: print(s, flush=True))
            json.dump(rep, open(os.path.join(a.out, PREFLIGHT), 'w'), indent=2, default=str)
            if rep['refused']:
                sys.exit(X.BUDGET)
            if not rep['ok']:
                print('Preflight failed: the round is not started and nothing more is spent. Fix the cause named above, then start again.')
                sys.exit(X.PREFLIGHT)
            verdict = rep['runs']
        else:
            verdict = {}
        for p in plan:
            ladder = (cfg.get('model_params') or {}).get(p['model']) or [{}]
            params = verdict[p['model']]['params'] if p['model'] in verdict else ladder[0]
            state['runs'].append({'model': p['model'], 'modes': p['modes'], 'folder': run_name([p['model']], a.out), 'params': params,
                                  'rung': ladder.index(params) if params in ladder else 0, 'status': 'pending', 'note': '', 'retries': 0})
        save_state(a.out, state, lock)
    import questions as C
    n_questions = len([c for c in C.load() if c.scorable])

    stop_all = threading.Event()

    def left():
        return None if deadline is None else (deadline - time.monotonic()) / 60

    def drive(entry):
        """Run one entry to the end, a limit stop, or a failure. Returns nothing: the entry carries the result."""
        folder = os.path.join(a.out, entry['folder'])
        if entry['status'] in ('complete', 'invalid', 'refused'):
            return
        while not stop_all.is_set():
            mins = left()
            if mins is not None and mins < 3:
                entry['status'] = 'stopped'
                return
            resume = os.path.exists(os.path.join(folder, 'config.json'))
            cmd = child_cmd(entry, a.out, (mins - 1) if mins is not None else 100000, resume, a.child_args)
            entry['status'] = 'running'
            save_state(a.out, state, lock)
            os.makedirs(folder, exist_ok=True)
            with open(os.path.join(folder, 'run.log'), 'a') as log:
                log.write(f'\n--- {dt.datetime.now().isoformat(timespec="seconds")} {" ".join(cmd[2:])}\n')
                log.flush()
                code = subprocess.call(cmd, stdout=log, stderr=subprocess.STDOUT)
            kind = classify(code)
            entry['exit'] = code
            if kind == 'complete':
                bad = unresolved(folder)
                if bad and entry['retries'] < rel['retries']:
                    entry['retries'] += 1
                    entry['note'] = f'{len(bad)} answers failed; retry {entry["retries"]}'
                    continue
                entry['status'] = 'complete' if not bad else 'failed'
                entry['note'] = '' if not bad else f'{len(bad)} answers still failing after {entry["retries"]} retries'
                return
            if kind == 'stopped':
                entry['status'] = 'stopped'
                return
            if kind == 'crashed' and entry['retries'] < rel['retries']:
                entry['retries'] += 1
                entry['note'] = f'crashed (exit {code}); relaunch {entry["retries"]} with --resume'
                time.sleep(5)
                continue
            tail = open(os.path.join(folder, 'run.log')).read()[-400:].strip().replace('\n', ' | ')
            ladder = (cfg.get('model_params') or {}).get(entry['model']) or [{}]
            if kind == 'invalid' and entry.get('rung', 0) + 1 < len(ladder):
                # Recovery: the answers were invalid with these settings. Keep the folder as evidence (it is archived at the end),
                # and start the run again, from the beginning, with the next entry of the model's list.
                bad_folder = f'{folder}-invalid-{entry.get("rung", 0)}'
                os.rename(folder, bad_folder)
                entry['rung'] = entry.get('rung', 0) + 1
                entry['params'] = ladder[entry['rung']]
                entry['retries'] = 0
                entry['note'] = f'settings {entry["rung"] - 1} gave invalid answers; restarted with {json.dumps(entry["params"])}'
                print(f'{entry["model"]}: {entry["note"]}', flush=True)
                continue
            entry['status'] = {'invalid': 'invalid', 'refused': 'refused'}.get(kind, 'failed')
            entry['note'] = f'exit {code}: {tail}'
            if kind == 'refused':
                stop_all.set()
            return

    def report_progress():
        while not done.wait(300 if not os.environ.get('RUN_ALL_FAST') else 1):
            lines = []
            for e in state['runs']:
                ok, bad = count_valid(os.path.join(a.out, e['folder']))
                tot = total_answers(e, cfg, n_questions)
                lines.append(f'{e["model"].split("/")[-1]}: {ok}/{tot} ({100 * ok // max(tot, 1)}%), {bad} errors, {e["status"]}')
            msg = f'[{dt.datetime.now():%H:%M}] ' + ' | '.join(lines)
            print(msg, flush=True)
            open(os.path.join(a.out, PROGRESS), 'w').write(msg + '\n')

    done = threading.Event()
    threading.Thread(target=report_progress, daemon=True).start()
    live = [e for e in state['runs'] if e['status'] not in ('complete', 'invalid', 'refused')]
    for e in live:
        if e['status'] in ('stopped', 'running', 'failed'):
            e['status'] = 'pending'         # a resume tries again
            e['retries'] = 0
    def safe_drive(entry):
        try:
            drive(entry)
        except Exception as e:      # noqa: BLE001  one run's bug must not kill the others
            entry['status'], entry['note'] = 'failed', f'orchestrator error: {e!r}'

    with ThreadPoolExecutor(max_workers=max(len(live), 1)) as ex:
        list(ex.map(safe_drive, live))
    done.set()
    save_state(a.out, state, lock)

    by = {s: [e for e in state['runs'] if e['status'] == s] for s in ('complete', 'stopped', 'invalid', 'refused', 'failed', 'pending')}
    print('\nRound status:')
    for e in state['runs']:
        ok, bad = count_valid(os.path.join(a.out, e['folder']))
        print(f'  {e["folder"]}: {e["status"]}  {ok}/{total_answers(e, cfg, n_questions)} answers, {bad} errors  {e.get("note", "")}')
    if by['refused']:
        print('The gateway refused (HTTP 402/401/403): raise the key budget or add credits (benchmark/RUN.md, section Before you start), then run_all.py --resume.')
        sys.exit(X.BUDGET)
    if by['stopped'] or by['pending']:
        print('Time limit reached. Relaunch: python3 benchmark/runner/run_all.py --resume --max-minutes 110')
        sys.exit(X.STOPPED)
    if by['invalid'] or by['failed']:
        print('The round is NOT complete: the runs above failed. Nothing was summarized or archived. Do not merge a partial round.')
        sys.exit(X.PARTIAL if by['complete'] else X.UNHEALTHY)

    # 4. complete
    import report
    import summarize
    folders = [os.path.join(a.out, e['folder']) for e in state['runs']]
    for f in folders:
        report.write(f)                     # a retried run needs its report again
    open(os.path.join(a.out, 'README.md'), 'w').write(summarize.build(folders))
    day = state['started'][:10]
    arch = a.archive_dir or os.path.join(ROOT, 'project', 'archive', f'benchmark-results-before-{day}')
    moved = archive_old(a.out, {e['folder'] for e in state['runs']}, arch)
    for name in (STATE, PROGRESS, PREFLIGHT):
        if os.path.exists(os.path.join(a.out, name)):
            os.remove(os.path.join(a.out, name))
    print(f'ROUND COMPLETE. {len(folders)} runs. Wrote {os.path.join(a.out, "README.md")}.')
    if moved:
        print(f'Earlier run folders moved to {os.path.relpath(arch, ROOT)}/: {", ".join(moved)}')
    print('Next: lint and tests, update project/plan.md, commit, push, pull request, merge (benchmark/RUN.md, section After the round).')
    sys.exit(X.OK)


if __name__ == '__main__':
    main()
