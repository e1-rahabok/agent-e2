# Run a benchmark round

How to run the final benchmark round, what it costs, how long it takes, and what it does when something fails. Not indexed.
Runner details: [benchmark/runner/README.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/README.md). Method: [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md).

## Give this prompt to your LLM

```text
Run the final benchmark round. Follow benchmark/RUN.md exactly.
I have approved everything it lists. Do not stop to ask me.
Stop only for the cases under "Needs the human".
Send me one short progress message every 15 minutes.
When the round is complete: merge it to main, then give me the summary.
```

- The LLM must be able to run shell commands and call the GitHub pull request tools (list under "Approve up front").
- That is all. Everything else is in this file and in the code.

## Before you start (only you can do these)
1. `AI_GATEWAY_API_KEY` is set in the environment of the session.
2. Credits: at least US$ 80. The preflight reads the balance and refuses the round if it does not cover the projected cost times 1.3.
3. Key budget: room for US$ 80 beyond what the key has used. The budget of a key is cumulative and cannot be read by the runner; it shows as HTTP 402. (On 2026-11-13 the key had used US$ 150.43 of 150.)
4. Everything is committed. The index version is the commit SHA: the questions, `knowledge/` and `harness/` must not change during the round. A resume after a change mixes two versions in one run.
5. The session works on its own branch, started from `main`.

## Expect

Two runs per candidate, Base (`baseline`) and Agent E2 (`agent-e2`), and the frontier reference in one mode, `web` (search available, Opus decides whether to use it); every question of the run set (196 on 2026-11-14), 5 runs each, judge openai/gpt-6.1-terra. Projected from the validity sample of 2026-11-14 (Gemma, 9 questions: US$ 0.0026 and 33 s per Agent E2 answer on the gateway, 2 model calls each) and the model prices; Opus from the round of 2026-11-13. Read these as plus or minus 30%; the preflight gives the real numbers before the round starts.

| Run folder | Modes | Answers | Request settings | Time | Cost US$ |
|---|---|---|---|---|---|
| `<date>-gemma-4-31b-it` | baseline, agent-e2 | 1,960 | default | about 50 min | about 3 |
| `<date>-qwen3.8-27b` | baseline, agent-e2 | 1,960 | reasoning off | about 50 min | about 3 |
| `<date>-muse-glimmer-30b` | baseline, agent-e2 | 1,960 | reasoning off | about 60 min | about 7 |
| `<date>-claude-opus-5.5` | web | 980 | effort medium, 8,000 tokens | about 70 min | about 27 |
| Total | | 6,860 | | 1.5 to 2 hours | about 40 (52 with the safety factor) |

- The four runs go in parallel, so the round takes as long as the slowest run (Opus, at its starting concurrency of 3; the runner raises it while the provider allows).
- An Agent E2 answer sends about 17,000 input tokens over its 2 model calls (the case call about 1,500, the answer call about 15,000 with the reading set), against about 400 for Base.
- Add about 3 minutes for the preflight (under US$ 1) and 1 relaunch: one command lives 2 hours, the runner stops at 110 minutes.
- The projection is checked again before anything long starts. If it exceeds the credits, `max_cost_usd` (150) or `max_hours` (6) in [`benchmark/runner/config.yaml`](runner/config.yaml), the round does not start.

## What happens

1. Preflight (`preflight.py`): credits; a sample of 7 questions (6 multiple-choice text questions and 1 screenshot question) in every mode of every run, with the real code and settings; the first request setting of each model that gives clean answers is chosen. A model with no clean setting stops the round before it spends anything.
2. Four `run.py` in parallel, one folder per model: `benchmark/results/<date>-<model>/`.
3. Health check inside each run: stops it when 25% of the last 40 answers are cut off, unreadable or failed.
4. Recovery (table below).
5. When all four are complete: [`benchmark/results/README.md`](results/README.md) (one analysis of all runs, written by `summarize.py`); the run folders of earlier rounds move to `project/archive/benchmark-results-before-<date>/`. The retrieval check outputs (`retrieval-<date>/`) stay.

## Steps for the LLM

1. Check `test -n "$AI_GATEWAY_API_KEY"` and `git status` (clean). If the key is missing: stop and tell the human.
2. Start the round in the background: `python3 benchmark/runner/run_all.py --max-minutes 110`. Use the longest background timeout (7,200,000 ms).
3. Every 15 minutes read `benchmark/results/.progress.txt` and send the human one line: answers done and errors per model, time left. Schedule the next check with `send_later` (15 minutes) or `ScheduleWakeup`. Never poll with `sleep`.
4. When the command ends, read its exit code and last lines:

| Exit | Meaning | What to do |
|---|---|---|
| 0 | Round complete | Go to "After the round" |
| 3 | Stopped at the time limit | Relaunch `python3 benchmark/runner/run_all.py --resume --max-minutes 110`. Repeat until 0. No other change |
| 4 | Preflight failed or the credits do not cover the round | Read the printed reason. A setting problem: nothing to fix by hand, the next settings were already tried. Credits: stop and tell the human the amount |
| 5 | A run produced invalid answers on its last settings | Stop and report: model, the printed reason, the run folder |
| 6 | The gateway refused (HTTP 402, 401, 403) | Stop and tell the human: raise the key budget or add credits, then say "resume". Then run `run_all.py --resume --max-minutes 110` |
| 7 | Some runs complete, others failed | Stop and report the list printed under "Round status". Do not merge a partial round |
| 1, other | The orchestrator itself crashed | Relaunch once with `--resume`. A second crash: stop and report the traceback |

   Recovery the runner does by itself, without you:
   - a run that crashed is relaunched with `--resume` (2 times);
   - answers that failed (HTTP 5xx, 429 that outlasted the retries) are retried the same way;
   - a run whose answers are invalid with the current settings starts again from the beginning with the next settings of its model (`model_params` in `config.yaml`); the invalid folder is kept and archived at the end;
   - a run stopped at the time limit continues where it stopped.

5. Do not edit `knowledge/`, [`benchmark/questions/`](questions), `harness/` or [`benchmark/runner/`](runner) during the round. If a defect needs a code change, stop and report; do not patch a running round.

## After the round

1. `ls benchmark/results`: four run folders, [`README.md`](results/README.md) and the retrieval check outputs (`retrieval-<date>/`), nothing else. Read [`README.md`](results/README.md).
2. `python3 project/tools/lint.py` reports 0 problems; `python3 -m unittest harness/test_tools.py` and `python3 -m unittest benchmark/runner/test_runner.py` pass. Read the results, not only the exit codes.
3. Add one entry to [`project/plan.md`](../project/plan.md) (Decisions, latest first): what ran, the final scores, time and cost against the projection, anything unexpected. Update the "Result so far" cells in [`benchmark/models.md`](models.md), section 4, from the README.
4. Commit everything (run folders without `traces.jsonl`, [`README.md`](results/README.md), the archive move, the plan and models changes). The message describes the change in plain words and names no model.
5. Push the session branch, open a pull request, merge it with a merge commit (not squash), and check that `main` holds [`benchmark/results/README.md`](results/README.md). Do this yourself in the same session.
6. Reply to the human: the Final score table and the Reading lines of the README, actual time and cost against the projection, anything the human must decide.

## Approve up front

Give these before the round so nothing waits for a click.

- Shell, run in the background up to 2 hours each:
  - `python3 benchmark/runner/run_all.py *`, `python3 benchmark/runner/preflight.py *`, `python3 benchmark/runner/summarize.py *`;
  - `python3 project/tools/lint.py`, `python3 -m unittest harness/test_tools.py`, `python3 -m unittest benchmark/runner/test_runner.py`;
  - reading: `cat`, `ls`, `tail`, `head`, `test -n "$AI_GATEWAY_API_KEY"`, `git status`, `git diff`, `git log`;
  - `git add`, `git commit`, `git push -u origin <session branch>`, `git fetch`, `git merge origin/main` (only if `main` moved).
- Edit and write: [`project/plan.md`](../project/plan.md), [`benchmark/models.md`](models.md), `benchmark/results/**`, `project/archive/**`.
- GitHub pull request tools: create, list, read and merge (`mcp__github__create_pull_request`, `mcp__github__list_pull_requests`, `mcp__github__pull_request_read`, `mcp__github__merge_pull_request`, `mcp__github__update_pull_request`).
- Scheduling: `send_later` (`mcp__claude-code-remote__send_later`) or `ScheduleWakeup`, for the 15-minute check.
- Network from the session: `ai-gateway.vercel.sh` (models, embeddings, search) and public web pages (the Opus `web` mode fetches pages the model chooses).
- Money: the credits and key budget under "Before you start". The runner spends nothing else.

## Needs the human

Only these stop the round:
- credits or key budget used up (exit 6), or credits too low at the start (exit 4);
- no clean request setting for a model, or invalid answers on its last setting (exits 4, 5);
- a failure the table above does not recover (exit 7, second crash);
- a merge conflict that is not in [`project/plan.md`](../project/plan.md) or [`benchmark/models.md`](models.md).

## Why the preflight and the health check exist

- The first full benchmark (2026-11-12) was accepted on "0 errors". No call had failed, but reasoning models spent their 4,000 tokens thinking: Qwen answered 85% of its baseline questions with a cut-off text, 549 of its 1,350 multiple-choice answers had no readable letter, and the run took 512 minutes.
- A valid answer (it can be scored) is a different property from a correct answer. The first is checked on a sample before the long run and while it goes; the second is the score.
- Every setting that decides validity (reasoning, `max_tokens`) is chosen by the sample and saved in the run folder's `config.json`.

## A smaller run

- One model, one mode: `python3 benchmark/runner/run.py --models google/gemma-4-31b-it --modes agent-e2 --runs 1 --questions L4-04`.
- `run.py --dry-run` prints the answers and a rough cost. It undercounts a model that thinks. Trust `preflight.py --models <id>` instead.
- `python3 benchmark/runner/run_all.py --dry-run` prints the plan of the round without any call.
