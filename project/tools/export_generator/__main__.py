"""Command line: python3 -m project.tools.export_generator <command>   (run from the repo root)

  list                      registered cases
  generate <id>|all         write benchmark/questions/<id>/<file> (or under --out)
  check <id>|all            re-read the files on disk, run each case's checks,
                            the size cap, and compare with a fresh generate
  --out DIR                 write to / read from DIR/<id>/ instead of benchmark/questions/<id>/

Exit code is non-zero on any failure. `python3 project/tools/export_generator` does
not work (relative imports); use -m from the repo root.
"""

import argparse
import sys
from pathlib import Path

from . import export_framework


def _select(cases, which):
    if which == "all":
        return [c for c in cases.values() if c.question_id.isdigit()]  # examples: by id only
    if which not in cases:
        raise SystemExit(f"unknown case {which!r}; known: {', '.join(sorted(cases))}")
    return [cases[which]]


def run_generate(cases, which, out_root):
    for case in _select(cases, which):
        files = case.generate(case.seed)
        export_framework.write_files(files, Path(out_root) / case.question_id)
        wrote = list(files)
        inline = case.generate_inline(case.seed)
        if inline:
            qp = export_framework.question_path(case.question_id)
            if qp is None:
                raise SystemExit(f"{case.question_id}: question file not found for inline blocks")
            with open(qp, encoding="utf-8", newline="") as f:
                md = f.read()
            md = export_framework.write_inline_blocks(md, inline)
            with open(qp, "w", encoding="utf-8", newline="") as f:
                f.write(md)
            wrote += [f"inline:{n}" for n in sorted(inline)]
        print(f"{case.question_id}: wrote {', '.join(wrote)}")
    return 0


def _check_inline(case, files):
    """Blocks on disk equal a fresh generate (generated ones), then the case's own checks."""
    inline = case.generate_inline(case.seed)
    qp = export_framework.question_path(case.question_id)
    if qp is None:
        return ["question file not found"] if inline or type(case).check_inline is not export_framework.QuestionExport.check_inline else []
    with open(qp, encoding="utf-8", newline="") as f:
        blocks = export_framework.read_inline_blocks(f.read())
    fails = []
    for n, text in inline.items():
        if blocks.get(n) != text.rstrip("\n"):
            fails.append(f"inline:{n}: block in the question file differs from the seeded output (edited or stale)")
    return fails + case.check_inline(blocks, files)


def run_check(cases, which, out_root):
    bad = 0
    for case in _select(cases, which):
        expected = case.generate(case.seed)
        d = Path(out_root) / case.question_id
        fails = []
        try:
            files = export_framework.read_files(expected, d)
        except OSError as e:
            fails.append(f"cannot read files: {e}")
            files = {}
        if files:
            fails += export_framework.check_size_cap(files)
            fails += case.check(files)
            for name, text in files.items():
                if text != expected[name]:
                    fails.append(f"{name}: differs from the seeded output (edited or stale)")
        fails += _check_inline(case, files)
        print(f"{case.question_id}: {'FAIL' if fails else 'ok'}")
        for f in fails:
            print(f"  - {f}")
        bad += bool(fails)
    return 1 if bad else 0


def main(argv=None):
    p = argparse.ArgumentParser(prog="export_generator", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("command", choices=["list", "generate", "check"])
    p.add_argument("target", nargs="?", default="all", help="question id or 'all'")
    p.add_argument("--out", default=str(export_framework.QUESTIONS_DIR), help="output root (default benchmark/questions)")
    a = p.parse_args(argv)
    cases = export_framework.load_cases()
    if a.command == "list":
        for cid in sorted(cases):
            print(f"{cid}\tseed={cases[cid].seed}")
        return 0
    if a.command == "generate":
        return run_generate(cases, a.target, a.out)
    return run_check(cases, a.target, a.out)


if __name__ == "__main__":
    sys.exit(main())
