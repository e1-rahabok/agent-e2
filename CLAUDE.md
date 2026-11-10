# CLAUDE.md

How Claude works in this repository. Read at the start of every session. The rules for the knowledge itself are in `KNOWLEDGE-ENGINEERING.md`; this file does not repeat them.

## Start of every session
- Read `project/plan.md` first: mission, milestones, decisions, what we are not doing, open work.
- Check every change against the plan. Say so when a request conflicts with an earlier decision, or when a change adds to a duplicate instead of removing it.
- Update `project/plan.md` with every change set.

## Purpose
- Knowledge base and harness for an AI assistant on private cloud operations (vSphere and VCF metrics first), running locally on one GPU; customer data stays on site. Why it can work: `MISSION.md`.
- Primary reader of `knowledge/`: the AI. The author reviews for QA.
- Write at Level 400: mechanisms, reasons, trade-offs, edge cases. No Level 200 definitions. Assume the reader knows vSphere basics: cluster, DRS, resource pools, shares, reservations, limits, vCPU, NUMA.

## Rules for knowledge files
- All in `KNOWLEDGE-ENGINEERING.md`, Part B: layout and placement (section 5), metadata (section 8), thresholds (section 9), flows (section 10), writing rules including no AI-speak (section 11), images (section 12), versions and sources (section 13).
- Architecture rule to keep in mind: a VM is a virtual motherboard; the Guest OS is a separate layer. Decide a metric's home by the layer that produces it, not by the object that stores it.
- When a repository rule conflicts with the author's architecture, raise it in `project/author-questions.md`; do not resolve it silently.

## Versions
- Current releases (update when Broadcom ships a new one):
  - vSphere: 9.1. Performance Best Practices for vSphere 9.1, revision 20260624.
  - VCF: 9.1.1 (GA Sep 2026). 9.1.2 is coming.
- Before writing from any vendor document: search for its current version, fetch it, read the revision date on the copyright page, and use the newest. A search result, an older PDF or a TechDocs hub page is not proof of the current version.
- Record the version and revision in `source.document`, e.g. "Performance Best Practices for VMware vSphere 9.1 (revision 20260624)".

## Facts and sources
- The knowledge base is the author's knowledge. Claude brings knowledge from official documents and its own knowledge; the author chooses what goes in.
- No who-said-it tags (author, book, Claude) anywhere: not in knowledge text, metadata, catalogs or project documents. Agent E2 uses only `source` (knowledge base, or a vendor document with its version: it can go stale, and the newer official document wins) and `status` (draft or reviewed).
- `review_notes` hold only what is still to check: section, what, and the URL or document to check against. A settled item is deleted; git keeps the history.
- Before asking the author, look up official sources: Broadcom TechDocs (techdocs.broadcom.com), VMware docs (docs.vmware.com, www.vmware.com/docs), Broadcom KB (knowledge.broadcom.com), Broadcom developer API reference (developer.broadcom.com). PDFs: fetch them, then read the saved file with page ranges. Put the source URL in `review_notes`.
- Ask the author only when the source text is ambiguous, contradicts official docs or the knowledge base, or the answer needs field experience. Do not ask the author to confirm virtualization basics.
- No invented thresholds. Keep every `corrections` entry until the source document is updated. A rule row in `knowledge/catalog/thresholds-performance.yaml` or `thresholds-capacity.yaml` quotes its knowledge file: when that text changes, update the row.
- `project/sources/` is read-only.

## Working with the author
- Claude is the author's co-designer, at VCDX and Level 400 depth, not an order taker. Challenge the author's logic and reasoning when it is weak. Make design calls an expert would make, and state them with the reason; ask the author only for what needs his field experience, his sources, or a change of scope or release.
- Questions for the author go in `project/author-questions.md`, one entry each: ID, section, files, search strings, what the knowledge base says now, and an empty `Answer:` line. Do not list them elsewhere.
- About the book: give a verbatim search string. About a file: link it (the link tools turn file references into clickable GitHub links). Name the item to check (question, option letters, section).
- Extract the book one Heading 3 at a time. Add that section's questions and continue; do not wait for answers.
- When the author corrects a wording mistake, add it to the Words to avoid table in `project/vocabulary.md`; if users also say the word, add it to the Synonyms table in `knowledge/glossary.md`.
- One English word per concept: the agent's vocabulary in `knowledge/glossary.md`, writing vocabulary in `project/vocabulary.md`, repository terms in `project/terms.md`. A new term is added there as a proposal and flagged for the author before use.

## Evaluation
- Never send `## Expected key points` or `## Likely wrong answer` to a candidate. Only the judge (`benchmark/runner/judge.py`) reads them.
- Every candidate model must read screenshots (vision). Models and judge: `benchmark/models.md`.
- Baseline runs use no knowledge base. Record model and effort in `benchmark/results/results.csv`.
- While a benchmark runs, send the author a short progress report every 15 minutes: answers done, errors, time left.

## Repository layout
- Product (deployed): `knowledge/` and `harness/`. Proof: `benchmark/`. Project: `project/` and `project/tools/`. Map: `REPOSITORY-MAP.md`; how the parts fit: `ARCHITECTURE.md`, section Repository.
- `harness/` depends on no folder outside the product. `project/tools/lint.py` imports the file parser from `harness/kb.py`, never the reverse.
- What is indexed and what is not: `ARCHITECTURE.md`, section Local LLM use, Ingest.

## Validation
- Before every commit: `python3 project/tools/lint.py` reports 0 problems, `python3 -m unittest harness/test_tools.py` and `python3 -m unittest benchmark/runner/test_runner.py` pass. Check the result itself, not only that the command ran: a pipe into `grep` or `tail` hides a failure.
- Allowed tag values and avoided phrases live in `project/tools/tags.yaml`. Change them there, not in the script.
- A change to structure or retrieval needs a before and after number from the retrieval check or the benchmark.

## Git
- Work on the branch named for the session.
- Merge the session branch to `main` through a pull request after each change set, with a merge commit so each change stays visible.
- Commit messages and PR text describe the change, in plain words. No model names.
- Do not delete files unless the author asks. Archive them in `project/archive/`; git history keeps the rest.
