"""Load the knowledge base the way ARCHITECTURE.md, section Local LLM use, describes.

- Index knowledge/**/*.md.
- Split each file at '## Metadata'; the yaml block becomes filter fields, never text.
- Chunk the body by '## ' heading; prefix each chunk with title and id.
- Leave out Mermaid charts: they repeat the numbered steps for GitHub.
- Keep only the id of a file link: [`id`](path.md) becomes `id`. The path is for reviewers on GitHub.
"""
import glob
import os
import re

import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
META = '\n## Metadata\n```yaml\n'


def split(path):
    """Metadata is the last section of the file: '## Metadata' and one yaml block.
    Returns (meta, body); meta is None when the block is missing. project/tools/lint.py uses this parser too."""
    s = open(path).read()
    m = list(re.finditer(r'\n## Metadata[ \t]*\n\s*```yaml[ \t]*\n', s))  # tolerant of blank lines a Markdown formatter adds
    if not m or not s.rstrip().endswith('```'):
        return None, s
    i = m[-1].start()
    head = s[m[-1].end():].rstrip().removesuffix('```')
    return yaml.safe_load(head) or {}, s[:i]

# A Mermaid chart repeats the numbered steps for GitHub; the model reads the steps (project/knowledge-rules/flows.md).
MERMAID = re.compile(r'\n```mermaid\n.*?\n```[ \t]*(?=\n)', re.S)

# A file link [`id`](relative/path.md) is clickable on GitHub; the model reads only the id.
FILE_LINK = re.compile(r'\[(`[^`\n]+`)\]\([^)\s]+\.md\)')

LINK_TYPES = ['related', 'internal_derive', 'same_name', 'same_meaning']
FILTER_FIELDS = ['product', 'object', 'technology', 'pillar', 'retriever_guide']


class Doc:
    def __init__(self, path, meta, body):
        self.path = path
        self.id = meta.get('id') or os.path.relpath(path, os.path.join(ROOT, 'knowledge'))[:-3]
        self.meta = meta
        lines = body.strip().split('\n')
        self.title = lines[0].lstrip('# ').strip() if lines else self.id
        self.body = FILE_LINK.sub(r'\1', MERMAID.sub('', body)).strip()
        self.status = meta.get('status', 'draft')
        self.links = {t: list(meta.get(t) or []) for t in LINK_TYPES}
        self.images = list(meta.get('images') or [])
        self.sections = self._sections()

    def _sections(self):
        parts = re.split(r'\n(?=## )', self.body)
        out = []
        for p in parts:
            p = p.strip()
            if not p:
                continue
            head = p.split('\n', 1)[0].lstrip('# ').strip() if p.startswith('## ') else 'Intro'
            out.append((head, p))
        return out

    def tags(self, field):
        v = self.meta.get(field)
        if v is None:
            return []
        return v if isinstance(v, list) else [v]


class Chunk:
    def __init__(self, doc, heading, text):
        self.doc = doc
        self.heading = heading
        self.text = f'{doc.title} ({doc.id}) > {heading}\n{text}'


# Knowledge given up front, not through search: indexing the one-line summaries would let search return them
# in place of the files that hold the mechanism (KNOWLEDGE-ENGINEERING.md, section 2).
NOT_INDEXED = ('knowledge/misconceptions.md',)


def load(root=ROOT):
    docs = {}
    for f in sorted(glob.glob(os.path.join(root, 'knowledge', '**', '*.md'), recursive=True)):
        if os.path.relpath(f, root) in NOT_INDEXED:
            continue
        meta, body = split(f)
        if meta is None:
            continue
        d = Doc(f, meta, body)
        docs[d.id] = d
    chunks = [Chunk(d, h, t) for d in docs.values() for h, t in d.sections]
    return docs, chunks


GLOSSARY_FIELDS = ('Also called', 'Not to confuse with', 'File')
GLOSSARY_ENTRY = re.compile(r'^- \*\*(.+?)\*\*: (.*)$')


def glossary(docs):
    """Entries of knowledge/glossary.md: one dict per entry (term, meaning, also, confusable, file, area).

    An entry is '- **Term**: meaning' with optional sub-bullets '  - Also called: a, b',
    '  - Not to confuse with Other term: difference.' and '  - File: `id`', under '### Area' headings
    (project/knowledge-rules/terminology.md).
    """
    g = docs.get('glossary')
    out = []
    if not g:
        return out
    area = ''
    for line in g.body.split('\n'):
        if line.startswith('### '):
            area = line[4:].strip()
            continue
        if area:
            m = GLOSSARY_ENTRY.match(line)
            if m:
                out.append({'term': m.group(1), 'meaning': m.group(2), 'area': area, 'also': [], 'confusable': None, 'file': ''})
                continue
            if not out or out[-1]['area'] != area or not line.startswith('  - '):
                continue
            field, _, value = line[4:].partition(': ')
            if field == 'Also called':
                out[-1]['also'] = [a.strip() for a in value.split(',') if a.strip()]
            elif field.startswith('Not to confuse with '):
                out[-1]['confusable'] = (field[len('Not to confuse with '):].strip(), value.strip().rstrip('.'))
            elif field == 'File':
                out[-1]['file'] = value.strip().strip('`')
    return out


def git_sha(root=ROOT):
    try:
        import subprocess
        return subprocess.check_output(['git', '-C', root, 'rev-parse', 'HEAD'], text=True).strip()
    except Exception:
        return 'unknown'
