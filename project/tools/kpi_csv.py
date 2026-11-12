"""Round trip the `kpi` section of knowledge/catalog/thresholds-performance.yaml through a CSV file.

  python3 project/tools/kpi_csv.py export [file.csv]   # default project/kpi.csv
  python3 project/tools/kpi_csv.py import [file.csv]   # writes the kpi section back, then run lint

Columns: object, metric, direction, then green, yellow, orange, red, zero for each of 5m, 20s, 2s.
Each value is where the colour starts; zero is where red ends (score 0). An empty cell means no value entered yet.
An interval is kept only when all five cells are filled.
"""
import csv, json, os, sys
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
YAML = os.path.join(ROOT, 'knowledge', 'catalog', 'thresholds-performance.yaml')
IVS, LVS = ('5m', '20s', '2s'), ('green', 'yellow', 'orange', 'red', 'zero')
HEAD = ['object', 'metric', 'direction'] + [f'{i} {l}' for i in IVS for l in LVS]


def _num(s):
    f = float(s)
    return int(f) if f == int(f) else f


def export(path):
    rows = yaml.safe_load(open(YAML)).get('kpi') or []
    with open(path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(HEAD)
        for r in rows:
            w.writerow([r['object'], r['metric'], r['direction']]
                       + [('' if r.get(i) is None else r[i][n]) for i in IVS for n in range(len(LVS))])
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
                sys.exit(f'{line["metric"]}: {i} needs all of green, yellow, orange, red, zero, or none')
            line[i] = [_num(c) for c in cells] if all(cells) else None
        out.append(line)
    return out


def _flow(v):
    return 'null' if v is None else '[' + ', '.join(str(x) for x in v) + ']'


def write(lines):
    """Replace the values; keep group, kb and excluded_when_green of each existing line (matched by object and metric)."""
    text = open(YAML).read()
    head = text[:text.index('\nkpi:')]
    old = {(r['object'], r['metric']): r for r in yaml.safe_load(text).get('kpi') or []}
    body = []
    for l in lines:
        o = old.get((l['object'], l['metric']), {})
        ex = ', excluded_when_green: true' if o.get('excluded_when_green') else ''
        body.append(f"- {{object: {l['object']}, metric: {json.dumps(l['metric'])}, group: {json.dumps(o.get('group') or '')}, "
                    f"direction: {l['direction']}, 5m: {_flow(l['5m'])}, 20s: {_flow(l['20s'])}, 2s: {_flow(l['2s'])}{ex}, "
                    f"kb: {o.get('kb') or ''}}}")
    open(YAML, 'w').write(head + '\nkpi:\n' + '\n'.join(body) + '\n')
    print(f'{len(lines)} rows written to {YAML}. Run: python3 project/tools/lint.py')


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, 'project', 'kpi.csv')
    if cmd == 'export':
        export(path)
    elif cmd == 'import':
        write(load(path))
    else:
        sys.exit(__doc__)
