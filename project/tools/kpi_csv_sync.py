"""Round trip the five-limit lines of the threshold catalog through a CSV file, for editing in a spreadsheet.

  python3 project/tools/kpi_csv_sync.py export [file.csv]   # default project/kpi.csv
  python3 project/tools/kpi_csv_sync.py import [file.csv]   # writes the limits back, then run lint

Lines: thresholds-performance.yaml section kpi; thresholds-capacity.yaml and thresholds-risk.yaml sections model and score.
One format for all (thresholds-performance.yaml, meta, limits_fields).

Columns: file, section, object, metric, direction, then best, green, yellow, orange, zero-at for each of 5m, 20s, 2s:
the values where the score is 100, 75, 50, 25 and 0 (a limit is where a colour band ends). An empty cell means no value
entered yet; an interval is kept only when all five cells are filled. Import changes only the limits and the direction:
every other field of a line (key, description, group, excluded_when_green, kb) and every other section stay as they are.
"""
import csv
import json
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CATALOG = os.path.join(ROOT, 'knowledge', 'catalog')
SECTIONS = (('thresholds-performance.yaml', 'kpi'), ('thresholds-capacity.yaml', 'model'), ('thresholds-capacity.yaml', 'score'),
            ('thresholds-risk.yaml', 'model'), ('thresholds-risk.yaml', 'score'))
IVS, LIMITS = ('5m', '20s', '2s'), ('best', 'green', 'yellow', 'orange', 'zero-at')
HEAD = ['file', 'section', 'object', 'metric', 'direction'] + [f'{i} {l}' for i in IVS for l in LIMITS]


def _num(s):
    f = float(s)
    return int(f) if f == int(f) else f


def _lines(name, section):
    return yaml.safe_load(open(os.path.join(CATALOG, name), encoding='utf-8')).get(section) or []


def export(path):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(HEAD)
        n = 0
        for name, section in SECTIONS:
            for r in _lines(name, section):
                w.writerow([name, section, r['object'], r['metric'], r['direction']]
                           + [('' if r.get(i) is None else r[i][k]) for i in IVS for k in range(5)])
                n += 1
    print(f'{n} lines written to {path}')


def load(path):
    out = {}
    with open(path, newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            line = {'object': r['object'].strip(), 'metric': r['metric'].strip(), 'direction': r['direction'].strip()}
            for i in IVS:
                cells = [(r.get(f'{i} {l}') or '').strip().replace(',', '') for l in LIMITS]
                if any(cells) and not all(cells):
                    sys.exit(f'{line["metric"]}: {i} needs all five limits ({", ".join(LIMITS)}), or none')
                line[i] = [_num(c) for c in cells] if all(cells) else None
            out.setdefault((r['file'].strip(), r['section'].strip()), []).append(line)
    return out


def _flow(v):
    return 'null' if v is None else '[' + ', '.join(str(x) for x in v) + ']'


def _text(o, l):
    desc = f", description: {json.dumps(o['description'], ensure_ascii=False)}" if o.get('description') else ''
    ex = ', excluded_when_green: true' if o.get('excluded_when_green') else ''
    key = f", key: {json.dumps(o['key'], ensure_ascii=False)}" if o.get('key') else ''
    return (f"- {{object: {l['object']}, metric: {json.dumps(l['metric'], ensure_ascii=False)}{key}{desc}, group: {json.dumps(o.get('group') or '')}, "
            f"direction: {l['direction']}, 5m: {_flow(l['5m'])}, 20s: {_flow(l['20s'])}, 2s: {_flow(l['2s'])}{ex}, kb: {o.get('kb') or ''}}}")


def write(groups):
    """Replace one section's lines in place; keep the other fields of each line, matched by object and metric."""
    for (name, section), lines in groups.items():
        if (name, section) not in SECTIONS:
            sys.exit(f'{name} {section}: not a five-limit section')
        p = os.path.join(CATALOG, name)
        text = open(p, encoding='utf-8').read()
        m = re.search(rf'^{section}:\n(.*?)(?=^[A-Za-z_]+:|\Z)', text, re.M | re.S)  # up to the next section
        old = {(r['object'], r['metric']): r for r in _lines(name, section)}
        body = '\n'.join(_text(old.get((l['object'], l['metric']), {}), l) for l in lines) + '\n'
        open(p, 'w', encoding='utf-8').write(text[:m.start(1)] + body + text[m.end(1):])
        print(f'{len(lines)} lines written to {name}, section {section}')
    print('Run: python3 project/tools/rules_check.py')


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, 'project', 'kpi.csv')
    if cmd == 'export':
        export(path)
    elif cmd == 'import':
        write(load(path))
    else:
        sys.exit(__doc__)
