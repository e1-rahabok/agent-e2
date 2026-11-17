# Run a benchmark round

How to run the final benchmark round, what it costs, how long it takes and what the runner does when something fails. Not indexed.
Runner details: [benchmark/runner/README.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/README.md). Method: [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md).

## Give this prompt to your LLM

```text
Run the final benchmark round. Follow benchmark/RUN.md exactly.
I have approved everything it lists. Do not stop to ask me.
Stop only for the cases under "Needs the human".
Send me one short progress message every 15 minutes.
When the round is complete: merge it to main, then give me the summary.
```

- The LLM needs to run shell commands and call the GitHub pull request tools (the list is under "Approve up front").
- Nothing else is needed. The rest is in this file and in the code.

## Before you start (only you can do these)
1. `AI_GATEWAY_API_KEY` is set in the environment of the session.
2. Credits: at least US$ 100 (the projection is US$ 77 with the safety factor). The preflight reads the balance and refuses the round if the balance is below the projected cost times 1.3.
3. Budgets: check both the key's budget and the team's budget (Vercel dashboard, AI Gateway, API Keys and Budgets & Spend). Each needs room for the projected cost times 1.3 plus margin, on top of what it has already used, and its refresh period must not reset in the middle of the round. The runner cannot read either budget. An empty one shows as HTTP 402, and the message says which one ("Team budget exceeded"). On the key had used US$ 150.43 of 150. On the round stopped on the team budget of US$ 100, with US$ 47 left on the key. Before the round, tell the human the amounts and the periods.
4. Everything is committed. The index version is the commit SHA, so the questions, `knowledge/` and `harness/` must not change during the round. A resume after a change would mix two versions in one run.
5. The session works on its own branch, started from `main`.
6. This is a development round, not the release round. The held-out set of 30 ([benchmark/design.md](design.md), section 7.5) is drawn at release and does not exist yet, so that gate is not read. The run set is every question with status `draft` or `reviewed`. On 2026-11-16 that is 288 drafts and 3 reviewed, so the scores are read before the author has reviewed the questions (Q256).
7. Commands use `python3`; on a machine where only `python` exists (Windows), use `python`.

## Expect

Each candidate runs twice, as Base (`baseline`) and as Agent E2 (`agent-e2`). The frontier reference runs in one mode, `web`: search is available and Opus decides whether to use it. Every question of the run set is asked (291 ; questions with status `awaiting-input`, `retired` or `deferred` do not run), 5 runs each. There is no judge, because every question is multiple choice (Q199).

The projection comes from the validity sample (Gemma, 9 questions: US$ 0.0026 and 33 s per Agent E2 answer on the gateway, 2 model calls each) and the model prices. The Opus figures come from the round. They were scaled from the 226-question projection to 291 questions (x 1.29). Read them as plus or minus 30%; the preflight gives the real numbers before the round starts.

| Run folder | Modes | Answers | Request settings | Time | Cost US$ |
|---|---|---|---|---|---|
| `<date>-gemma-4-31b-it` | baseline, agent-e2 | 2,910 | default | about 80 min | about 4.5 |
| `<date>-qwen3.8-27b` | baseline, agent-e2 | 2,910 | reasoning off | about 80 min | about 4.5 |
| `<date>-muse-glimmer-30b` | baseline, agent-e2 | 2,910 | reasoning off | about 90 min | about 10 |
| `<date>-claude-opus-5.5` | web | 1,455 | effort medium, 8,000 tokens | about 105 min | about 40 |
| Total | | 10,185 | | about 2 hours | about 59 (77 with the safety factor) |

- The larger reading set adds about 11,000 input tokens to each of the 4,365 Agent E2 answers, which costs about US$ 5 to 10 more on the three candidates. Read the total as about US$ 66 (about 85 with the safety factor). The table rows above are from before this change. The preflight prices it for real.
- The four runs go in parallel, so the round lasts as long as the slowest run. That is Opus, at its starting concurrency of 3; the runner raises the concurrency while the provider allows.
- An Agent E2 answer sends about 28,500 input tokens over its 2 model calls, against about 400 for Base. The case call takes about 1,500. The answer call takes about 27,000 with the reading set, which averaged 20,000 tokens before the related tier and 27,000 after, against the 32,000 budget.
- Add about 3 minutes for the preflight (under US$ 1) and 1 relaunch. One command lives 2 hours and the runner stops at 110 minutes.
- The projection is checked again before anything long starts. If it is above the credits, `max_cost_usd` (150) or `max_hours` (6) in [`benchmark/runner/config.yaml`](runner/config.yaml), the round does not start.

## What happens

1. Preflight (`preflight_check.py`): it checks the credits, then asks a sample of 7 questions (6 multiple-choice text questions and 1 screenshot question) in every mode of every run, with the real code and settings. For each model it picks the first request setting that gives clean answers. A model with no clean setting stops the round before anything is spent.
2. Four `answer_questions.py` in parallel, one folder per model: `benchmark/results/<date>-<model>/`.
3. Health check inside each run: stops it when 25% of the last 40 answers are cut off, unreadable or failed.
4. Recovery (table below).
5. When all four runs are complete, `summary_all_runs.py` writes [`benchmark/results/README.md`](results/README.md), one analysis of all runs. The run folders of earlier rounds move to `project/archive/benchmark-results-before-<date>/`. The retrieval check outputs (`retrieval-<date>/`) stay.

## Steps for the LLM

1. Check `test -n "$AI_GATEWAY_API_KEY"` and that `git status` is clean. If the key is missing, stop and tell the human.
2. Start the round in the background with one command and no wrapper shell, `nohup` or `&`: `python3 benchmark/runner/run_round.py --max-minutes 110`. Use the longest background timeout (7,200,000 ms). The system then reports when the command itself ends. A wrapped run reported the wrapper's end after seconds. The same rule applies to any run started by hand with `answer_questions.py --resume`.
3. Every 10 minutes run `python3 benchmark/runner/check_round_alive.py` and send the human one line: per run, the verdict (ALIVE, DONE, STALLED, DEAD, MACHINE RESTARTED), good answers against the total, time left. Say "running" only when the command says ALIVE and the good-answer count moved since the last check. After STALLED, DEAD or MACHINE RESTARTED, relaunch with `python3 benchmark/runner/run_round.py --resume --max-minutes 110` (it resumes every unfinished run, whatever stopped it) and tell the human. Schedule the next check with `send_later` or `ScheduleWakeup`, and never poll with `sleep`. The runner pushes answers and configs to the branch `snapshots/round-<date>` every 15 minutes, so do not commit run folders by hand during the round.
4. When the command ends, read its exit code and last lines:

| Exit | Meaning | What to do |
|---|---|---|
| 0 | Round complete | Go to "After the round" |
| 3 | Stopped at the time limit | Relaunch `python3 benchmark/runner/run_round.py --resume --max-minutes 110`. Repeat until 0. No other change |
| 4 | Preflight failed or the credits do not cover the round | Read the printed reason. For a setting problem there is nothing to fix by hand, because the next settings were already tried. For credits, stop and tell the human the amount |
| 5 | A run produced invalid answers on its last settings | Stop and report: model, the printed reason, the run folder |
| 6 | The gateway refused (HTTP 402, 401, 403) | Stop and tell the human. The saved error shows which budget ran out (the team's or the key's). The human raises it or adds credits and says "resume"; then run `run_round.py --resume --max-minutes 110`, which resumes the refused runs too |
| 8 | The gateway or a provider kept failing | The runner waits and resumes the same folder by itself (`release.outage_waits` times). Only when it gives up, stop and report the run and the error text. Do not change settings |
| 7 | Some runs complete, others failed | Stop and report the list printed under "Round status". Do not merge a partial round |
| 1, other | The orchestrator itself crashed | Relaunch once with `--resume`. A second crash: stop and report the traceback |

   The runner recovers by itself from these:
   - a run that crashed is relaunched with `--resume`, up to 2 times;
   - answers that failed (HTTP 5xx, or 429 that outlasted the retries of up to `gateway_retry_minutes`) are retried the same way;
   - a gateway or provider outage (exit 8) never counts against the settings; the runner waits and resumes the same folder;
   - a run whose answers are invalid with the current settings starts again from the beginning with the next settings of its model (`model_params` in `config.yaml`), and the invalid folder is kept and archived at the end;
   - a run stopped at the time limit continues where it stopped.

5. Do not edit `knowledge/`, [`benchmark/questions/`](questions), `harness/` or [`benchmark/runner/`](runner) during the round. If a defect needs a code change, stop and report it. Do not patch a running round.

## After the round

1. Run `ls benchmark/results`. It should show four run folders, [`README.md`](results/README.md) and the retrieval check outputs (`retrieval-<date>/`), nothing else. Read [`README.md`](results/README.md).
2. `python3 project/tools/lint.py` must report 0 problems, and `python3 -m unittest harness/test_tools.py` and `python3 -m unittest benchmark/runner/test_runner.py` must pass. Read the output, not only the exit codes.
3. Add one entry to [`project/plan.md`](../project/plan.md) (Decisions, latest first) with what ran, the final scores, time and cost against the projection, and anything unexpected. Update the "Result so far" cells in [`benchmark/models.md`](models.md), section 4, from the README.
4. Commit everything: the run folders without `traces.jsonl`, [`README.md`](results/README.md), the archive move, and the plan and models changes. The commit message describes the change in plain words and names no model.
5. Delete nothing yourself. Tell the human that the branch `snapshots/round-<date>` can be deleted (a cloud session cannot). Push the session branch, open a pull request, merge it with a merge commit (not squash) and check that `main` holds [`benchmark/results/README.md`](results/README.md). Do all of this in the same session.
6. Reply to the human with the Final score table and the Reading lines of the README, the actual time and cost against the projection, and anything the human must decide.

## Approve up front

Give these before the round, so that nothing waits for a click.

- Shell, run in the background for up to 2 hours each:
  - `python3 benchmark/runner/run_round.py *`, `python3 benchmark/runner/preflight_check.py *`, `python3 benchmark/runner/summary_all_runs.py *`;
  - `python3 project/tools/lint.py`, `python3 -m unittest harness/test_tools.py`, `python3 -m unittest benchmark/runner/test_runner.py`;
  - reading: `cat`, `ls`, `tail`, `head`, `test -n "$AI_GATEWAY_API_KEY"`, `git status`, `git diff`, `git log`;
  - `git add`, `git commit`, `git push -u origin <session branch>`, `git fetch`, `git merge origin/main` (only if `main` moved).
- Edit and write: [`project/plan.md`](../project/plan.md), [`benchmark/models.md`](models.md), `benchmark/results/**`, `project/archive/**`.
- GitHub pull request tools: create, list, read and merge (`mcp__github__create_pull_request`, `mcp__github__list_pull_requests`, `mcp__github__pull_request_read`, `mcp__github__merge_pull_request`, `mcp__github__update_pull_request`).
- Scheduling: `send_later` (`mcp__claude-code-remote__send_later`) or `ScheduleWakeup`, for the 15-minute check.
- Network from the session: `ai-gateway.vercel.sh` (models, embeddings, search) and public web pages (in the Opus `web` mode the model chooses which pages to fetch).
- Money: the credits and the key budget under "Before you start". The runner spends nothing else.

## Needs the human

Only these stop the round.
- credits or key budget used up (exit 6), or credits too low at the start (exit 4);
- no clean request setting for a model, or invalid answers on its last setting (exits 4, 5);
- a failure the table above does not recover (exit 7, second crash);
- a merge conflict that is not in [`project/plan.md`](../project/plan.md) or [`benchmark/models.md`](models.md).

## Why the preflight and the health check exist

- The first full benchmark was accepted on "0 errors". No call had failed, but the reasoning models spent their 4,000 tokens thinking. Qwen answered 85% of its baseline questions with a cut-off text, 549 of its 1,350 multiple-choice answers had no readable letter, and the run took 512 minutes.
- A valid answer (one that can be scored) is not the same as a correct answer. Validity is checked on a sample before the long run and again while it goes. Correctness is the score.
- The sample chooses every setting that decides validity (reasoning, `max_tokens`) and saves it in the run folder's `config.json`.

## A smaller run

- One model, one mode: `python3 benchmark/runner/answer_questions.py --models google/gemma-4-31b-it --modes agent-e2 --runs 1 --questions L4-004`.
- `answer_questions.py --dry-run` prints the answers and a rough cost. It undercounts a model that thinks, so trust `preflight_check.py --models <id>` instead.
- `python3 benchmark/runner/run_round.py --dry-run` prints the plan of the round without any call.
