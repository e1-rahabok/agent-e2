# Benchmark runner

Runs every question (multiple choice, screenshot, free text) against the candidate open-weight models through Vercel AI Gateway, scores them automatically (letters, or a judge model for free text), and writes a report with one final score.
A whole round (four runs, preflight, recovery, summary) without anyone at the keyboard: [benchmark/RUN.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/RUN.md).
Design: [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md). Models and judge: [benchmark/models.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/models.md). Not indexed.

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
python3 benchmark/runner/run.py --models google/gemma-4-31b-it --modes agent-e2 --runs 1 --questions L4-04
```
- Smallest real benchmark: one model, one mode, one question.

```bash
python3 benchmark/runner/run.py
```
- Full matrix from `config.yaml`.

```bash
python3 benchmark/runner/run.py --resume benchmark/results/<run-folder>
```
- Continue a benchmark; failed answers are retried.

```bash
python3 benchmark/runner/preflight.py
python3 benchmark/runner/run_all.py --max-minutes 110
python3 benchmark/runner/run_all.py --resume --max-minutes 110
```
- The final round: a sample first, then all runs in parallel, then the summary. See "A whole round" below and [benchmark/RUN.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/RUN.md).

```bash
python3 -m unittest benchmark/runner/test_runner.py
```
- Scoring tests: judge reply parsing, final score, sub-score groups, question tags. No API calls.

- Up-front blocks of Agent E2's answer prompt (config `primer`, both on): `--primer rules` or `--primer all`. The choice is stored in `config.json` (`primer`). Design: [harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md), section 4.5.

## Retrieval check (no model)
```bash
python3 benchmark/runner/retrieval_eval.py
```
- Recall of each question's `knowledge` files in search and in Agent E2's reading set (the code-only case: no model call). Add `--embeddings` for hybrid search (needs `AI_GATEWAY_API_KEY`).
- Why it is needed, how to read the result, what to do when it is low: [benchmark/retrieval-check.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/retrieval-check.md).

## Methodology

### Final score
- Method: [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), section 7.4. Report table `Final score`; code `report.py`, function `final`.

### Free text and the judge
- `answer_type: judged` questions are sent without options, with an open-answer prompt ([harness/modes.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/modes.py), `PROMPTS['open']`). The verifier does not run on them: it checks letters only.
- `judge.py` sends the prompt, images, `## Expected key points`, `## Likely wrong answer` and the answer to `judge_model`, and reads back a JSON score 0-3.
- The runner refuses a benchmark where the judge is also a candidate.
- Rubric and checks: [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), section 14. Report table `Free-text answers (judge)`.

### Screenshots
- Questions with image attachments are sent with all their images (track `vision`). There is no text-only track.
- The runner refuses a candidate without the gateway `vision` tag when screenshot questions are in the benchmark: reading screenshots is a basic requirement ([benchmark/models.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/models.md)).

### Multiple choice: question and score
- A multiple-choice question has one or more correct options.
- A run asks every question once, per model and mode.
- 5 runs per question. The answer is sampled at the model card's temperature (1.0), so one run is one draw; the case of Agent E2 is read at temperature 0, the answer is not. The 5 runs give the mean (final score), the consensus-of-3 projection and consistency. Reason: [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), section 7.2.
- Every question says: "Choose all the correct options. There can be more than one." One option is appended: "Unsure". There is no "Not covered" option: the system answers from the knowledge base first and from the model's own knowledge where it is silent (author, Q038, 2026-11-05).
- Exact: answer letters match the key exactly. 1 or 0 per answer.
- Classes: correct (exact letters), Unsure (chosen alone), confident wrong (anything else, including unparseable). The model is told a wrong answer is worse than Unsure. No points: see [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), section 7.1.
- Stable correct: share of multiple-choice questions answered exactly right in all 5 runs. Report table `Multiple choice: luck-free scores`. Reported as consistency; the final score uses the mean of the runs (since 2026-11-13).
- Luck: share of questions right in some runs only. Counted as not known.
- Override (table `Final score`): share of knowledge base answers that state the misconception although every needed file was in the context. Prior override, not a retrieval miss.
- Confident-wrong rate: share of answers that are wrong and not Unsure. Accuracy when answered: exact share among non-Unsure answers.
- Exact (mean over runs) is still reported in table `Scores`.
- Reason and design: [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), section 7.
- Partial: credit for each correct letter picked, minus wrong letters. Shows near misses on multi-answer questions.
- Majority: for each question, take the answer given most often over the 5 runs, then score it. Shows what the model answers "usually".
- Margin: 95% interval on Majority, from the number of questions (about ±5 points at 200 questions; benchmark/design.md, section 4).

### Modes: baseline, agent-e2, web

| | Baseline | Agent E2 (`agent-e2`) | Web (frontier reference) |
|---|---|---|---|
| Knowledge base | None | Yes | None |
| Who decides what to read | Nobody | The agent's code, from the knowledge base's map | The model: web search and page fetch are offered (`tool_choice: auto`); it may search, fetch, or answer without either |
| Model calls | 1 | 2 in the common case: the case (temperature 0, so the same question gets the same reading set) and the answer (the model card's sampling, as a local server runs it); plus a gap follow-up and a repair when needed | 1, plus up to 5 tool calls when the model chooses to search |
| What the model gets | The prompt only | The case, computed facts, catalog facts, the reading set (16K), the up-front blocks, the prompt | The prompt and the pages it chose to read |
| Runs on | Every candidate | Every candidate | The frontier reference only |

- Two runs per candidate (author, 2026-11-14): Base and Agent E2. Agent E2 is the shipped system ([harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md)); Base is the same model alone. The frontier reference runs one mode, `web`: search is available and Opus decides whether to use it, as in a chat product. There is no run with search removed: a user cannot switch it off, so that run measures nothing a user meets (author, 2026-11-13).
- Agent E2 answers pass the answer verifier ([harness/verify.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/verify.py)): a missing ANSWER line, a letter that is not an option, or Unsure mixed with other letters gets one repair turn. Baseline and web are not verified.
- Recall column: the needed files whose text reached the model (the reading set and any gap follow-up). Agent E2 only: Base and web read no knowledge base.
- Classic and agentic modes were removed on 2026-11-14; `run.py` refuses them.

### Index version
- The knowledge base changes with every commit. A score is only meaningful next to the knowledge that produced it.
- Index version = the git commit SHA of the repository when the benchmark started. Example: `de5f19e22860`.
- To see the exact knowledge files a benchmark used: `git checkout <index version>`.
- Two runs with different index versions compare knowledge-base changes. Two runs with the same index version compare models or settings.
- The runner reads the files on disk but records the commit SHA. Commit all knowledge changes before a benchmark, or the recorded version is wrong.

### Hybrid retrieval
- Retrieval searches only the `knowledge/` files. With `web.enabled` (on), Agent E2 reads the links in the question, and searches vendor sites when the question asks for current facts (ARCHITECTURE.md, section 5).
- In the benchmark the models and the embedding model run in the cloud through Vercel AI Gateway, to compare candidates cheaply. In production the chosen model runs locally; the knowledge base lookup is the same.
- Retrieval = finding the knowledge-base sections to give the model. Used by Agent E2's reading plan.
- The knowledge files are cut into chunks, one per `##` heading.
- Two searches run on the same prompt:
  - Keyword search (BM25): scores chunks that share the prompt's words. Strong on exact terms: metric names, counter names such as %LAT_M.
  - Vector search (embeddings): an embedding model (`embedding_model` in `config.yaml`) turns each chunk and the prompt into vectors; nearest vectors score highest. Strong on meaning when the words differ, e.g. "VM waits for memory" vs "page-fault latency".
- Fusion: reciprocal rank fusion. Each chunk gets 1 / (60 + rank) from each list; the sums decide the order. A chunk ranked well by both searches comes first.
- Best chunk per file; the reading plan takes the top `search_k` (6) files, then adds linked files and one search per claim ([harness/planner.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/planner.py)).
- Hybrid = both searches fused. `bm25` in a report = embeddings were off or unavailable; keyword search only.
- Why hybrid: keyword search misses paraphrases; vector search misses rare exact terms. Fusing both is the common practice for technical text.

### Concurrency (speed)
- Requests sent to the gateway at the same time, per model. Cost does not change with concurrency: the same tokens are sent, only in parallel.
- Ceiling: set by the model providers' rate limits behind the gateway, not by the runner. Not documented per model; found by trial. Above it, providers return HTTP 429. The client retries 429, 408 and 5xx; an answer that still fails is listed, and `--resume` retries it.
- Limit: a Claude Code cloud background command stops after 2 hours (see Long runs below).

**Adaptive concurrency** ([governor.py](governor.py), `adaptive_concurrency` in `config.yaml`; `--no-adaptive` turns it off):
- Each model starts at its proven value: `concurrency` (12), or its entry in `concurrency_by_model` (anthropic/claude-opus-5.5: 3; the provider rate-limits above that in a short trial; the governor kept 5 in the baseline run and 7 in the web run of 2026-11-13). The proven value is the floor: the runner never goes below it. `--concurrency N` sets one proven value for every model.
- It then probes upward in steps of 2, up to 2 steps (12, 14, 16). Each level is measured over a window of 40 answers (the first answers after a change are dropped).
- A step is kept only if the window has no error and the answers per minute rise by at least half of the ideal gain (12 to 14: at least +8.3% of the ideal +16.7%; 14 to 16: at least +7.1%). A step that fails returns to the last level that held, and probing stops.
- Any HTTP 429 returns the model to its proven value for the rest of the run. A 429 at the proven value changes nothing and prints a warning: that model's proven value is too high, so lower its entry in `concurrency_by_model` and resume.
- A window holds one mode: baseline, Agent E2 and web answers take different times. A window that spans two modes is thrown away and the base level is measured again.
- Tasks run model by model, so one model probes at a time; the others wait at their proven value.
- The console prints each decision (`concurrency <model>: 14 kept, 36.2 answers/min is 1.12x the 32.3 at 12`) and, every 25 answers, the current level of each model.
- Tested offline (a fake clock, [test_runner.py](test_runner.py), class GovernorTest). The first live run is the real test: watch the decision lines.

### Long runs: stop and resume
- `--max-minutes N` (or `max_minutes` in `config.yaml`): after N minutes the runner starts no new answer, lets the running ones finish, prints `Resume: python3 benchmark/runner/run.py --resume <folder>` and exits with code 3. It writes no `report.md`: a stopped run is not a result. Exit code 0 = finished, 3 = stopped at the limit.
- In a Claude Code cloud session start every long run with `--max-minutes 110`: the 2-hour limit kills a command in the middle of an answer; this stops it clean, a few minutes earlier.
- `--resume <folder>` needs no other flag: models, modes, runs, temperature, questions, judge and primer are read from the folder's `config.json`, so a resume cannot change what the run measures (a resume without `--models` once ran every model of `config.yaml` into the folder). A flag you pass still overrides. Saved answers are kept; answers that failed are retried. `config.json` keeps the original `started` time and lists each resume in `resumed`.
- Cannot be done inside the process: a command cannot extend the 2-hour limit of the session that started it. The relaunch is a new command: when a run exits with code 3 (or its process is gone and the folder has fewer answers than the matrix), start `python3 benchmark/runner/run.py --resume <folder> --max-minutes 110` again. The 15-minute progress check does this on its own: it counts the rows of `answers.csv` by `model` and relaunches a dead run.
- `index_version` in `config.json` is the commit at the last resume; each row of `answers.csv` keeps the commit of its own answer. A resume after a change to the knowledge base mixes two versions in one run: stop edits to `knowledge/` during a run.

### Request settings per model (reasoning)
- A reasoning model spends tokens thinking before it writes the `ANSWER:` line. `max_tokens` counts the thinking. When the thinking uses all of it, the answer is cut off, no letter is found and the answer scores as wrong: the run measures the cap, not the model.
- Measured on 2026-11-12 with the default settings: alibaba/qwen3.8-27b used 3,700-4,300 tokens per answer in every mode (85% of its baseline answers hit the 4,000 cap, 549 of its 1,350 multiple-choice answers had no readable letter) and took 25-38 s per answer; google/gemma-4-31b-it used 160-380 tokens and 9-20 s.
- `model_params` in `config.yaml` lists, per model, the request settings in order of preference. Fields: `reasoning` (sent to the gateway as is: `{effort: none}`, `{enabled: false}`; the model's `reasoning_options` in the gateway `/v1/models` list what it accepts) and `max_tokens`. `run.py` without `--params` uses the first entry; `preflight.py` picks the first entry that answers cleanly. The choice is saved in the run folder's `config.json` under `model_params`, and a resume keeps it.
- Measured live on 2026-11-13: `{effort: none}` cut a Qwen answer from 303 to 41 tokens; `{enabled: false}` removed Muse's thinking; Opus accepts `{effort: medium}`.
- The setting is part of the measurement: a model with reasoning off may score differently from the same model with it on. The summary README lists the settings of every run.

### Health check (during a run)
- [health.py](health.py) watches the last 40 answers of each model. A bad answer is an API error, a multiple-choice answer with no readable letter, or an answer cut off at `max_tokens` (the gateway's `finish_reason` is `length`; column `truncated`). When 25% of them are bad (after 20 answers) the run stops starting new answers, writes no report and exits with code 5. The answers stay in the folder.
- An HTTP 402 (credits or key budget) or 401 or 403 (key) stops the run at once with code 6: every further answer would fail the same way.
- `--no-health` turns it off (the preflight uses that: it judges the sample itself). Tested in `test_runner.py`, class HealthTest.

### Preflight (before a round)
- [preflight.py](preflight.py) answers a sample (4 multiple-choice, 2 judged, 1 screenshot question; 6 multiple-choice when the set has no judged question, as since 2026-11-14) in every mode of every run of the round, through `run.py`: the code and the settings of the real run. It tries a model's `model_params` entries in order until one passes: no API error, 95% of letters readable, no answer cut off, mean completion tokens under half of `max_tokens`, every mode answered.
- It reads the credits (`/v1/credits`), projects time and cost of the whole round from the sample, and refuses the round when the projected cost times `release.cost_safety` is above the credits or `release.max_cost_usd`, or the time is above `release.max_hours`. The key's own budget cannot be read; it shows only as an HTTP 402.
- The projection is rough: seven questions per mode. Live on 2026-11-13: 1.5 to 2.5 minutes of wall time for two models at once, about US$ 0.55 for all four.

### A whole round: run_all.py
- [run_all.py](run_all.py) runs `release.runs` of `config.yaml` (one run.py per model, all at once, each in `benchmark/results/<date>-<model>/`): preflight, runs, recovery, summary. Playbook, approvals and expectations: [benchmark/RUN.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/RUN.md).
- Recovery: a run that crashed (exit 1 and others) is relaunched with `--resume`, up to `release.retries` times; answers that failed are retried the same way. A run whose answers are invalid (exit 5) restarts from the beginning with the next entry of the model's `model_params`; the invalid folder is kept as evidence and moves to the archive at the end. A refused key (exit 6) stops the round.
- State is in `benchmark/results/.round.json` (not in git). `--resume` continues a round after exit 3 or exit 6; without it a second start is refused while a round is in progress; `--new` discards the state.
- When every run is complete it writes [benchmark/results/README.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/results/README.md) with [summarize.py](summarize.py) (one analysis of all runs, every number from the run folders) and moves earlier run folders to `project/archive/benchmark-results-before-<date>/`. It does not commit or merge.
- Exit codes ([exitcodes.py](exitcodes.py)): 0 done; 1 crashed; 3 stopped at `--max-minutes`, relaunch with `--resume`; 4 preflight failed; 5 invalid answers; 6 credits or key refused; 7 some runs done, others failed.

### Temperature
- Temperature controls randomness in the model's word choice. 0 = always the most likely word. Higher = more varied.
- Each model runs with the sampling settings of its own card (`generation_config.json` on Hugging Face): `config.yaml`, key `sampling` (author, 2026-11-13).
  - Gemma 4 31B and Muse Glimmer 30B: temperature 1.0, top_p 0.95, top_k 64. Qwen 3.8 27B: temperature 1.0, top_p 0.95, top_k 20.
  - Reason: a local server (vLLM, and others that read the card) applies these by default, so the benchmark sees what a user sees. Until 2026-11-13 every model ran at 0.2.
  - The frontier reference sends none: the provider's default, as a chat user meets it.
  - The judge and Agent E2's case call (stage 1) run at temperature 0: a reading step, not an answer.
  - The gateway accepted top_p and top_k for all three candidates (one call each, 2026-11-13). Whether every provider honours top_k is not known.
- `--temperature` replaces the settings for every model: an experiment, not the release run.

## What it does
1. Loads `knowledge/` exactly as `ARCHITECTURE.md`, section Local LLM use: metadata split off, body chunked by `##` heading.
2. Builds the index: BM25, plus embeddings (`embedding_model`) when the API key is set. Embeddings are cached in `harness/.cache/`.
3. Loads every question with an answer key (`answer` letters, or `## Expected key points`). Questions without one are listed as skipped.
4. For each model, mode, question and run:
   - multiple choice: shuffles the options (same order for every model and mode within a run) and appends "Unsure"; free text: sends the prompt as written;
   - answers in the mode:
     - `baseline`: no knowledge base;
     - `agent-e2`: the six stages of harness/AGENT.md: the case, the reading plan (16K tokens), computed facts, the answer, the checks (verifier, one gap follow-up);
     - `web`: the frontier reference, web search and page fetch at the model's choice;
   - multiple choice: parses `ANSWER:`, maps letters back, scores exact match, partial credit, misconception picked, Unsure pick;
   - free text: the judge scores 0-3; credit = score / 3;
5. Questions with image attachments are sent with their images (track `vision`); every candidate must have vision.
6. Writes the benchmark folder: `answers.csv`, `config.json`, `traces.jsonl`, `report.md`.

## Output: `benchmark/results/<date>-<model>/`
- One folder per run, named for the day it started and the model (`20261114-gemma-4-31b-it`; a second folder of the same name gets `-2`). [benchmark/results/README.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/results/README.md) is the only file at that level: the analysis of all runs of a round.
| File | Content | In git |
|---|---|---|
| `config.json` | Index version (git SHA), models with tags and prices, request settings per model (`model_params`), up-front blocks, judge and its price, settings | Yes |
| `answers.csv` | One row per answer: model, provider, mode, track, question, answer type, input, level, run, option order, letters, scores (exact, partial, misconception, unsure, credit, confident wrong), judge model, score and missed point, answer text (free text), retrieval recall (Agent E2), model calls (`steps`), stages that acted (`tools_used`: compute, gap, repair, consensus) or the web reference's tools, verifier flags, repaired, tokens, latency, cost | Yes |
| `report.md` | Final score and sub-scores; release gate and consensus projection; free-text judge table; multiple-choice matrix (exact, partial, majority, margin, consistency, misconception, parse failures, recall, model calls, cost), by area and task; hardest questions | Yes |
| `traces.jsonl` | Full prompt and retrieval trace per answer | No (large); keep locally |
| `run.log` | Console output of the run, written by `run_all.py` | No |

## Question fields used
| Field | Meaning |
|---|---|
| `answer_type` | `deterministic` (letters) or `judged` (judge) |
| `level` | `100`, `200`, `300`, `400` |
| `input` | `text`, `table`, `screenshot`; checked against the attachments by lint |
| `answer` | Correct option letters, as in `## Prompt` |
| `misconception` | Option letters that are the known wrong answer |
| `knowledge` | Files the answer should come from; used for retrieval recall |

- Options in `## Prompt` are lines starting with `A. ` to `H. `. Text after the options (for example `Hint:`) is kept below them.
- The prompt states the problem in words; the images supply the values.
- Free text: `## Expected key points` and `## Likely wrong answer` go to the judge, never to the candidate.
- [project/tools/lint.py](https://github.com/e1-rahabok/agent-e2/blob/main/project/tools/lint.py) checks these fields.

## Limits
- Provider name is recorded when the gateway returns it; the field is not documented as stable.
- Cost is estimated from gateway list prices in `/models`; check the Vercel invoice. The summary README adds the judge cost from the judge tokens in `traces.jsonl`.
- Mock runs prove the pipeline only. Their scores are random, including the mock judge.
- The judge is a model: its scores carry its errors. The author checks every 0 and every split between runs ([benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), section 14).
