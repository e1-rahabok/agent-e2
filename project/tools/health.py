"""Health of the knowledge base: the numbers KNOWLEDGE-ENGINEERING.md, section 7, tracks. No targets except those the plan sets.

Run: python3 project/tools/health.py
Prints: size of the indexed text, review status, open review notes and corrections, up-front lines, files no question
names, files no other file links to, and source notes no knowledge file cites. Lint checks each file; this describes the set.
"""
import collections
import glob
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'harness'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb  # noqa: E402
import primer  # noqa: E402
import sources  # noqa: E402

INLINE_ID = re.compile(r'`((?:vsphere|guest-os|sp5-framework|vcf-operations)/[a-z0-9\-/]+)`')


def questions():
    """Knowledge ids named by run questions (metadata knowledge and knowledge_main)."""
    named = set()
    for f in glob.glob(os.path.join(ROOT, 'benchmark', 'questions', '*.md')):
        fm, _ = kb.split(f)
        if not fm or fm.get('status') not in ('draft', 'reviewed'):
            continue
        named.update(fm.get('knowledge') or [])
        if fm.get('knowledge_main'):
            named.add(fm['knowledge_main'])
    return named


def report(docs):
    rows = []
    n = len(docs)
    rows.append(('Knowledge files', n))
    rows.append(('Indexed text, tokens (about)', sum(primer.tokens(d.body) for d in docs.values())))
    status = collections.Counter(d.status for d in docs.values())
    rows.append(('Reviewed', f'{status["reviewed"]} of {n}'))
    notes = [d for d in docs.values() if d.meta.get('review_notes')]
    rows.append(('Open review notes', f'{sum(len(d.meta["review_notes"]) for d in notes)} in {len(notes)} files'))
    corr = [d for d in docs.values() if d.meta.get('corrections')]
    rows.append(('Corrections to vendor documents', f'{sum(len(d.meta["corrections"]) for d in corr)} in {len(corr)} files'))
    rows.append(('Up-front misconception lines', sum(1 for d in docs.values() if d.meta.get('up_front'))))
    named = questions()
    rows.append(('Files no question names', sum(1 for i in docs if i not in named and i != 'glossary')))
    inbound = set()
    for i, d in docs.items():
        for t in kb.LINK_TYPES:
            inbound.update(x for x in d.links[t] if x != i)
        inbound.update(x for x in INLINE_ID.findall(d.body) if x != i)
    rows.append(('Files no other file links to', sum(1 for i in docs if i not in inbound and i != 'glossary')))
    t = sources.trace(docs)
    rows.append(('Source notes cited by no knowledge file', f'{sum(1 for v in t.values() if not v)} of {len(t)}'))
    return rows


def main():
    for name, value in report(kb.load()[0]):
        print(f'{name:<42} {value}')


if __name__ == '__main__':
    main()
