# CLAUDE-PROJECT.md

Rules, tools and paths of agent-e2, the repository of Agent E2. Loaded with [CLAUDE.md](CLAUDE.md), which holds the method. This repository is one of several; work across them follows the workspace's [CLAUDE-PROJECT.md](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/CLAUDE-PROJECT.md).

## Files of the method

- Roadmap, open questions and the specification that binds several repositories: the workspace's [ROADMAP.md](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/ROADMAP.md), [OPEN-QUESTIONS.md](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/OPEN-QUESTIONS.md), [brief](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/spec/brief.md) (goals, scope, constraints, risks) and [system design](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/spec/design/system.md) (contracts and design choices).
- No milestone hook runs here. Before acting, read the open milestone in the workspace's ROADMAP.md: the first heading that does not end with ": done".
- Requirements of this repository: [`project/requirements/`](project/requirements) (DESIGN-4). The Agent E2 API's contract requirements are in the workspace's [agent-e2-api.md](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/spec/requirements/agent-e2-api.md). Each requirement belongs to the workspace milestone that ROADMAP.md names.

## This repository

How Claude works in this repository. Read at the start of every session. The design of the knowledge is in [`KNOWLEDGE-ENGINEERING.md`](KNOWLEDGE-ENGINEERING.md), its rules in [`project/knowledge-rules/`](project/knowledge-rules); this file does not repeat them.

## Start of every session
- Read [`project/plan.md`](project/plan.md) first: mission, milestones, what we are not doing, open work.
- Check every change against the plan and the documents that own the rules. Say so when a request conflicts with an earlier decision, or when a change adds to a duplicate instead of removing it.
- Update [`project/plan.md`](project/plan.md) with every change set: status and open work only. A decision goes to the document that owns its rule, with its reason; the commit and the pull request record when it was made. No dates or decision log in the plan.
- Before writing any text, read the workspace's [writing rules](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/writing/README.md), for documents, diagram labels, commit messages and PR text, and [`project/knowledge-rules/writing.md`](project/knowledge-rules/writing.md) for knowledge files. Before every commit, reread what you wrote against them and against the workspace's [flagged phrases](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/writing/flagged-phrases.yaml): no slogans, no "X, not Y", headings as noun phrases. The workspace's style check runs on every pull request.

## Purpose
- Knowledge base and harness for an AI assistant on private cloud operations (vSphere and VCF metrics first), running locally on enterprise GPU (one GPU is an ideal, not a constraint; up to four large GPUs are acceptable); customer data stays on site. That is the target after release 1.0 (SCOPE-12 in the workspace's [brief](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/spec/brief.md)); release 1.0 runs Gemma 4 31B through Vercel AI Gateway (SCOPE-1, SCOPE-6). Why it can work: [`MISSION.md`](MISSION.md).
- Primary reader of `knowledge/`: the AI. The author reviews it for QA in that machine form, as the model gets it ([`project/tools/model_view.py`](project/tools/model_view.py)); no second copy is written for people.
- Write at Level 400: mechanisms, reasons, trade-offs, edge cases. No Level 200 definitions. Assume the reader knows vSphere basics: cluster, DRS, resource pools, shares, reservations, limits, vCPU, NUMA.

## Rules for knowledge files
- Design (where knowledge lives, forms, Level 400 and misconceptions): [`KNOWLEDGE-ENGINEERING.md`](KNOWLEDGE-ENGINEERING.md). Rules, one module each in [`project/knowledge-rules/`](project/knowledge-rules): placement, flows, metadata (with the dimensions not to mix), thresholds, writing (including no AI-speak, images, versions and sources), terminology, vocabulary (words to avoid).
- Architecture rule to keep in mind: a VM is a virtual motherboard; the Guest OS is a separate layer. Decide a metric's home by the layer that produces it, not by the object that stores it.
- When a repository rule conflicts with the author's architecture, raise it in [`project/author-questions.md`](project/author-questions.md); do not resolve it silently.

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
- No invented thresholds. Keep every `corrections` entry until the vendor document it corrects is updated. A row in `knowledge/catalog/thresholds-*.yaml` that has a `quote` quotes its knowledge file: when that text changes, update the row.
- [`project/sources/`](project/sources) holds the source documents. The author adds them; Claude may edit them.
- One master: the knowledge base. isvara.io (its articles are written from the knowledge base's export in release 1.0, the workspace's milestones M4 to M7) and the author's books (written by hand, informal style) are products for people, not sources. Extraction from the books is complete. New knowledge comes from [`project/sources/`](project/sources), stated once in KNOWLEDGE-ENGINEERING.md section 2. The knowledge base is a superset of the books: never name the book or write "the source document" in knowledge files or their metadata; `source.document` is `Knowledge base` plus any vendor document. A file digested from a source note names the note in `source.path`; the note holds the evidence ([`project/sources/README.md`](project/sources/README.md)).

## Working with the author
- [`MISSION.md`](MISSION.md) holds goals and stretch targets, not hard rules. Few rules hold in IT operations management: challenge every assumption, the author's and the repository's included, when evidence says it blocks the mission.
- Claude is the author's co-designer, at VCDX and Level 400 depth, not an order taker. Challenge the author's logic and reasoning when it is weak. Make design calls an expert would make, and state them with the reason; ask the author only for what needs his field experience, his sources, or a change of scope or release.
- Questions for the author go in [`project/author-questions.md`](project/author-questions.md), section Release 1.0 (blocks release 1.0) or Future release (later release), one entry each: ID, section, files, search strings, what the knowledge base says now, and an empty `Answer:` line. Do not list them elsewhere.
- A question ID is `Q-E2-` and the next free number. The workspace's questions are `Q-WS-` numbers.
- A question that binds several repositories goes to the workspace's [OPEN-QUESTIONS.md](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/OPEN-QUESTIONS.md) (DESIGN-23).
- Releases and their milestones are the workspace's ([ROADMAP.md](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/ROADMAP.md)); "release 1.0" in this repository means the workspace's release 1.0. The milestones in [`project/plan.md`](project/plan.md) are A1 to A6.
- A bad answer the author reports is a type of question that fails, not one wording. Find the type and its cause. Prefer the model's reading over a new code rule (keyword patterns, regexes), and remove the rules it replaces. Add 20 or more wordings of the type, with neighbours that must not change, to [`benchmark/runner/screen_answer_check.yaml`](benchmark/runner/screen_answer_check.yaml); run [`screen_answer_check.py`](benchmark/runner/screen_answer_check.py) on the real model before and after, read the answers, and report the table. Then fix, verify and merge without asking; ask only for field experience or a change of scope.
- About the book: give a verbatim search string. About a file: link it (the link tools turn file references into clickable GitHub links). Name the item to check (question, option letters, section).
- Before proposing to remove, archive or replace anything: look at it, list every consumer (the model, code, the author as reviewer, isvara.io), and say what each one loses.
- When the author corrects a wording mistake, add it to the Words to avoid table in [`project/knowledge-rules/vocabulary.md`](project/knowledge-rules/vocabulary.md); if users also say the word, add it to the Also called line of its entry in [`knowledge/glossary.md`](knowledge/glossary.md).
- One English word per concept: the agent's vocabulary in [`knowledge/glossary.md`](knowledge/glossary.md), words to avoid in [`project/knowledge-rules/vocabulary.md`](project/knowledge-rules/vocabulary.md), repository terms in [`project/terms.md`](project/terms.md). A new term is added there as a proposal and flagged for the author before use.

## Evaluation
- The benchmark is a proof, not a goal. It proves that Agent E2 works: the shipped configuration against the release gate and the frontier reference. No mode, run, metric or setting is kept for the benchmark's own sake. Development diagnostics come from free checks first: the retrieval check, traces, unit tests.
- Never send `## Answers` or `## Explanation` to a candidate: they are the key, for reviewers only. `## Answers` (the correct letters) is the only key the runner reads; the benchmark's scoring is set arithmetic, no judge (archived, Q-E2-199): every benchmark question is multiple choice. The free-text answer set of release 1.0 has its own grader ([R-E2-005](project/requirements/answer-service.md)).
- Every candidate model must read screenshots (vision). Models: [`benchmark/models.md`](benchmark/models.md).
- Baseline runs use no knowledge base. The model and its reasoning setting are in the run folder's `config.json` (`model_params`).
- Run a benchmark round: [`benchmark/RUN.md`](benchmark/RUN.md) (one prompt, the approvals to give up front, time and cost).
- Never start a full benchmark round: the author ruled it out, and `round_executor.py` refuses one.
- Test a change with the free checks, then with the answer set when it changes what the model reads or the model: the workspace's [test plan](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/spec/test-plan.md), section Tests for each kind of change.
- Start a paid step under US$10 without asking, after naming its need: the author, 2026-11-28: "Anything under $10 no need my approval" (CONSTRAINT-1). Run the answer set at its default limit, US$9 (`--max-cost-usd`).
- Wait for the author's go before a paid step of US$10 or more, and give it the limit the go names ([test-spending.md](project/requirements/test-spending.md)).
- After a paid step: report what it spent and what the key has left.
- When a round exits at its spending limit (exit 9): stop and tell the author; never raise `release.max_cost_usd` (US$25 a round, DESIGN-31 in the workspace's system design).
- While a benchmark runs, send the author a short progress report every 15 minutes: answers done, errors, time left.

## Repository layout
- Product (deployed): `knowledge/` and `harness/`. Proof: `benchmark/`. Project: `project/` and [`project/tools/`](project/tools). Map: [`REPOSITORY-MAP.md`](REPOSITORY-MAP.md); how the parts fit: [`ARCHITECTURE.md`](ARCHITECTURE.md), section Repository.
- `harness/` depends on no folder outside the product. [`project/tools/rules_check.py`](project/tools/rules_check.py) imports the file parser from [`harness/knowledge_loader.py`](harness/knowledge_loader.py), never the reverse.
- Code file names: rule in [`project/terms.md`](project/terms.md), section Code file names.
- Diagrams in the root documents are SVG. Read the `<details>` text under an image, not the SVG: it is generated from the SVG and holds every box and arrow. To change a diagram, edit its script ([`project/tools/product_diagram.py`](project/tools/product_diagram.py), [`knowledge_diagram.py`](project/tools/knowledge_diagram.py), [`document_diagrams.py`](project/tools/document_diagrams.py)), run it, then run `python3 project/tools/diagram_text.py`. Never edit an SVG or a text block by hand: the next run of the script overwrites a hand-edited SVG, and lint fails on a block that differs from its image.
- What is indexed and what is not: [`ARCHITECTURE.md`](ARCHITECTURE.md), section Local LLM use, Ingest.

## Validation
- Before every commit: `python3 project/tools/rules_check.py` reports 0 problems, `python3 -m unittest harness/test_harness.py` and `python3 -m unittest benchmark/runner/test_runner.py` pass. Check the result itself, not only that the command ran: a pipe into `grep` or `tail` hides a failure.
- On every pull request: [.github/workflows/tests.yml](.github/workflows/tests.yml) runs the same three, and every `project/tools/test_*.py`.
- Allowed tag values and avoided phrases live in [`project/tools/rules_check_values.yaml`](project/tools/rules_check_values.yaml). Change them there, not in the script.
- A change to structure or retrieval needs a before and after number from the retrieval check or the benchmark. The retrieval check runs on the run set as it is (Q-E2-206); re-baseline when the question bank changes.

## Git
- Work on the branch named for the session.
- Merge the session branch to `main` through a pull request after each change set, with a merge commit so each change stays visible.
- Always land the work on `main`: merge the pull request yourself in the same session, with no open pull request or side branch left behind. Before ending, check that `main` holds the change.
- The branch of a merged pull request is deleted by the repository setting "Automatically delete head branches". Every other branch that is not ahead of `main` is deleted by [.github/workflows/branch-cleanup.yml](.github/workflows/branch-cleanup.yml) (DESIGN-28 in the workspace's [system design](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/spec/design/system.md)). A cloud session cannot delete a branch (HTTP 403), and does not ask the author to. The author reads only `main`.
- Commit messages and PR text describe the change, in plain words. No model names.
- Do not delete files unless the author asks. Git history keeps every deleted file.
