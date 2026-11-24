# Sources

Source documents the knowledge is written from: the author's material, vendor PDFs and source notes. Extraction from the author's books is complete; isvara.io is a product made from the knowledge, not a source. The knowledge base is the one master and a superset of these sources (KNOWLEDGE-ENGINEERING.md, section 2). The author adds sources; Claude may edit them (author, 2026-11-14). Not indexed, not shipped, not read at run time.

What is here:
- Source notes: one Markdown file per topic, a few pages long, written by the author with Claude from the author's material, documentation and the environment (KNOWLEDGE-ENGINEERING.md, section 6).
- Vendor documents (PDFs) and the author's files: Word documents, spreadsheets, draw.io diagrams, decks, JSON exports.
- `evidence/`: screenshots, API output and lab results that source notes cite.
- `export-templates/`: the column layouts of tool exports, for benchmark CSVs.
- `future/`: sources for later releases (below).

The files cut across VCF components (vSphere, vSAN, NSX, the Guest OS), so they sit in one folder, not under a component.

## Source note
A source note carries its evidence, so the knowledge files that are digested from it do not have to. Format:

```markdown
# <Topic>

- Release: <the release the note describes, e.g. VCF 9.1.1>
- Date: <yyyy-mm-dd of the last change>

## <Heading>
- <Claim about vendor behaviour, or a measured number> [E1]
- <The author's own judgment: no tag>

## Evidence
- E1: <vendor document, version, revision, page> <URL>
- E2: evidence/<file>.png (<product and build>, <date>)
- E3: <API call> on <product and build>; output evidence/<file>.json
- E4: Lab test: <setup>, <date>; result evidence/<file>
```

- Tag every claim about vendor behaviour and every measured number. The author's judgment as an expert needs no tag: it is the knowledge base's own source.
- Evidence is primary: a vendor document with its version and page, a screenshot, API output, or a lab result. A summary written by a model is not evidence, and neither is another source note.
- Remove customer data from screenshots and API output before they are added to `evidence/`.
- A knowledge file digested from a note names it in `source.path`: `project/sources/<note>.md > <heading>`, several separated by `;`.
- Lint checks every note a knowledge file cites: the note exists and is not in `future/`, the cited headings exist, the `Release:` line is there, every `[E<n>]` tag has an entry in `## Evidence`, and every `evidence/` file named there exists. A note that no knowledge file cites is not checked yet.
- Which knowledge files each note feeds: `python3 project/tools/source_trace.py`. When a note changes, recheck those files.

## future/
Sources for future releases. Not digested: nothing in them is in `knowledge/`, and each file says so in its first line. Move a file up to `project/sources/` when a release takes it in (author, 2026-11-15, Q229).
