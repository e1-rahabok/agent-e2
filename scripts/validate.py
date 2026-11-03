#!/usr/bin/env python3
"""Validate knowledge-base files. Run before every merge: python3 scripts/validate.py
Exit code 0 = pass, 1 = problems found. Allowed values come from
knowledge/glossary/terminology.md (section 'Allowed tag values')."""
import glob, os, re, sys, yaml

TERMS = 'knowledge/glossary/terminology.md'
REQUIRED = ['id', 'retriever_guide', 'scope', 'technology', 'pillar', 'product',
            'source', 'corrections', 'review_notes', 'status']
LIST_FIELDS = ['technology', 'pillar', 'product', 'object', 'instance']
LINK_FIELDS = ['related', 'internal_derive', 'same_name', 'same_meaning']
OLD_FIELDS = ['type', 'resources', 'objects', 'derived_from', 'same_name_as', 'kind']

def load_allowed():
    text = open(TERMS).read()
    m = re.search(r'## Allowed tag values.*?```yaml\n(.*?)```', text, re.S)
    if not m:
        sys.exit(f'{TERMS}: section "Allowed tag values" with a yaml block not found')
    return yaml.safe_load(m.group(1))

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
    EXEMPT_WORDS = {'knowledge/glossary/terminology.md'}  # defines the avoided words
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
        for r in re.findall(r'`((?:vsphere|foundations)/[a-z0-9\-/]+)`', body):
            if r not in ids: bad(f, f'inline link "{r}" does not exist')
        if '/metrics/' in f:
            if fm.get('retriever_guide') != 'metric-meaning': bad(f, 'metric file must have retriever_guide: metric-meaning')
            if not fm.get('object'): bad(f, 'metric file must have object')
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

    for f in sorted(glob.glob('evaluation/cases/**/*.md', recursive=True)):
        t = open(f).read()  # evaluation cases keep front matter at the top
        fm = yaml.safe_load(t.split('---\n', 2)[1]) if t.startswith('---\n') else {}
        for r in (fm or {}).get('knowledge') or []:
            if r not in ids: bad(f, f'knowledge link "{r}" does not exist')

    # every image file must be linked from a knowledge file, so the AI gets its context
    for img in glob.glob('knowledge/**/images/*.png', recursive=True):
        if os.path.normpath(img) not in linked_images:
            bad(img, 'image not linked from any knowledge file')

    for p in problems: print(p)
    print(f'{len(docs)} knowledge files checked, {len(problems)} problems')
    return 1 if problems else 0

if __name__ == '__main__':
    sys.exit(main())
