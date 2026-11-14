# Harness

The software around the model: the tools, guards and model client the agent runs on. Together with the agent it turns a question into a grounded, checked answer: a neuro-symbolic expert system ([AGENT.md](AGENT.md)). Not indexed.
Why the system can win: [MISSION.md](../MISSION.md). How one question flows through it: [ARCHITECTURE.md](../ARCHITECTURE.md). The agent it hosts: [AGENT.md](AGENT.md).

## 1. What it is for
A small model alone fails at Level 400 in predictable ways. Each part of the harness takes one of those jobs away from the model, so the model only has to read and reason.

| Failure of a model alone | Harness part | What it does instead |
|---|---|---|
| Does not know the Level 400 fact, nor which file holds it | Reading plan (`planner.py`), retrieval (`retrieval.py`, `kb.py`) | Code chooses the files: those the question names, search hits, their mechanism links, one search per claim |
| Reads one meaning of a label that has two | Link expansion (`retrieval.py`) | Brings the `same_name` file on the other object with the first |
| Gets a unit, rollup, statistics level or threshold wrong | Catalog (`catalog.py`) | Returns the exact value from the vSphere 9.1 tables, with its source |
| Slips on arithmetic | Calculator (`calc.py`) | Computes the conversion and names the rule's source file |
| Slips on a multi-step capacity plan | Planning calculator (`capacity.py`) | Six numbers per host (3 models × CPU and memory), the binding one, HA hosts on top; class defaults from the catalog |
| Skips troubleshooting steps | Flow file read whole (tier 1 of the plan); flow executor (`flows.py`) | Serves the steps in order; executable steps (Q166) to build |
| Answers in a broken format or guesses | Verifier (`verify.py`) | Rejects letters that are not options, Unsure mixed with others; one repair turn |
| Answers from memory | The agent (`agent.py`, `AGENT.md`) | The model answers only with the reading set and the computed facts in front of it; the knowledge base wins |

## 2. Design rules
- Code does what can be exact: search, lookup, arithmetic, step order, format checks. The model does only what needs language.
- The knowledge base is the source of truth; the harness never adds facts of its own.
- One harness for benchmark and deployment, so the benchmarked system is the shipped system. Only the model endpoint differs (`llm.py`).
- Every tool returns its source, so the answer can cite it and a reviewer can check it.
- The harness depends on `knowledge/` only. Nothing in `benchmark/` or `project/` is read at run time.

## 3. How it knows the knowledge base
- At start, `kb.py` loads every indexed file: the metadata block becomes filter fields and links; the body is chunked by `##` heading, each chunk prefixed with the file title and id.
- `retrieval.py` builds a keyword index (BM25) and an embedding index over the chunks, fused by rank, with metadata filters and link expansion.
- `catalog.py` compiles `knowledge/catalog/*.yaml` and the colour bands in the KPI files into an in-memory SQLite database.
- `flows.py` reads the numbered steps of each health-check, troubleshooting and decision-tree file (its `retriever_guide`, wherever it sits) directly; there is no second copy.
- So the harness knows the content by structure: ids, headings, tags, links and catalog rows. How the agent plans with it: `AGENT.md`, section 4.2. How the knowledge is shaped for this: [`KNOWLEDGE-ENGINEERING.md`](../KNOWLEDGE-ENGINEERING.md) and its rule modules in [`project/knowledge-rules/`](../project/knowledge-rules). Full ingest, query and answer contract: [`ARCHITECTURE.md`](../ARCHITECTURE.md), section Local LLM use.

## 4. Modules
| File | Job |
|---|---|
| `kb.py` | Load `knowledge/`: metadata split off, body chunked by `##` heading, chunks prefixed with title and id. |
| `retrieval.py` | Hybrid search (BM25 + embeddings, reciprocal rank fusion), metadata filters, links of a file by type. |
| `catalog.py` | Metric catalog in SQLite: lookups by counter, chart label, esxtop field or title; chart and API units; thresholds; colour bands; object relations and paths. |
| `calc.py` | Safe arithmetic plus domain functions (summation ms ↔ %, units with vCenter KB/kb rules, CPU capacity, esxtop state sums). Each result names its source. |
| `capacity.py` | Planning calculator (`capacity.plan`; not yet wired into the agent, `AGENT.md` section 7): how many VMs of a class fit per host, or how full a host or cluster is for a VM mix. Allocation, reservation and utilization × CPU and memory; defaults are catalog rows `planning-*`. Method: [`sp5-framework/capacity/class-of-service-planning`](../knowledge/sp5-framework/capacity/class-of-service-planning.md), section Planning calculator. |
| `web.py` | Public web knowledge: URLs in the question read before the model starts; search only for current facts (a pattern list); system names dropped from queries; private addresses refused; pages trimmed and labelled untrusted. Config key `web`. |
| `flows.py` | Flow executor: a health check, troubleshooting or decision-tree file as ordered steps, one at a time, with the next step and the steps it refers to. Today read by lint (every flow parses) and the unit tests; not called by the agent until executable steps (Q166). |
| `verify.py` | Hard issues (no ANSWER line, letters that are not options, Unsure mixed with others) get one repair turn. Soft issues (no REASON, unknown file id, an ungrounded number) are recorded only. |
| `planner.py` | Stage 2, the reading plan (`AGENT.md`, section 4.2): named files, search, mechanism links, one search per claim, packed by tier with best sections. Also read by the retrieval check. |
| `agent.py` | The agent: stages 1 and 3-6 (case, compute, ask, answer, check). Design: `AGENT.md`. |
| `modes.py` | Entry point `answer(mode, ...)`: `agent-e2` (the agent), and the benchmark references `baseline` (the model alone) and `web` (the model alone with web search); prompts; verifier repair; consensus on one reading set; the conversation (`converse`). |
| `clarify.py` | One clarifying round: the `chat` and `chat_final` prompt rules, `CLARIFY:` parsing; the conversation runs through `modes.converse`. |
| `terms.py` | The user's words matched against [`knowledge/catalog/user-terms.yaml`](../knowledge/catalog/user-terms.yaml): knowledge-base terms for the query, files for tier 2, a note per misconception. Switch `term_map`. |
| `primer.py` | Up-front blocks of the answer prompt (misconceptions, confusable pairs), generated from the knowledge base; switch `primer` in the config. |
| `llm.py` | Model client: Vercel AI Gateway for the benchmark; a local OpenAI-compatible server (vLLM, llama.cpp) at the site. `deterministic` calls (the case) run at temperature 0. `MockClient` runs offline. |
| `test_tools.py` | Unit tests: `python3 -m unittest harness/test_tools.py` from the repository root. |

## 5. Tools
The agent's code calls them; the model calls none (`AGENT.md`, section 1).

| Tool | Returns | Called in |
|---|---|---|
| `retrieval.search`, `retrieval.links` | File ids and best chunks; linked files by type | Stage 2, the reading plan |
| `catalog.lookup`, `catalog.facts_for` | Counter unit, rollup, statistics level, esxtop field, thresholds with source, KPI levels, object relations | Stage 1 (names of the case), stage 2 (counter keys), the reading set's catalog facts |
| `calc.evaluate` | Result plus source notes | Stage 3, summation conversions |
| `capacity.plan` | VMs per host, or how full a host or cluster is for a planned VM mix | To wire into stage 3 |
| `flows.run` | Steps of a flow file, or one step with next and references | To wire into stage 3 with executable steps (Q166) |
| `web.gather`, `web.block` | Pages the question links, and vendor search results for current facts, trimmed and labelled untrusted | Stage 5, after the knowledge base text |

## 6. Settings and checks
- Settings live in [`benchmark/runner/config.yaml`](../benchmark/runner/config.yaml): `verify` and `catalog_facts` (not in the file: their defaults in code are true; `catalog_facts` puts catalog facts at the top of the reading set), `search_k`, `context_tokens`, `plan_section_tokens`, `plan_derive_n`, `plan_claims_max`, `term_map`, `term_map_files`, `case_model`, `case_max_tokens`, `gap_followup`, `query_expansion`, `consensus_samples`, `context_window`, `image_tokens`, `primer` (one switch per up-front block).
- `.cache/` holds embedding vectors (not in git). The catalog is rebuilt in memory at each start (under a second).
- Tools: `python3 -m unittest harness/test_tools.py`. Retrieval without a model: `python3 benchmark/runner/retrieval_eval.py`. Whole system: [`benchmark/runner/README.md`](../benchmark/runner/README.md).
- The runner records `tools_used`, `verify_flags` and `repaired` per answer. A soft verifier issue becomes a repair trigger only when results show it predicts wrong answers.

## 6a. Consensus
- Setting `consensus_samples` (n). Multiple-choice questions of Agent E2: the harness asks up to n answer samples on one reading set (stages 1-4 run once). The letters stand only when every sample gives the same set. A disagreement, an Unsure or an unreadable reply makes the answer Unsure, with the reason "not settled". It stops at the first disagreement, so a split costs 2 samples, not n.
- Code: `answer` and `_consensus` in [`modes.py`](modes.py). Baseline and web stay one sample: they measure the model alone. Open answers stay one sample: free text has no letters to compare.
- Why (previous generation, round of 2026-11-13, [`benchmark/results/analysis-2026-11-13.md`](../project/archive/benchmark-results-before-2026-11-14/analysis-2026-11-13.md)):
  - The confident-wrong rate was 19-30% in the knowledge base modes against a gate of 3%.
  - Unsure was chosen in only 1-6% of multiple-choice answers. The prompt rule "a wrong answer is worse than Unsure" does not make a 30B model abstain: it does not know what it does not know.
  - 55-75% of the confident-wrong multiple-choice answers were partly right, and the same question got different letters in different runs (luck 48-63%). Disagreement between samples is the signal the model cannot give about itself.
- Projected on the previous generation (n = 3, from its 5 recorded runs; archived analysis above): multiple-choice confident-wrong 10-22% fell to 0-4%, at about 5 points of final score; the most unstable model paid 14. The gate puts confident-wrong first ([`benchmark/design.md`](../benchmark/design.md), section 7.5). With one reading set shared by the samples, a disagreement now comes from the reasoning alone.
- What it does not fix: judged (open) answers. Their confident-wrong rate stays 31-41%, so the overall rate stays near 15%. Next lever: Q199 in [`project/author-questions.md`](../project/author-questions.md) and the analysis file above.
- Cost: up to n model passes per answer. On a local vLLM server the samples share the prompt cache and run as one batch, so latency rises little.
- Benchmark: keeps `consensus_samples: 1` and reads the projection in `report.md` (section Consensus of 3, projected). The projection is the exact mean over all draws of 3 of the 5 runs, so it costs no model call. The deployed profile sets 3.

## 7. Planned
- `draw_mermaid` tool: render a flow or layer diagram that no stored image shows.
- Verifier: every metric name in an answer exists as a metric file title or is a quoted user term.
- The rest of the agent's build order: [`AGENT.md`](AGENT.md), section 7.
