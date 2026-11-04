# Harness

The software around the model. It turns a question into a grounded answer. Not indexed. Design: `project/solution-design.md`, sections 2 and 6.

| File | Job |
|---|---|
| `kb.py` | Load `knowledge/`: metadata split off, body chunked by `##` heading, chunks prefixed with title and id. |
| `retrieval.py` | Hybrid search (BM25 + embeddings, reciprocal rank fusion), metadata filters, link expansion (`same_name`, `related`). |
| `catalog.py` | Metric catalog: `knowledge/catalog/*.yaml` plus metric-file metadata, compiled to an in-memory SQLite database. Lookups by counter, chart label, esxtop field or title; thresholds; colour bands read from the knowledge files; object relations and paths. |
| `calc.py` | Calculator: safe arithmetic plus domain functions (summation ms ↔ %, unit conversion with vCenter KB/kb rules, CPU capacity, esxtop state sums). Each function returns a note naming its source. |
| `flows.py` | Flow executor: diagnosis files served as ordered steps, one step at a time, with the next step and the steps a step refers to. Reads the markdown directly; no second copy of the flow. |
| `verify.py` | Answer verifier. Hard issues (no ANSWER line, letters that are not options, Unsure or Not covered mixed with other letters) get one repair turn. Soft issues (no REASON, unknown file id, a number with a unit that the model was never shown) are recorded only. |
| `modes.py` | Answer modes: baseline (no knowledge base, no verifier), classic (one lookup; context starts with catalog facts for the files it holds), agentic (tool loop: search, read_file, follow_links, get_images, catalog, calculate, flow). Prompts and answer format. |
| `llm.py` | Model client: Vercel AI Gateway for testing (OpenAI-compatible API); a local OpenAI-compatible server (vLLM, llama.cpp) for deployment. `MockClient` exercises the tool loop offline. |
| `test_tools.py` | Unit tests: `python3 -m unittest harness/test_tools.py` from the repository root. |

## Agentic tools
| Tool | Returns | Use |
|---|---|---|
| search | File ids, titles, snippets | Always first (or catalog). |
| read_file | One file or one section | The only source of prose facts. |
| follow_links | Linked files by type | `same_name` before answering about a metric. |
| get_images | Image records of a file | Diagrams and charts. |
| catalog | Counter unit, rollup, statistics level, esxtop field, thresholds with source, object relations | Exact values; never depends on retrieval rank. |
| calculate | Result plus source notes | Any arithmetic or unit conversion. |
| flow | Steps of a diagnosis file, or one step with next and references | Troubleshooting questions. |

## Config keys (`benchmark/runner/config.yaml`)
- `verify` (default true): run the verifier in classic and agentic modes.
- `catalog_facts` (default true): put catalog facts at the top of the classic context.

## Notes
- `.cache/` holds embedding vectors (not in git). The catalog is rebuilt in memory at each start (under a second).
- Used by `benchmark/runner/run.py`, so the tested system is the shipped system. The runner records `tools_used`, `verify_flags` and `repaired` per answer.
- Soft verifier issues do not change answers yet. Promote one to a repair trigger only when results show it predicts wrong answers.
