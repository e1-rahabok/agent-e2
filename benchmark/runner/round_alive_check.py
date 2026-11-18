#!/usr/bin/env python3
"""Is the round alive? One command for every progress check.

2026-11-16: the machine restarted twice and killed two runs; the progress reports read the stale answer counts as progress for
25 minutes. A progress report says "running" only when this command says ALIVE and the counts moved.

For each run folder of the round (.round.json, or --folders) it prints:
  - whether a process of run_executor.py works on the folder;
  - good answers against the total, and the time of the last written answer (minutes ago);
  - the cost so far;
  and a verdict: DONE, ALIVE, STALLED (no answer written for --stall-minutes), DEAD (not finished, no process: relaunch with --resume),
  MACHINE RESTARTED (the machine booted after the last answer was written).
LOW BUDGET is printed when the cost of the runs reaches --warn-share of --budget (default release.max_cost_usd of runner_config.yaml).

  python3 benchmark/runner/round_alive_check.py
  python3 benchmark/runner/round_alive_check.py --budget 100 --stall-minutes 5

Exit code 0: every run is DONE or ALIVE. 2: a run is STALLED, DEAD or the machine restarted, or the budget is low.
"""
import argparse
import csv
import datetime as dt
import json
import os
import re
import subprocess
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, '..', 'results')
CHILD = 'run_executor.py'


def folder_numbers(folder):
    """(good answers, total, cost US$, time of the last written answer or None) of one run folder."""
    total = 0
    try:
        c = json.load(open(os.path.join(folder, 'config.json'), encoding='utf-8'))
        total = len(c.get('questions') or []) * int(c.get('runs') or 0) * len(c.get('modes') or [])
    except (OSError, ValueError):
        pass
    path = os.path.join(folder, 'answers.csv')
    if not os.path.exists(path):
        return 0, total, 0.0, None
    good, cost = set(), 0.0
    with open(path, encoding='utf-8', newline='') as f:
        for r in csv.DictReader(f):
            if not r.get('error'):
                good.add((r['model'], r['mode'], r['question_id'], r['track'], r['run']))
            cost += float(r.get('cost_usd') or 0)
    return len(good), total, cost, dt.datetime.fromtimestamp(os.path.getmtime(path))


def processes_for(folder_name, ps_lines):
    """Processes of run_executor.py (or run.py, its old name) that work on this folder."""
    return [ln for ln in ps_lines if (CHILD in ln or re.search(r'(^|[/\s])run\.py\b', ln)) and folder_name in ln]


def run_status(folder, now, ps_lines, boot_time, stall_minutes=5):
    name = os.path.basename(os.path.normpath(folder))
    good, total, cost, last = folder_numbers(folder)
    alive = bool(processes_for(name, ps_lines))
    minutes = None if last is None else (now - last).total_seconds() / 60
    if total and good >= total:
        verdict = 'DONE'
    elif last is not None and boot_time is not None and boot_time > last and not alive:
        verdict = 'MACHINE RESTARTED'
    elif not alive:
        verdict = 'DEAD'
    elif minutes is not None and minutes > stall_minutes:
        verdict = 'STALLED'
    else:
        verdict = 'ALIVE'
    return {'folder': name, 'verdict': verdict, 'alive': alive, 'good': good, 'total': total, 'cost': cost, 'minutes_since_write': minutes}


def ps_lines():
    out = subprocess.run(['ps', '-eo', 'args'], capture_output=True, text=True).stdout
    return [ln for ln in out.splitlines() if ln.strip()]


def boot_time(now):
    try:
        up = float(open('/proc/uptime').read().split()[0])
        return now - dt.timedelta(seconds=up)
    except (OSError, ValueError):
        return None


def folders_of_round(results):
    state = os.path.join(results, '.round.json')
    if os.path.exists(state):
        return [os.path.join(results, e['folder']) for e in json.load(open(state, encoding='utf-8'))['runs']]
    return sorted(os.path.dirname(p) for p in
                  (os.path.join(results, n, 'config.json') for n in os.listdir(results)) if os.path.exists(p))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--results', default=RESULTS)
    ap.add_argument('--folders', nargs='+', help='run folders (default: the runs of .round.json, else every folder with a config.json)')
    ap.add_argument('--config', default=os.path.join(HERE, 'runner_config.yaml'))
    ap.add_argument('--stall-minutes', type=float, default=5)
    ap.add_argument('--budget', type=float, help='US$ to warn against (default: release.max_cost_usd of the config)')
    ap.add_argument('--warn-share', type=float, default=0.8)
    a = ap.parse_args()
    now = dt.datetime.now()      # answers.csv times are local times of the machine
    folders = a.folders or folders_of_round(a.results)
    budget = a.budget if a.budget is not None else (yaml.safe_load(open(a.config, encoding='utf-8')).get('release') or {}).get('max_cost_usd')
    lines, boot, rows = ps_lines(), boot_time(now), []
    print(f'{now:%H:%M:%S} machine up {((now - boot).total_seconds() / 60 if boot else float("nan")):.0f} min (booted {boot:%H:%M:%S})' if boot else f'{now:%H:%M:%S}')
    for f in folders:
        rows.append(run_status(f, now, lines, boot, a.stall_minutes))
    for r in rows:
        ago = '-' if r['minutes_since_write'] is None else f'{r["minutes_since_write"]:.1f} min ago'
        print(f'  {r["verdict"]:<18} {r["folder"]}: {r["good"]}/{r["total"]} good, last write {ago}, US$ {r["cost"]:.2f}')
    spent = sum(r['cost'] for r in rows)
    low = bool(budget) and spent >= a.warn_share * budget
    if budget:
        print(f'  spend of these runs US$ {spent:.2f} of the budget US$ {budget:.0f}' + ('  LOW BUDGET' if low else ''))
    bad = [r for r in rows if r['verdict'] not in ('DONE', 'ALIVE')]
    for r in bad:
        print(f'  -> {r["folder"]}: {r["verdict"]}. Relaunch with: python3 benchmark/runner/{CHILD} --out benchmark/results --resume benchmark/results/{r["folder"]}')
    sys.exit(2 if bad or low else 0)


if __name__ == '__main__':
    main()
