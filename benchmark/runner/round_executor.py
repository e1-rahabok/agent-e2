#!/usr/bin/env python3
"""Run a whole benchmark round without anyone at the keyboard: preflight, all runs in parallel, recovery, summary.

  python3 benchmark/runner/round_executor.py --milestone M3 --max-minutes 110   # start the round for a milestone (stops cleanly after 110 minutes: exit 3)
  python3 benchmark/runner/round_executor.py --resume --max-minutes 110   # continue after exit 3 (or after a top-up, exit 6)
  python3 benchmark/runner/round_executor.py --dry-run               # print the plan; no API call

Steps (benchmark/RUN.md has the full playbook):
  1. Preflight (round_sample_check.py): credits, a sample answered per model and mode, request settings chosen per model, time and cost projected.
     A run that fails the sample is not started. Nothing is spent on the long run before this passes.
  2. One run_executor.py per entry of config `release.runs`, all at once, each in its own folder `<date>-<model>`.
  3. Recovery: a crashed run is relaunched with --resume (config `release.retries` times); answers that failed are retried the same way;
     a run stopped by the time limit is relaunched by you with --resume. A run whose answers are invalid, or a refused key, is not retried.
  4. When every run is complete: round_summary.py writes benchmark/results/README.md, earlier run folders are deleted (git history keeps them).
The full round runs only for a milestone (R-E2-031): a new round needs --milestone. Answers whose inputs are unchanged are copied from
the earlier run folders (answer_reuse.py, R-E2-029). The round stops at its spending limit, release.max_cost_usd (spending_stop.py, R-E2-030).
Exit codes: exit_codes.py. 0 = the round is complete; 3 = relaunch with --resume; 6 = top up credits or key budget, then --resume;
9 = the spending limit was reached: tell the human; 4, 5, 7 = a run failed: read the printed list.
"""
import argparse
import csv
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'harness'))
import answer_reuse  # noqa: E402
import exit_codes  # noqa: E402
import spending_stop  # noqa: E402
from run_folder_names import run_name  # noqa: E402

ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
RESULTS = os.path.join(ROOT, 'benchmark', 'results')
STATE = '.round.json'
PROGRESS = '.progress.txt'
PREFLIGHT = '.preflight.json'


# ---------- pure helpers (tested) ----------

def classify(code):
    """What the exit code of one run_executor.py means for the orchestrator."""
    return {exit_codes.OK: 'complete', exit_codes.STOPPED: 'stopped', exit_codes.UNHEALTHY: 'invalid', exit_codes.BUDGET: 'refused', exit_codes.GATEWAY_DOWN: 'outage'}.get(code, 'crashed')


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


def reconcile_with_folders(state, out_dir, cfg, n_questions):
    """A resume starts from what the folders hold, not from what the state file says. A run whose folder has every answer is complete
    (it may have been finished by hand); a run stopped by the time limit, a refused key, an outage or a crash is pending again.
    Only a run the health check marked invalid (a real setting problem) stays as it is. Returns the entries that changed."""
    changed = []
    for e in state['runs']:
        folder = os.path.join(out_dir, e['folder'])
        ok, _ = count_valid(folder)
        before = e['status']
        if ok >= total_answers(e, cfg, n_questions) and not unresolved(folder):
            e['status'], e['note'] = 'complete', ''
        elif e['status'] in ('refused', 'stopped', 'running', 'failed', 'pending', 'outage'):
            e['status'] = 'pending'
        e['retries'], e['outage_waits'] = 0, 0
        if e['status'] != before:
            changed.append(e)
    return changed


def total_answers(entry, cfg, n_questions):
    return len(entry['modes']) * n_questions * entry.get('runs', cfg['runs'])


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
    cmd = [sys.executable, os.environ.get('RUN_ALL_CHILD') or os.path.join(HERE, 'run_executor.py'), '--out', out_dir, '--max-minutes', f'{minutes_left:.1f}'] + extra.split()
    if resume:
        cmd += ['--resume', os.path.join(out_dir, entry['folder'])]
    else:
        cmd += ['--models', entry['model'], '--modes', ','.join(entry['modes']), '--name', entry['folder'],
                '--runs', str(entry.get('runs') or ''),
                '--params', json.dumps({entry['model']: entry['params']} if entry.get('params') else {})]
        if not entry.get('runs'):
            i = cmd.index('--runs'); del cmd[i:i + 2]
        if entry.get('hosts'):
            cmd += ['--hosts', json.dumps({entry['model']: entry['hosts']})]
    return cmd


def round_folders(out_dir, state):
    """Every run folder of the round, the ones kept as evidence of invalid settings included: all of them spent money."""
    names = {e['folder'] for e in state['runs']}
    return [os.path.join(out_dir, n) for n in sorted(os.listdir(out_dir))
            if n in names or any(n.startswith(f'{x}-invalid-') for x in names)] if os.path.isdir(out_dir) else []


def list_price(out_dir, state):
    """List-price cost of the answers the round asked itself (reused answers cost nothing again)."""
    total = 0.0
    for f in round_folders(out_dir, state):
        path = os.path.join(f, 'answers.csv')
        if os.path.exists(path):
            with open(path, newline='') as fh:
                total += answer_reuse.new_spending(csv.DictReader(fh))
    return total


def set_stop_files(out_dir, state, on):
    """Write (on) or remove the spending stop file in every run folder of the round."""
    for e in state['runs']:
        folder = os.path.join(out_dir, e['folder'])
        path = os.path.join(folder, spending_stop.STOP_FILE)
        if on:
            os.makedirs(folder, exist_ok=True)
            open(path, 'w').write('The round reached its spending limit (release.max_cost_usd).\n')
        elif os.path.exists(path):
            os.remove(path)


def remove_old(results_dir, keep):
    """Delete run folders that are not part of this round; git history keeps them. Return their names."""
    removed = []
    for name in sorted(os.listdir(results_dir)):
        p = os.path.join(results_dir, name)
        if name in keep or not os.path.isdir(p) or not os.path.exists(os.path.join(p, 'config.json')):
            continue
        shutil.rmtree(p)
        removed.append(name)
    return removed


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
    ap.add_argument('--config', default=os.path.join(HERE, 'runner_config.yaml'))
    ap.add_argument('--out', default=RESULTS)
    ap.add_argument('--max-minutes', type=float, help='stop cleanly after this many minutes (exit 3); a Claude Code cloud background command lives 120: use 110')
    ap.add_argument('--resume', action='store_true', help='continue the round in progress (benchmark/results/.round.json)')
    ap.add_argument('--new', action='store_true', help='discard a round in progress and start again')
    ap.add_argument('--skip-preflight', action='store_true', help='start without the sample (not for the real round)')
    ap.add_argument('--only', help='comma-separated models: run only these entries of release.runs')
    ap.add_argument('--dry-run', action='store_true', help='print the plan and stop')
    ap.add_argument('--milestone', help='the milestone of the workspace ROADMAP.md this round serves, e.g. M3: a new round needs it (R-E2-031)')
    ap.add_argument('--child-args', default='', help='test only: extra flags for every run_executor.py, e.g. "--mock --runs 1 --questions L4-0"')
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
    if not (state or a.dry_run):
        if not a.milestone:
            ap.error('a new round needs --milestone, the milestone of the workspace ROADMAP.md it serves (for example M3): '
                     'the full round runs only before a milestone is closed (R-E2-031). Between milestones the free checks and the answer set test each change.')
        if not re.fullmatch(r'M\d+', a.milestone):
            ap.error(f'--milestone {a.milestone!r}: give a milestone of the workspace ROADMAP.md, such as M3')
    only = set(a.only.split(',')) if a.only else None
    plan = [p for p in rel['runs'] if not only or p['model'] in only]

    if a.dry_run:
        print(f'Round plan: {len(plan)} runs.')
        for p in plan:
            print(f'  {p["model"]}: {", ".join(p["modes"])}, {p.get("runs", cfg["runs"])} runs per question  settings {json.dumps((cfg.get("model_params") or {}).get(p["model"]) or [{}])}')
        print(f'  folders: {a.out}/<date>-<model>; limit {rel["max_cost_usd"]} US$ spent (the round stops there), {rel["max_hours"]} h')
        print('  a new round needs --milestone; answers whose inputs are unchanged are reused from the run folders already there')
        return

    if not os.environ.get('AI_GATEWAY_API_KEY'):
        sys.exit('AI_GATEWAY_API_KEY is not set.')

    # 1. preflight (a fresh round only: a resume keeps the settings its folders started with)
    if not state:
        state = {'started': dt.datetime.now().isoformat(timespec='seconds'), 'milestone': a.milestone, 'start_balance': None, 'runs': []}
        if not a.skip_preflight:
            import round_sample_check
            from model_client import GatewayClient
            print('Preflight: a sample per model and mode (about 3 minutes, under US$ 1).', flush=True)
            rep = round_sample_check.run_preflight(cfg, a.config, plan, GatewayClient(cfg['gateway']), log=lambda s: print(s, flush=True), only=only)
            round_sample_check.show(rep, log=lambda s: print(s, flush=True))
            json.dump(rep, open(os.path.join(a.out, PREFLIGHT), 'w'), indent=2, default=str)
            if rep['refused']:
                sys.exit(exit_codes.BUDGET)
            if not rep['ok']:
                print('Preflight failed: the round is not started and nothing more is spent. Fix the cause named above, then start again.')
                sys.exit(exit_codes.PREFLIGHT)
            verdict = rep['runs']
            state['start_balance'] = rep.get('credits')      # the spending stop counts the drop from here (spending_stop.py)
        else:
            verdict = {}
        hosts = {}
        if cfg.get('spread_runs_over_providers') and not a.skip_preflight and not a.child_args:
            import inference_providers
            client = GatewayClient(cfg['gateway'], retry_seconds=15)      # a host that is down must fail fast
            for p in plan:
                ladder = (cfg.get('model_params') or {}).get(p['model']) or [{}]
                params = verdict[p['model']]['params'] if p['model'] in verdict else ladder[0]
                hosts[p['model']] = inference_providers.choose_hosts(client, p['model'], params, log=lambda s: print(s, flush=True))
                print(f'{p["model"]}: runs spread over {hosts[p["model"]] or "one host (the gateway chooses)"}', flush=True)
        for p in plan:
            ladder = (cfg.get('model_params') or {}).get(p['model']) or [{}]
            params = verdict[p['model']]['params'] if p['model'] in verdict else ladder[0]
            state['runs'].append({'model': p['model'], 'modes': p['modes'], 'folder': run_name([p['model']], a.out), 'params': params,
                                  'rung': ladder.index(params) if params in ladder else 0, 'status': 'pending', 'note': '', 'retries': 0,
                                  'hosts': hosts.get(p['model'], []), 'runs': p.get('runs', cfg['runs'])})
        save_state(a.out, state, lock)
    import question_files
    n_questions = len([c for c in question_files.load() if c.scorable])

    stop_all = threading.Event()
    spent = threading.Event()
    balance = None
    if state.get('start_balance') is not None:
        from model_client import GatewayClient
        balance = GatewayClient(cfg['gateway']).credits
    stop = spending_stop.SpendingStop(rel['max_cost_usd'], lambda: list_price(a.out, state), state.get('start_balance'), balance,
                                      every_seconds=0 if os.environ.get('RUN_ALL_FAST') else 60)

    def check_spending():
        if not spent.is_set() and stop.reached():
            spent.set()
            set_stop_files(a.out, state, True)
            print(f'[{dt.datetime.now():%H:%M}] SPENDING LIMIT: US$ {stop.spent():.2f} spent of US$ {rel["max_cost_usd"]} '
                  '(release.max_cost_usd): no new answer starts; the answers in progress finish.', flush=True)

    def left():
        return None if deadline is None else (deadline - time.monotonic()) / 60

    def drive(entry):
        """Run one entry to the end, a limit stop, or a failure. Returns nothing: the entry carries the result."""
        folder = os.path.join(a.out, entry['folder'])
        if entry['status'] in ('complete', 'invalid'):
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
            if kind == 'outage':
                # The gateway or a provider failed, not the settings: keep every answer, wait, resume the same folder.
                waits = entry.get('outage_waits', 0)
                if waits < rel.get('outage_waits', 12):
                    entry['outage_waits'] = waits + 1
                    entry['note'] = f'gateway or provider failing (exit {code}); waiting, then resume {waits + 1}'
                    print(f'{entry["model"]}: {entry["note"]}', flush=True)
                    save_state(a.out, state, lock)
                    wait = 0.05 if os.environ.get('RUN_ALL_FAST') else rel.get('outage_wait_seconds', 180)
                    stop_all.wait(wait)
                    continue
                entry['status'], entry['note'] = 'failed', f'the gateway kept failing after {waits} waits'
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

    def spending_loop():
        while not done.wait(1 if os.environ.get('RUN_ALL_FAST') else 30):
            check_spending()
    snap = cfg.get('snapshots') or {}

    def take_snapshot():
        try:
            import run_folders_backup
            c = run_folders_backup.snapshot(ROOT, a.out, run_folders_backup.branch_name(snap.get('branch_prefix', 'snapshots/round-'), state['started'][:10]),
                                   snap.get('remote', 'origin'))
            if c:
                print(f'[{dt.datetime.now():%H:%M}] snapshot {c[:12]} pushed', flush=True)
        except Exception as e:      # noqa: BLE001  a snapshot must never stop the round
            print(f'[{dt.datetime.now():%H:%M}] snapshot failed: {e}', flush=True)

    def snapshot_loop():
        while not done.wait(snap.get('every_minutes', 15) * 60):
            take_snapshot()

    if snap.get('enabled') and not a.dry_run and not os.environ.get('RUN_ALL_NO_SNAPSHOTS'):
        threading.Thread(target=snapshot_loop, daemon=True).start()
    if a.resume:
        for e in reconcile_with_folders(state, a.out, cfg, n_questions):
            print(f'{e["folder"]}: {e["status"]} (from the folder: the state file said otherwise)', flush=True)
        save_state(a.out, state, lock)
        set_stop_files(a.out, state, False)        # a resume checks the limit again, which the human may have raised
    check_spending()
    threading.Thread(target=spending_loop, daemon=True).start()
    live = [e for e in state['runs'] if e['status'] not in ('complete', 'invalid')]
    for e in live:
        if e['status'] in ('stopped', 'running', 'failed', 'refused', 'outage'):
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
    check_spending()
    save_state(a.out, state, lock)
    if snap.get('enabled') and not os.environ.get('RUN_ALL_NO_SNAPSHOTS'):
        take_snapshot()

    by = {s: [e for e in state['runs'] if e['status'] == s] for s in ('complete', 'stopped', 'invalid', 'refused', 'failed', 'pending')}
    print('\nRound status:')
    for e in state['runs']:
        ok, bad = count_valid(os.path.join(a.out, e['folder']))
        print(f'  {e["folder"]}: {e["status"]}  {ok}/{total_answers(e, cfg, n_questions)} answers, {bad} errors  {e.get("note", "")}')
    if by['refused']:
        print('The gateway refused (HTTP 402/401/403): raise the key budget or add credits (benchmark/RUN.md, section Before you start), then round_executor.py --resume.')
        sys.exit(exit_codes.BUDGET)
    if spent.is_set() and (by['stopped'] or by['pending']):
        print(f'Spending limit reached: US$ {stop.spent():.2f} spent of US$ {rel["max_cost_usd"]} (release.max_cost_usd, R-E2-030). The round is NOT complete. '
              'Tell the human the amount. Only the human raises the limit; then: python3 benchmark/runner/round_executor.py --resume --max-minutes 110')
        sys.exit(exit_codes.SPENT)
    if by['stopped'] or by['pending']:
        print('Time limit reached. Relaunch: python3 benchmark/runner/round_executor.py --resume --max-minutes 110')
        sys.exit(exit_codes.STOPPED)
    if by['invalid'] or by['failed']:
        print('The round is NOT complete: the runs above failed. Nothing was summarized or archived. Do not merge a partial round.')
        sys.exit(exit_codes.PARTIAL if by['complete'] else exit_codes.UNHEALTHY)

    # 4. complete
    import score_report
    import round_summary
    folders = [os.path.join(a.out, e['folder']) for e in state['runs']]
    for f in folders:
        score_report.write(f)                     # a retried run needs its report again
    open(os.path.join(a.out, 'README.md'), 'w').write(round_summary.build(folders, milestone=state.get('milestone')))
    removed = remove_old(a.out, {e['folder'] for e in state['runs']})
    for name in (STATE, PROGRESS, PREFLIGHT):
        if os.path.exists(os.path.join(a.out, name)):
            os.remove(os.path.join(a.out, name))
    print(f'ROUND COMPLETE. {len(folders)} runs. Wrote {os.path.join(a.out, "README.md")}.')
    if removed:
        print(f'Earlier run folders deleted (git history keeps them): {", ".join(removed)}')
    print('Next: lint and tests, update project/plan.md, commit, push, pull request, merge (benchmark/RUN.md, section After the round).')
    sys.exit(exit_codes.OK)


if __name__ == '__main__':
    main()
