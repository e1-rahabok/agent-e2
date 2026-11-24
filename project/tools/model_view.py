"""What the model gets from one knowledge file, for the author's review (author, 2026-11-24: the reviewer reads the
machine form, as the LLM sees it).

Run: python3 project/tools/model_view.py <id or path> [<id or path> ...]
Example: python3 project/tools/model_view.py vsphere/technology/cpu/concepts/vcpu-states

Prints, from the same code the harness runs (harness/knowledge_loader.py, upfront_knowledge.py, catalog_database.py), so
the view cannot drift from what the model gets:
  1. the chunks search indexes, one per `## ` section, each with its prefix and token count;
  2. the up-front line, when the file has one (it reaches every answer);
  3. glossary entries that point to the file;
  4. the catalog rows the file brings as exact facts;
  5. what the model never gets: Mermaid charts, image pixels, the metadata fields kept for review.
Not shown: how a question ranks the chunks. The retrieval check (benchmark/runner/retrieval_check.py) measures that.
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'harness'))
import catalog_database  # noqa: E402
import knowledge_loader  # noqa: E402
import upfront_knowledge  # noqa: E402

REVIEW_ONLY = ('status', 'source', 'review_notes', 'corrections')   # never embedded (KNOWLEDGE-ENGINEERING.md, section 3)


def find(docs, arg):
    """A knowledge id, or a path to a knowledge file (absolute or from the repository root)."""
    key = arg.strip().removesuffix('.md').removeprefix('knowledge/')
    if key in docs:
        return docs[key]
    path = os.path.abspath(arg if os.path.isabs(arg) else os.path.join(ROOT, arg))
    return next((d for d in docs.values() if os.path.abspath(d.path) == path), None)


def view(docs, chunks, doc, catalog=None):
    """The model's view of one file, as text."""
    out = [f'# Model view: {doc.title} ({doc.id})', f'Status: {doc.status}. File: {os.path.relpath(doc.path, ROOT)}', '']
    mine = [c for c in chunks if c.doc is doc]
    total = sum(upfront_knowledge.tokens(c.text) for c in mine)
    out.append(f'## 1. Chunks search indexes: {len(mine)}, about {total} tokens')
    for n, c in enumerate(mine, 1):
        out += ['', f'--- chunk {n} of {len(mine)}, about {upfront_knowledge.tokens(c.text)} tokens ---', c.text]
    out += ['', '## 2. Up-front line (reaches every answer)']
    belief = doc.meta.get('up_front')
    if not belief:
        out.append('None.')
    else:
        line = upfront_knowledge.up_front_line(doc, belief)
        out.append(upfront_knowledge.rules_block({doc.id: doc}).split('\n', 1)[-1] if line
                   else f'Marked up_front "{belief}", but no single Misconceptions line starts with it: nothing is sent.')
    out += ['', '## 3. Glossary entries that point to this file']
    entries = [e for e in knowledge_loader.glossary(docs) if e['file'] == doc.id]
    out += [f"- {e['term']}: {e['meaning']}" + (f" Also called: {', '.join(e['also'])}." if e['also'] else '')
            + (f" Not to confuse with {e['confusable'][0]}: {e['confusable'][1]}." if e['confusable'] else '')
            for e in entries] or ['None.']
    out += ['', '## 4. Catalog rows, exact facts (with the file in the reading set)']
    facts = (catalog or catalog_database.get(docs)).facts_for([doc.id], max_rows=1000)
    out.append(facts.split('\n', 1)[1] if facts else 'None.')
    out += ['', '## 5. Never sent to the model']
    raw = open(doc.path).read()
    charts = len(knowledge_loader.MERMAID.findall('\n' + raw))
    out.append(f'- Mermaid charts: {charts}.' + (' Every fact in a chart must also be in the text.' if charts else ''))
    images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', doc.body)
    out.append(f'- Image pixels: {len(images)} image(s). The model gets only the alt text and the text around it.')
    for alt, path in images:
        out.append(f'  - {os.path.basename(path)}: alt text "{alt}"')
    kept = [k for k in REVIEW_ONLY if doc.meta.get(k)]
    out.append('- Metadata kept for review: ' + (', '.join(
        f"{k} ({len(doc.meta[k])})" if isinstance(doc.meta[k], list) else k for k in kept) or 'none') + '.')
    out.append('- Metadata used as filters and links, not as text: '
               + ', '.join(f for f in knowledge_loader.FILTER_FIELDS + knowledge_loader.LINK_TYPES if doc.meta.get(f)) + '.')
    return '\n'.join(out)


def main(args):
    if not args or args[0] in ('-h', '--help'):
        print(__doc__)
        return 0 if args else 2
    docs, chunks = knowledge_loader.load()
    status = 0
    for n, arg in enumerate(args):
        doc = find(docs, arg)
        if doc is None:
            print(f'Not a knowledge file: {arg}', file=sys.stderr)
            status = 1
            continue
        print(('\n\n' if n else '') + view(docs, chunks, doc))
    return status


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
