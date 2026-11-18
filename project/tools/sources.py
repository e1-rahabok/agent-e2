"""Source notes and the knowledge files digested from them (KNOWLEDGE-ENGINEERING.md, section 6; project/sources/README.md).

Run: python3 project/tools/sources.py      Prints each source note and the knowledge files whose source.path cites it.
The trace is read from the knowledge files' metadata, so it is never kept by hand. lint.py calls check() on every
note a knowledge file cites: the note exists (not in future/), the cited headings exist, and the note has its
Release line and an Evidence section whose tags resolve.
"""
import glob
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SOURCES = os.path.join(ROOT, 'project', 'sources')
sys.path.insert(0, os.path.join(ROOT, 'harness'))

# source.path: "project/sources/<note>.md > Heading > Subheading; <another source>"
NOTE_REF = re.compile(r'project/sources/([^\s;>]+?\.md)((?:[ \t]*>[ \t]*[^;>]+)*)')
HEADING = re.compile(r'^#{1,6}[ \t]+(.+?)[ \t]*#*[ \t]*$', re.M)
FENCE = re.compile(r'^```.*?^```', re.M | re.S)
TAG = re.compile(r'\[(E\d+(?:,[ \t]*E\d+)*)\]')
ENTRY = re.compile(r'^- (E\d+):[ \t]*(.+)$', re.M)
EVIDENCE_FILE = re.compile(r'\bevidence/[^\s,;)]+')


def refs(path_value):
    """(note, [heading, ...]) for each source note a source.path names."""
    out = []
    for m in NOTE_REF.finditer(str(path_value or '')):
        heads = [h.strip() for h in m.group(2).split('>') if h.strip()]
        out.append((m.group(1), heads))
    return out


def _read(note):
    with open(os.path.join(SOURCES, note), encoding='utf-8') as f:
        return f.read()


def headings(text):
    return {h.strip('*_ ') for h in HEADING.findall(FENCE.sub('', text))}


def evidence(text):
    """The entries of '## Evidence': {'E1': 'text', ...}."""
    m = re.search(r'^## Evidence[ \t]*\n(.*?)(?=^## |\Z)', text, re.M | re.S)
    return dict(ENTRY.findall(m.group(1))) if m else {}


def check(note, heads):
    """Problems of one cited note, as strings."""
    if note.startswith('future/'):
        return [f'cites {note}: future/ holds sources not yet digested (project/sources/README.md)']
    if not os.path.exists(os.path.join(SOURCES, note)):
        return [f'cites project/sources/{note}, which does not exist']
    text = _read(note)
    out = []
    have = headings(text)
    for h in heads:
        if h not in have:
            out.append(f'cites heading "{h}" of {note}, which has no such heading')
    if not re.search(r'^- Release:[ \t]*\S', text, re.M):
        out.append(f'{note}: a cited note needs a "- Release:" line under its title')
    entries = evidence(text)
    if not entries:
        out.append(f'{note}: a cited note needs a "## Evidence" section with "- E1: ..." entries')
    for group in TAG.findall(text):
        for t in re.split(r',[ \t]*', group):
            if t not in entries:
                out.append(f'{note}: tag [{t}] has no entry in ## Evidence')
    for e, body in entries.items():
        for p in EVIDENCE_FILE.findall(body):
            if not os.path.exists(os.path.join(SOURCES, p)):
                out.append(f'{note}: evidence {e} names {p}, which does not exist')
    return out


def notes():
    """Every source note: the Markdown files of project/sources/, outside future/, except README.md."""
    out = []
    for f in sorted(glob.glob(os.path.join(SOURCES, '**', '*.md'), recursive=True)):
        rel = os.path.relpath(f, SOURCES)
        if rel == 'README.md' or rel.startswith('future' + os.sep) or rel.startswith('export-templates' + os.sep):
            continue
        out.append(rel)
    return out


def trace(docs):
    """{note: [knowledge id, ...]} from source.path; docs is kb.load()[0]."""
    out = {n: [] for n in notes()}
    for i, d in sorted(docs.items()):
        for note, _ in refs((d.meta.get('source') or {}).get('path')):
            out.setdefault(note, []).append(i)
    return out


def main():
    import kb
    t = trace(kb.load()[0])
    for note, ids in t.items():
        print(f'{note}: {len(ids)} knowledge files')
        for i in ids:
            print(f'  {i}')
    print(f'{sum(1 for v in t.values() if not v)} of {len(t)} notes cited by no knowledge file')


if __name__ == '__main__':
    main()
