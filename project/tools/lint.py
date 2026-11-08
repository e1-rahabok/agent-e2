#!/usr/bin/env python3
"""Lint knowledge-base files and benchmark questions. Run before every merge: python3 project/tools/lint.py
Exit code 0 = pass, 1 = problems found. Allowed values come from
project/tools/tags.yaml."""
import glob, os, re, sys, yaml

HARNESS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'harness')
sys.path.insert(0, HARNESS)
from kb import split, MOVED  # noqa: E402  (the parser the harness uses, so lint and retrieval read files the same way)

TERMS = 'project/tools/tags.yaml'
REQUIRED = ['id', 'retriever_guide', 'scope', 'technology', 'pillar', 'product',
            'source', 'corrections', 'review_notes', 'status']
LIST_FIELDS = ['technology', 'pillar', 'product', 'object', 'instance', 'layer']
LINK_FIELDS = ['related', 'internal_derive', 'same_name', 'same_meaning']
OLD_FIELDS = ['type', 'resources', 'objects', 'derived_from', 'same_name_as', 'kind']

def load_allowed():
    return yaml.safe_load(open(TERMS))

def main():
    allowed = load_allowed()
    problems = []
    def bad(path, msg): problems.append(f'{path}: {msg}')
    linked_images = set()

    files = [f for f in sorted(glob.glob('knowledge/**/*.md', recursive=True))]
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
        # vSphere folders: foundations/, technology/<tech>/, object-types/<object>/, tools/<ui>/ (esxtop, vsphere-client; screens/ inside).
        if f.startswith('knowledge/vsphere/'):
            parts = f.split('/')
            if parts[2] not in VSPHERE_TOP:
                bad(f, f'knowledge/vsphere/ holds only {", ".join(VSPHERE_TOP)}/')
            elif parts[2] == 'technology' and parts[3] not in allowed['technology']:
                bad(f, f'technology folder "{parts[3]}" is not a technology tag value')
            elif parts[2] == 'object-types' and parts[3] not in OBJECT_FOLDERS:
                bad(f, f'object-types folder "{parts[3]}" not allowed. Allowed: {", ".join(OBJECT_FOLDERS)}')
            elif parts[2] == 'tools' and parts[3] not in allowed['ui']:
                bad(f, f'tools folder "{parts[3]}" is not a ui tag value ({", ".join(allowed["ui"])})')
        if f.startswith('knowledge/operations-management/'):
            if fm.get('scope') != 'operations-management': bad(f, 'file in knowledge/operations-management/ must have scope: operations-management')
            if f.split('/')[2] not in PILLAR_FOLDERS: bad(f, f'pillar folder not allowed. Allowed: {", ".join(PILLAR_FOLDERS)}')
        if '/screens/' in f:
            if fm.get('ui') not in allowed['ui']: bad(f, f'screen file needs ui: {", ".join(allowed["ui"])}')
            if not fm.get('ui_version'): bad(f, 'screen file needs ui_version')
            for r in fm.get('metrics_shown') or []:
                if r not in ids: bad(f, f'metrics_shown link "{r}" does not exist')
        if f.startswith('knowledge/vcf-operations/'):
            if fm.get('scope') != 'vcf-operations': bad(f, 'file in knowledge/vcf-operations/ must have scope: vcf-operations')
            if f.split('/')[2] not in VCF_OPERATIONS_TOP: bad(f, f'knowledge/vcf-operations/ holds only {", ".join(VCF_OPERATIONS_TOP)}/')
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

    seen_ids, level_numbers = {}, {}
    for f in sorted(glob.glob('benchmark/questions/**/*.md', recursive=True)):
        t = open(f).read()  # benchmark questions: metadata at the end, like knowledge files
        if t.startswith('---\n'): bad(f, 'front matter at the top: move it to a ## Metadata section at the end')
        fm, _ = split(f)
        if fm is None: bad(f, 'missing ## Metadata section with one yaml block at the end'); fm = {}
        for r in (fm or {}).get('knowledge') or []:
            if r in MOVED: bad(f, f'knowledge link "{r}" moved: use "{MOVED[r]}" (knowledge/moved.yaml)')
            elif r not in ids: bad(f, f'knowledge link "{r}" does not exist')
        for k in ('product', 'technology'):
            v = (fm or {}).get(k)
            if not isinstance(v, list) or not v: bad(f, f'{k} must be a non-empty list')
            else:
                for x in v:
                    if x not in allowed[k]: bad(f, f'{k} "{x}" not allowed')
        if os.path.dirname(f) != 'benchmark/questions': bad(f, 'questions live in one flat folder: benchmark/questions/')
        qid = str((fm or {}).get('id') or '')
        if not re.fullmatch(r'\d{4}', qid): bad(f, 'id must be a stable 4-digit number, quoted, e.g. "0007" (benchmark/README.md)')
        elif qid in seen_ids: bad(f, f'id {qid} is also used by {seen_ids[qid]}')
        else: seen_ids[qid] = f
        lv = (fm or {}).get('level')
        mm = re.match(r'L(\d)-(\d{2,3})-', os.path.basename(f))
        if not mm or not isinstance(lv, int) or int(mm.group(1)) != lv // 100:
            bad(f, f'file name must start with L{(lv or 0) // 100}-<nn>- (benchmark/README.md); run project/tools/renumber_questions.py')
        else: level_numbers.setdefault(lv, []).append(int(mm.group(2)))
        for a in (fm or {}).get('attachments') or []:
            if not str(a).startswith(f'{qid}/'): bad(f, f'attachment {a} must live in the folder {qid}/')
        for k in ('scope', 'area', 'tests', 'pillar', 'format', 'input_type'):
            if k in (fm or {}): bad(f, f'tag "{k}" is no longer used (benchmark/README.md, section Tags removed)')
        if (fm or {}).get('task') not in ('read-metric', 'troubleshoot', 'decide-capacity', 'explain-mechanism', 'judge-setting'):
            bad(f, 'task must be read-metric, troubleshoot, decide-capacity, explain-mechanism or judge-setting (benchmark/design.md, section 3.1)')
        if (fm or {}).get('origin') not in ('book', 'quiz', 'real-ticket', 'synthetic'):
            bad(f, 'origin must be book, quiz, real-ticket or synthetic')
        if (fm or {}).get('status') not in ('draft', 'awaiting-input', 'reviewed', 'retired'):
            bad(f, 'status must be draft, awaiting-input, reviewed or retired')
        if (fm or {}).get('status') == 'awaiting-input' and '\n## Input to supply\n' not in t:
            bad(f, 'awaiting-input question needs a ## Input to supply section describing the screenshot or table')
        if not (fm or {}).get('knowledge'):
            bad(f, 'knowledge must list at least one knowledge id')
        at = (fm or {}).get('answer_type')
        if at not in ('deterministic', 'judged'):
            bad(f, f'answer_type "{at}" must be deterministic or judged (benchmark/design.md, section 3.3)')
        if (fm or {}).get('level') not in (100, 200, 300, 400):
            bad(f, 'level must be 100, 200, 300 or 400 (benchmark/design.md, section 3.2)')
        atts = (fm or {}).get('attachments') or []
        derived = ([ 'table'] if any(a.lower().endswith(('.csv', '.xlsx', '.xls')) for a in atts) else []) + \
                  (['screenshot'] if any(a.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')) for a in atts) else [])
        if sorted((fm or {}).get('input') or []) != sorted(derived or ['text']):
            bad(f, f'input must be {derived or ["text"]}, from the attachments (benchmark/design.md, section 3.4)')
        if at == 'deterministic':
            prompt = re.search(r'## Prompt\n(.*?)\n## ', t, re.S)
            letters = set(re.findall(r'^(?:[-*]\s+)?([A-H])\.\s', prompt.group(1), re.M)) if prompt else set()
            for k in ('answer', 'trap'):
                for x in fm.get(k) or []:
                    if str(x) not in letters: bad(f, f'{k} letter {x} is not an option in ## Prompt')
            if not fm.get('answer'): bad(f, 'deterministic question has no answer')
        for att in (fm or {}).get('attachments') or []:
            if not os.path.exists(os.path.join('benchmark', 'questions', att)) and (fm or {}).get('status') != 'awaiting-input':
                bad(f, f'attachment not found: {att}')

    for lv, ns in level_numbers.items():
        if sorted(ns) != list(range(1, len(ns) + 1)):
            bad('benchmark/questions', f'level {lv} file numbers must run 01..{len(ns):02d} without gaps; run project/tools/renumber_questions.py')
    sys.path.insert(0, 'project/tools')
    from link_refs import DOCS as LINKED_DOCS
    for d in LINKED_DOCS:
        for ref in re.findall(r'benchmark/questions/(L\d-\d+-[\w-]+\.md)', open(d).read()):
            if not os.path.exists(os.path.join('benchmark', 'questions', ref)): bad(d, f'link to a question that does not exist: {ref}')
    for f in files + sorted(glob.glob('benchmark/questions/*.md')):
        text = open(f).read()
        for pat in allowed.get('injection_patterns', []):
            if re.search(pat, text): bad(f, f'possible prompt injection or hidden text (pattern {pat})')
    import subprocess  # author-facing documents: file references must be clickable links
    r = subprocess.run([sys.executable, 'project/tools/link_refs.py', '--check'], capture_output=True, text=True)
    for line in r.stdout.splitlines(): bad(line.split(':')[0], line.split(': ', 1)[1])
    import kb as _kb, primer  # agent up-front blocks: sources present, size within budget (harness/AGENT.md, section 3)
    pdocs, _ = _kb.load()
    for b in primer.BLOCKS:
        if not primer.build(pdocs, {b: True}): bad('harness/primer.py', f'up-front block "{b}" is empty: its source section is missing')
    n = primer.tokens(primer.build(pdocs, {b: True for b in primer.BLOCKS}))
    if n > primer.BUDGET_TOKENS: bad('harness/primer.py', f'up-front blocks are {n} tokens, above the budget of {primer.BUDGET_TOKENS}')
    check_tables(bad)
    check_titles(bad)
    check_moved(ids, bad)
    check_repo_terms(allowed, bad)
    check_catalog(allowed, ids, {fm.get('id'): body for fm, body in docs.values()}, bad)
    check_flows({fm.get('id'): (fm, body) for fm, body in docs.values()}, bad)

    # every image file must be linked from a knowledge file, so the AI gets its context
    for img in glob.glob('knowledge/**/images/*.png', recursive=True):
        if os.path.normpath(img) not in linked_images:
            bad(img, 'image not linked from any knowledge file')

    for p in problems: print(p)
    print(f'{len(docs)} knowledge files checked, {len(problems)} problems')
    return 1 if problems else 0

def check_repo_terms(allowed, bad):
    """One word per concept in the repository (project/terms.md): flag the replaced words."""
    skip = ('project/terms.md', 'project/author-questions.md', 'project/tools/tags.yaml')
    records = ('project/archive/', 'project/review-', 'benchmark/results/')
    for f in sorted(glob.glob('**/*.md', recursive=True)):
        if f in skip or f.startswith(records):
            continue
        for i, line in enumerate(open(f).read().split('\n'), 1):
            for pat, use in (allowed.get('avoid_repo_terms') or {}).items():
                if re.search(pat, line):
                    bad(f, f'line {i}: repository term "{re.search(pat, line).group(0)}": use "{use}" (project/terms.md)')
            for pat, use in (allowed.get('avoid_ai_speak') or {}).items():
                if re.search(pat, line):
                    bad(f, f'line {i}: AI-speak "{re.search(pat, line).group(0)}": {use} (KNOWLEDGE-ENGINEERING.md, section 11)')


def check_moved(ids, bad):
    """knowledge/moved.yaml points to files that exist; active files use current ids, not moved ones."""
    for old, new in MOVED.items():
        if new not in ids: bad('knowledge/moved.yaml', f'"{old}" points to "{new}", which does not exist')
        if old in ids: bad('knowledge/moved.yaml', f'"{old}" is moved but a file with that id exists')
    if not MOVED:
        return
    old_ids = '|'.join(re.escape(o) for o in sorted(MOVED, key=len, reverse=True))
    pat = re.compile(r'(?:`(' + old_ids + r')`|blob/main/knowledge/(' + old_ids + r')\.md)')
    records = ('project/archive/', 'project/review-', 'benchmark/results/')
    for f in sorted(glob.glob('**/*.md', recursive=True)):
        if f.startswith(records):
            continue
        for i, line in enumerate(open(f).read().split('\n'), 1):
            for m in pat.finditer(line):
                o = m.group(1) or m.group(2)
                bad(f, f'line {i}: moved id "{o}": use "{MOVED[o]}" (run project/tools/link_refs.py for links)')


def check_titles(bad):
    """Short titles and headings: the title is prefixed to every chunk (harness/kb.py), so a list of contents in it repeats in every chunk."""
    for f in sorted(glob.glob('knowledge/**/*.md', recursive=True)):
        for i, line in enumerate(open(f).read().split('\n'), 1):
            m = re.match(r'(#{1,3}) (.*)', line)
            if not m:
                continue
            words, limit = len([w for w in re.sub(r'\([^)]*\)', '', m.group(2)).split() if w != '|']), (8 if m.group(1) == '#' else 9)
            if words > limit:
                bad(f, f'line {i}: heading of {words} words; at most {limit}: name the topic, put details in the body')
            if m.group(1) == '#' and ': ' in m.group(2) and m.group(2).split(': ', 1)[1].count(',') >= 2:
                bad(f, f'line {i}: title lists its contents after a colon; name the topic only')


def check_tables(bad):
    """Tables need a blank line before (else they render as text) and after (else the next line becomes a table row)."""
    for f in sorted(glob.glob('**/*.md', recursive=True)):
        if f.startswith('benchmark/results/') or f.startswith('project/archive/'):
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


VSPHERE_TOP = ['foundations', 'technology', 'object-types', 'tools']
VCF_OPERATIONS_TOP = ['concepts', 'kpis', 'metrics', 'diagnosis', 'ui']
OBJECT_FOLDERS = ['vm', 'esxi', 'cluster', 'resource-pool', 'datastore', 'datastore-cluster', 'datacenter', 'vcenter', 'distributed-switch']
PILLAR_FOLDERS = ['performance', 'capacity']
CATALOG = 'knowledge/catalog'
THRESHOLD_SOURCES = ['book', 'author', 'vsphere-9.1-docs', 'performance-best-practices-9.1', 'microsoft']
OPERATORS = ['>', '>=', '<', '<=', '=', 'range']


def check_catalog(allowed, ids, bodies, bad, docs=None):
    """knowledge/catalog/*.yaml: valid tags, existing knowledge ids, thresholds still quoted in their files, band tables matched."""
    objects = set(allowed['object'])
    seen_thresholds, yaml_bands = set(), set()
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
        elif name in ('thresholds-performance.yaml', 'thresholds-capacity.yaml'):
            for n, r in enumerate(rows):
                w = f'row {n + 1} ({r.get("id")})'
                if r.get('id') in seen_thresholds: bad(path, f'{w}: duplicate id (ids are unique across both threshold files)')
                seen_thresholds.add(r.get('id'))
                if r.get('kind') == 'bands':
                    for k in ('id', 'metric', 'bands', 'source', 'kb'):
                        if r.get(k) in (None, ''): bad(path, f'{w}: {k} missing')
                    bd = r.get('bands') or {}
                    if any(bd.get(k) in (None, '') for k in ('green', 'yellow', 'orange', 'red')): bad(path, f'{w}: bands need green, yellow, orange, red')
                    if bd.get('grey') and name == 'thresholds-performance.yaml': bad(path, f'{w}: grey (wastage) is a capacity band only')
                    if r.get('interval') and r['interval'] not in ('2s', '20s', '5m', '1d'): bad(path, f'{w}: interval must be 2s, 20s, 5m or 1d')
                    if r.get('source') not in THRESHOLD_SOURCES: bad(path, f'{w}: source "{r.get("source")}" not allowed')
                    kb_ok(path, w, r.get('kb'))
                    yaml_bands.add((r.get('kb'), r.get('metric'), r.get('group') or '', bd.get('green'), bd.get('yellow'), bd.get('orange'), bd.get('red')))
                    continue
                if r.get('kind') != 'rule': bad(path, f'{w}: kind must be rule or bands')
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
            bad(path, 'unknown catalog file: add its checks to project/tools/lint.py')

    # Band tables in knowledge files and band rows in the threshold files must match, both ways.
    import kb as _kb, catalog as _cat
    table = {(b['kb'], b['metric'], b['group'], b['green'], b['yellow'], b['orange'], b['red']) for b in _cat.bands_from_docs(_kb.load()[0])}
    for t in sorted(table - yaml_bands):
        bad(f'knowledge/{t[0]}.md', f'band row "{t[1]}" has no matching row in a threshold file (knowledge/catalog/thresholds-*.yaml)')
    for t in sorted(yaml_bands - table):
        bad('knowledge/catalog', f'band row "{t[1]}" ({t[0]}) does not match the table in its kb file')


def check_flows(docs, bad):
    """Diagnosis files must parse into steps for the flow tool (harness/flows.py); step references must exist."""
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
