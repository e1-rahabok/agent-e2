#!/usr/bin/env python3
"""Resume the benchmark round that a machine restart interrupted, if there is one. Does nothing otherwise.

Called by the SessionStart hook (.claude/hooks/resume_unfinished_benchmark_round.sh), so a restart does not wait for the next progress check
(2026-11-16: the machine restarted twice and killed the runs both times; they stayed dead until a check noticed).

It starts `run_all_models_in_one_round.py --resume` in the background, detached, when ALL of these hold:
  - a round is in progress (benchmark/results/.round.json exists);
  - at least one run of it is unfinished by its folder (the folder exists and not every answer is there) and is not marked invalid
    (a real settings failure waits for the author);
  - no process of answer_questions_for_one_model.py is working on any of its folders.

  python3 benchmark/runner/resume_unfinished_round_if_any.py             # resume if needed
  python3 benchmark/runner/resume_unfinished_round_if_any.py --dry-run   # say what it would do
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
import check_round_is_alive as CA  # noqa: E402
import question_files_and_answer_parsing as C  # noqa: E402
import run_all_models_in_one_round as RA  # noqa: E402

RESULTS = os.path.join(HERE, '..', 'results')


def decide(results, cfg, n_questions, ps_lines):
    """('resume', [folders]) or ('nothing', reason)."""
    state_path = os.path.join(results, RA.STATE)
    if not os.path.exists(state_path):
        return 'nothing', 'no round in progress'
    state = json.load(open(state_path, encoding='utf-8'))
    unfinished = []
    for e in state['runs']:
        folder = os.path.join(results, e['folder'])
        if not os.path.isdir(folder):
            continue    # a state file left over from a finished round: its folders were renamed or archived
        ok, _ = RA.count_valid(folder)
        done = ok >= RA.total_answers(e, cfg, n_questions) and not RA.unresolved(folder)
        if not done and e['status'] != 'invalid':
            unfinished.append(e['folder'])
    if not unfinished:
        return 'nothing', 'every run is finished, or waits for the author (invalid)'
    working = [f for f in unfinished if CA.processes_for(f, ps_lines)]
    if working:
        return 'nothing', f'already running: {", ".join(working)}'
    return 'resume', unfinished


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--results', default=RESULTS)
    ap.add_argument('--config', default=os.path.join(HERE, 'config.yaml'))
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--max-minutes', default='110')
    a = ap.parse_args()
    if not os.path.exists(os.path.join(a.results, RA.STATE)):
        print('no round in progress: nothing to do')
        return
    cfg = yaml.safe_load(open(a.config, encoding='utf-8'))
    n_questions = len([c for c in C.load() if c.scorable])
    what, detail = decide(a.results, cfg, n_questions, CA.ps_lines())
    if what == 'nothing':
        print(f'nothing to do: {detail}')
        return
    cmd = [sys.executable, os.path.join(HERE, 'run_all_models_in_one_round.py'), '--out', a.results, '--resume', '--max-minutes', a.max_minutes]
    print(f'resuming {", ".join(detail)}: {" ".join(cmd)}')
    if a.dry_run:
        return
    log = open(os.path.join(a.results, '.resume-on-start.log'), 'a')
    subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, start_new_session=True)


if __name__ == '__main__':
    main()
