"""Up-front knowledge: blocks added to Agent E2's answer prompt. Design: harness/AGENT.md, section 4.5.

Each block is generated from the knowledge base at start, so it cannot drift from it:
  rules      Level 300 misconceptions: the `## Misconceptions` lines marked `up_front` in their knowledge files
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

def rules_block(docs):
    """The up-front misconceptions: the `## Misconceptions` line of each knowledge file whose metadata `up_front` names
    its wrong belief. One home (author, Q211): the line lives in its file; this block only collects it."""
    import kb
    lines = []
    for i in sorted(docs):
        belief = docs[i].meta.get('up_front')
        if not belief:
            continue
        line = up_front_line(docs[i], belief)
        if line:
            right = line.split('→', 1)[1].strip() if '→' in line else ''
            lines.append(f'- "{belief}" → {kb.FILE_LINK.sub(r"\\1", right)} See `{i}`.')
    return '\n'.join(['## Level 300 misconceptions'] + lines) if lines else ''


def up_front_line(doc, belief):
    """The line of the file's `## Misconceptions` section that starts with the quoted belief, or None."""
    for head, text in doc.sections:
        if head == 'Misconceptions':
            hits = [l for l in text.split('\n') if l.startswith(f'- "{belief}"')]
            return hits[0] if len(hits) == 1 else None
    return None


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
