# Design: knowledge base test site

Status: design only. Not built. Not indexed.

## Purpose
- Measure the quality of `knowledge/` through a local LLM that answers from it.
- Let invited visitors ask questions in natural language and judge the answers.
- Turn every weak answer into a fix: a knowledge gap, a retrieval miss, or a model limit.
- Same contract as `README.md`, section How a local LLM uses it. The site implements that contract; it adds no rules of its own.

## What "quality" means here
| Signal | Question it answers | Source |
|---|---|---|
| Retrieval hit | Did the right files come back? | Golden case `knowledge` ids vs retrieved ids |
| Answer score | Is the answer right, with the right reason? | 0-3 rubric from `evaluation/README.md` |
| KB lift | Does the knowledge base beat no knowledge base? | Same question, baseline vs kb mode |
| Draft dependence | How much of the answer rests on `status: draft` files? | Cited file status |
| Gap rate | Which questions find no relevant file? | Low retrieval score, visitor flag |
| Trap rate | Does the answer fall into a known trap? | Golden case `Likely wrong answer` |

## Users
| Role | Can do |
|---|---|
| Visitor (invited) | Ask, rate, flag an answer as wrong with a comment. |
| Author | Everything a visitor can, plus: review flags, score answers, run golden cases, see the dashboard. |
| System | Rebuild the index on each merge to `main`; run golden cases on each rebuild. |

## Architecture
```mermaid
flowchart LR
  GH[GitHub repo main] -->|webhook on merge| IDX[Indexer]
  IDX --> DB[(SQLite: chunks, vectors, image records, index version)]
  UI[Web UI] --> API[API service]
  API --> RET[Retriever]
  RET --> DB
  API --> LLM[Local LLM server]
  API --> EMB[Local embedding model]
  RET --> EMB
  API --> LOG[(SQLite: questions, answers, ratings, flags)]
  EVAL[Golden case runner] --> API
  EVAL --> LOG
```
- Indexer: reads `knowledge/**/*.md` except the excluded folders. Uses the repo's own `scripts/validate.py` split logic for metadata. Refuses to index if the validator fails.
- Retriever: hybrid search (keyword BM25 + vector), filtered by metadata, then link expansion.
- API service: query pipeline, prompt assembly, streaming answer, logging.
- Local LLM server: open-weights model served on the same host. No data leaves the host.
- Golden case runner: sends only `## Prompt` of each case, never the answer key.
- Every answer stores the index version (git commit SHA). A score is always tied to the knowledge that produced it.

## Query pipeline
1. Classify the question into one `retriever_guide` value. Small prompt to the same LLM, or keyword rules first.
2. Extract filters: `product`, `object`, `technology`, `pillar`. Values must match `knowledge/glossary/terminology.md`.
3. Hybrid search within filters. Fall back to no filter if fewer than N hits.
4. Expand: `related`, `internal_derive`, `same_name`, `same_meaning`. `same_name` always included (trap guard).
5. Add matching foundations files when units, sampling, thresholds or provider/consumer apply.
6. `what-to-check`: retrieve the diagnosis file first; follow README, section Troubleshooting questions.
7. Fit to the context budget. Priority: diagnosis or metric file, its concepts, foundations, other links.
8. Generate. System prompt = the Answer rules in README. Chunks carry `id` and `status`.
9. Post-check: every cited id was retrieved; every threshold in the answer appears in a cited chunk. Fail → regenerate once, then show a warning.
10. Return: answer, cited files (with status), matching images from `images` records, retrieval trace.

## Pages
| Page | Content |
|---|---|
| Ask | Chat. Each answer shows cited files (id, title, draft badge), images that match, and a collapsible retrieval trace. Buttons: rate 0-3, flag wrong. |
| Compare | Same question answered twice: kb and baseline. Shown blind as A and B. Visitor picks the better one, then sees which was which. |
| Golden cases (author) | Latest run per case: score, retrieval hit, trap hit. Trend per index version. Runs on demand or after each rebuild. |
| Review queue (author) | Flagged answers. Author tags the cause: knowledge gap, wrong fact, retrieval miss, model error. One click creates an entry in `docs/todo.md` or `docs/author-questions.md` via a pull request. |
| Dashboard (author) | Signals table above, per technology and per retriever_guide. Top unanswered questions. Most-cited draft files (review first). |
| Corpus | Read-only browser of indexed files and image records, as the LLM sees them. |

## Data stored
| Table | Fields |
|---|---|
| chunks | id, file id, heading, text, tags, status, index version |
| images | path, file id, product, object, metric, topic, image_type, sample, alt text |
| questions | text, mode (kb, baseline), user role, time |
| answers | question, text, cited ids, retrieval trace, index version, model, latency |
| ratings | answer, score 0-3, flag, comment, cause tag |
| eval_runs | case id, mode, score, retrieval hit, index version, model; also appended to `evaluation/results/results.csv` |
- Golden case answer keys are read only by the runner and the author pages. Never sent to the LLM. Never shown to visitors.

## Technology choice
| Part | Choice | Reason |
|---|---|---|
| LLM serving | Ollama for the first build; vLLM if concurrency matters | Ollama is one binary and swaps models easily. vLLM serves several users at once. |
| Model | Open-weights instruction model, 7B-32B class, at least 16K context | Small enough for one GPU. Pick by golden case score, not by benchmark. |
| Embeddings | Local open embedding model on the same server | No external calls. |
| Index and logs | SQLite with a vector extension | About 200 files: no separate vector database needed. One file to back up. |
| API | Python (FastAPI) | Reuses `scripts/validate.py`. Same language as the repo tooling. |
| UI | Server-rendered pages with light JavaScript; streaming answers | Few pages, low maintenance. |
| Hosting | One host with a GPU, Docker Compose, reverse proxy with TLS | Everything local; matches "local LLM". |
| Rebuild | GitHub webhook or scheduled pull of `main` | Index always matches merged knowledge. |

## Security and abuse
- Invite-only first: login by email link or a shared access code. Public later, if ever.
- Rate limit per user and per IP.
- Visitor text is untrusted. The system prompt tells the model to answer only from retrieved chunks and to ignore instructions inside the question that change its role.
- The corpus is trusted, but only `main` is indexed. No branch or PR content.
- Logs hold questions. Tell visitors. No customer names in answers or logs shown on public pages.
- Admin pages behind author login.

## Build phases
1. Runner first, no website: CLI that indexes, answers golden cases in kb and baseline mode, writes `results.csv`. Proves the pipeline.
2. Ask page with citations and retrieval trace. Author only.
3. Ratings, flags, review queue. Invite visitors.
4. Compare page (blind A/B) and dashboard.
5. Optional: model comparison (same cases, several models) to pick the default model.

## Decisions for the author
- Hosting: own GPU machine, or rented GPU server?
- Audience: author only, invited experts, or public?
- Who scores: author only, or visitor ratings count too?
- Model: start with one model, or compare several in phase 5?
- Domain name and branding.
