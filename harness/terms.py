"""Question understanding before search: map the words a user writes to the knowledge base.

Users write Level 300 terms ("CPU usage is high", "steal time", "the real-time chart"). The term map
(knowledge/catalog/user-terms.yaml) turns each hit into three things, all deterministic:
  - knowledge-base terms added to the search query;
  - knowledge files pulled into the context;
  - one note per hit for the model: the misreading the words carry and what to read instead.
"""
import os
import re

import yaml

from kb import ROOT

PATH = os.path.join(ROOT, 'knowledge', 'catalog', 'user-terms.yaml')
_ROWS = None


def rows(path=PATH):
    global _ROWS
    if _ROWS is None or path != PATH:
        data = yaml.safe_load(open(path)) if os.path.exists(path) else {}
        out = []
        for r in (data or {}).get('rows') or []:
            r = dict(r)
            r['_match'] = [re.compile(p, re.I) for p in r.get('match') or []]
            r['_unless'] = re.compile(r['unless'], re.I) if r.get('unless') else None
            out.append(r)
        if path != PATH:
            return out
        _ROWS = out
    return _ROWS


def match(question, table=None):
    """Rows whose patterns appear in the question, in table order."""
    hits = []
    for r in table if table is not None else rows():
        if any(p.search(question) for p in r['_match']) and not (r['_unless'] and r['_unless'].search(question)):
            hits.append(r)
    return hits


def query(question, hits):
    """The question plus the knowledge-base terms of the hits."""
    extra = ' '.join(dict.fromkeys(h['means'] for h in hits if h.get('means')))
    return question + ('\n' + extra if extra else '')


def files(hits, docs=None, n=3):
    """Files of the hits, first file of each hit first, at most n, only ids that exist."""
    out = []
    for depth in range(3):
        for h in hits:
            f = (h.get('files') or [])[depth:depth + 1]
            for i in f:
                if i not in out and (docs is None or i in docs):
                    out.append(i)
    return out[:n]


def block(hits):
    """Notes for the model, one line per hit."""
    if not hits:
        return ''
    lines = [f"- {h['note']} (`{(h.get('files') or [''])[0]}`)" for h in hits]
    return 'Terms in this question (read with the files cited):\n' + '\n'.join(lines)
