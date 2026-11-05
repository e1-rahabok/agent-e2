# Benchmark runner

Runs every question (multiple choice, screenshot, free text) against the candidate open-weight models through Vercel AI Gateway, scores them automatically (letters, or a judge model for free text), and writes a report with one final score.
Design: `benchmark/design.md`. Models and judge: `benchmark/models.md`. Not indexed.

## Setup
- Python 3.10+ with `pyyaml` and `requests`.
- Environment variable `AI_GATEWAY_API_KEY` (Vercel AI Gateway API key). Never commit it.
- Settings: `config.yaml` (models, judge, modes, runs, temperature, budgets, provider pinning).

## Commands
```bash
python3 benchmark/runner/run.py --dry-run
```
- Shows the matrix, the number of answers and a cost estimate. No API calls.

```bash
python3 benchmark/runner/run.py --mock --runs 2
```
- Offline pipeline check: random answers, real retrieval, no API calls.

```bash
python3 benchmark/runner/run.py --models google/gemma-4-31b-it --modes classic --runs 1 --questions cpu-004
```
- Smallest real benchmark: one model, one mode, one question.

```bash
python3 benchmark/runner/run.py
```
- Full matrix from `config.yaml`.

```bash
python3 benchmark/runner/run.py --resume benchmark/results/<benchmark-id>
```
- Continue a benchmark; failed answers are retried.

```bash
python3 -m unittest benchmark/runner/test_runner.py
```
- Scoring tests: judge reply parsing, final score, question kinds. No API calls.

## Retrieval check (no model)
```bash
python3 benchmark/runner/retrieval_eval.py
```
- Recall of each question's `knowledge` files in search and in the classic context. Add `--embeddings` for hybrid search (needs `AI_GATEWAY_API_KEY`).

## Methodology

### Final score
- One number, 0-100%, per model and mode: the mean question credit over all questions. Sub-scores: by answer type (deterministic, judged), by input type (text, table, screenshot), by level (100-400). Report table `Final score`.
- Question credit = the worst of its runs: multiple choice 1 or 0 (Stable correct); free text the lowest judge score / 3.
- Full method: `benchmark/design.md`, section 7.4.

### Free text and the judge
- `answer_type: judged` questions are sent without options, with an open-answer prompt (`harness/modes.py`, `PROMPTS['open']`). The verifier does not run on them: it checks letters only.
- `judge.py` sends the prompt, images, `## Expected key points`, `## Likely wrong answer` and the answer to `judge_model`, and reads back a JSON score 0-3.
- The runner refuses a benchmark where the judge is also a candidate.
- Rubric and checks: `benchmark/design.md`, section 14. Report table `Free-text answers (judge)`.

### Screenshots
- Questions with image attachments are sent with all their images (track `vision`). There is no text-only track.
- The runner refuses a candidate without the gateway `vision` tag when screenshot questions are in the benchmark: reading screenshots is a basic requirement (`benchmark/models.md`).

### Multiple choice: question and score
- A multiple-choice question has one or more correct options.
- A run asks every question once, per model and mode.
- 5 runs per question, because hosted models do not answer the same way twice. Reason: `benchmark/design.md`, section 7.2.
- Every question says: "Choose all the correct options. There can be more than one." One option is appended: "Unsure". There is no "Not covered" option: the system answers from the knowledge base first and from the model's own knowledge where it is silent (author, Q038, 2026-11-05).
- Exact: answer letters match the key exactly. 1 or 0 per answer.
- Classes: correct (exact letters), Unsure (chosen alone), confident wrong (anything else, including unparseable). The model is told a wrong answer is worse than Unsure. No points: see `benchmark/design.md`, section 7.1.
- Stable correct: share of multiple-choice questions answered exactly right in all 5 runs. Report table `Multiple choice: luck-free scores`. It is the multiple-choice credit in the final score.
- Luck: share of questions right in some runs only. Counted as not known.
- Override (table `Final score`): share of knowledge base answers that state the trap although every needed file was in the context. Prior override, not a retrieval miss.
- Confident-wrong rate: share of answers that are wrong and not Unsure. Accuracy when answered: exact share among non-Unsure answers.
- Exact (mean over runs) is still reported in table `Scores`.
- Reason and design: `benchmark/design.md`, section 7.
- Partial: credit for each correct letter picked, minus wrong letters. Shows near misses on multi-answer questions.
- Majority: for each question, take the answer given most often over the 5 runs, then score it. Shows what the model answers "usually".
- Margin: 95% interval on Majority. Set by the number of questions: 17 questions gives about ±20-24 points.

### Modes: baseline, classic, agentic

| | Baseline | Classic | Agentic |
|---|---|---|---|
| Knowledge base | None | Yes | Yes |
| Who looks up | Nobody | The runner | The model |
| Lookups | 0 | 1, before the model starts | Up to `agent_max_calls` (8), chosen by the model |
| What the model gets | The prompt only | Catalog facts for the retrieved files, then the top `classic_k` (6) files from one hybrid lookup, plus files linked by `same_name` and `related`, within `context_tokens` (8K) | What it asks for with tools `search`, `read_file`, `follow_links`, `get_images`, `catalog`, `calculate`, `flow`, within `agent_tool_tokens` (12K) |
| Can it go back for more | - | No | Yes |
| What it measures | The model's own knowledge | What the knowledge base adds with no tool skill from the model | Whether the model can use the knowledge base fully |

- Classic = classic RAG (retrieval-augmented generation): retrieve once, then answer. The standard, older pattern. "Classic" is this benchmark's label, not an industry term.
- Agentic is the target design. The knowledge base links (`same_name`, `related`, `internal_derive`), traps and diagnosis files exist so a model can follow a chain across files.
- Classic and agentic answers pass the answer verifier (`harness/verify.py`): a missing ANSWER line, a letter that is not an option, or Unsure mixed with other letters gets one repair turn. Baseline is not verified.
- Classic is the reference point for agentic: agentic should score at least as high, or the model is not using the tools well.
- The agentic limits (8 calls, 12K tokens) are cost caps for the benchmark, not a design choice.
- Benchmark 20261103-081849: agentic scored below classic for 7 of 8 small models. Cause: weak tool use (recall 0-50% vs 63% for classic; some models made almost no calls; one broke the answer format). A model problem, not a knowledge-base problem.

### Index version
- The knowledge base changes with every commit. A score is only meaningful next to the knowledge that produced it.
- Index version = the git commit SHA of the repository when the benchmark started. Example: `de5f19e22860`.
- To see the exact knowledge files a benchmark used: `git checkout <index version>`.
- Two runs with different index versions compare knowledge-base changes. Two runs with the same index version compare models or settings.
- The runner reads the files on disk but records the commit SHA. Commit all knowledge changes before a benchmark, or the recorded version is wrong.

### Hybrid retrieval
- No internet access in any mode. Retrieval searches only the `knowledge/` files.
- In the benchmark the models and the embedding model run in the cloud through Vercel AI Gateway, to compare candidates cheaply. In production the chosen model runs locally; the knowledge base lookup is the same.
- Retrieval = finding the knowledge-base sections to give the model. Used in classic and agentic modes.
- The knowledge files are cut into chunks, one per `##` heading.
- Two searches run on the same prompt:
  - Keyword search (BM25): scores chunks that share the prompt's words. Strong on exact terms: metric names, counter names such as %LAT_M.
  - Vector search (embeddings): an embedding model (`embedding_model` in `config.yaml`) turns each chunk and the prompt into vectors; nearest vectors score highest. Strong on meaning when the words differ, e.g. "VM waits for memory" vs "page-fault latency".
- Fusion: reciprocal rank fusion. Each chunk gets 1 / (60 + rank) from each list; the sums decide the order. A chunk ranked well by both searches comes first.
- Best chunk per file; top files go to the model (classic: `classic_k`, plus linked files).
- Hybrid = both searches fused. `bm25` in a report = embeddings were off or unavailable; keyword search only.
- Why hybrid: keyword search misses paraphrases; vector search misses rare exact terms. Fusing both is the common practice for technical text.

### Concurrency (speed)
- `concurrency` in `config.yaml` = requests sent to the gateway at the same time. Default 12.
- Cost does not change with concurrency: the same tokens are sent, only in parallel.
- Tested in benchmark 20261103-081849:

| Concurrency | Answers per minute | Errors |
|---|---|---|
| 4 | about 25 | 0 (128 answers) |
| 12 | about 54 | 0 (2032 answers) |

- At 12, the full matrix (2160 answers) took about 38 minutes.
- Limit: a Claude Code cloud background command stops after 2 hours. `--resume` continues a stopped run; saved answers are kept.
- Ceiling: set by the model providers' rate limits behind the gateway, not by the runner. Not documented per model; find it by trial.
- Above the ceiling, providers return HTTP 429. The runner retries 429, 408 and 5xx. Answers still failing are listed; `--resume` retries them.
- To try a higher value: `--concurrency 16` (or 20) on one benchmark. Keep it if errors stay at 0 and answers per minute rise.
- Limits differ per model. anthropic/claude-opus-5.5 failed at 12 (HTTP 429 "No access to this model at this time"); 3 ran with 0 errors. Use `--concurrency 3` for frontier models.

### Temperature
- Temperature controls randomness in the model's word choice. 0 = always the most likely word. Higher = more varied.
- Set to 0.2 in `config.yaml`.
- Reasons:
  - Factual multiple-choice questions need stable answers, so temperature stays low.
  - 0 does not make hosted models deterministic (see Why 5 runs). The 5 runs measure the remaining variation either way.
  - Some reasoning models loop or repeat at 0. Their vendors advise against greedy decoding. A small value avoids this.
  - The benchmark should match production: `config.yaml` says to use the value the website will use. The website value is not fixed yet; 0.2 is the working assumption.
- Fixed for a whole run. Comparing runs at different temperatures mixes two effects.
- The 0.2 choice is a design default, not a measured optimum. A temperature sweep (0, 0.2, 0.7) on the best model would test it.

## What it does
1. Loads `knowledge/` exactly as `ARCHITECTURE.md`, section Local LLM use: metadata split off, body chunked by `##` heading.
2. Builds the index: BM25, plus embeddings (`embedding_model`) when the API key is set. Embeddings are cached in `harness/.cache/`.
3. Loads every question with an answer key (`answer` letters, or `## Expected key points`). Questions without one are listed as skipped.
4. For each model, mode, question and run:
   - multiple choice: shuffles the options (same order for every model and mode within a run) and appends "Unsure"; free text: sends the prompt as written;
   - answers in the mode:
     - `baseline`: no knowledge base;
     - `classic`: one search, link expansion (`same_name`, `related`), 8K-token context;
     - `agentic`: tool loop with `search`, `read_file`, `follow_links`, `get_images`; at most 8 calls and 12K tokens of tool output. Search first, no repeated calls, a same_name reminder. Falls back to classic after 2 tool-format errors;
   - multiple choice: parses `ANSWER:`, maps letters back, scores exact match, partial credit, trap hit, Not-covered pick, Unsure pick;
   - free text: the judge scores 0-3; credit = score / 3;
5. Questions with image attachments are sent with their images (track `vision`); every candidate must have vision.
6. Writes the benchmark folder and appends one summary row per model, mode and question to `benchmark/results/results.csv`.

## Output: `benchmark/results/<benchmark-id>/`
| File | Content | In git |
|---|---|---|
| `config.json` | Index version (git SHA), models with tags and prices, settings | Yes |
| `answers.csv` | One row per answer: model, provider, mode, track, question, answer type, input, level, run, option order, letters, scores (exact, partial, unsure, credit, confident wrong), judge model, score and missed point, answer text (free text), retrieval recall, tool steps, tools used, verifier flags, repaired, tokens, latency, cost | Yes |
| `report.md` | Final score and sub-scores; free-text judge table; multiple-choice matrix (exact, partial, majority, margin, consistency, trap, parse failures, recall, fallback, cost), by area and level; hardest questions | Yes |
| `traces.jsonl` | Full prompt and retrieval trace per answer | No (large); keep locally |

## Question fields used
| Field | Meaning |
|---|---|
| `answer_type` | `deterministic` (letters) or `judged` (judge) |
| `level` | `100`, `200`, `300`, `400` |
| `input` | `text`, `table`, `screenshot`; checked against the attachments by lint |
| `answer` | Correct option letters, as in `## Prompt` |
| `trap` | Option letters that are the known wrong answer |
| `knowledge` | Files the answer should come from; used for retrieval recall |

- Options in `## Prompt` are lines starting with `A. ` to `H. `. Text after the options (for example `Hint:`) is kept below them.
- The prompt states the problem in words; the images supply the values.
- Free text: `## Expected key points` and `## Likely wrong answer` go to the judge, never to the candidate.
- `project/tools/lint.py` checks these fields.

## Limits
- Provider name is recorded when the gateway returns it; the field is not documented as stable.
- Cost is estimated from gateway list prices in `/models`; check the Vercel invoice.
- Mock runs prove the pipeline only. Their scores are random, including the mock judge.
- The judge is a model: its scores carry its errors. The author checks every 0 and every split between runs (`benchmark/design.md`, section 14).
