# Requirements: spending on tests

How Agent E2's tests that call a model keep the author's spending down: what is asked again, when a run stops, and when the full round runs. Every requirement here belongs to milestone M3 in the workspace's [ROADMAP.md](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/ROADMAP.md); the author asked for them on 2026-11-28, before M3 opened. The design and its reasons are DESIGN-31 in the workspace's [system design](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/spec/design/system.md), and the budget is CONSTRAINT-1 in its [brief](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/spec/brief.md). Other IDs are explained in the [glossary](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/spec/glossary.md).

Files involved:

- The round and its runs: [benchmark/runner/round_executor.py](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/round_executor.py) and [benchmark/runner/run_executor.py](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/run_executor.py), with their settings in [benchmark/runner/runner_config.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/runner_config.yaml).
- The inputs of an answer and the earlier answers: [benchmark/runner/answer_reuse.py](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/answer_reuse.py).
- The money spent: [benchmark/runner/spending_stop.py](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/spending_stop.py).
- How to run a round: [benchmark/RUN.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/RUN.md).

### R-E2-029 An unchanged answer is not asked again

Why: an answer whose inputs have not changed is one more sample of the same thing, so asking again spends money and measures nothing new. In November 2026 the frontier reference was about half of each round, though its answers do not depend on Agent E2 and most questions had not changed.

Source: the author, 2026-11-28 ("no re-grading of answers that haven't changed", [round 6](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/spec/author-input/interview-round-6.md#spending-on-tests)); CONSTRAINT-1; DESIGN-31.

- Given a benchmark run, and the run folders already in [`benchmark/results/`](../../benchmark/results)
- When an answer's inputs equal those of an earlier answer that did not fail
- And the inputs are: the question as the model sees it in that run (stem, options in the run's order, tables) and its images; the mode, the model, its request settings and the run number; for the baseline and web modes, the code and prompts that build their requests; for Agent E2, every file of `knowledge/` and `harness/` except the tests, the answer settings of `runner_config.yaml` and the search method
- Then the earlier answer is copied into the run, its column `reused_from` names the run that first asked it, and no model is called for it
- And it is scored against the question's current key, which is not an input
- And a run started with `--no-reuse` asks every answer
- And a round's spending counts only the answers it asked

Test scenarios:
- T-E2-029a (anywhere, automated by [benchmark/runner/test_runner.py](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/test_runner.py), offline with the mock client): a second run into the same results folder reuses every answer, calls no model, and scores what the first run scored; with `--no-reuse` it asks every answer.
- T-E2-029b (anywhere, automated by the same file): a changed question stem asks that question again in every mode and reuses the others; a changed knowledge file asks every Agent E2 answer again and reuses the baseline answers.
- T-E2-029c (anywhere, automated by the same file): a changed answer key reuses the answer and scores it against the new key.

### R-E2-030 A test run stops at its budget

Why: the round of 16 November 2026 cost US$115 against a projection of US$77 to 85, because only the projection was checked before the round started.

Source: CONSTRAINT-1 (US$100 a test run at most); the author, 2026-11-28 ("It can't be $71. Way too expensive", on the projection of the full round); DESIGN-31.

- Given a benchmark round, and the limit `release.max_cost_usd` of `runner_config.yaml`, US$25
- When the money it has spent reaches the limit: the larger of the list price of the tokens of the answers it asked, runs restarted with other settings included, and the drop in the gateway's credit balance since its preflight
- Then it starts no new answer, lets the answers in progress finish, and exits with code 9, naming the amount spent and the limit
- And the preflight still refuses a round whose projected cost is above the limit
- And a resume after the author raises the limit continues where the round stopped

Test scenarios:
- T-E2-030a (anywhere, automated by [benchmark/runner/test_runner.py](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/test_runner.py)): a round whose run records answers worth more than the limit exits with code 9 and leaves a stop file in the run's folder; a resume removes the stop file before it starts the run again.
- T-E2-030b (anywhere, automated by the same file, offline with the mock client): a run whose folder holds a stop file starts no answer and exits with code 3.
- T-E2-030c (anywhere, automated by the same file): the spending counted is the larger of the two figures; a balance that cannot be read counts the list price alone.

### R-E2-031 The full round runs only for a milestone

Why: between milestones, the free checks and the answer set test each change, and three full rounds in one week of November 2026 spent US$350. Release 1.0 runs Gemma 4 31B, so the other candidates choose nothing in it. The frontier reference is a comparison, so one answer per question gives its score, and it cost US$58 of the US$71 a round of 5 runs would cost. Gemma's 3 runs keep the score within about 6 points and still give the projection of 3 answer samples agreeing.

Source: the author, 2026-11-28 ("the full test run only at milestones", [round 6](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/spec/author-input/interview-round-6.md#spending-on-tests)); SCOPE-6 (Gemma 4 31B); DESIGN-31.

- Given [`benchmark/runner/round_executor.py`](../../benchmark/runner/round_executor.py)
- When a new round starts
- Then it refuses to start without `--milestone`, the milestone of the workspace's ROADMAP.md the round serves, such as `M3`, and the round's summary names that milestone
- And release 1.0's round asks Gemma 4 31B in the baseline and Agent E2 modes, 3 runs per question, and the frontier reference, Claude Opus 5.5, in the web mode, 1 run per question

Test scenarios:
- T-E2-031a (anywhere, automated by [benchmark/runner/test_runner.py](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/test_runner.py)): a new round without `--milestone` exits with code 2 and starts no run; with `--milestone M3` it starts; a resume needs no milestone.
- T-E2-031b (anywhere, automated by the same file): `release.runs` of `runner_config.yaml` holds exactly those two entries with their runs per question, and `release.max_cost_usd` is 25; each run of a round asks its own number of runs per question, and a resume keeps it.
