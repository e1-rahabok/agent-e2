# CLAUDE.md

Standing rules for this repository. Read at the start of every session.

## Purpose
- Knowledge base for an AI assistant on vSphere and VCF metrics.
- Primary reader: the AI. The author reviews for QA only.
- No text aimed at human motivation or narrative. See `docs/philosophy-and-structure.md`.

## Level
- Write at Level 400: mechanisms, reasons, trade-offs, edge cases.
- No Level 200 definitions. Assume the reader knows vSphere basics: cluster, DRS, resource pools, shares, reservations, limits, vCPU, NUMA.
- Target: the current release in the Versions section. Never write from an older release when a newer one exists.

## Versions
- Current releases (update when Broadcom ships a new one):
  - vSphere: 9.1. Performance Best Practices for vSphere 9.1, revision 20260624.
  - VCF: 9.1.1 (GA Sep 2026). 9.1.2 is coming.
- Before writing from any vendor document:
  - search for the current version of that document, e.g. "Performance Best Practices for VMware vSphere 9.1",
  - fetch it and read the revision date on the copyright page,
  - if a newer version exists than the one you have, use the newer one.
- Do not treat a search result, an older PDF, or a TechDocs hub page as the current version. Check the version each time.
- Record the version and revision in `source.document`, e.g. "Performance Best Practices for VMware vSphere 9.1 (revision 20260624)".
- If a file was written from an older version, add a `review_notes` line naming the newer version, and re-check the file before setting `status: reviewed`.

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
- Record any fact not from the book in `review_notes`, naming the section, until the author confirms.
- Audit information lives only in the metadata block. Never put markers such as author corrections or Claude-knowledge tags in headings or body text.
- No invented thresholds. A threshold goes in only if the book, the author or an official source gives it. Quote the source.
- Keep every `corrections` entry, naming the section it affects. Clear it only when the source document is updated.
- `knowledge/raw-input/` is read-only.

## Architecture: VM vs Guest OS
- A VM is a virtual motherboard, not a complete machine. The Guest OS (Windows, Linux) is a separate layer that runs on it.
- Never file, tag or describe a Guest OS metric as a VM metric. Guest OS metrics go in `<technology>/metrics/guest-os/` with `layer: [guest-os]` and no `object: VirtualMachine`.
- VM metrics go in `<technology>/metrics/virtual-motherboard/` with `layer: [virtual-motherboard]` and `object: [VirtualMachine]`.
- That vCenter or VCF Operations store a counter on the VM object does not make it a VM metric. Decide by the layer that produces it.
- When a repository rule conflicts with the author's architecture, raise it in `docs/author-questions.md`; do not resolve it silently.
- `scripts/validate.py` enforces the folder and tag rules.

## Writing
- One fact per bullet or table row.
- Explain the mechanism and the reason before the metric name.
- One vSphere managed object type per metric file (VirtualMachine, HostSystem, ClusterComputeResource, Datastore, ...). Instance levels such as per-vCPU go in the `instance` tag.
- Folder rules: technology first (cpu, memory, storage, network, system), then concepts / metrics / configuration / diagnosis. Tags and field meanings: see `README.md`.
- CPU scheduling language: a vCPU is a thread in the scheduler. It demands runtime. The kernel decides how much runtime it gets. Do not write "need", "want", "wish", or "uses only X% of what it needs".
- Formulas as plain text. Diagrams as Mermaid plus a text explanation. Troubleshooting flows: rule in `README.md`, section Troubleshooting flow diagrams.
- Every knowledge file ends with a `## Metadata` section holding one yaml block (see `README.md`). No front matter at the top.
- Keep the author's own diagrams from the book in `knowledge/vsphere/<technology>/images/`, linked under the section they explain, with alt text. Name each file by what it shows (pattern in `README.md`, section Images). Tag each image in the metadata `images` list.
- Quotation marks only for verbatim text. Paraphrase without quotes, so the author can search the book for real quotes.
- Do not ask the author to confirm virtualization basics (for example: Steal Time exists only in a VM). Resolve them from own knowledge.
- When asking the author about the book, give a verbatim search string.
- When asking the author to check a file, give its full GitHub URL on `main`, so it is clickable. Name the item to check (case id, option letters, section).
- Questions for the author go in `docs/author-questions.md`, one entry each: ID, section, files, search strings, what the knowledge base says now, and an empty `Answer:` line. Do not list them elsewhere.
- Extract the book one Heading 3 at a time. Add that section's questions to `docs/author-questions.md` and continue; do not wait for answers.
- Use terms from `knowledge/glossary/terminology.md`. Tag values must match it. A new term is added there as a proposal and flagged for the author before use.
- When the author corrects a wording mistake, add it to the Words to avoid table in the terminology file.

## Evaluation
- Never send `## Expected key points` or `## Likely wrong answer` to the AI under test.
- Baseline runs use no knowledge base. Record model and effort in `evaluation/results/results.csv`.
- During an Auto Test run, send the author a short progress report every 15 minutes: answers done, errors, time left.

## Do not index
- `knowledge/_templates/`, `knowledge/raw-input/`, `evaluation/`, `docs/`, `README.md`, `CLAUDE.md`.

## Validation
- Run `python3 scripts/validate.py` before every merge. Do not merge if it fails.
- Allowed tag values and avoided phrases live in `knowledge/glossary/terminology.md` (section Allowed tag values). Change them there, not in the script.

## Git
- Work on the branch named for the session.
- Early development: merge the session branch to `main` through a pull request, automatically, after each change set. Use a merge commit so each change stays visible.
- Commit messages and PR text describe the change. No model names.
- Do not delete files unless the author asks. Git history keeps them.
