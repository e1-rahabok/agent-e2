#!/usr/bin/env python3
"""Resume the benchmark round that a machine restart interrupted, if there is one. Does nothing otherwise.

Called by the SessionStart hook (.claude/hooks/resume_unfinished_benchmark_round.sh), so a restart does not wait for the next progress check
(2026-11-16: the machine restarted twice and killed the runs both times; they stayed dead until a check noticed).

It starts `round_executor.py --resume` in the background, detached, when ALL of these hold:
  - a round is in progress (benchmark/results/.round.json exists);
  - at least one run of it is unfinished by its folder (the folder exists and not every answer is there) and is not marked invalid
    (a real settings failure waits for the author);
  - no process of run_executor.py is working on any of its folders.

  python3 benchmark/runner/round_resume.py             # resume if needed
  python3 benchmark/runner/round_resume.py --dry-run   # say what it would do
"""
import argparse
import json
import os
import subprocess
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'harness'))
import round_alive_check  # noqa: E402
import question_files  # noqa: E402
import round_executor  # noqa: E402

RESULTS = os.path.join(HERE, '..', 'results')


def decide(results, cfg, n_questions, ps_lines):
    """('resume', [folders]) or ('nothing', reason)."""
    state_path = os.path.join(results, round_executor.STATE)
    if not os.path.exists(state_path):
        return 'nothing', 'no round in progress'
    state = json.load(open(state_path, encoding='utf-8'))
    unfinished = []
    for e in state['runs']:
        folder = os.path.join(results, e['folder'])
        if not os.path.isdir(folder):
            continue    # a state file left over from a finished round: its folders were renamed or archived
        ok, _ = round_executor.count_valid(folder)
        done = ok >= round_executor.total_answers(e, cfg, n_questions) and not round_executor.unresolved(folder)
        if not done and e['status'] != 'invalid':
            unfinished.append(e['folder'])
    if not unfinished:
        return 'nothing', 'every run is finished, or waits for the author (invalid)'
    working = [f for f in unfinished if round_alive_check.processes_for(f, ps_lines)]
    if working:
        return 'nothing', f'already running: {", ".join(working)}'
    return 'resume', unfinished


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--results', default=RESULTS)
    ap.add_argument('--config', default=os.path.join(HERE, 'runner_config.yaml'))
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--max-minutes', default='110')
    a = ap.parse_args()
    if not os.path.exists(os.path.join(a.results, round_executor.STATE)):
        print('no round in progress: nothing to do')
        return
    cfg = yaml.safe_load(open(a.config, encoding='utf-8'))
    n_questions = len([c for c in question_files.load() if c.scorable])
    what, detail = decide(a.results, cfg, n_questions, round_alive_check.ps_lines())
    if what == 'nothing':
        print(f'nothing to do: {detail}')
        return
    cmd = [sys.executable, os.path.join(HERE, 'round_executor.py'), '--out', a.results, '--resume', '--max-minutes', a.max_minutes]
    print(f'resuming {", ".join(detail)}: {" ".join(cmd)}')
    if a.dry_run:
        return
    log = open(os.path.join(a.results, '.resume-on-start.log'), 'a')
    subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, start_new_session=True)


if __name__ == '__main__':
    main()
