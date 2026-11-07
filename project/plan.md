# Plan

Read first, every session. One page: mission, milestones with exit criteria, decisions, what we are not doing, and the open work under each milestone. Update it with every change set. Not indexed.
Why the mission is possible: `MISSION.md`. Last review: [project/review-2026-11-06.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/review-2026-11-06.md). Questions waiting for the author: [project/author-questions.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/author-questions.md).

## Mission
- An open-weight model on one GPU, offline, answers Level 400 private cloud operations questions better than a frontier model.
- Release gate: final score at least 85% on the shipped configuration (live test); target 99%; confident-wrong rate near 0.

## Milestones
| # | Milestone | Exit criteria | Status |
|---|---|---|---|
| M1 | Knowledge base complete for 1.0 | Book Parts 1 and 3 and the VCF Operations chapters extracted; operations flows confirmed by the author; stubs filled or merged; every flow has a diagram; the most-cited files reviewed | In progress |
| M2 | 100 questions | 100 questions at the allocation ([benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), section 3.6); every attachment supplied; synthetic share decided; held-out set kept by the author | 90 written, 66 scorable |
| M3 | Retrieval | Retrieval check: every needed file in the context for most questions (target to set with the author); the three experiments of the review scored | 3 fixes done: hybrid 72% to 75%, 57 of 90 complete |
| M4 | Gateway benchmark | The 100 questions run on the candidates and the frontier reference; model and mode chosen; up-front blocks measured | Waits for M1 and M2 (author, 2026-11-06) |
| M5 | Live test | [benchmark/live-test.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/live-test.md) passed on the chosen model, offline | Planned |
| M6 | Release 1.0 | Every knowledge file reviewed; release score from the live test; offline bundle; the app calls `harness/` | Planned |

- After 1.0: screen library and screenshot read-back (1.1); data files (1.2); read-only VCF Operations connection; vSAN, NSX, Kubernetes, Linux content.

## Decisions (latest first)
- 2026-11-06, author: the product is named Agent E2 (two words); an LLM-based expert system, built as agentic RAG on a local LLM. It will replace AskIO on isvara.io. Repository rename to agent-e2 waits on the author (GitHub settings).
- 2026-11-06, author, on [project/review-2026-11-06.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/review-2026-11-06.md):
  - No benchmark run until the 100 questions and the knowledge base are complete.
  - Folders stay technology first: a technology works across Guest OS, VM, ESXi and cluster; master how it works, then apply it to the object.
  - VCF Operations content moved to [knowledge/vcf-operations](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations); tool references to [knowledge/vsphere/tools](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/tools); operations flows under [knowledge/operations-management](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management).
  - The three retrieval fixes go ahead (done; M3); knowledge depth and the review order go to the author (Q060-Q064); a live test plan is added.
  - Screenshots are read in 1.0; the screen library is 1.1.
  - The author writes the real-ticket questions, picked to complement the existing ones.
  - Context budget: 16K, 20K and 24K all give 76% (57 of 90); the misses are files never retrieved, not files cut by the budget.
  - Context budget set to 16K (author, 2026-11-06).
  - Source documents moved to [project/sources](https://github.com/e1-rahabok/agent-e2/blob/main/project/sources), writing templates to [project/templates](https://github.com/e1-rahabok/agent-e2/blob/main/project/templates): `knowledge/` holds only what the model reads (author, 2026-11-06).
  - This plan replaces `project/todo.md` (archived as [project/archive/todo-2026-11-06.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/archive/todo-2026-11-06.md)).
- Earlier decisions: [project/archive/review-2026-11-04.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/archive/review-2026-11-04.md), section 9; [project/author-questions.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/author-questions.md), section Resolved.

## Not doing
| What | Why |
|---|---|
| Object-first folders | Declined twice (2026-11-04, 2026-11-06) |
| Fine-tuning the model | Facts change and must be cited; retrieval supplies them (`ARCHITECTURE.md`, section Local LLM use) |
| A benchmark run before M1 and M2 | Author, 2026-11-06 |
| MoE models of 120B | Less compute per token than the dense candidates on twice the memory ([benchmark/models.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/models.md)) |
| The test website | Not started; design archived ([project/archive/design-kb-test-site.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/archive/design-kb-test-site.md)) |

## Open work
- 2026-11-07: moved ids. [knowledge/moved.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/moved.yaml) maps 298 old ids (from git history) to current ids; `kb.resolve()` follows it; lint flags old ids in questions and active documents; the link tool rewrites links to moved files; the retrieval check stops on an unknown id instead of dropping it.
### M1 Knowledge base
- Thresholds: one place since 2026-11-06 ([knowledge/catalog/thresholds-performance.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-performance.yaml), `thresholds-capacity.yaml`). Open: 31 prose statements in 24 files without a row (`python3 project/tools/threshold_inventory.py`); grey (wastage) values for the capacity bands; 5-minute readings where only 20-second ones exist.
- Book Part 1: Performance Management extracted 2026-11-06 into 4 files ([operations-management/performance/](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/performance) performance-vs-capacity, realms-and-layers, kpi-vs-sla; [Noisy neighbour: limit, reservation and share per resource](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/foundations/noisy-neighbour.md)); 20 challenges to the author, Q065-Q084; Q065-Q071 and Q073-Q082 answered and applied; open: Q072, Q083-Q085. `python3 project/tools/answered.py` lists answered open questions, multi-line answers included. Next: Capacity Management, then Your Private Cloud (SLA, SP5 framework), then Configuration Management.
- Author input: Q060 (VM slow triage order), Q061 (capacity decision order), Q062 (health check), Q063 (Book Part 1, VCF Operations chapters), Q064 (review order); Q065-Q084 (Part 1, Performance Management); all other open author questions.
- VCF Operations: map its objects, engines and metric groups; fetch the VCF Operations 9.1 metric reference from TechDocs into the catalog.
- Stubs: fill from the book, or fold into the family file, the 8 files under 60 words (review, section 2), then the rest under 120 words.
- Flows: a Mermaid diagram for each of the 11 flows without one; the author's draw.io flows converted where they exist. New flows after Q060-Q062.
- `## Traps` in the 6 metric files that lack it; then lint requires it.
- Performance Best Practices 9.1 (revision 20260624), still to read: p. 19 network hardware; p. 46 Enhanced Data Path and traffic shaping; pp. 39-45 storage; pp. 66-75 vCenter, vMotion, Storage vMotion; pp. 82-95 Storage DRS, HA, FT, vSAN, Lifecycle Manager, content library, Kubernetes (only what the knowledge base needs); p. 59 guest memory (2 MB pages). KB 316514 (Retreat Mode), KB 55806 (scheduler options).
- Re-check against 9.1: [Side-channel vulnerabilities and the ESX scheduler](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/configuration/side-channel-scheduling.md) (written from 9.0); shorten [vSphere Cluster Services (vCLS)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/concepts/vcls.md) to the 9.1 status (official release notes, not third-party).
- Open points to verify: power policy name ("Maximum performance" vs "High Performance"); Hyper-Threading penalties (37.5% VM, 50% ESXi) need author confirmation; `numPCPUs` in the dense-mode trigger; KB number for the ESXi CPU Usage 100% cap; memory reservation headroom percentage; Predictive DRS and DPM requirements in VCF Operations terms.
- Capacity model: split the vSphere cluster part out of [Capacity model: total, usable, buffer, projection](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/capacity/capacity-model.md) if it is not cross-product.
- Catalog: rows without a knowledge file (cluster and resource pool memory, datastore space, DPU charts); counter group of the per-host and per-VM-disk datastore charts (vSphere API reference); esxtop fields mapped to the `vsphere/tools/esxtop/` files; `interval` and `instance` of each band after Q048.
- Tags assigned during migration (pillar, object, metric_class) to be reviewed by the author; `metric_class` of Wait, Idle, Swapped, Swap Used, Ballooned to confirm.
- Book corrections for the author's next edition (P-states vs Turbo; idle frequency below base; wait sub-questions): strings in [project/archive/todo-2026-11-06.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/archive/todo-2026-11-06.md), section Open points from book extraction.
- Field heuristics not written in the books: through author questions and real tickets (M2).
- Later: the author's "My Recommendation" column in [CPU frequency, Turbo and their impact on a VM](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/concepts/cpu-frequency.md); book terminology for the glossary.

### M2 Questions
- 10 more questions: 1 at Level 200, 9 at Level 300, in the tasks below allocation (decide-capacity, troubleshoot, judge-setting, explain-mechanism).
- Author: files for L4-26 to L4-49; Q058 (synthetic share, review of L4-14 to L4-50); real-ticket questions written by the author, the held-out set cut from them.
- `trap_type` in question metadata and a coverage script for the blueprint counts.
- Split `L4-05` (two hosts, letters per host) into one deterministic question per host.
- Question ideas from the book chapters (CPU, Windows, memory traps): [project/archive/todo-2026-11-06.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/archive/todo-2026-11-06.md), section Evaluation.
- Per-question answer length in the runner (the long question L4-50 has 10 key points; the open-answer prompt caps at 250 words).
- Table input: a harness table tool (load Excel or CSV, filter, sort, aggregate, top-N) and table attachments in the runner.

### M3 Retrieval
- Done 2026-11-06 (the three fixes of the review, section 3.2), keyword search, 90 questions: baseline 70% of needed files in the classic context, 50 of 90 complete.
  - `expand_derive` (internal_derive of the top hits): 71%, 52 of 90. On.
  - `route_diagnosis` (troubleshooting question gets its flow first): 71%, 51 of 90. On.
  - `query_expansion` (glossary synonyms): no change; the glossary has 2 synonym rows. Implemented, off.
  - Together: 73%, 53 of 90. With hybrid search (embeddings): 72% to 75%, 51 to 57 of 90.
- 2026-11-06, Part 1 Performance Management added (4 files): classic context 76%, 57 to 56 of 90 complete. Gained 0019 and 0024; lost 0023 (ballooned file pushed out by performance-vs-capacity) and 0080 (capacity-model pushed out by noisy-neighbour, which covers thin provisioning). Kept: the new files hold the right ideas for both.
- Next, measured the same way:
  - Context budget: 12K gives 75% (55 of 90), 16K gives 76% (57 of 90). 16K still fits the 32K window with images and the answer; decide with the author, because it changes every classic run.
  - The query "VM CPU Ready: rollup, unit and statistics level" does not return the VM CPU Ready file in the top 6; vcenter-statistics and distributed-switch files rank first, and ranking shifts when files are added. Look at chunk scoring and the file-level aggregation.
  - Query understanding: map counter names, chart labels and esxtop fields in the question to their files through the catalog.
  - A larger local embedding model (hybrid adds 1 point over keyword search).
  - Re-ranker: a local cross-encoder re-scores the top chunks after fusion (from the review of an external best-practice note, author, 2026-11-06). Targets the ranking misses above. Measured 2026-11-06 (bge-reranker-v2-m3, BM25 base 56 of 90 complete): replace top 30: 44; replace top 10: 52; fuse top 30: 51; fuse top 10: 56; question without options, top 20: 50 (replace), 52 (fuse). No gain: a general re-ranker does not know which file an expert needs (traps, mechanisms behind a metric). Off; code kept. Next: retry with hybrid search, or a re-ranker tuned on the synthetic set.
  - Synthetic retrieval-only set: about 5 questions per knowledge file, the key is the source file; no model, no judge, no author review. Catches ranking drift when files are added.

### M4 Gateway benchmark
- Run: 100 questions, 3 candidates and the frontier reference, baseline, classic and agentic, 5 runs; then the up-front blocks for the best candidate (`--primer`).
- After it: check `tools_used` and `verify_flags` against wrong answers; groundedness per answer: the judge marks each claim as supported or not by the sent context, so each wrong answer is sorted into knowledge, retrieval or model automatically; budget test (answers that hit 8 calls re-run with 16); primed agentic start; concurrency 16 if errors stay at 0.
- Delete the old results (`benchmark/results/20261103-*`) once the 100 questions are complete.
- Watch for a current-generation dense vision model of about 70B: first challenger when it exists.

### M5 Live test
- The code changes in [benchmark/live-test.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/live-test.md), section 4: `--local` server, vision and context from config, judge later, timings per turn.
- Constrained final line: grammar-guided decoding (vLLM, llama.cpp) for the `ANSWER:` line only, reasoning left free; would replace the repair turn.
- Measure seconds per model turn on the target GPU; set the time limit from the operator session.

### M6 Release 1.0
- Every knowledge file `status: reviewed`; remove the draft rule from the answer prompt.
- The app calls `harness/` (retrieval, tools, prompt, verifier) with the benchmarked embedding model; prompt version, settings, model and index version stored with every answer.
- Rate and flag every answer with a cause; offline bundle import; local viewer as the default source link; guided troubleshooting shows step and branch.
- Benchmark question idea from the demo: "most important CPU metrics on an ESXi host" (trap: utilization and load average first).
