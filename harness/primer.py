"""Up-front knowledge for the agent: five blocks added to the system prompt. Design: harness/AGENT.md, section 3.

Each block is generated from the knowledge base at start, so it cannot drift from it:
  map        what each area holds, what each file kind answers, which tool serves it (from ids and retriever_guide)
  rules      Level 300 misconceptions and their corrections (knowledge/misconceptions.md)
  terms      confusable pairs (knowledge/glossary.md, column Not to confuse with)
  flows      flow index by kind (every health-check, troubleshooting and decision-tree file: title and id)
  procedure  how to use the tools (fixed text: procedure, not facts)
Each block has a switch in benchmark/runner/config.yaml, key agent_primer. All off by default until the benchmark
shows a gain (harness/AGENT.md, section 7).
"""
import os
import re
from collections import Counter, defaultdict

BLOCKS = ('map', 'rules', 'terms', 'flows', 'procedure')
BUDGET_TOKENS = 3000          # all five blocks together; lint checks it
MISCONCEPTIONS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'knowledge', 'misconceptions.md')

KINDS = {  # folder kind -> what it answers and which tool serves it
    'concepts': ('how it works, why a value behaves so', 'search, read_file'),
    'metrics': ('what a counter means on one object', 'catalog, read_file, follow_links(same_name)'),
    'configuration': ('what a setting does', 'search, read_file'),
    'health-check': ('is this object healthy, on every pillar: the what', 'flow'),
    'troubleshooting': ('why is it down or slow: from a complaint, alert or failed health check step', 'flow'),
    'decision-tree': ('can it, should it, how much: one operational question, ending in a choice to act', 'flow'),
    'kpis': ('a performance KPI: sub-metrics, bands, scoring', 'catalog, read_file'),
    'models': ('a capacity or risk model: sub-metrics, bands, decision', 'catalog, read_file'),
    'tools': ('how esxtop or the vSphere Client shows the counters', 'read_file'),
}

PROCEDURE = """## Procedure
- Health check, troubleshooting or decision question: find the matching flow (index above, or search with its retriever_guide), then call flow and follow its steps in order.
- A unit, rollup, statistics level, esxtop field or threshold: call catalog. Never answer a number from memory.
- Any arithmetic or conversion: call calculate.
- About a metric: read its file, then follow_links(same_name) to the same label on other objects.
- Cite the ids of the files you read. If they do not settle the question, say so."""


def _area(doc_id):
    parts = doc_id.split('/')
    if parts[:2] in (['vsphere', 'technology'], ['vsphere', 'object-types'], ['vsphere', 'tools']) and len(parts) > 3:
        return '/'.join(parts[:3])
    if parts[0] in ('guest-os', 'vsphere', 'sp5-framework') and len(parts) > 2:
        return '/'.join(parts[:2])
    return parts[0] if len(parts) > 1 else 'glossary'


def _kind(doc_id):
    for k in KINDS:
        if f'/{k}/' in f'/{doc_id}/':
            return k
    return 'other'


def map_block(docs):
    areas = defaultdict(Counter)
    for i in docs:
        areas[_area(i)][_kind(i)] += 1
    lines = ['## Map of the knowledge base',
             'File kinds (folder name in the id):']
    lines += [f'- {k}/: {q}. Tool: {t}.' for k, (q, t) in KINDS.items()]
    lines += ['- other: overviews, comparisons, observability rules.', 'Areas (files by kind):']
    for a in sorted(areas):
        c = areas[a]
        lines.append(f'- {a}: ' + ', '.join(f'{c[k]} {k}' for k in list(KINDS) + ['other'] if c[k]))
    return '\n'.join(lines)


def rules_block(docs):
    """The bullet lines of knowledge/misconceptions.md under its first '## ' heading, whatever that heading says."""
    if not os.path.exists(MISCONCEPTIONS):
        return ''
    with open(MISCONCEPTIONS) as f:
        t = f.read()
    m = re.search(r'^## .*$', t, re.M)
    import kb
    lines = [kb.FILE_LINK.sub(r'\1', l) for l in t[m.end():].split('\n') if l.startswith('- ')] if m else []
    return '\n'.join(['## Level 300 misconceptions'] + lines) if lines else ''


def terms_block(docs):
    """One line per glossary entry with a 'Not to confuse with' cell."""
    import kb
    rows = [e for e in kb.glossary(docs) if e['confusable']]
    if not rows:
        return ''
    lines = [f"- {e['term']} vs {e['confusable'][0]}: {e['confusable'][1]}" + (f" (`{e['file']}`)" if e['file'] else '')
             for e in rows]
    return '\n'.join(['## Confusable terms'] + lines)


def flows_block(docs):
    heads = {'health-check': 'Health checks (object -> flow id)', 'troubleshooting': 'Troubleshooting (symptom -> flow id)',
             'decision-tree': 'Decision trees (question -> flow id)'}
    lines = []
    for k, head in heads.items():
        rows = sorted((d.title, d.id) for i, d in docs.items() if _kind(i) == k)
        if rows:
            lines += [f'## {head}'] + [f'- {t}: {i}' for t, i in rows]
    return '\n'.join(lines)


def build(docs, switches):
    """Return the switched-on blocks as one text, in fixed order; '' when none is on."""
    make = {'map': map_block, 'rules': rules_block, 'terms': terms_block, 'flows': flows_block,
            'procedure': lambda _d: PROCEDURE}
    parts = [make[b](docs) for b in BLOCKS if (switches or {}).get(b)]
    parts = [p for p in parts if p]
    if not parts:
        return ''
    return '# What you know about the knowledge base\n\n' + '\n\n'.join(parts)


def tokens(text):
    return len(re.sub(r'\s+', ' ', text)) // 4
