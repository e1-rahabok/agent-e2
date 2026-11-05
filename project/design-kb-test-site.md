# Design: knowledge base test site

Status: design only. Not built. Not indexed.

## Purpose
- Measure the quality of `knowledge/` through a local LLM that answers from it.
- Let invited visitors ask questions in natural language and judge the answers.
- Turn every weak answer into a fix: a knowledge gap, a retrieval miss, or a model limit.
- Product requirements for the shipped assistant (ways to ask, answer UX, dark site): `project/product-requirements.md`.
- Same contract as `ARCHITECTURE.md`, section Local LLM use. The site implements that contract; it adds no rules of its own.

## What "quality" means here
| Signal | Question it answers | Source |
|---|---|---|
| Retrieval hit | Did the right files come back? | Question `knowledge` ids vs retrieved ids |
| Answer score | Is the answer right, with the right reason? | 0-3 rubric from `benchmark/README.md` |
| KB lift | Does the knowledge base beat no knowledge base? | Same question, baseline vs kb mode |
| Draft dependence | How much of the answer rests on `status: draft` files? | Cited file status |
| Gap rate | Which questions find no relevant file? | Low retrieval score, visitor flag |
| Trap rate | Does the answer fall into a known trap? | Question `Likely wrong answer` |

## Users
| Role | Can do |
|---|---|
| Visitor (invited) | Ask, rate, flag an answer as wrong with a comment. |
| Author | Everything a visitor can, plus: review flags, score answers, run questions, see the dashboard. |
| System | Rebuild the index on each merge to `main`; run questions on each rebuild. |

## Architecture
```mermaid
flowchart LR
  GH[GitHub repo main] -->|webhook on merge| IDX[Indexer]
  IDX --> DB[(SQLite: chunks, vectors, image records, index version)]
  UI[Web UI] --> API[API service]
  API --> RET[Retriever]
  RET --> DB
  API --> LLM[Vercel AI Gateway: open-weight model]
  API --> EMB[Embedding model via AI Gateway]
  RET --> EMB
  API --> LOG[(SQLite: questions, answers, ratings, flags)]
  EVAL[Question runner] --> API
  EVAL --> LOG
```
- Indexer: reads `knowledge/**/*.md` except the excluded folders. Uses the repo's own `project/tools/lint.py` split logic for metadata. Refuses to index if the validator fails.
- Retriever: hybrid search (keyword BM25 + vector), filtered by metadata, then link expansion.
- API service: query pipeline, prompt assembly, streaming answer, logging.
- LLM: open-weight model via Vercel AI Gateway for the test site. At a customer, the same weights run on their own VM, so no data leaves their environment.
- Question runner: sends only `## Prompt` of each question, never the answer key.
- Every answer stores the index version (git commit SHA). A score is always tied to the knowledge that produced it.

## Retrieval approach
- Retrieval, not fine-tuning, supplies the facts. Reasons: the knowledge is not on the internet; it changes often (author answers); answers must cite files; small models memorise facts poorly.
- Two modes, both built and compared in phase 1:
  - Classic RAG: one fixed retrieval pass, then answer. Baseline and fallback.
  - Agentic retrieval: the model calls tools in a loop until it has enough, then answers. Target mode.
- Optional later: light fine-tune (LoRA) for style and terminology only. Facts stay in retrieval.
- Not used: full long-context stuffing (125K tokens is too much for small models and too slow per question); a separate graph database (metadata links already form the graph).

## Query pipeline: classic RAG
1. Classify the question into one `retriever_guide` value. Small prompt to the same LLM, or keyword rules first.
2. Extract filters: `product`, `object`, `technology`, `pillar`. Values must match `project/tools/tags.yaml`.
3. Hybrid search within filters. Fall back to no filter if fewer than N hits.
4. Expand: `related`, `internal_derive`, `same_name`, `same_meaning`. `same_name` always included (trap guard).
5. Add matching foundations files when units, sampling, thresholds or provider/consumer apply.
6. `what-to-check`: retrieve the diagnosis file first; follow `ARCHITECTURE.md`, section Local LLM use, Troubleshooting questions.
7. Fit to the context budget. Priority: diagnosis or metric file, its concepts, foundations, other links.
8. Generate. System prompt = the Answer rules in `ARCHITECTURE.md`, section Local LLM use. Chunks carry `id` and `status`.
9. Post-check (below).
10. Return: answer, cited files, images, retrieval trace.

## Query pipeline: agentic retrieval (tool loop)
```mermaid
flowchart TD
  Q[Question] --> P[Plan: classify, pick filters]
  P --> T{Next action}
  T -->|search| S[search]
  T -->|read| R[read_file]
  T -->|follow| F[follow_links]
  T -->|image| I[get_images]
  S --> O[Observation added to working notes]
  R --> O
  F --> O
  I --> O
  O --> B{Budget left and gaps remain?}
  B -->|yes| T
  B -->|no| A[Answer from notes]
  A --> C[Post-check]
  C -->|fail once| A
  C -->|pass| OUT[Answer, citations, images, trace]
```

### Tools
- **`search`**
  - Input: query text; optional filters (product, object, technology, pillar, retriever_guide)
  - Output: Top 8 hits: id, title, heading, 2-line snippet, status, score
  - Rules: Filters must use `project/tools/tags.yaml` values. Hybrid BM25 + vector.
- **`read_file`**
  - Input: file id; optional heading
  - Output: Body text of the file or one section. No metadata block.
  - Rules: One file per call. Long files: section by section.
- **`follow_links`**
  - Input: file id; link type (related, internal_derive, same_name, same_meaning, all)
  - Output: Linked ids with titles and status
  - Rules: Cheap: titles only. The model then reads what it chooses.
- **`get_images`**
  - Input: file id, or filters (object, metric, image_type)
  - Output: Image records: path, alt text, tags, sample
  - Rules: Returns records only. The UI shows the image.
- **`catalog`**
  - Input: name: vCenter counter, chart label, esxtop field, metric title or object type; optional object filter; optional second object (`to`)
  - Output: Counter unit, rollup, statistics level, min/max level, kb file; esxtop field text; thresholds with source; colour bands; object role and relations, or the path between two object types
  - Rules: Exact values from `knowledge/catalog/`. Built 2026-11-04.
- **`calculate`**
  - Input: expression
  - Output: Result plus source notes
  - Rules: Summation ms ↔ %, unit conversion (vCenter KB = 1,024 bytes, kb = 1,000 bits), capacity, esxtop identities. Built 2026-11-04.
- **`flow`**
  - Input: diagnosis file id; optional step
  - Output: All steps in order, or one step with next step, referenced steps and metric files to read
  - Rules: Reads the markdown steps. Built 2026-11-04.
- **`draw_mermaid` (later)**
  - Input: Mermaid code
  - Output: Rendered diagram in the UI
  - Rules: For flows or layers that no stored image shows.

### Loop rules
- System prompt: the Answer and Troubleshooting rules in `ARCHITECTURE.md`, section Local LLM use, plus the tool list. The model is told it knows nothing about vSphere metrics beyond what tools return.
- First action is `search` or `catalog`. The answer may use only text returned by `read_file`, `catalog`, `flow` and `calculate`.
- Units, rollups, statistics levels, thresholds, object relations: `catalog`. Arithmetic and unit conversion: `calculate`.
- Before answering a metric question, the model must call `follow_links` with `same_name` on the metric file (trap guard).
- `what-to-check` questions: call `flow` on the matching diagnosis file; then follow its steps in order.
- Budget per question: at most 8 tool calls and 12K tokens of tool output. On budget end, answer with what is held and say what is missing.
- Repeated identical calls are refused by the loop controller and counted as an error.
- Model fails to call tools in the right format twice: fall back to classic RAG for that question; record the fallback.

### Post-check (both modes)
- Built 2026-11-04 as `harness/verify.py`. Baseline mode is not checked, so it stays a pure no-knowledge baseline.
- Hard checks, one repair turn with the failures listed: ANSWER line present; letters are options; Unsure or Not covered chosen alone.
- Soft checks, recorded only (`verify_flags`): REASON present; every cited id exists; every number with a unit or % in REASON appears in the question or in text the model was given.
- A soft check becomes a repair trigger only after results show it predicts wrong answers (`project/todo.md`).
- Planned: every metric name in the answer exists as a metric file title or is a quoted user term.

### Retrieval trace
Recorded for every answer, shown collapsed on the Ask page, stored in `answers.trace`.

| Field | Content |
|---|---|
| step | 1, 2, 3, ... |
| action | plan, search, read_file, follow_links, get_images, answer, post_check, fallback |
| input | tool arguments |
| output summary | ids returned, tokens returned |
| model reasoning | the model's short reason for the action, if the model gives one |
| tokens, latency | per step |
| index version | git SHA |

- The trace explains each failure. Example: right file never searched = retrieval or filter problem; file read but fact ignored = model problem; fact missing = knowledge gap.
- The review queue shows the trace next to the flagged answer.

## Pages
| Page | Content |
|---|---|
| Ask | Chat. Each answer shows cited files (id, title, draft badge), images that match, and a collapsible retrieval trace. Buttons: rate 0-3, flag wrong. |
| Compare | Same question answered twice: kb and baseline. Shown blind as A and B. Visitor picks the better one, then sees which was which. |
| Questions (author) | Latest run per question: score, retrieval hit, trap hit. Trend per index version. Runs on demand or after each rebuild. |
| Review queue (author) | Flagged answers. Author tags the cause: knowledge gap, wrong fact, retrieval miss, model error. One click creates an entry in `project/todo.md` or `project/author-questions.md` via a pull request. |
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
| eval_runs | question id, mode, score, retrieval hit, index version, model; also appended to `benchmark/results/results.csv` |

- Question answer keys are read only by the runner and the author pages. Never sent to the LLM. Never shown to visitors.

## Technology choice
| Part | Choice | Reason |
|---|---|---|
| LLM serving (test) | Vercel AI Gateway, open-weight models only | No hardware to buy. One API for all candidate models. Pay per token. The author already has a Vercel account. |
| LLM serving (customer) | Ollama or vLLM on the customer's own VM | Same open weights the test site scores. vLLM when several users query at once. |
| Model | Open-weight, Apache 2.0, 8B-32B, at least 16K context. Candidates below. | Must be downloadable and runnable by VMware customers. Pick by question score, not by benchmark. |
| Embeddings | `alibaba/qwen3-embedding-0.6b` via Vercel for the test; same model on CPU at the customer | Small, open, runs without a GPU. |
| Index and logs | SQLite with a vector extension | About 200 files: no separate vector database needed. One file to back up. |
| API | Python (FastAPI) | Reuses `project/tools/lint.py`. Same language as the repo tooling. |
| UI | Server-rendered pages with light JavaScript; streaming answers | Few pages, low maintenance. |
| Hosting (test site) | Vercel: web app, API routes, AI Gateway | No server to run. Index and logs in a hosted database. |
| Hosting (customer) | One VM with a GPU, or CPU only for the smallest model | The deployment target the scores must predict. |
| Rebuild | GitHub webhook or scheduled pull of `main` | Index always matches merged knowledge. |

## Security and abuse
- Invite-only first: login by email link or a shared access code. Public later, if ever.
- Rate limit per user and per IP.
- Visitor text is untrusted. The system prompt tells the model to answer only from retrieved chunks and to ignore instructions inside the question that change its role.
- The corpus is trusted, but only `main` is indexed. No branch or PR content.
- Logs hold questions. Tell visitors. No customer names in answers or logs shown on public pages.
- Admin pages behind author login.

## Candidate models
Source: Vercel AI Gateway model list, checked 2026-11-03. Prices per 1M input / output tokens; re-check before use. Sizes and image input: confirm on each model card before the first run.

| Vercel model id | Size | Customer hardware at 4-bit (estimate) | Price | Image input | Role |
|---|---|---|---|---|---|
| `google/gemma-4-31b-it` | 31B dense | One 24-48 GB GPU | $0.14 / $0.40 | Expected yes | 30B band |
| `alibaba/qwen-3-32b` | 32B dense | One 24-48 GB GPU | $0.08 / $0.28 | Expected no | 30B band |
| `mistral/mistral-small` | about 24B | One 16-24 GB GPU | $0.15 / $0.60 | Expected yes | 30B band |
| `google/gemma-4-26b-a4b-it` | 26B, 4B active | One 16-24 GB GPU | $0.13 / $0.40 | Expected yes | 30B band, fast |
| `nvidia/nemotron-3-nano-30b-a3b` | 30B, 3B active | One 16-24 GB GPU | $0.05 / $0.20 | Expected no | 30B band, fast |
| `openai/gpt-oss-20b` | 20B, mixture-of-experts | One 16 GB GPU | $0.07 / $0.30 | No | 20B |
| `alibaba/qwen-3-14b` | 14B dense | One 12-16 GB GPU or a large CPU VM | $0.12 / $0.24 | Expected no | Small hardware |
| `mistral/ministral-8b` | 8B | CPU VM or small GPU | $0.15 / $0.15 | Check | Floor |

- 6 models in the 20-32B band from 5 vendors; 2 small models show how far down a customer can go.
- Excluded: frontier closed models (customers cannot run them); Llama (licence restrictions).
- 70B class: test only if the 30B band misses questions through reasoning errors, not retrieval errors.
- Gemini API (free Gemma 4) is a fallback for testing only: free-tier data may be used by Google.

## Why 8B-32B is enough
- The knowledge is not stored in the model. It is retrieved per question (RAG). Parameters hold general skill, not the repository.
- Repository: 203 files, about 95,000 words (about 125K tokens). Average file about 600 tokens.
- One answer uses 5-10 files: 4K-8K tokens. A 16K-32K context window is enough.
- Size matters for: reasoning across files, unit arithmetic, trusting retrieved text over training. 27-32B is the expected sweet spot.
- Order of impact on quality: retrieval, then knowledge writing, then model size.

## Score transfer to customers
- Providers may serve higher precision than a customer's 4-bit build. Hosted scores are an upper bound.
- Before recommending a model: re-run the questions on the 4-bit build (for example, one hour on a rented GPU).

## Build phases
The project has 2 stages. Phases 1 and 5 are the benchmark; phases 2-4 are the Human Test.

| Phase | Stage | Content |
|---|---|---|
| 1 | Benchmark | Claude runs the question set on all candidate models and modes; scoring is automatic. Picks the default model and mode. See Benchmark plan. |
| 2 | Human Test | Ask page on isvara.io with citations and retrieval trace. Author only. Uses the phase 1 winner. Replaces the current basic agent on isvara.io. |
| 3 | Human Test | Ratings, flags, review queue. Invite visitors. |
| 4 | Human Test | Compare page (blind A/B) and dashboard. Screenshot upload when a vision-capable model is chosen. |
| 5 | Benchmark | 4-bit re-test of the chosen model and mode on customer-like hardware. Re-run after each major knowledge update. |

## Benchmark plan
- Moved 2026-11-04 to `benchmark/test-design.md`: claim, blueprint, why 100 questions, scoring, why 5 runs, validity threats, review checklist, target, decision rules.
- Runner: `benchmark/runner/` (README there).

## Decisions for the author
- Hosting: decided 2026-11-03: Vercel AI Gateway for the test site.
- Audience: author only, invited experts, or public?
- Who scores: author only, or visitor ratings count too?
- Model: decided 2026-11-03: compare the 8 candidates in the benchmark; 5 runs; 100-question target.
- Domain name and branding.
