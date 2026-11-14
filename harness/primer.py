"""Up-front knowledge: blocks added to Agent E2's answer prompt. Design: harness/AGENT.md, section 4.5.

Each block is generated from the knowledge base at start, so it cannot drift from it:
  rules      Level 300 misconceptions and their corrections (knowledge/misconceptions.md)
  terms      confusable pairs (knowledge/glossary.md, column Not to confuse with)
A confident wrong belief is never looked up, so its correction is in place before the model reasons. Each block has a
switch in benchmark/runner/config.yaml, key primer. The map, flow index and procedure blocks of the tool loop are gone
(2026-11-14): they told the model how to plan its lookups, and the agent's code plans now (archived in
project/archive/legacy/harness-tool-loop-2026-11-14/primer.py).
"""
import os
import re

BLOCKS = ('rules', 'terms')
BUDGET_TOKENS = 3000          # all blocks together; lint checks it
MISCONCEPTIONS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'knowledge', 'misconceptions.md')

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


def build(docs, switches):
    """Return the switched-on blocks as one text, in fixed order; '' when none is on."""
    make = {'rules': rules_block, 'terms': terms_block}
    parts = [make[b](docs) for b in BLOCKS if (switches or {}).get(b)]
    parts = [p for p in parts if p]
    if not parts:
        return ''
    return '# What you know before you read\n\n' + '\n\n'.join(parts)


def tokens(text):
    return len(re.sub(r'\s+', ' ', text)) // 4
