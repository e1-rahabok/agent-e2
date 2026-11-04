"""Load the knowledge base the way README 'How a local LLM uses it' describes.

- Index knowledge/**/*.md except _templates and raw-input.
- Split each file at '## Metadata'; the yaml block becomes filter fields, never text.
- Chunk the body by '## ' heading; prefix each chunk with title and id.
"""
import glob
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from lint import split  # noqa: E402  (same parser as the linter)

LINK_TYPES = ['related', 'internal_derive', 'same_name', 'same_meaning']
FILTER_FIELDS = ['product', 'object', 'technology', 'pillar', 'retriever_guide']


class Doc:
    def __init__(self, path, meta, body):
        self.path = path
        self.id = meta.get('id') or os.path.relpath(path, os.path.join(ROOT, 'knowledge'))[:-3]
        self.meta = meta
        lines = body.strip().split('\n')
        self.title = lines[0].lstrip('# ').strip() if lines else self.id
        self.body = body.strip()
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


def load(root=ROOT):
    docs = {}
    for f in sorted(glob.glob(os.path.join(root, 'knowledge', '**', '*.md'), recursive=True)):
        if '/_templates/' in f or '/raw-input/' in f:
            continue
        meta, body = split(f)
        if meta is None:
            continue
        d = Doc(f, meta, body)
        docs[d.id] = d
    chunks = [Chunk(d, h, t) for d in docs.values() for h, t in d.sections]
    return docs, chunks


def git_sha(root=ROOT):
    try:
        import subprocess
        return subprocess.check_output(['git', '-C', root, 'rev-parse', 'HEAD'], text=True).strip()
    except Exception:
        return 'unknown'
