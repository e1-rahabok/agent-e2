# Harness

The software around the model. It turns a question into a grounded, checked answer. Not indexed.
Why the system can win: [MISSION.md](../MISSION.md). How one question flows through it: [ARCHITECTURE.md](../ARCHITECTURE.md). The agent it hosts: [AGENT.md](AGENT.md).

## 1. What it is for
A small model alone fails at Level 400 in predictable ways. Each part of the harness takes one of those jobs away from the model, so the model only has to read and reason.

| Failure of a model alone | Harness part | What it does instead |
|---|---|---|
| Does not know the Level 400 fact | Retrieval (`retrieval.py`, `kb.py`) | Finds the knowledge file, then its linked traps and mechanisms |
| Reads one meaning of a label that has two | Link expansion (`retrieval.py`) | Brings the `same_name` file on the other object with the first |
| Gets a unit, rollup, statistics level or threshold wrong | Catalog (`catalog.py`) | Returns the exact value from the vSphere 9.1 tables, with its source |
| Slips on arithmetic | Calculator (`calc.py`) | Computes the conversion and names the rule's source file |
| Skips troubleshooting steps | Flow executor (`flows.py`) | Serves the diagnosis steps in order, one at a time |
| Answers in a broken format or guesses | Verifier (`verify.py`) | Rejects letters that are not options, Unsure mixed with others; one repair turn |
| Answers from memory, or loops | Agent rules and budgets (`agent.py`, `AGENT.md`) | Lookup first, no repeats, same-name check, call and token budgets |

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
- `flows.py` reads the numbered steps of each `diagnosis/` file directly; there is no second copy.
- So the harness knows the content by structure: ids, headings, tags, links and catalog rows. What the agent is told about it: `AGENT.md`, section 3. How the agent finds files: `AGENT.md`, section 3. How the knowledge is shaped for this: `KNOWLEDGE-ENGINEERING.md`, Part B. Full ingest, query and answer contract: `ARCHITECTURE.md`, section Local LLM use.

## 4. Modules
| File | Job |
|---|---|
| `kb.py` | Load `knowledge/`: metadata split off, body chunked by `##` heading, chunks prefixed with title and id. |
| `retrieval.py` | Hybrid search (BM25 + embeddings, reciprocal rank fusion), metadata filters, link expansion (`same_name`, `related`). |
| `catalog.py` | Metric catalog in SQLite: lookups by counter, chart label, esxtop field or title; chart and API units; thresholds; colour bands; object relations and paths. |
| `calc.py` | Safe arithmetic plus domain functions (summation ms ↔ %, units with vCenter KB/kb rules, CPU capacity, esxtop state sums). Each result names its source. |
| `flows.py` | Flow executor: a diagnosis file as ordered steps, one at a time, with the next step and the steps it refers to. |
| `verify.py` | Hard issues (no ANSWER line, letters that are not options, Unsure mixed with others) get one repair turn. Soft issues (no REASON, unknown file id, an ungrounded number) are recorded only. |
| `modes.py` | Answer modes and prompts: baseline (model alone), classic (one lookup); agentic is handed to `agent.py`. |
| `agent.py` | The agent loop: tools, rules (lookup first, no repeats, same-name check), budgets, fallback, verifier. Design: `AGENT.md`. |
| `primer.py` | The agent's five up-front blocks, generated from the knowledge base; switches `agent_primer` in the config. |
| `llm.py` | Model client: Vercel AI Gateway for the benchmark; a local OpenAI-compatible server (vLLM, llama.cpp) at the site. `MockClient` runs the loop offline. |
| `test_tools.py` | Unit tests: `python3 -m unittest harness/test_tools.py` from the repository root. |

## 5. Agentic tools
| Tool | Returns | Use |
|---|---|---|
| search | File ids, titles, snippets | Always first (or catalog). |
| read_file | One file or one section | The only source of prose facts. |
| follow_links | Linked files by type | `same_name` before answering about a metric. |
| get_images | Image records of a file | Diagrams and charts. |
| catalog | Counter unit, rollup, statistics level, esxtop field, thresholds with source, object relations | Exact values; never depends on retrieval rank. |
| calculate | Result plus source notes | Any arithmetic or unit conversion. |
| flow | Steps of a diagnosis file, or one step with next and references | Troubleshooting questions. |

## 6. Settings and checks
- Settings live in `benchmark/runner/config.yaml`: `verify` (default true), `catalog_facts` (default true: catalog facts at the top of the classic context), `classic_k`, `context_tokens`, `expand_derive`, `route_diagnosis`, `query_expansion`, `agent_max_calls`, `agent_tool_tokens`, `context_window`, `image_tokens`, `agent_primer` (one switch per up-front block). Each retrieval switch carries its measured effect in the config comment.
- `.cache/` holds embedding vectors (not in git). The catalog is rebuilt in memory at each start (under a second).
- Tools: `python3 -m unittest harness/test_tools.py`. Retrieval without a model: `python3 benchmark/runner/retrieval_eval.py`. Whole system: `benchmark/runner/README.md`.
- The runner records `tools_used`, `verify_flags` and `repaired` per answer. A soft verifier issue becomes a repair trigger only when results show it predicts wrong answers.

## 7. Planned
- `draw_mermaid` tool: render a flow or layer diagram that no stored image shows.
- Verifier: every metric name in an answer exists as a metric file title or is a quoted user term.
- Question understanding before search (question type, object, layer as filters) and query rewriting with glossary synonyms: `ARCHITECTURE.md`, section Status.
