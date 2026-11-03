# Auto Test runner

Runs the golden multiple-choice questions against candidate open-weight models through Vercel AI Gateway, scores them automatically, and writes a report.
Design: `docs/design-kb-test-site.md`, section Auto Test plan. Not indexed.

## Setup
- Python 3.10+ with `pyyaml` and `requests`.
- Environment variable `AI_GATEWAY_API_KEY` (Vercel AI Gateway API key). Never commit it.
- Settings: `config.yaml` (models, modes, runs, temperature, budgets, provider pinning).

## Commands
```bash
python3 tools/autotest/run.py --dry-run
```
- Shows the matrix, the number of answers and a cost estimate. No API calls.

```bash
python3 tools/autotest/run.py --mock --runs 2
```
- Offline pipeline check: random answers, real retrieval, no API calls.

```bash
python3 tools/autotest/run.py --models openai/gpt-oss-20b --modes classic --runs 1 --cases cpu-004
```
- Smallest real test: one model, one mode, one question.

```bash
python3 tools/autotest/run.py
```
- Full matrix from `config.yaml`.

```bash
python3 tools/autotest/run.py --resume evaluation/results/autotest/<run-id>
```
- Continue a run; failed answers are retried.

## Methodology

### Question and score
- Each golden case is a multiple-choice question with one or more correct options.
- A run asks every question once, per model and mode.
- 5 runs per question, because hosted models do not answer the same way twice. Reason: `docs/design-kb-test-site.md`, section Why 5 runs.
- Exact: answer letters match the key exactly. 1 or 0 per answer.
- Model score for a run = Exact averaged over the questions, 0-100%.
- Model score in the report = the average of its 5 run scores. Column `Exact`.
- Partial: credit for each correct letter picked, minus wrong letters. Shows near misses on multi-answer questions.
- Majority: for each question, take the answer given most often over the 5 runs, then score it. Shows what the model answers "usually".
- Margin: 95% interval on Majority. Set by the number of questions: 17 questions gives about ±20-24 points.

### Modes: baseline, classic, agentic

| | Baseline | Classic | Agentic |
|---|---|---|---|
| Knowledge base | None | Yes | Yes |
| Who looks up | Nobody | The runner | The model |
| Lookups | 0 | 1, before the model starts | Up to `agent_max_calls` (8), chosen by the model |
| What the model gets | The question only | Top `classic_k` (6) files from one hybrid lookup, plus files linked by `same_name` and `related`, within `context_tokens` (8K) | What it asks for with tools `search`, `read_file`, `follow_links`, `get_images`, within `agent_tool_tokens` (12K) |
| Can it go back for more | - | No | Yes |
| What it measures | The model's own knowledge | What the knowledge base adds with no tool skill from the model | Whether the model can use the knowledge base fully |

- Classic = classic RAG (retrieval-augmented generation): retrieve once, then answer. The standard, older pattern. "Classic" is this test's label, not an industry term.
- Agentic is the target design. The knowledge base links (`same_name`, `related`, `internal_derive`), traps and diagnosis files exist so a model can follow a chain across files.
- Classic is the reference point for agentic: agentic should score at least as high, or the model is not using the tools well.
- The agentic limits (8 calls, 12K tokens) are cost caps for the test, not a design choice.
- Run 20261103-081849: agentic scored below classic for 7 of 8 small models. Cause: weak tool use (recall 0-50% vs 63% for classic; some models made almost no calls; one broke the answer format). A model problem, not a knowledge-base problem.

### Index version
- The knowledge base changes with every commit. A score is only meaningful next to the knowledge that produced it.
- Index version = the git commit SHA of the repository when the run started. Example: `de5f19e22860`.
- To see the exact knowledge files a run used: `git checkout <index version>`.
- Two runs with different index versions compare knowledge-base changes. Two runs with the same index version compare models or settings.
- The runner reads the files on disk but records the commit SHA. Commit all knowledge changes before a run, or the recorded version is wrong.

### Hybrid retrieval
- No internet access in any mode. Retrieval searches only the `knowledge/` files.
- In this test the models and the embedding model run in the cloud through Vercel AI Gateway, to compare candidates cheaply. In production the chosen model runs locally; the knowledge base lookup is the same.
- Retrieval = finding the knowledge-base sections to give the model. Used in classic and agentic modes.
- The knowledge files are cut into chunks, one per `##` heading.
- Two searches run on the same question:
  - Keyword search (BM25): scores chunks that share the question's words. Strong on exact terms: metric names, counter names such as %LAT_M.
  - Vector search (embeddings): an embedding model (`embedding_model` in `config.yaml`) turns each chunk and the question into vectors; nearest vectors score highest. Strong on meaning when the words differ, e.g. "VM waits for memory" vs "page-fault latency".
- Fusion: reciprocal rank fusion. Each chunk gets 1 / (60 + rank) from each list; the sums decide the order. A chunk ranked well by both searches comes first.
- Best chunk per file; top files go to the model (classic: `classic_k`, plus linked files).
- Hybrid = both searches fused. `bm25` in a report = embeddings were off or unavailable; keyword search only.
- Why hybrid: keyword search misses paraphrases; vector search misses rare exact terms. Fusing both is the common practice for technical text.

### Concurrency (speed)
- `concurrency` in `config.yaml` = requests sent to the gateway at the same time. Default 12.
- Cost does not change with concurrency: the same tokens are sent, only in parallel.
- Tested in run 20261103-081849:

| Concurrency | Answers per minute | Errors |
|---|---|---|
| 4 | about 25 | 0 (128 answers) |
| 12 | about 54 | 0 (2032 answers) |

- At 12, the full matrix (2160 answers) took about 38 minutes.
- Limit: a Claude Code cloud background command stops after 2 hours. `--resume` continues a stopped run; saved answers are kept.
- Ceiling: set by the model providers' rate limits behind the gateway, not by the runner. Not documented per model; find it by test.
- Above the ceiling, providers return HTTP 429. The runner retries 429, 408 and 5xx. Answers still failing are listed; `--resume` retries them.
- To test a higher value: `--concurrency 16` (or 20) on one run. Keep it if errors stay at 0 and answers per minute rise.
- Limits differ per model. anthropic/claude-opus-5.5 failed at 12 (HTTP 429 "No access to this model at this time"); 3 ran with 0 errors. Use `--concurrency 3` for frontier models.

### Temperature
- Temperature controls randomness in the model's word choice. 0 = always the most likely word. Higher = more varied.
- Set to 0.2 in `config.yaml`.
- Reasons:
  - Factual multiple-choice questions need stable answers, so temperature stays low.
  - 0 does not make hosted models deterministic (see Why 5 runs). The 5 runs measure the remaining variation either way.
  - Some reasoning models loop or repeat at 0. Their vendors advise against greedy decoding. A small value avoids this.
  - The test should match production: `config.yaml` says to use the value the website will use. The website value is not fixed yet; 0.2 is the working assumption.
- Fixed for a whole run. Comparing runs at different temperatures mixes two effects.
- The 0.2 choice is a design default, not a measured optimum. A temperature sweep (0, 0.2, 0.7) on the best model would test it.

## What it does
1. Loads `knowledge/` exactly as README, section How a local LLM uses it: metadata split off, body chunked by `##` heading.
2. Builds the index: BM25, plus embeddings (`embedding_model`) when the API key is set. Embeddings are cached in `tools/autotest/.cache/`.
3. Loads golden cases with `format: multiple-choice`. Other formats are listed as skipped.
4. For each model, mode, case and run:
   - shuffles the options (same order for every model and mode within a run) and appends "Not covered by the knowledge base";
   - answers in the mode:
     - `baseline`: no knowledge base;
     - `classic`: one search, link expansion (`same_name`, `related`), 8K-token context;
     - `agentic`: tool loop with `search`, `read_file`, `follow_links`, `get_images`; at most 8 calls and 12K tokens of tool output. Search first, no repeated calls, a same_name reminder. Falls back to classic after 2 tool-format errors;
   - parses `ANSWER:` and maps letters back;
   - scores exact match, partial credit, trap hit, Not-covered pick.
5. Questions with image attachments get a second `vision` track on models tagged `vision` on the gateway.
6. Writes the run folder and appends one summary row per model, mode and case to `evaluation/results/results.csv`.

## Output: `evaluation/results/autotest/<run-id>/`
| File | Content | In git |
|---|---|---|
| `config.json` | Index version (git SHA), models with tags and prices, settings | Yes |
| `answers.csv` | One row per answer: model, provider, mode, track, case, run, option order, letters, scores, retrieval recall, tool steps, tokens, latency, cost | Yes |
| `report.md` | Score matrix (exact, partial, majority, margin, consistency, trap, parse failures, recall, fallback, cost), by area and level, hardest questions | Yes |
| `traces.jsonl` | Full question and retrieval trace per answer | No (large); keep locally |

## Golden case fields used
| Field | Meaning |
|---|---|
| `format` | `multiple-choice` (auto-scored), `free-text` (judge or author), `compound` (scored by hand) |
| `level` | `recall`, `l400`, `multi-hop`, `screenshot` |
| `answer` | Correct option letters, as in `## Prompt` |
| `trap` | Option letters that are the known wrong answer |
| `knowledge` | Files the answer should come from; used for retrieval recall |
- Options in `## Prompt` are lines starting with `A. ` to `H. `. Text after the options (for example `Hint:`) is kept below them.
- The prompt text must stand alone without the image: the text track sends no image.
- `scripts/validate.py` checks these fields.

## Limits
- Provider name is recorded when the gateway returns it; the field is not documented as stable.
- Cost is estimated from gateway list prices in `/models`; check the Vercel invoice.
- Mock runs prove the pipeline only. Their scores are random.
