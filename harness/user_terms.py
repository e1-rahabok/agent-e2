"""Question understanding before search: map the words a user writes to the knowledge base.

Users write Level 300 terms ("CPU usage is high", "steal time", "the real-time chart"). The term map
(knowledge/catalog/user-terms.yaml) turns each hit into three things, all deterministic:
  - knowledge-base terms added to the search query;
  - knowledge files pulled into the context;
  - one note per hit for the model: the misconception the words carry and what to read instead.
A row that names a product label (`label`) has no note of its own: its note and first file come from the glossary
entry of that label (Product label, Invites, Better name; KNOWLEDGE-ENGINEERING.md, section Product label and better
model), so the correction has one home. When such a row matches, the answer rules add the teaching order once
(LABEL_ORDER, harness/expert_agent.py): an instruction, not knowledge, so it is not charged to the reading set.
"""
import os
import re

import yaml

import knowledge_loader
from knowledge_loader import ROOT

PATH = os.path.join(ROOT, 'knowledge', 'catalog', 'user-terms.yaml')
GLOSSARY = os.path.join(ROOT, 'knowledge', 'glossary.md')
_ROWS = None

# The teaching order of a product label, narrowed (Q-E2-208): only when a matched row names a label, and inside the
# answer's length and shape, not added to them. Steps 1, 3 and 4 go in the conclusion; 2 and 5 fold into the
# mechanism and what to check next.
LABEL_ORDER = ('- A product label in "Terms in this question" (Computes, Invites, Better model): quote the label as the '
               'screen shows it, never reworded; the product uses a simpler model, not a wrong one. Inside the usual length: '
               'the conclusion names the label, the reading it invites, why that reading fails, and the better model with its '
               'name; the mechanism says what the product computes; what to check next says what to read instead.\n')


def labels(path=GLOSSARY):
    """Glossary entries that carry a product label, by term."""
    if not os.path.exists(path):
        return {}
    meta, body = knowledge_loader.split(path)
    if meta is None:
        return {}
    return {e['term']: e for e in knowledge_loader.glossary({'glossary': knowledge_loader.Doc(path, meta, body)}) if e['label']}


def label_note(e):
    """One line for the model from a product label entry: what it computes, what it invites, the better model."""
    name, model = e['better'] or ('', '')
    return f"{e['term']} (product label). Computes: {e['meaning']} Invites: {e['invites']} Better model, {name}: {model}"


def label_hits(question, case=None, table=None):
    """The matched rows that name a product label, from the question and the case."""
    hits = match(question, table)
    return [h for h in hits + case_labels(case, hits, table) if h.get('label')]


def rows(path=PATH, glossary_path=GLOSSARY):
    global _ROWS
    if _ROWS is None or path != PATH or glossary_path != GLOSSARY:
        data = yaml.safe_load(open(path)) if os.path.exists(path) else {}
        lab = labels(glossary_path)
        out = []
        for r in (data or {}).get('rows') or []:
            r = dict(r)
            if r.get('label'):
                e = lab.get(r['label'])
                if not e:
                    continue          # lint names the row whose label has no glossary entry
                r['note'] = label_note(e)
                r['files'] = list(dict.fromkeys(([e['file']] if e['file'] else []) + list(r.get('files') or [])))
            r['_match'] = [re.compile(p, re.I) for p in r.get('match') or []]
            r['_unless'] = re.compile(r['unless'], re.I) if r.get('unless') else None
            out.append(r)
        if path != PATH or glossary_path != GLOSSARY:
            return out
        _ROWS = out
    return _ROWS


def match(question, table=None):
    """Rows whose patterns appear in the question, the most hits first, table order within a tie."""
    hits = []
    for r in table if table is not None else rows():
        n = sum(len(p.findall(question)) for p in r['_match'])
        if n and not (r['_unless'] and r['_unless'].search(question)):
            hits.append((n, dict(r, _n=n)))
    hits.sort(key=lambda x: -x[0])   # stable: a row the question hits many times (the esxtop CPU fields) outranks one incidental word
    return [r for _, r in hits]


def case_labels(case, matched, table=None):
    """Label rows that the case names and the question text did not: a label read from a screenshot (expert_agent.py, stage 1)."""
    names = '. '.join(' '.join(str(m.get(k) or '') for k in ('object', 'name', 'unit')).strip()
                      for m in (case or {}).get('metrics') or [] if isinstance(m, dict))
    if not names:
        return []
    ids = {h['id'] for h in matched}
    return [h for h in match(names, table) if h.get('label') and h['id'] not in ids]


def query(question, hits):
    """The question plus the knowledge-base terms of the hits."""
    extra = ' '.join(dict.fromkeys(h['means'] for h in hits if h.get('means')))
    return question + ('\n' + extra if extra else '')


def files(hits, docs=None, n=3):
    """Files of the hits: the first two of a clearly strongest hit, then the first file of each hit, at most n, only ids that exist."""
    out = []
    for i in ((hits[0].get('files') or [])[:2] if hits and hits[0].get('_n', 0) >= 2 * (hits[1].get('_n', 0) if len(hits) > 1 else 0) else []):   # a row the question hits at least twice as often as any other gives its two files first
        if i not in out and (docs is None or i in docs):
            out.append(i)
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
    lines = [f"- {'Possible wrong premise: ' if h.get('premise') else ''}{h['note']} (`{(h.get('files') or [''])[0]}`)" for h in hits]
    return 'Terms in this question (read with the files cited):\n' + '\n'.join(lines)
