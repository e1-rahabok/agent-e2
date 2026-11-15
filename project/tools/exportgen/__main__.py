"""Command line: python3 -m project.tools.exportgen <command>   (run from the repo root)

  list                      registered cases
  generate <id>|all         write benchmark/questions/<id>/<file> (or under --out)
  check <id>|all            re-read the files on disk, run each case's checks,
                            the size cap, and compare with a fresh generate
  --out DIR                 write to / read from DIR/<id>/ instead of benchmark/questions/<id>/

Exit code is non-zero on any failure. `python3 project/tools/exportgen` does
not work (relative imports); use -m from the repo root.
"""

import argparse
import sys
from pathlib import Path

from . import core


def _select(cases, which):
    if which == "all":
        return list(cases.values())
    if which not in cases:
        raise SystemExit(f"unknown case {which!r}; known: {', '.join(sorted(cases))}")
    return [cases[which]]


def run_generate(cases, which, out_root):
    for case in _select(cases, which):
        files = case.generate(case.seed)
        core.write_files(files, Path(out_root) / case.question_id)
        print(f"{case.question_id}: wrote {', '.join(files)}")
    return 0


def run_check(cases, which, out_root):
    bad = 0
    for case in _select(cases, which):
        expected = case.generate(case.seed)
        d = Path(out_root) / case.question_id
        fails = []
        try:
            files = core.read_files(expected, d)
        except OSError as e:
            fails.append(f"cannot read files: {e}")
            files = {}
        if files:
            fails += core.check_size_cap(files)
            fails += case.check(files)
            for name, text in files.items():
                if text != expected[name]:
                    fails.append(f"{name}: differs from the seeded output (edited or stale)")
        print(f"{case.question_id}: {'FAIL' if fails else 'ok'}")
        for f in fails:
            print(f"  - {f}")
        bad += bool(fails)
    return 1 if bad else 0


def main(argv=None):
    p = argparse.ArgumentParser(prog="exportgen", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("command", choices=["list", "generate", "check"])
    p.add_argument("target", nargs="?", default="all", help="question id or 'all'")
    p.add_argument("--out", default=str(core.QUESTIONS_DIR), help="output root (default benchmark/questions)")
    a = p.parse_args(argv)
    cases = core.load_cases()
    if a.command == "list":
        for cid in sorted(cases):
            print(f"{cid}\tseed={cases[cid].seed}")
        return 0
    if a.command == "generate":
        return run_generate(cases, a.target, a.out)
    return run_check(cases, a.target, a.out)


if __name__ == "__main__":
    sys.exit(main())
