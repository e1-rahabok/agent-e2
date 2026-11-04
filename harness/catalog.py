"""Metric catalog: knowledge/catalog/*.yaml plus knowledge-file metadata, compiled to SQLite.

Exact lookups that do not depend on retrieval luck: unit, rollup and statistics level of a vCenter counter,
the esxtop field behind a name, thresholds with their source, and how managed objects relate.

Tables:
  counters    vCenter chart counters (knowledge/catalog/vcenter-counters.yaml)
  api_counters  counters as the vCenter API returns them, with API units (knowledge/catalog/vcenter-api-counters.yaml)
  esxtop      esxtop panel fields (knowledge/catalog/esxtop-fields.yaml)
  thresholds  curated thresholds (knowledge/catalog/thresholds.yaml) + colour bands parsed from knowledge files
  metrics     one row per knowledge metric file, from its metadata
  objects, relations   object model (knowledge/catalog/objects.yaml)
"""
import json
import os
import re
import sqlite3
import threading
from collections import deque

import yaml

from kb import ROOT

CATALOG_DIR = os.path.join(ROOT, 'knowledge', 'catalog')
ROLLUPS = ('average', 'summation', 'latest', 'maximum', 'minimum', 'none')
OBJECT_ALIASES = {
    'vm': 'VirtualMachine', 'virtual machine': 'VirtualMachine', 'virtualmachine': 'VirtualMachine',
    'host': 'HostSystem', 'esxi': 'HostSystem', 'esx': 'HostSystem', 'hostsystem': 'HostSystem',
    'cluster': 'ClusterComputeResource', 'clustercomputeresource': 'ClusterComputeResource',
    'datastore': 'Datastore', 'datastore cluster': 'StoragePod', 'storagepod': 'StoragePod',
    'resource pool': 'ResourcePool', 'resourcepool': 'ResourcePool', 'datacenter': 'Datacenter', 'data center': 'Datacenter',
}
BAND_HEAD = re.compile(r'^\|(.+)\|\s*Green\s*\|\s*Yellow\s*\|\s*Orange\s*\|\s*Red\s*\|\s*$')


def load_yaml(name):
    return yaml.safe_load(open(os.path.join(CATALOG_DIR, name)))


def norm_object(value):
    if not value:
        return None
    return OBJECT_ALIASES.get(value.strip().lower(), value.strip())


def bands_from_docs(docs):
    """Colour band tables (Green | Yellow | Orange | Red) in knowledge files, one row per metric."""
    out = []
    for d in docs.values():
        lines = d.body.split('\n')
        for i, line in enumerate(lines):
            m = BAND_HEAD.match(line.strip())
            if not m:
                continue
            lead = [c.strip() for c in m.group(1).split('|')]
            mcol = next((n for n, c in enumerate(lead) if c.lower() == 'metric'), len(lead) - 1)
            for row in lines[i + 2:]:
                if not row.strip().startswith('|'):
                    break
                cells = [c.strip() for c in row.strip().strip('|').split('|')]
                if len(cells) != len(lead) + 4:
                    continue
                out.append({'kb': d.id, 'group': ' / '.join(c for n, c in enumerate(cells[:len(lead)]) if n != mcol),
                            'metric': cells[mcol], 'green': cells[-4], 'yellow': cells[-3], 'orange': cells[-2], 'red': cells[-1],
                            'object': ', '.join(d.meta.get('object') or []), 'source': (d.meta.get('source') or {}).get('document', '')})
    return out


class Catalog:
    def __init__(self, docs):
        self.docs = docs
        self.lock = threading.Lock()
        self.db = sqlite3.connect(':memory:', check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self._build()

    # ---------- build ----------
    def _build(self):
        c = self.db
        c.executescript('''
          CREATE TABLE api_counters (counter TEXT, name TEXT, object TEXT, rollup TEXT, stat_type TEXT, unit TEXT, level INT,
                                     summary TEXT, kb TEXT);
          CREATE TABLE counters (counter TEXT, name TEXT, grp TEXT, object TEXT, shows TEXT, chart TEXT, label TEXT, unit TEXT,
                                 stat_type TEXT, rollup TEXT, level INT, minmax_level INT, description TEXT, page INT, kb TEXT);
          CREATE TABLE esxtop (panel TEXT, field TEXT, key TEXT, description TEXT, page INT);
          CREATE TABLE thresholds (id TEXT, metric TEXT, object TEXT, layer TEXT, operator TEXT, value REAL, value_high REAL, unit TEXT,
                                   condition TEXT, meaning TEXT, source TEXT, kb TEXT);
          CREATE TABLE bands (kb TEXT, grp TEXT, metric TEXT, object TEXT, green TEXT, yellow TEXT, orange TEXT, red TEXT, source TEXT);
          CREATE TABLE metrics (id TEXT, title TEXT, object TEXT, layer TEXT, technology TEXT, metric_class TEXT, instance TEXT,
                                same_name TEXT, same_meaning TEXT, status TEXT);
          CREATE TABLE objects (type TEXT, role TEXT, layer TEXT, supplies TEXT, charts INT, note TEXT, kb TEXT);
          CREATE TABLE relations (src TEXT, dst TEXT, kind TEXT, cardinality TEXT);
          CREATE TABLE formulas (formula TEXT, source TEXT);
        ''')
        for r in load_yaml('vcenter-api-counters.yaml')['rows']:
            c.execute('INSERT INTO api_counters VALUES (?,?,?,?,?,?,?,?,?)',
                      (r['counter'], r['counter'].split('.', 1)[1], r['object'], r['rollup'], r['stat_type'], r['unit'],
                       r['level'], r.get('summary', ''), r.get('kb')))
        cv = load_yaml('vcenter-counters.yaml')
        for r in cv['rows']:
            grp, _, name = r['counter'].rpartition('.') if r['counter'].count('.') == 1 else (r['counter'].split('.')[0], '', '.'.join(r['counter'].split('.')[1:]))
            if '.' not in r['counter']:
                grp, name = '', r['counter']
            c.execute('INSERT INTO counters VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                      (r['counter'], name, grp, r['object'], r.get('shows'), r['chart'], r['label'], r['unit'], r['stat_type'],
                       r['rollup'], r['level'], r.get('minmax_level'), r.get('description', ''), r.get('page'), r.get('kb')))
        doc = cv['meta']['source']['document']
        es = load_yaml('esxtop-fields.yaml')
        for r in es['rows']:
            c.execute('INSERT INTO esxtop VALUES (?,?,?,?,?)', (r['panel'], r['field'], _esx_key(r['field']), r['description'], r.get('page')))
        for f in es.get('formulas') or []:
            c.execute('INSERT INTO formulas VALUES (?,?)', (f['formula'], f'esxtop {f["panel"]} panel, {doc}, p. {f["page"]}'))
        for r in load_yaml('thresholds.yaml')['rows']:
            c.execute('INSERT INTO thresholds VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
                      (r['id'], r['metric'], r.get('object'), r.get('layer'), r['operator'], r['value'], r.get('value_high'), r.get('unit'),
                       r.get('condition'), r.get('meaning'), r['source'], r['kb']))
        for b in bands_from_docs(self.docs):
            c.execute('INSERT INTO bands VALUES (?,?,?,?,?,?,?,?,?)',
                      (b['kb'], b['group'], b['metric'], b['object'], b['green'], b['yellow'], b['orange'], b['red'], b['source']))
        for d in self.docs.values():
            if '/metrics/' not in d.id:
                continue
            m = d.meta
            c.execute('INSERT INTO metrics VALUES (?,?,?,?,?,?,?,?,?,?)',
                      (d.id, d.title, ', '.join(m.get('object') or []), ', '.join(m.get('layer') or []), ', '.join(m.get('technology') or []),
                       m.get('metric_class') or '', ', '.join(m.get('instance') or []), ', '.join(m.get('same_name') or []),
                       ', '.join(m.get('same_meaning') or []), d.status))
        ob = load_yaml('objects.yaml')
        self.layers = ob['layers']
        for o in ob['objects']:
            c.execute('INSERT INTO objects VALUES (?,?,?,?,?,?,?)',
                      (o['type'], o['role'], o.get('layer'), ', '.join(o.get('supplies') or []), int(bool(o.get('charts'))),
                       o.get('note', ''), ', '.join(o.get('kb') or [])))
        for r in ob['relations']:
            c.execute('INSERT INTO relations VALUES (?,?,?,?)', (r['from'], r['to'], r['kind'], r['cardinality']))
        c.commit()

    def _q(self, sql, args=()):
        with self.lock:
            return [dict(r) for r in self.db.execute(sql, args).fetchall()]

    # ---------- lookups ----------
    def lookup(self, name, object=None, limit=8):
        """Find a metric by vCenter counter (cpu.ready.summation), chart label (Ready), esxtop field (%RDY, DAVG)
        or knowledge-file title. Returns counters, esxtop fields, metric files and thresholds, best first."""
        q = (name or '').strip()
        obj = norm_object(object)
        key = q.lower()
        parts = key.split('.')
        if len(parts) > 1 and parts[-1] in ROLLUPS:
            key = '.'.join(parts[:-1])
        words = [w for w in re.findall(r'[a-z0-9%]+', key) if len(w) > 1 or w == '%']
        counters = []
        for r in self._q('SELECT * FROM counters' + (' WHERE object = ?' if obj else ''), (obj,) if obj else ()):
            s = _score(key, words, exact=[r['counter'].lower(), r['name'].lower(), r['label'].lower()],
                       text=f"{r['counter']} {r['label']} {r['chart']}".lower(), desc=r['description'].lower())
            if s:
                counters.append((s, r))
        api = []
        for r in self._q('SELECT * FROM api_counters' + (' WHERE object = ?' if obj else ''), (obj,) if obj else ()):
            s = _score(key, words, exact=[r['counter'].lower(), r['name'].lower()], text=r['counter'].lower(), desc=r['summary'].lower())
            if s:
                api.append((s, r))
        esx = []
        ek = _esx_key(q)
        for r in self._q('SELECT * FROM esxtop'):
            s = 100 if ek and r['key'] == ek else _score(key, words, exact=[r['field'].lower()], text=r['field'].lower(), desc=r['description'].lower()) // 2
            if s:
                esx.append((s, r))
        metrics = []
        for r in self._q('SELECT * FROM metrics'):
            if obj and obj not in r['object'].split(', '):
                continue
            s = _score(key, words, exact=[r['title'].lower()], text=r['title'].lower(), desc='')
            if s:
                metrics.append((s, r))
        counters, esx, metrics, api = _best(counters, limit * 3), _best(esx, limit), _best(metrics, limit), _best(api, limit)
        seen, uniq = set(), []
        for r in counters:   # the same counter appears on several charts of one object
            k = (r['counter'], r['object'], r['unit'], r['rollup'], r['level'])
            if k not in seen:
                seen.add(k)
                uniq.append(r)
        counters = uniq[:limit]
        kb_ids = list(dict.fromkeys([r['kb'] for r in counters + api if r['kb']] + [r['id'] for r in metrics]))
        thresholds = self.thresholds(name=q, kb_ids=kb_ids, object=obj, limit=limit)
        return {'query': q, 'object': obj,
                'counters': [_compact(r, ('counter', 'object', 'shows', 'chart', 'label', 'unit', 'stat_type', 'rollup', 'level', 'minmax_level', 'kb')) for r in counters],
                'api': [_compact(r, ('counter', 'object', 'unit', 'stat_type', 'rollup', 'level', 'summary', 'kb')) for r in api],
                'esxtop': [_compact(r, ('panel', 'field', 'description')) for r in esx],
                'metric_files': [_compact(r, ('id', 'title', 'object', 'layer', 'metric_class', 'same_name')) for r in metrics],
                **thresholds}

    def thresholds(self, name=None, kb_ids=(), object=None, limit=8):
        """Thresholds and colour bands for a metric name and/or knowledge files."""
        obj = norm_object(object)
        key = (name or '').lower()
        words = [w for w in re.findall(r'[a-z0-9%]+', key) if len(w) > 2]
        th, bd = [], []
        for r in self._q('SELECT * FROM thresholds'):
            s = 50 if r['kb'] in kb_ids else 0
            s += _score(key, words, exact=[r['metric'].lower()], text=r['metric'].lower(), desc='') if key else 0
            if obj and r['object'] and r['object'] != obj:
                s //= 2
            if s:
                th.append((s, r))
        for r in self._q('SELECT * FROM bands'):
            s = 40 if r['kb'] in kb_ids else 0
            s += _score(key, words, exact=[r['metric'].lower()], text=r['metric'].lower(), desc='') if key else 0
            if s:
                bd.append((s, r))
        th, bd = _best(th, limit), _best(bd, limit)
        return {'thresholds': [_compact(r, ('metric', 'object', 'operator', 'value', 'value_high', 'unit', 'condition', 'meaning', 'source', 'kb')) for r in th],
                'bands': [_compact(r, ('metric', 'grp', 'green', 'yellow', 'orange', 'red', 'kb')) for r in bd]}

    def object_info(self, type_):
        t = norm_object(type_)
        rows = self._q('SELECT * FROM objects WHERE type = ?', (t,))
        if not rows:
            return {'error': f'unknown object {type_}', 'objects': [r['type'] for r in self._q('SELECT type FROM objects')]}
        rels = self._q('SELECT * FROM relations WHERE src = ? OR dst = ?', (t, t))
        return {**_compact(rows[0], ('type', 'role', 'layer', 'supplies', 'charts', 'note', 'kb')),
                'relations': [f"{r['src']} {r['kind']} {r['dst']} ({r['cardinality']})" for r in rels]}

    def path(self, src, dst):
        """Shortest relation path between two object types, edges usable in both directions."""
        a, b = norm_object(src), norm_object(dst)
        edges = self._q('SELECT * FROM relations')
        nbr = {}
        for e in edges:
            nbr.setdefault(e['src'], []).append((e['dst'], f"{e['src']} {e['kind']} {e['dst']} ({e['cardinality']})"))
            nbr.setdefault(e['dst'], []).append((e['src'], f"{e['src']} {e['kind']} {e['dst']} ({e['cardinality']})"))
        seen, dq = {a: []}, deque([a])
        while dq:
            n = dq.popleft()
            if n == b:
                return {'from': a, 'to': b, 'path': seen[n]}
            for m, label in nbr.get(n, []):
                if m not in seen:
                    seen[m] = seen[n] + [label]
                    dq.append(m)
        return {'from': a, 'to': b, 'path': None, 'error': 'no path'}

    def formulas(self):
        return self._q('SELECT * FROM formulas')

    def facts_for(self, ids, max_rows=14):
        """Compact catalog facts for knowledge files already in the context (classic mode)."""
        if not ids:
            return ''
        marks = ','.join('?' * len(ids))
        rows = self._q(f'SELECT * FROM counters WHERE kb IN ({marks})', tuple(ids))
        seen, lines = set(), []
        for r in rows:
            k = (r['counter'], r['object'], r['unit'], r['rollup'], r['level'])
            if k in seen:
                continue
            seen.add(k)
            mm = f", min/max at level {r['minmax_level']}" if r['minmax_level'] else ''
            lines.append(f"- {r['object']} {r['counter']} ({r['label']}): {r['unit']}, {r['stat_type']}, {r['rollup']}, "
                         f"statistics level {r['level']}{mm}. [{r['kb']}]")
        for r in self._q(f'SELECT * FROM thresholds WHERE kb IN ({marks})', tuple(ids)):
            hi = f"-{r['value_high']:g}" if r['value_high'] is not None else ''
            cond = f" with {r['condition']}" if r['condition'] else ''
            lines.append(f"- Threshold: {r['metric']} {r['operator']} {r['value']:g}{hi} {r['unit'] or ''}{cond}: {r['meaning']} "
                         f"(source: {r['source']}) [{r['kb']}]")
        if not lines:
            return ''
        return 'Catalog facts (exact):\n' + '\n'.join(lines[:max_rows])

    def stats(self):
        return {t: self._q(f'SELECT COUNT(*) AS n FROM {t}')[0]['n']
                for t in ('counters', 'api_counters', 'esxtop', 'thresholds', 'bands', 'metrics', 'objects', 'relations')}


def _esx_key(s):
    """esxtop field key: upper case, no % sign, no unit suffix. %RDY -> RDY, DAVG/cmd -> DAVG/CMD."""
    s = (s or '').strip().upper()
    s = re.sub(r'\s*\((MB|MB/S|%)\)$', '', s)
    return s.lstrip('%')


def _score(key, words, exact, text, desc):
    if not key:
        return 0
    if key in exact:
        return 100
    if words and all(w in text for w in words):
        return 60 + (10 if text.startswith(words[0]) else 0)
    if len(words) >= 3 and sum(w in text for w in words) >= len(words) - 1:
        return 40
    if desc and words and all(w in desc for w in words):
        return 20
    return 0


def _best(scored, limit, keep=0.6):
    """Best rows first; drop rows far below the best score so weak matches do not crowd the answer."""
    scored = sorted(scored, key=lambda x: -x[0])
    if not scored:
        return []
    top = scored[0][0]
    return [r for s, r in scored if s >= top * keep][:limit]


def _compact(r, keys):
    return {k: r[k] for k in keys if r.get(k) not in (None, '')}


_CACHE = {}


def get(docs):
    """One catalog per knowledge-base load (shared by threads)."""
    k = id(docs)
    if k not in _CACHE:
        _CACHE[k] = Catalog(docs)
    return _CACHE[k]


if __name__ == '__main__':
    import sys
    import kb as K
    docs, _ = K.load()
    cat = Catalog(docs)
    print(json.dumps(cat.stats()))
    if len(sys.argv) > 1:
        print(json.dumps(cat.lookup(' '.join(sys.argv[1:])), indent=1, ensure_ascii=False))
