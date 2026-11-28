# Benchmark runner

Runs every question (multiple choice, with text, tables or screenshots) against the candidate open-weight models through Vercel AI Gateway, scores the letters automatically, and writes a report with one final score.
A whole round (preflight, runs, recovery, summary), only before a milestone is closed, without anyone at the keyboard: [benchmark/RUN.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/RUN.md).
Design: [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md). Models: [benchmark/models.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/models.md). Not indexed.

## Setup
- Python 3.10+ with `pyyaml` and `requests`.
- Environment variable `AI_GATEWAY_API_KEY` (Vercel AI Gateway API key). Never commit it.
- Settings: `runner_config.yaml` (models, modes, runs, temperature, budgets, provider pinning).

## Commands
```bash
python3 benchmark/runner/run_executor.py --dry-run
```
- Shows the matrix, the number of answers and a cost estimate. No API calls.

```bash
python3 benchmark/runner/run_executor.py --mock --runs 2
```
- Offline pipeline check: random answers, real retrieval, no API calls.

```bash
python3 benchmark/runner/run_executor.py --models google/gemma-4-31b-it --modes agent-e2 --runs 1 --questions L4-004
```
- Smallest real benchmark: one model, one mode, one question.

```bash
python3 benchmark/runner/run_executor.py
```
- Full matrix from `runner_config.yaml`.

```bash
python3 benchmark/runner/run_executor.py --resume benchmark/results/<run-folder>
```
- Continue a benchmark; failed answers are retried.

```bash
python3 benchmark/runner/round_sample_check.py
python3 benchmark/runner/round_executor.py --milestone M3 --max-minutes 110
python3 benchmark/runner/round_executor.py --resume --max-minutes 110
```
- The full round, for a milestone of the workspace's ROADMAP.md: a sample first, then all runs in parallel, then the summary. See "A whole round" below and [benchmark/RUN.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/RUN.md).

```bash
python3 -m unittest benchmark/runner/test_runner.py
```
- Scoring tests: final score, sub-score groups, question tags. No API calls.

- Up-front blocks of Agent E2's answer prompt (config `primer`, both on): `--primer rules` or `--primer all`. The choice is stored in `config.json` (`primer`). Design: [harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md), section 4.5.

## Retrieval check (no model)
```bash
python3 benchmark/runner/retrieval_check.py
```
- Recall of each question's `knowledge` files in search and in Agent E2's reading set (the code-only case: no model call). Add `--embeddings` for hybrid search (needs `AI_GATEWAY_API_KEY`).

## Topic check
```bash
python3 benchmark/runner/topic_check.py
```
- Does Agent E2 tell a question that continues the topic from one that starts a new topic ([harness/topic_decision.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/topic_decision.py))? Scores the labelled pairs of [topic_check_pairs.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/topic_check_pairs.yaml) three ways: always continue, code alone, code then the model. Counts lost context (the worse error) apart from extra context. `--no-model` runs offline; the model step needs `AI_GATEWAY_API_KEY` (one call per pair the code cannot settle). Add a pair for every wrong decision seen in the live test.

## Screen answer check
```bash
python3 benchmark/runner/screen_answer_check.py --out /tmp/answers.json
```
- Does Agent E2 answer a question typed on a PCM screen the way it asks ([harness/answer_service.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/answer_service.py))? Runs each wording of [screen_answer_check.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/screen_answer_check.yaml) through the service on the real model, with the page's facts as PCM sends them ([screen_answer_check_pages.json](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/screen_answer_check_pages.json), PCM story M-5), and checks by code: the page's values used exactly when needed, the answer shape, and what the answer must or must not say. No judge: read the answers in `--out` too. Needs `AI_GATEWAY_API_KEY`; about 36 answers, 3 minutes at 8 workers. Run it before and after a change to how the service reads a question or shapes an answer; add the wordings of every wrong answer seen in the live test, several per type (CLAUDE.md, Working with the author).

- Why it is needed, how to read the result, what to do when it is low: [benchmark/retrieval-check.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/retrieval-check.md).

## Methodology

### Final score
- Method: [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), section 7.4. Report table `Final score`; code `score_report.py`, function `final`.

### Free text
- Not in the benchmark: every question is multiple choice, and `run_executor.py` refuses a question without options. The judge is deleted; git history keeps it ([project/archive/legacy/judge-2026-11-14 at commit ebbc7dc](https://github.com/e1-rahabok/agent-e2/blob/ebbc7dc0be3268abc0f4939fe1ea40e400ac9bbb/project/archive/legacy/judge-2026-11-14)). Its rubric, for the grader of the release 1.0 answer set: [benchmark/free-text-rubric.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/free-text-rubric.md).

### Screenshots
- Questions with image attachments are sent with all their images (track `vision`). There is no text-only track.
- The runner refuses a candidate without the gateway `vision` tag when screenshot questions are in the benchmark: reading screenshots is a basic requirement ([benchmark/models.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/models.md)).

### Multiple choice: question and score
- A multiple-choice question has one or more correct options.
- A run asks every question once, per model and mode.
- 5 runs per question. The answer is sampled at the model card's temperature (1.0), so one run is one draw; the case of Agent E2 is read at temperature 0, the answer is not. The 5 runs give the mean (final score), the consensus-of-3 projection and consistency. Reason: [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), section 7.2.
- Every question says: "Choose all the correct options. There can be more than one." One option is appended: "Unsure". There is no "Not covered" option: the system answers from the knowledge base first and from the model's own knowledge where it is silent.
- Exact: answer letters match the key exactly. 1 or 0 per answer.
- Classes: correct (exact letters), Unsure (chosen alone), confident wrong (anything else, including unparseable). The model is told a wrong answer is worse than Unsure. No points: see [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), section 7.1.
- Stable correct: share of multiple-choice questions answered exactly right in all 5 runs. Report table `Multiple choice: luck-free scores`. Reported as consistency; the final score uses the mean of the runs.
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
| What the model gets | The prompt only | The case, computed facts, catalog facts, the reading set (32K), the up-front blocks, the prompt | The prompt and the pages it chose to read |
| Runs on | Every candidate | Every candidate | The frontier reference only |

- Two runs per candidate: Base and Agent E2. Agent E2 is the shipped system ([harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md)); Base is the same model alone. The frontier reference runs one mode, `web`: search is available and Opus decides whether to use it, as in a chat product. There is no run with search removed: a user cannot switch it off, so that run measures nothing a user meets.
- Agent E2 answers pass the answer verifier ([harness/answer_check.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/answer_check.py)): a missing ANSWER line, a letter that is not an option, or Unsure mixed with other letters gets one repair turn. Baseline and web are not verified.
- Recall column: the needed files whose text reached the model (the reading set and any gap follow-up). Agent E2 only: Base and web read no knowledge base.
- Classic and agentic modes were removed; `run_executor.py` refuses them.

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
  - Vector search (embeddings): an embedding model (`embedding_model` in `runner_config.yaml`) turns each chunk and the prompt into vectors; nearest vectors score highest. Strong on meaning when the words differ, e.g. "VM waits for memory" vs "page-fault latency".
- Fusion: reciprocal rank fusion. Each chunk gets 1 / (60 + rank) from each list; the sums decide the order. A chunk ranked well by both searches comes first.
- Best chunk per file; the reading plan takes the top `search_k` (6) files, then adds linked files and one search per claim ([harness/reading_plan.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/reading_plan.py)).
- Hybrid = both searches fused. `bm25` in a report = embeddings were off or unavailable; keyword search only.
- Why hybrid: keyword search misses paraphrases; vector search misses rare exact terms. Fusing both is the common practice for technical text.

### Concurrency (speed)
- Requests sent to the gateway at the same time, per model. Cost does not change with concurrency: the same tokens are sent, only in parallel.
- Ceiling: set by the model providers' rate limits behind the gateway, not by the runner. Not documented per model; found by trial. Above it, providers return HTTP 429. The client retries 429, 408 and 5xx; an answer that still fails is listed, and `--resume` retries it.
- Limit: a Claude Code cloud background command stops after 2 hours (see Long runs below).

**Adaptive concurrency** ([adaptive_concurrency.py](adaptive_concurrency.py), `adaptive_concurrency` in `runner_config.yaml`; `--no-adaptive` turns it off):
- Each model starts at its proven value: `concurrency` (12), or its entry in `concurrency_by_model` (anthropic/claude-opus-5.5: 3; the provider rate-limits above that in a short trial). The proven value is the floor: the runner never goes below it. `--concurrency N` sets one proven value for every model.
- It then probes upward in steps of 2, up to 2 steps (12, 14, 16). Each level is measured over a window of 40 answers (the first answers after a change are dropped).
- A step is kept only if the window has no error and the answers per minute rise by at least half of the ideal gain (12 to 14: at least +8.3% of the ideal +16.7%; 14 to 16: at least +7.1%). A step that fails returns to the last level that held, and probing stops.
- Any HTTP 429 returns the model to its proven value for the rest of the run. A 429 at the proven value changes nothing and prints a warning: that model's proven value is too high, so lower its entry in `concurrency_by_model` and resume.
- A window holds one mode: baseline, Agent E2 and web answers take different times. A window that spans two modes is thrown away and the base level is measured again.
- Tasks run model by model, so one model probes at a time; the others wait at their proven value.
- The console prints each decision (`concurrency <model>: 14 kept, 36.2 answers/min is 1.12x the 32.3 at 12`) and, every 25 answers, the current level of each model.
- Tested offline (a fake clock, [test_runner.py](test_runner.py), class AdaptiveConcurrencyTest). The first live run is the real test: watch the decision lines.

### Long runs: stop and resume
- `--max-minutes N` (or `max_minutes` in `runner_config.yaml`): after N minutes the runner starts no new answer, lets the running ones finish, prints `Resume: python3 benchmark/runner/run_executor.py --resume <folder>` and exits with code 3. It writes no `report.md`: a stopped run is not a result. Exit code 0 = finished, 3 = stopped at the limit.
- In a Claude Code cloud session start every long run with `--max-minutes 110`: the 2-hour limit kills a command in the middle of an answer; this stops it clean, a few minutes earlier.
- `--resume <folder>` needs no other flag: models, modes, runs, temperature, questions and primer are read from the folder's `config.json`, so a resume cannot change what the run measures (a resume without `--models` once ran every model of `runner_config.yaml` into the folder). A flag you pass still overrides. Saved answers are kept; answers that failed are retried. `config.json` keeps the original `started` time and lists each resume in `resumed`.
- Cannot be done inside the process: a command cannot extend the 2-hour limit of the session that started it. The relaunch is a new command: when a run exits with code 3 (or its process is gone and the folder has fewer answers than the matrix), start `python3 benchmark/runner/run_executor.py --resume <folder> --max-minutes 110` again. The 15-minute progress check does this on its own: it counts the rows of `answers.csv` by `model` and relaunches a dead run.
- `index_version` in `config.json` is the commit at the last resume; each row of `answers.csv` keeps the commit of its own answer. A resume after a change to the knowledge base mixes two versions in one run: stop edits to `knowledge/` during a run.

### Reused answers
- [answer_reuse.py](answer_reuse.py) hashes the inputs of each answer into the column `inputs_hash` of `answers.csv` (R-E2-029 in [test-spending.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/requirements/test-spending.md)). Before it asks anything, `run_executor.py` reads the `answers.csv` of every other folder in [benchmark/results](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/results) (not the `-invalid-` ones) and copies each answer with the same hash and no error: no model is called, the column `reused_from` names the folder, and the answer is scored again against the current `## Answers`.
- The inputs: the mode, the model, its request settings, the run number, the track, the question as the model sees it in that run (stem, options in the run's order, tables) and its images. Baseline adds the code and prompts that build its request; web adds its tools, the `web` settings and [public_web_lookup.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/public_web_lookup.py); Agent E2 adds every file of `knowledge/` and `harness/` except the tests, the keys of `runner_config.yaml` that reach an answer (every key except those in `SCHEDULE_KEYS`) and the search method.
- Why the whole of `knowledge/` and `harness/` for Agent E2: a change to a file the answer did not read can still change what search finds (DESIGN-31, rejected option b).
- `--no-reuse` asks every answer. The cost of a run counts only the answers it asked.

### Spending stop
- [spending_stop.py](spending_stop.py) counts what a round has spent: the larger of the list price of the answers it asked (`cost_usd`, the folders restarted with other settings included) and the drop in the gateway's credit balance since the preflight, read at most once a minute (R-E2-030). The balance also counts web searches, retries and failed calls; the list price also counts calls paid by the author's own provider key, which the balance never sees.
- At `release.max_cost_usd` (US$ 25, DESIGN-31) `round_executor.py` writes `.spending-stop` into each run folder. A run starts no new answer while the file is there, lets the running ones finish and exits with code 3; the round then exits with code 9 (`SPENT`). A resume removes the files and checks the limit again, so it continues only after the limit is raised.

### Answer set
- [answer_grader.py](answer_grader.py) runs the answer set of release 1.0 (R-E2-004 to R-E2-006 in [answer-service.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/requirements/answer-service.md)): one YAML file per question in [benchmark/answer-set](https://github.com/e1-rahabok/agent-e2/tree/main/benchmark/answer-set), each with its key points, its likely wrong answer and its knowledge files.
- `python3 benchmark/runner/answer_grader.py --check` tests the set with no model call: the count of each kind, the fields, the knowledge files, no run of 12 words shared with a multiple-choice question, and a row of `key-check.md` for each question.
- Without `--check` it answers each question 3 times through the service, has Claude Haiku 5.5 at low effort grade each answer 0 to 3 by the [rubric](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/free-text-rubric.md), and writes `benchmark/results/answer-set-<date>/report.md`. It needs the gateway key and stops at US$ 100 (exit 9). Exit 1: a limit is missed.
- A grade is reused when the answer, the question with its key points, the rubric and the grader are the same; an answer is reused when the question, the run and every file of `knowledge/` and `harness/` are the same (`benchmark/results/answer-set-cache`).

### Request settings per model (reasoning)
- A reasoning model spends tokens thinking before it writes the `ANSWER:` line. `max_tokens` counts the thinking. When the thinking uses all of it, the answer is cut off, no letter is found and the answer scores as wrong: the run measures the cap, not the model.
- Measured with the default settings: alibaba/qwen3.8-27b used 3,700-4,300 tokens per answer in every mode (85% of its baseline answers hit the 4,000 cap, 549 of its 1,350 multiple-choice answers had no readable letter) and took 25-38 s per answer; google/gemma-4-31b-it used 160-380 tokens and 9-20 s.
- `model_params` in `runner_config.yaml` lists, per model, the request settings in order of preference. Fields: `reasoning` (sent to the gateway as is: `{effort: none}`, `{enabled: false}`; the model's `reasoning_options` in the gateway `/v1/models` list what it accepts) and `max_tokens`. `run_executor.py` without `--params` uses the first entry; `round_sample_check.py` picks the first entry that answers cleanly. The choice is saved in the run folder's `config.json` under `model_params`, and a resume keeps it.
- Measured live : `{effort: none}` cut a Qwen answer from 303 to 41 tokens; `{enabled: false}` removed Muse's thinking; Opus accepts `{effort: medium}`.
- The setting is part of the measurement: a model with reasoning off may score differently from the same model with it on. The summary README lists the settings of every run.

### Health check (during a run)
- [bad_answer_guard.py](bad_answer_guard.py) watches the last 40 answers of each model. A bad answer is an API error, a multiple-choice answer with no readable letter, or an answer cut off at `max_tokens` (the gateway's `finish_reason` is `length`; column `truncated`). When 25% of them are bad (after 20 answers) the run stops starting new answers, writes no report and exits with code 5. The answers stay in the folder.
- A failure of the gateway or of a provider (HTTP 408, 429, 5xx after the retries, a dropped connection) is not a bad answer. It has its own window (the same 40 and 25%) and stops the run with code 8, `GATEWAY_DOWN`: not a setting problem, so nothing restarts with other settings. `round_executor.py` waits `release.outage_wait_seconds` and resumes the same folder, up to `release.outage_waits` times. The client keeps retrying a failing call for `gateway_retry_minutes` (5) first. Why: a 2-minute burst of HTTP 503 counted as invalid answers, stopped two runs and restarted both from zero.
- An HTTP 402 (credits or key budget) or 401 or 403 (key) stops the run at once with code 6: every further answer would fail the same way. The 402 text names the budget that ran out: the key's or the team's.
- `--no-health` turns it off (the preflight uses that: it judges the sample itself). Tested in `test_runner.py`, class StopRunOnBadAnswersTest.

### Preflight (before a round)
- [round_sample_check.py](round_sample_check.py) answers a sample (6 multiple-choice text questions and 1 screenshot question) in every mode of every run of the round, through `run_executor.py`: the code and the settings of the real run. It tries a model's `model_params` entries in order until one passes: no API error, 95% of letters readable, no answer cut off, mean completion tokens under half of `max_tokens`, every mode answered.
- It reads the credits (`/v1/credits`), which become the start of the spending stop's balance drop, projects time and cost of the whole round from the sample, and refuses the round when the projected cost times `release.cost_safety` is above the credits or `release.max_cost_usd`, or the time is above `release.max_hours`. The key's own budget cannot be read; it shows only as an HTTP 402.
- The projection is rough: seven questions per mode. Live : 1.5 to 2.5 minutes of wall time for two models at once, about US$ 0.55 for all four.

### A whole round: round_executor.py
- [round_executor.py](round_executor.py) runs `release.runs` of `runner_config.yaml` (one run_executor.py per model, all at once, each in `benchmark/results/<date>-<model>/`): preflight, runs, recovery, summary. Release 1.0's round is Gemma 4 31B (baseline, agent-e2) and the frontier reference (web).
- A new round needs `--milestone M<n>`, the milestone of the workspace's ROADMAP.md it serves (R-E2-031); without it the round refuses to start (exit 2). The summary names the milestone. A resume needs none. Playbook, approvals and expectations: [benchmark/RUN.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/RUN.md).
- Recovery: a run that crashed (exit 1 and others) is relaunched with `--resume`, up to `release.retries` times; answers that failed are retried the same way. A gateway outage (exit 8) waits and resumes the same folder. A run whose answers are invalid (exit 5: cut off, unreadable, a bad request) restarts from the beginning with the next entry of the model's `model_params`; the invalid folder is kept as evidence and moves to the archive at the end. A refused key (exit 6) stops the round.
- State is in `benchmark/results/.round.json` (not in git). `--resume` resumes every unfinished run, whatever stopped it: it starts from the folders, not from the state file (`reconcile_with_folders`). A folder with every answer is complete; a run stopped by the time limit, a refused key, an outage or a crash is pending again; only a run marked invalid for its settings waits. Without `--resume` a second start is refused while a round is in progress; `--new` discards the state.
- Snapshots: every `snapshots.every_minutes` (15) and at the end, [run_folders_backup.py](run_folders_backup.py) pushes the `answers.csv`, `config.json` and `report.md` of every run folder to the branch `snapshots/round-<date>`, built with a temporary git index, so the working branch is not touched. The branch is never merged; the author deletes it after the round.
- Hosts: with `spread_runs_over_providers`, [inference_providers.py](inference_providers.py) reads a model's provider hosts from the gateway's own reply (`message.provider_metadata.gateway.routing`), drops a host that fails a tiny call pinned to it, and gives run r the preferred host r mod n, the others as fallback. The host of every answer is in the column `provider`; scores are pooled over the hosts. `concurrency_per_provider` (off) would count the proven concurrency per host.
- Starting runs: start each run with one background command, with no wrapper shell, `nohup` or `&`: the system then reports the run's own end (a wrapper reports its own end after seconds).
- [round_alive_check.py](round_alive_check.py): per run, whether a process works on the folder, good answers against the total, the time of the last written answer and the cost. Verdicts: DONE, ALIVE, STALLED (no answer for `--stall-minutes`), DEAD, MACHINE RESTARTED; LOW BUDGET at 80% of `--budget`. A progress report says "running" only when it says ALIVE and the counts moved. Exit 0 when every run is DONE or ALIVE, 2 otherwise.
- [round_resume.py](round_resume.py), called by the SessionStart hook [.claude/hooks/resume_unfinished_benchmark_round.sh](https://github.com/e1-rahabok/agent-e2/blob/main/.claude/hooks/resume_unfinished_benchmark_round.sh): when a round is in progress, a run is unfinished and no process works on it, it starts `round_executor.py --resume` detached. It does nothing otherwise. Not tested live: whether a machine restart starts a session (and so the hook) without a message is not known.
- When every run is complete it writes [benchmark/results/README.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/results/README.md) with [round_summary.py](round_summary.py) (one analysis of all runs, every number from the run folders) and deletes earlier run folders (git history keeps them). It does not commit or merge.
- Exit codes ([exit_codes.py](exit_codes.py)): 0 done; 1 crashed; 3 stopped at `--max-minutes`, relaunch with `--resume`; 4 preflight failed; 5 invalid answers; 6 credits, key or team budget refused; 7 some runs done, others failed; 8 the gateway or a provider kept failing (wait, then resume the same folder); 9 the round spent `release.max_cost_usd`.

### Temperature
- Temperature controls randomness in the model's word choice. 0 = always the most likely word. Higher = more varied.
- Each model runs with the sampling settings of its own card (`generation_config.json` on Hugging Face): `runner_config.yaml`, key `sampling`.
  - Gemma 4 31B and Muse Glimmer 30B: temperature 1.0, top_p 0.95, top_k 64. Qwen 3.8 27B: temperature 1.0, top_p 0.95, top_k 20.
  - Reason: a local server (vLLM, and others that read the card) applies these by default, so the benchmark sees what a user sees. Until every model ran at 0.2.
  - The frontier reference sends none: the provider's default, as a chat user meets it.
  - Agent E2's case call (stage 1) runs at temperature 0: a reading step, not an answer.
  - The gateway accepted top_p and top_k for all three candidates. Whether every provider honours top_k is not known.
- `--temperature` replaces the settings for every model: an experiment, not the release run.

## What it does
1. Loads `knowledge/` exactly as `ARCHITECTURE.md`, section Local LLM use: metadata split off, body chunked by `##` heading.
2. Builds the index: BM25, plus embeddings (`embedding_model`) when the API key is set. Embeddings are cached in `harness/.cache/`.
3. Loads every question with an answer key (`## Answers` letters). Questions without one are listed as skipped.
4. For each model, mode, question and run:
   - multiple choice: shuffles the options (same order for every model and mode within a run) and appends "Unsure"; free text: sends the prompt as written;
   - answers in the mode:
     - `baseline`: no knowledge base;
     - `agent-e2`: the six stages of harness/AGENT.md: the case, the reading plan (32K tokens), computed facts, the answer, the checks (verifier, one gap follow-up);
     - `web`: the frontier reference, web search and page fetch at the model's choice;
   - multiple choice: parses `ANSWER:`, maps letters back, scores exact match, partial credit, misconception picked, Unsure pick;
5. Questions with image attachments are sent with their images (track `vision`); every candidate must have vision.
6. Writes the benchmark folder: `answers.csv`, `config.json`, `traces.jsonl`, `report.md`.

## Output: `benchmark/results/<date>-<model>/`
- One folder per run, named for the day it started and the model (`20261114-gemma-4-31b-it`; a second folder of the same name gets `-2`). [benchmark/results/README.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/results/README.md) is the only file at that level: the analysis of all runs of a round.
| File | Content | In git |
|---|---|---|
| `config.json` | Index version (git SHA), models with tags and prices, request settings per model (`model_params`), up-front blocks, settings | Yes |
| `answers.csv` | One row per answer: model, provider, mode, inputs hash, the folder it was reused from (empty when asked), track, question, answer type, input, level, run, option order, letters, scores (exact, partial, misconception, unsure, credit, confident wrong), retrieval recall (Agent E2), model calls (`steps`), stages that acted (`tools_used`: compute, gap, repair, consensus) or the web reference's tools, verifier flags, repaired, tokens, latency, cost | Yes |
| `report.md` | Final score and sub-scores; release gate and consensus projection; multiple-choice matrix (exact, partial, majority, margin, consistency, misconception, parse failures, recall, model calls, cost), by area and task; hardest questions | Yes |
| `traces.jsonl` | Full prompt and retrieval trace per answer | No (large); keep locally |
| `run.log` | Console output of the run, written by `round_executor.py` | No |

## Question fields used
| Field | Meaning |
|---|---|
| `answer_type` | `deterministic` (letters); the only type (Q-E2-199) |
| `level` | `100`, `200`, `300`, `400` |
| `input` | `text`, `table`, `screenshot`; checked against the attachments by lint |
| `misconception` | Option letters that are the known wrong answer |
| `knowledge` | Files the answer should come from; used for retrieval recall |

- Options in `## Prompt` are lines starting with `A. ` to `H. `. Text after the options (for example `Hint:`) is kept below them.
- The prompt states the problem in words; the images supply the values.
- `## Answers` (the correct letters) and `## Explanation` are the key; never sent to a candidate. The runner reads only `## Answers`.
- [project/tools/rules_check.py](https://github.com/e1-rahabok/agent-e2/blob/main/project/tools/rules_check.py) checks these fields.

## Limits
- Provider name is recorded when the gateway returns it; the field is not documented as stable.
- Cost is estimated from gateway list prices in `/models`; check the Vercel invoice.
- Mock runs prove the pipeline only. Their scores are random.
