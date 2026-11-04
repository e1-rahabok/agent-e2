#!/usr/bin/env python3
"""Lint knowledge-base files and benchmark cases. Run before every merge: python3 tools/lint.py
Exit code 0 = pass, 1 = problems found. Allowed values come from
tools/tags.yaml."""
import glob, os, re, sys, yaml

TERMS = 'tools/tags.yaml'
REQUIRED = ['id', 'retriever_guide', 'scope', 'technology', 'pillar', 'product',
            'source', 'corrections', 'review_notes', 'status']
LIST_FIELDS = ['technology', 'pillar', 'product', 'object', 'instance', 'layer']
LINK_FIELDS = ['related', 'internal_derive', 'same_name', 'same_meaning']
OLD_FIELDS = ['type', 'resources', 'objects', 'derived_from', 'same_name_as', 'kind']

def load_allowed():
    return yaml.safe_load(open(TERMS))

META = '\n## Metadata\n```yaml\n'

def split(path):
    """Metadata is the last section of the file: '## Metadata' and one yaml block."""
    s = open(path).read()
    i = s.rfind(META)
    if i < 0 or not s.rstrip().endswith('```'):
        return None, s
    head = s[i + len(META):].rstrip().removesuffix('```')
    return yaml.safe_load(head) or {}, s[:i]

def main():
    allowed = load_allowed()
    problems = []
    def bad(path, msg): problems.append(f'{path}: {msg}')
    linked_images = set()

    files = [f for f in sorted(glob.glob('knowledge/**/*.md', recursive=True))
             if '/_templates/' not in f and '/raw-input/' not in f]
    docs = {}
    for f in files:
        fm, body = split(f)
        if fm is None:
            bad(f, 'no metadata block at the end (## Metadata + yaml)'); continue
        docs[f] = (fm, body)

    ids = {fm.get('id') for fm, _ in docs.values()}
    EXEMPT_WORDS = {'knowledge/glossary.md'}  # defines the avoided words
    for f, (fm, body) in docs.items():
        expected = f[len('knowledge/'):-3]
        if fm.get('id') != expected:
            bad(f, f'id "{fm.get("id")}" does not match path "{expected}"')
        for k in REQUIRED:
            if k not in fm: bad(f, f'missing field "{k}"')
        for k in OLD_FIELDS:
            if k in fm: bad(f, f'old field "{k}" is no longer used')
        for k in ['retriever_guide', 'scope', 'metric_class', 'status']:
            v = fm.get(k)
            if v is not None and v not in allowed[k]:
                bad(f, f'{k} "{v}" not allowed. Allowed: {", ".join(allowed[k])}')
        for k in LIST_FIELDS:
            v = fm.get(k)
            if v is None: continue
            if not isinstance(v, list): bad(f, f'{k} must be a list'); continue
            for x in v:
                if x not in allowed[k]:
                    hint = ' (vCPU is an instance: use instance: per-vcpu)' if k == 'object' and str(x).lower() == 'vcpu' else ''
                    bad(f, f'{k} "{x}" not allowed{hint}. Allowed: {", ".join(allowed[k])}')
        for k in LINK_FIELDS:
            for r in fm.get(k) or []:
                if r not in ids: bad(f, f'{k} link "{r}" does not exist')
        # every image link needs an entry in metadata 'images' with valid tags
        entries = {e.get('path'): e for e in (fm.get('images') or []) if isinstance(e, dict)}
        body_imgs = set(re.findall(r'!\[[^\]]*\]\(([^)]+)\)', body))
        for p in body_imgs - set(entries): bad(f, f'image {p} has no entry in metadata images')
        for p in set(entries) - body_imgs: bad(f, f'metadata images entry {p} is not linked in the body')
        for p, e in entries.items():
            for k in ('product', 'object', 'image_type'):
                vals = e.get(k)
                if not vals: bad(f, f'images entry {p}: {k} missing'); continue
                for x in (vals if isinstance(vals, list) else [vals]):
                    if x not in allowed[k]: bad(f, f'images entry {p}: {k} "{x}" not allowed')
            if not e.get('metric') and not e.get('topic'):
                bad(f, f'images entry {p}: needs metric or topic')
        for img in re.findall(r'!\[[^\]]*\]\(([^)]+)\)', body):
            full = os.path.normpath(os.path.join(os.path.dirname(f), img))
            linked_images.add(full)
            if not os.path.exists(full):
                bad(f, f'image not found: {img}')
        for r in re.findall(r'`((?:vsphere|foundations|guest-os|operations-management|vcf-operations)/[a-z0-9\-/]+)`', body):
            if r not in ids: bad(f, f'inline link "{r}" does not exist')
        # vSphere folders: foundations/, technology/<tech>/, object-types/<object>/, screens/<ui>/.
        if f.startswith('knowledge/vsphere/'):
            parts = f.split('/')
            if parts[2] not in VSPHERE_TOP:
                bad(f, f'knowledge/vsphere/ holds only {", ".join(VSPHERE_TOP)}/')
            elif parts[2] == 'technology' and parts[3] not in allowed['technology']:
                bad(f, f'technology folder "{parts[3]}" is not a technology tag value')
            elif parts[2] == 'object-types' and parts[3] not in OBJECT_FOLDERS:
                bad(f, f'object-types folder "{parts[3]}" not allowed. Allowed: {", ".join(OBJECT_FOLDERS)}')
        if f.startswith('knowledge/operations-management/'):
            if fm.get('scope') != 'operations-management': bad(f, 'file in knowledge/operations-management/ must have scope: operations-management')
            if f.split('/')[2] not in PILLAR_FOLDERS: bad(f, f'pillar folder not allowed. Allowed: {", ".join(PILLAR_FOLDERS)}')
        if '/screens/' in f:
            if fm.get('ui') not in allowed['ui']: bad(f, f'screen file needs ui: {", ".join(allowed["ui"])}')
            if not fm.get('ui_version'): bad(f, 'screen file needs ui_version')
            for r in fm.get('metrics_shown') or []:
                if r not in ids: bad(f, f'metrics_shown link "{r}" does not exist')
        if f.startswith('knowledge/vcf-operations/') and fm.get('scope') != 'vcf-operations':
            bad(f, 'file in knowledge/vcf-operations/ must have scope: vcf-operations')
        # A VM is a virtual motherboard. The Guest OS (Windows, Linux) is not a Broadcom product and not part of the VM:
        # its knowledge lives in knowledge/guest-os/, outside knowledge/vsphere/.
        layer = fm.get('layer') or []
        title = body.lstrip().split('\n', 1)[0]
        if f.startswith('knowledge/guest-os/'):
            if fm.get('scope') != 'guest-os': bad(f, 'file in knowledge/guest-os/ must have scope: guest-os')
            if layer != ['guest-os']: bad(f, 'file in knowledge/guest-os/ must have layer: [guest-os]')
            if 'VirtualMachine' in (fm.get('object') or []): bad(f, 'Guest OS file must not have object VirtualMachine: the Guest OS is a layer, not the VM')
        else:
            # Boundary files (Guest OS vs VM, Guest OS sizing from VM data) stay in vSphere; Guest OS metrics never do.
            if 'guest-os' in layer or fm.get('scope') == 'guest-os' or ('/metrics/' in f and title.startswith(('# Guest OS ', '# Windows', '# Linux'))):
                bad(f, 'Guest OS knowledge must live in knowledge/guest-os/, not under vSphere')
        if '/metrics/' in f:
            if fm.get('retriever_guide') != 'metric-meaning': bad(f, 'metric file must have retriever_guide: metric-meaning')
            if f.startswith('knowledge/guest-os/'):
                pass  # Guest OS metrics have no vSphere object; rules below
            elif not fm.get('object'): bad(f, 'metric file must have object')
            if '/metrics/virtual-motherboard/' in f and (fm.get('layer') or []) != ['virtual-motherboard']:
                bad(f, 'VM metric file must have layer: [virtual-motherboard]')
            if not fm.get('metric_class'): bad(f, 'metric file must have metric_class')
            if '/comparisons/' not in f and len(fm.get('object') or []) > 1:
                bad(f, 'metric file must have exactly one object type (comparisons excepted)')
        if f in EXEMPT_WORDS: continue
        for pat in allowed.get('avoid_everywhere', []):
            if re.search(pat, body): bad(f, f'body contains audit marker matching {pat}')
        if 'cpu' in (fm.get('technology') or []):
            for line in body.splitlines():
                checked = line
                for ok in allowed.get('allow_in_cpu_files', []):
                    checked = re.sub(ok, '', checked)
                for pat in allowed.get('avoid_in_cpu_files', []):
                    if re.search(pat, checked, re.I):
                        bad(f, f'word to avoid ({pat}) in: {line.strip()[:100]}')

    for f in sorted(glob.glob('benchmark/cases/**/*.md', recursive=True)):
        t = open(f).read()  # benchmark cases: metadata at the end, like knowledge files
        if t.startswith('---\n'): bad(f, 'front matter at the top: move it to a ## Metadata section at the end')
        fm, _ = split(f)
        if fm is None: bad(f, 'missing ## Metadata section with one yaml block at the end'); fm = {}
        for r in (fm or {}).get('knowledge') or []:
            if r not in ids: bad(f, f'knowledge link "{r}" does not exist')
        for k in ('product', 'technology'):
            v = (fm or {}).get(k)
            if not isinstance(v, list) or not v: bad(f, f'{k} must be a non-empty list')
            else:
                for x in v:
                    if x not in allowed[k]: bad(f, f'{k} "{x}" not allowed')
        if os.path.dirname(f) != 'benchmark/cases': bad(f, 'cases live in one flat folder: benchmark/cases/')
        fmt = (fm or {}).get('format')
        if fmt not in ('multiple-choice', 'free-text', 'compound'):
            bad(f, f'format "{fmt}" must be multiple-choice, free-text or compound')
        if fmt == 'multiple-choice':
            prompt = re.search(r'## Prompt\n(.*?)\n## ', t, re.S)
            letters = set(re.findall(r'^([A-H])\.\s', prompt.group(1), re.M)) if prompt else set()
            for k in ('answer', 'trap'):
                for x in fm.get(k) or []:
                    if str(x) not in letters: bad(f, f'{k} letter {x} is not an option in ## Prompt')
            if not fm.get('answer'): bad(f, 'multiple-choice case has no answer')
            if fm.get('level') not in ('recall', 'l400', 'multi-hop', 'screenshot'):
                bad(f, 'level must be recall, l400, multi-hop or screenshot')
        for att in (fm or {}).get('attachments') or []:
            if not os.path.exists(os.path.join('benchmark', 'attachments', att)):
                bad(f, f'attachment not found: {att}')

    for f in files + sorted(glob.glob('benchmark/cases/*.md')):
        text = open(f).read()
        for pat in allowed.get('injection_patterns', []):
            if re.search(pat, text): bad(f, f'possible prompt injection or hidden text (pattern {pat})')
    check_tables(bad)
    check_catalog(allowed, ids, {fm.get('id'): body for fm, body in docs.values()}, bad)
    check_flows({fm.get('id'): (fm, body) for fm, body in docs.values()}, bad)

    # every image file must be linked from a knowledge file, so the AI gets its context
    for img in glob.glob('knowledge/**/images/*.png', recursive=True):
        if os.path.normpath(img) not in linked_images:
            bad(img, 'image not linked from any knowledge file')

    for p in problems: print(p)
    print(f'{len(docs)} knowledge files checked, {len(problems)} problems')
    return 1 if problems else 0

def check_tables(bad):
    """Tables need a blank line before (else they render as text) and after (else the next line becomes a table row)."""
    for f in sorted(glob.glob('**/*.md', recursive=True)):
        if '/raw-input/' in f or '/autotest/' in f or f.startswith('project/archive/'):
            continue
        lines, fence = open(f).read().split('\n'), False
        for i, line in enumerate(lines):
            if line.startswith('```'):
                fence = not fence
            if (not fence and i > 0 and line.startswith('|') and i + 1 < len(lines) and lines[i + 1].startswith('|---')
                    and lines[i - 1].strip() and not lines[i - 1].startswith(('|', '#'))):
                bad(f, f'line {i + 1}: table needs a blank line before it')
            if (not fence and line.startswith('|') and i + 1 < len(lines) and lines[i + 1].strip()
                    and not lines[i + 1].startswith('|')):
                bad(f, f'line {i + 2}: blank line needed after a table (an image or text right after it becomes a table row)')


VSPHERE_TOP = ['foundations', 'technology', 'object-types', 'screens']
OBJECT_FOLDERS = ['vm', 'esxi', 'cluster', 'resource-pool', 'datastore', 'datastore-cluster', 'datacenter', 'vcenter', 'distributed-switch']
PILLAR_FOLDERS = ['performance', 'capacity']
CATALOG = 'knowledge/catalog'
THRESHOLD_SOURCES = ['book', 'author', 'vsphere-9.1-docs', 'performance-best-practices-9.1', 'microsoft']
OPERATORS = ['>', '>=', '<', '<=', '=', 'range']


def check_catalog(allowed, ids, bodies, bad):
    """knowledge/catalog/*.yaml: valid tags, existing knowledge ids, thresholds still quoted in their files."""
    objects = set(allowed['object'])
    def kb_ok(path, where, ref):
        if ref and ref not in ids and not ref.startswith('catalog/'):
            bad(path, f'{where}: kb "{ref}" does not exist')
    for path in sorted(glob.glob(f'{CATALOG}/*.yaml')):
        try:
            data = yaml.safe_load(open(path))
        except yaml.YAMLError as e:
            bad(path, f'yaml error: {e}'); continue
        meta = data.get('meta') or {}
        for k in ('id', 'title', 'review_notes', 'status'):
            if k not in meta: bad(path, f'meta.{k} missing')
        if meta.get('status') not in allowed['status']: bad(path, f'meta.status "{meta.get("status")}" not allowed')
        if meta.get('id') != path[len('knowledge/'):-5]: bad(path, f'meta.id "{meta.get("id")}" does not match path')
        name = os.path.basename(path)
        rows = data.get('rows') or []
        if name == 'vcenter-counters.yaml':
            for n, r in enumerate(rows):
                w = f'row {n + 1} ({r.get("counter")})'
                for k in ('counter', 'object', 'chart', 'label', 'unit', 'stat_type', 'rollup', 'level', 'page'):
                    if r.get(k) in (None, ''): bad(path, f'{w}: {k} missing')
                if r.get('object') not in objects: bad(path, f'{w}: object "{r.get("object")}" not allowed')
                if r.get('level') not in (1, 2, 3, 4): bad(path, f'{w}: level must be 1-4')
                if r.get('minmax_level') not in (None, 4): bad(path, f'{w}: minmax_level must be 4')
                if r.get('stat_type') not in ('Rate', 'Absolute', 'Delta'): bad(path, f'{w}: stat_type "{r.get("stat_type")}"')
                if r.get('rollup') not in ('Average', 'Summation', 'Latest', 'Minimum', 'Maximum'): bad(path, f'{w}: rollup "{r.get("rollup")}"')
                kb_ok(path, w, r.get('kb'))
        elif name == 'vcenter-api-counters.yaml':
            for n, r in enumerate(rows):
                w = f'row {n + 1} ({r.get("counter")})'
                for k in ('counter', 'object', 'rollup', 'stat_type', 'unit', 'level'):
                    if r.get(k) in (None, ''): bad(path, f'{w}: {k} missing')
                if r.get('object') not in objects: bad(path, f'{w}: object "{r.get("object")}" not allowed')
                if r.get('stat_type') not in ('rate', 'absolute', 'delta'): bad(path, f'{w}: stat_type "{r.get("stat_type")}"')
                if r.get('level') not in (1, 2, 3, 4): bad(path, f'{w}: level must be 1-4')
                kb_ok(path, w, r.get('kb'))
        elif name == 'esxtop-fields.yaml':
            for n, r in enumerate(rows):
                for k in ('panel', 'field', 'description', 'page'):
                    if r.get(k) in (None, ''): bad(path, f'row {n + 1}: {k} missing')
        elif name == 'thresholds.yaml':
            seen = set()
            for n, r in enumerate(rows):
                w = f'row {n + 1} ({r.get("id")})'
                if r.get('id') in seen: bad(path, f'{w}: duplicate id')
                seen.add(r.get('id'))
                for k in ('id', 'metric', 'operator', 'value', 'meaning', 'source', 'kb', 'quote'):
                    if r.get(k) in (None, ''): bad(path, f'{w}: {k} missing')
                if r.get('interval') and r['interval'] not in ('2s', '20s', '5m', '1d'): bad(path, f'{w}: interval must be 2s, 20s, 5m or 1d')
                if r.get('operator') not in OPERATORS: bad(path, f'{w}: operator "{r.get("operator")}" not allowed')
                if r.get('operator') == 'range' and r.get('value_high') is None: bad(path, f'{w}: range needs value_high')
                if r.get('source') not in THRESHOLD_SOURCES: bad(path, f'{w}: source "{r.get("source")}" not allowed')
                if r.get('object') and r['object'] not in objects: bad(path, f'{w}: object "{r["object"]}" not allowed')
                if r.get('layer') and r['layer'] not in allowed['layer']: bad(path, f'{w}: layer "{r["layer"]}" not allowed')
                kb_ok(path, w, r.get('kb'))
                if r.get('kb') in bodies and r.get('quote') and r['quote'] not in bodies[r['kb']]:
                    bad(path, f'{w}: quote no longer in {r["kb"]}: update the row or the file')
        elif name == 'objects.yaml':
            types = set()
            for o in data.get('objects') or []:
                types.add(o.get('type'))
                if o.get('type') not in objects: bad(path, f'object "{o.get("type")}" not allowed')
                if o.get('layer') and o['layer'] not in allowed['layer']: bad(path, f'{o.get("type")}: layer "{o["layer"]}" not allowed')
                for ref in o.get('kb') or []: kb_ok(path, o.get('type'), ref)
            for r in data.get('relations') or []:
                for end in ('from', 'to'):
                    if r.get(end) not in types: bad(path, f'relation {r}: "{r.get(end)}" is not in objects')
            for l in data.get('layers') or []:
                if l.get('layer') not in allowed['layer']: bad(path, f'layer "{l.get("layer")}" not allowed')
        else:
            bad(path, 'unknown catalog file: add its checks to tools/lint.py')


def check_flows(docs, bad):
    """Diagnosis files must parse into steps for the flow tool (harness/flows.py); step references must exist."""
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'harness'))
    import flows

    class _Doc:
        def __init__(self, i, fm, body):
            self.id, self.meta, self.title = i, fm, body.lstrip().split('\n', 1)[0].lstrip('# ')
            parts = [p.strip() for p in re.split(r'\n(?=## )', body.strip()) if p.strip()]
            self.sections = [(p.split('\n', 1)[0].lstrip('# ').strip() if p.startswith('## ') else 'Intro', p) for p in parts]
    for i, msg in flows.check({i: _Doc(i, fm, body) for i, (fm, body) in docs.items()}):
        bad(f'knowledge/{i}.md', msg)


if __name__ == '__main__':
    sys.exit(main())
