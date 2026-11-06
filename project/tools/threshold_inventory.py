"""List threshold statements in knowledge prose that have no row in the threshold files.

    python3 project/tools/threshold_inventory.py          # one line per statement: file, line, text
    python3 project/tools/threshold_inventory.py --count  # totals only

A statement counts when a line compares a metric with a number and a unit (above 5%, below 10 ms, at least 2 GB, ...).
Rows in knowledge/catalog/thresholds-*.yaml cover a line when their quote is in it; colour-band table rows are covered by
their band rows. Each listed line needs a row with its source, or the number goes if it has no source.
"""
import glob
import os
import re
import sys

import yaml

PAT = re.compile(r'\b(above|below|over|under|more than|less than|at least|at most|exceeds?|within|higher than|lower than)\s+'
                 r'\d[\d,.]*\s*(%|ms|µs|us|GB|MB|KB|GHz|MHz|x)\b|[<>]=?\s*\d[\d,.]*\s*(%|ms)', re.I)


def main():
    quotes = []
    for f in glob.glob('knowledge/catalog/thresholds-*.yaml'):
        quotes += [r['quote'] for r in yaml.safe_load(open(f))['rows'] if r.get('quote')]
    found = []
    for f in sorted(glob.glob('knowledge/**/*.md', recursive=True)):
        if '/raw-input/' in f or '/_templates/' in f:
            continue
        body = open(f).read().split('\n## Metadata')[0]
        for n, line in enumerate(body.split('\n'), 1):
            if line.lstrip().startswith('|') or line.lstrip().startswith('- "'):  # tables (bands) and trap lines
                continue
            if PAT.search(line) and not any(q in line for q in quotes):
                found.append((f, n, line.strip()[:160]))
    if '--count' in sys.argv:
        print(f'{len(found)} statements in {len({x[0] for x in found})} files without a threshold row')
    else:
        for f, n, t in found:
            print(f'{f}:{n}: {t}')


if __name__ == '__main__':
    sys.exit(main())
