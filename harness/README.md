# Harness

The software around the model. It turns a question into a grounded answer. Not indexed. Design: `project/solution-design.md`, section 2.

| File | Job |
|---|---|
| `kb.py` | Load `knowledge/`: metadata split off, body chunked by `##` heading, chunks prefixed with title and id. |
| `retrieval.py` | Hybrid search (BM25 + embeddings, reciprocal rank fusion), metadata filters, link expansion (`same_name`, `related`). |
| `modes.py` | Answer modes: baseline (no knowledge base), classic (one lookup), agentic (model-driven tool loop: search, read_file, follow_links, get_images). Prompts and answer format. |
| `llm.py` | Model client: Vercel AI Gateway for testing (OpenAI-compatible API); a local OpenAI-compatible server (vLLM, llama.cpp) for deployment. |

- `.cache/` holds embedding vectors (not in git).
- Used by `benchmark/runner/run.py`, so the tested system is the shipped system.
- Planned: metric catalog lookup, calculator and unit tools, troubleshooting flow executor, answer verifier.
