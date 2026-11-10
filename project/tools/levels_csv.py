"""Round trip the `levels` table of knowledge/catalog/thresholds-performance.yaml through a CSV file.

  python3 project/tools/levels_csv.py export [file.csv]   # default project/levels.csv
  python3 project/tools/levels_csv.py import [file.csv]   # writes the levels section back, then run lint

Columns: object, metric, direction, 5m yellow/orange/red, 20s yellow/orange/red, 2s yellow/orange/red, from.
An empty cell means no source gives the value. A row interval is kept only when all three cells are filled.
"""
import csv, json, os, sys
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
YAML = os.path.join(ROOT, 'knowledge', 'catalog', 'thresholds-performance.yaml')
IVS, LVS = ('5m', '20s', '2s'), ('yellow', 'orange', 'red')
HEAD = ['object', 'metric', 'direction'] + [f'{i} {l}' for i in IVS for l in LVS] + ['from']


def _num(s):
    f = float(s)
    return int(f) if f == int(f) else f


def export(path):
    rows = yaml.safe_load(open(YAML)).get('levels') or []
    with open(path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(HEAD)
        for r in rows:
            w.writerow([r['object'], r['metric'], r['direction']]
                       + [('' if r.get(i) is None else r[i][n]) for i in IVS for n in range(3)] + [r['from']])
    print(f'{len(rows)} rows written to {path}')


def load(path):
    out = []
    for r in csv.DictReader(open(path, newline='', encoding='utf-8-sig')):
        if not (r.get('metric') or '').strip():
            continue
        line = {'object': r['object'].strip(), 'metric': r['metric'].strip(), 'direction': r['direction'].strip()}
        for i in IVS:
            cells = [(r.get(f'{i} {l}') or '').strip().replace(',', '') for l in LVS]
            if any(cells) and not all(cells):
                sys.exit(f'{line["metric"]}: {i} needs all of yellow, orange, red, or none')
            line[i] = [_num(c) for c in cells] if all(cells) else None
        line['from'] = r['from'].strip()
        out.append(line)
    return out


def _flow(v):
    return 'null' if v is None else '[' + ', '.join(str(x) for x in v) + ']'


def write(lines):
    text = open(YAML).read()
    head = text[:text.index('\nlevels:')]
    body = [f"- {{object: {l['object']}, metric: {json.dumps(l['metric'])}, direction: {l['direction']}, "
            f"5m: {_flow(l['5m'])}, 20s: {_flow(l['20s'])}, 2s: {_flow(l['2s'])}, from: {l['from']}}}" for l in lines]
    open(YAML, 'w').write(head + '\nlevels:\n' + '\n'.join(body) + '\n')
    print(f'{len(lines)} rows written to {YAML}. Run: python3 project/tools/lint.py')


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, 'project', 'levels.csv')
    if cmd == 'export':
        export(path)
    elif cmd == 'import':
        write(load(path))
    else:
        sys.exit(__doc__)
