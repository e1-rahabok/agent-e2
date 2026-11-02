# CLAUDE.md

Standing rules for this repository. Read at the start of every session.

## Purpose
- Knowledge base for an AI assistant on vSphere and VCF metrics.
- Primary reader: the AI. The author reviews for QA only.
- No text aimed at human motivation or narrative. See `docs/philosophy-and-structure.md`.

## Level
- Write at Level 400: mechanisms, reasons, trade-offs, edge cases.
- No Level 200 definitions. Assume the reader knows vSphere basics: cluster, DRS, resource pools, shares, reservations, limits, vCPU, NUMA.
- Target: vSphere 9 and VCF 9. Check version differences before writing.

## Check the docs before asking the author
- Before asking the author a question, look up official sources:
  - Broadcom TechDocs: techdocs.broadcom.com
  - VMware docs: docs.vmware.com, www.vmware.com/docs
  - Broadcom KB: knowledge.broadcom.com
  - Broadcom developer API reference: developer.broadcom.com
- Use WebSearch and WebFetch.
- PDFs: fetch them, then read the saved file with Read, using page ranges.
- Put the source URL in `review_notes` for any fact taken from official docs.
- Ask the author only when:
  - the source text is ambiguous,
  - the source contradicts official docs or the knowledge base,
  - the answer needs field experience (tribal knowledge).

## Facts and sources
- Allowed fact sources: the author's book, the author's answers, official docs, Claude's own knowledge.
- Mark any fact not from the book `[claude-knowledge]`. List it in `review_notes` until the author confirms.
- No invented thresholds. A threshold goes in only if the book, the author or an official source gives it. Quote the source.
- Keep every `[author-correction ...]` marker. Clear a `corrections` entry only when the source document is updated.
- `knowledge/raw-input/` is read-only.

## Writing
- One fact per bullet or table row.
- Explain the mechanism and the reason before the metric name.
- Never mix vantage points in one counter file: vCPU, VM, ESXi, cluster, datastore, guest OS.
- CPU scheduling language: a vCPU is a thread in the scheduler. It demands runtime. The kernel decides how much runtime it gets. Do not write "need", "want", "wish", or "uses only X% of what it needs".
- Formulas as plain text. Diagrams as Mermaid plus a text explanation.
- Every new knowledge file has YAML front matter (see `README.md`).

## Evaluation
- Never send `## Expected key points` or `## Likely wrong answer` to the AI under test.
- Baseline runs use no knowledge base. Record model and effort in `evaluation/results/results.csv`.

## Do not index
- `knowledge/_templates/`, `knowledge/raw-input/`, `evaluation/`, `docs/`, `README.md`, `CLAUDE.md`.

## Git
- Work on the branch named for the session. Do not push to `main`.
- Commit messages and PR text describe the change. No model names.
- Do not delete files unless the author asks. Git history keeps them.
