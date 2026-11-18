#!/usr/bin/env python3
"""Push a snapshot of the run folders to a separate git branch, without touching the working branch.

Why: the run folders exist only on the machine that runs the round. 2026-11-16: the machine stopped twice; had it lost its disk, every
answer since the last hand-made push would have been lost. A snapshot costs seconds and never touches the running processes.

What: the answers.csv, config.json and report.md of every run folder under benchmark/results (traces.jsonl and run.log stay out: they are
large and not needed to resume). Each snapshot is one commit on the branch `snapshots/round-<date>`, chained on the previous snapshot,
built with a temporary git index, so the working branch, its index and its files are not touched.

The branch is never merged: a merge commit would keep every snapshot in main for good. The author deletes it after the round
(a cloud session cannot delete a branch).

  python3 benchmark/runner/run_folders_backup.py            # one snapshot now
  python3 benchmark/runner/run_folders_backup.py --no-push  # commit to the local branch only

round_executor.py takes one every `snapshots.every_minutes` (runner_config.yaml) and one at the end of the round.
"""
import argparse
import datetime as dt
import glob
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
KEEP = ('answers.csv', 'config.json', 'report.md')


def git(repo, *args, env=None, check=True):
    p = subprocess.run(['git', '-C', repo, *args], capture_output=True, text=True, env=env)
    if check and p.returncode:
        raise RuntimeError(f'git {" ".join(args)}: {p.stderr.strip() or p.stdout.strip()}')
    return p.stdout.strip()


def snapshot_files(repo, results):
    """Paths (relative to the repository) of the files to snapshot; files outside the repository are skipped."""
    out = []
    for folder in sorted(glob.glob(os.path.join(results, '*', 'config.json'))):
        d = os.path.dirname(folder)
        for name in KEEP:
            p = os.path.join(d, name)
            rel = os.path.relpath(os.path.realpath(p), os.path.realpath(repo))
            if os.path.exists(p) and not rel.startswith('..'):
                out.append(rel)
    return out


def branch_name(prefix='snapshots/round-', day=None):
    return f'{prefix}{day or dt.date.today().isoformat()}'


def snapshot(repo=ROOT, results=None, branch=None, remote='origin', push=True, message=None):
    """One snapshot commit. Returns the commit id, or None when nothing changed since the previous snapshot."""
    results = results or os.path.join(repo, 'benchmark', 'results')
    branch = branch or branch_name()
    files = snapshot_files(repo, results)
    if not files:
        return None
    ref = f'refs/heads/{branch}'
    with tempfile.TemporaryDirectory() as tmp:
        env = dict(os.environ, GIT_INDEX_FILE=os.path.join(tmp, 'index'))
        git(repo, 'read-tree', 'HEAD', env=env)
        git(repo, 'add', '-f', '--', *files, env=env)
        tree = git(repo, 'write-tree', env=env)
    previous = git(repo, 'rev-parse', '--verify', '--quiet', ref, check=False)
    parent = previous or git(repo, 'rev-parse', 'HEAD')
    if git(repo, 'rev-parse', f'{parent}^{{tree}}') == tree:
        return None
    msg = message or f'Benchmark round snapshot {dt.datetime.now():%Y-%m-%d %H:%M} (answers, configs and reports; no traces)'
    ident = {'GIT_AUTHOR_NAME': os.environ.get('GIT_AUTHOR_NAME') or git(repo, 'config', 'user.name', check=False) or 'benchmark runner',
             'GIT_AUTHOR_EMAIL': os.environ.get('GIT_AUTHOR_EMAIL') or git(repo, 'config', 'user.email', check=False) or 'runner@localhost'}
    ident.update(GIT_COMMITTER_NAME=ident['GIT_AUTHOR_NAME'], GIT_COMMITTER_EMAIL=ident['GIT_AUTHOR_EMAIL'])
    commit = git(repo, 'commit-tree', tree, '-p', parent, '-m', msg, env=dict(os.environ, **ident))
    git(repo, 'update-ref', ref, commit)
    if push:
        git(repo, 'push', '-q', remote, f'{ref}:{ref}')
    return commit


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--results')
    ap.add_argument('--branch')
    ap.add_argument('--remote', default='origin')
    ap.add_argument('--no-push', action='store_true')
    a = ap.parse_args()
    c = snapshot(ROOT, a.results, a.branch, a.remote, push=not a.no_push)
    print(f'snapshot {c[:12]} on {a.branch or branch_name()}' if c else 'nothing changed since the last snapshot')
    sys.exit(0)


if __name__ == '__main__':
    main()
