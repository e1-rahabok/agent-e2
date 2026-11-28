# Run a benchmark round

How to run the full benchmark round, what it costs, how long it takes and what the runner does when something fails. The full round runs only before a milestone of the workspace's [ROADMAP.md](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/ROADMAP.md) is closed, and it stops when it has spent US$ 100 (R-E2-030 and R-E2-031 in [test-spending.md](../project/requirements/test-spending.md)). Between milestones, the free checks and the answer set test each change. Not indexed.
Runner details: [benchmark/runner/README.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/README.md). Method: [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md).

## Give this prompt to your LLM

```text
Run the full benchmark round for milestone M<n>. Follow benchmark/RUN.md exactly.
I have approved everything it lists. Do not stop to ask me.
Stop only for the cases under "Needs the human".
Send me one short progress message every 15 minutes.
When the round is complete: merge it to main, then give me the summary.
```

- The LLM needs to run shell commands and call the GitHub pull request tools (the list is under "Approve up front").
- Nothing else is needed. The rest is in this file and in the code.

## Before you start (only you can do these)
1. `AI_GATEWAY_API_KEY` is set in the environment of the session.
2. Credits: at least US$ 30 (the projection is about US$ 21 with the safety factor). The preflight reads the balance and refuses the round if the balance is below the projected cost times 1.3.
3. Budgets: check both the key's budget and the team's budget (Vercel dashboard, AI Gateway, API Keys and Budgets & Spend). Each needs room for US$ 25, the most a round spends, on top of what it has already used, and its refresh period must not reset in the middle of the round. The runner cannot read either budget. An empty one shows as HTTP 402, and the message says which one ("Team budget exceeded"). Before the round, tell the human the amounts and the periods.
4. Everything is committed. The index version is the commit SHA, so the questions, `knowledge/` and `harness/` must not change during the round. A resume after a change would mix two versions in one run.
5. The session works on its own branch, started from `main`.
6. The round serves the milestone named with `--milestone` (the workspace's open milestone, such as `M3`), and its summary names it. It is not yet the release gate. The held-out set of 30 ([benchmark/design.md](design.md), section 7.5) is drawn at release and does not exist yet, so that gate is not read. The run set is every question with status `draft` or `reviewed`. Most are drafts (count: `python3 project/tools/question_coverage.py`), so the scores are read before the author has reviewed the questions (Q-E2-256).
7. Commands use `python3`; on a machine where only `python` exists (Windows), use `python`.

## Expect

Release 1.0 runs Gemma 4 31B (SCOPE-6 in the workspace's [brief](https://github.com/e1-rahabok/private-cloud-workspace/blob/main/spec/brief.md)), so the round asks it twice, as Base (`baseline`) and as Agent E2 (`agent-e2`). The frontier reference runs in one mode, `web`: search is available and Opus decides whether to use it. Qwen and Muse-Glimmer are left out until the model of the on-premises deployment is chosen (`release.runs` in [`runner_config.yaml`](runner/runner_config.yaml)). Every question of the run set is asked (291 ; questions with status `awaiting-input`, `retired` or `deferred` do not run): 3 runs each for Gemma, 1 for Opus (`runs` of each entry of `release.runs`). There is no judge, because every question is multiple choice (Q-E2-199).

The figures are scaled from the round of 2026-11-16 (5 runs each), the last one with the 32,000-token reading set. The list price is what the runner records; the gateway billed more, because providers charge above the list price and failed or retried calls also cost money. Read them as plus or minus 30%; the preflight gives the real numbers before the round starts.

| Run folder | Answers | Time | Cost US$, list price and billed |
|---|---|---|---|
| `<date>-gemma-4-31b-it` | 1,746 | about 2 hours | 5.00 and 7.80 |
| `<date>-claude-opus-5.5` | 291 | under 1 hour | 11.50 and 11.70 |
| Total | 2,037 | about 2 hours | 16.50 and 19.50 |

- Gemma runs the modes `baseline` and `agent-e2` at its default request settings. Opus runs the mode `web` at effort medium and 8,000 tokens.
- With the safety factor of 1.3, the projection is about US$ 21, under the limit of US$ 25.
- A later round reuses the Opus and Base answers whose questions have not changed, so a change to Agent E2 alone costs about US$ 7.
- The two runs go in parallel, so the round lasts as long as the slower run. Opus starts at a concurrency of 3; the runner raises it while the provider allows.
- An Agent E2 answer sends about 28,500 input tokens over its 2 model calls, against about 400 for Base. The case call takes about 1,500. The answer call takes about 27,000 with the reading set, against the 32,000 budget.
- Add about 3 minutes for the preflight (under US$ 1) and 1 or 2 relaunches. One command lives 2 hours and the runner stops at 110 minutes.
- The projection is checked again before anything long starts. If it is above the credits, `max_cost_usd` (25) or `max_hours` (6) in [`benchmark/runner/runner_config.yaml`](runner/runner_config.yaml), the round does not start.

### Spending stop and reused answers

- An answer whose inputs are unchanged since an earlier round is copied from that round's run folder, and no model is called for it (R-E2-029). Its `reused_from` column names the folder that first asked it, and it is scored against the current answer key. The inputs are listed in [`answer_reuse.py`](runner/answer_reuse.py): for Agent E2, any change to `knowledge/` or `harness/` asks every Agent E2 answer again; the reference and Base answers are asked again only when their question or their request changes.
- The folders of the round of 2026-11-16 have no inputs fingerprint, so the first round after it asks every answer. From then on, a round asks only what changed.
- While the round runs, it counts the money it has spent: the larger of the list price of the answers it asked and the drop in the gateway's credit balance since the preflight (R-E2-030). At US$ 25 it starts no new answer, lets the answers in progress finish, and exits with code 9.

## What happens

1. Preflight (`round_sample_check.py`): it checks the credits, then asks a sample of 7 questions (6 multiple-choice text questions and 1 screenshot question) in every mode of every run, with the real code and settings. For each model it picks the first request setting that gives clean answers. A model with no clean setting stops the round before anything is spent.
2. Two `run_executor.py` in parallel, one folder per model: `benchmark/results/<date>-<model>/`. Each first copies the answers whose inputs are unchanged since the earlier round, then asks the rest.
3. Health check inside each run: stops it when 25% of the last 40 answers are cut off, unreadable or failed.
4. Recovery (table below).
5. When both runs are complete, `round_summary.py` writes [`benchmark/results/README.md`](results/README.md), one analysis of all runs, with the milestone and the number of reused answers. The run folders of earlier rounds are deleted; git history keeps them, and the new folders hold the answers reused from them. The retrieval check outputs (`retrieval-<date>/`) stay.

## Steps for the LLM

1. Check `test -n "$AI_GATEWAY_API_KEY"` and that `git status` is clean. If the key is missing, stop and tell the human.
2. Start the round in the background with one command and no wrapper shell, `nohup` or `&`: `python3 benchmark/runner/round_executor.py --milestone M<n> --max-minutes 110`, with the milestone the human named. Without `--milestone` the round refuses to start (exit 2). A resume needs no milestone. Use the longest background timeout (7,200,000 ms). The system then reports when the command itself ends. A wrapped run reported the wrapper's end after seconds. The same rule applies to any run started by hand with `run_executor.py --resume`.
3. Every 10 minutes run `python3 benchmark/runner/round_alive_check.py` and send the human one line: per run, the verdict (ALIVE, DONE, STALLED, DEAD, MACHINE RESTARTED), good answers against the total, time left. Say "running" only when the command says ALIVE and the good-answer count moved since the last check. After STALLED, DEAD or MACHINE RESTARTED, relaunch with `python3 benchmark/runner/round_executor.py --resume --max-minutes 110` (it resumes every unfinished run, whatever stopped it) and tell the human. Schedule the next check with `send_later` or `ScheduleWakeup`, and never poll with `sleep`. The runner pushes answers and configs to the branch `snapshots/round-<date>` every 15 minutes, so do not commit run folders by hand during the round.
4. When the command ends, read its exit code and last lines:

| Exit | Meaning | What to do |
|---|---|---|
| 0 | Round complete | Go to "After the round" |
| 3 | Stopped at the time limit | Relaunch `python3 benchmark/runner/round_executor.py --resume --max-minutes 110`. Repeat until 0. No other change |
| 4 | Preflight failed or the credits do not cover the round | Read the printed reason. For a setting problem there is nothing to fix by hand, because the next settings were already tried. For credits, stop and tell the human the amount |
| 5 | A run produced invalid answers on its last settings | Stop and report: model, the printed reason, the run folder |
| 6 | The gateway refused (HTTP 402, 401, 403) | Stop and tell the human. The saved error shows which budget ran out (the team's or the key's). The human raises it or adds credits and says "resume"; then run `round_executor.py --resume --max-minutes 110`, which resumes the refused runs too |
| 8 | The gateway or a provider kept failing | The runner waits and resumes the same folder by itself (`release.outage_waits` times). Only when it gives up, stop and report the run and the error text. Do not change settings |
| 7 | Some runs complete, others failed | Stop and report the list printed under "Round status". Do not merge a partial round |
| 9 | The round spent its limit of US$ 25 | Stop and tell the human the amount spent. Never raise `max_cost_usd` |
| 1, other | The orchestrator itself crashed | Relaunch once with `--resume`. A second crash: stop and report the traceback |

   The runner recovers by itself from these:
   - a run that crashed is relaunched with `--resume`, up to 2 times;
   - answers that failed (HTTP 5xx, or 429 that outlasted the retries of up to `gateway_retry_minutes`) are retried the same way;
   - a gateway or provider outage (exit 8) never counts against the settings; the runner waits and resumes the same folder;
   - a run whose answers are invalid with the current settings starts again from the beginning with the next settings of its model (`model_params` in `runner_config.yaml`), and the invalid folder is kept and archived at the end;
   - a run stopped at the time limit continues where it stopped.

5. Do not edit `knowledge/`, [`benchmark/questions/`](questions), `harness/` or [`benchmark/runner/`](runner) during the round. If a defect needs a code change, stop and report it. Do not patch a running round.

## After the round

1. Run `ls benchmark/results`. It should show two run folders, [`README.md`](results/README.md) and the retrieval check outputs (`retrieval-<date>/`), nothing else. Read [`README.md`](results/README.md).
2. `python3 project/tools/rules_check.py` must report 0 problems, and `python3 -m unittest harness/test_harness.py` and `python3 -m unittest benchmark/runner/test_runner.py` must pass. Read the output, not only the exit codes.
3. Update the Gateway benchmark row of [`project/plan.md`](../project/plan.md) with the final scores, and its open work with anything unexpected. Time and cost against the projection go in the pull request text. Update the "Result so far" cells in [`benchmark/models.md`](models.md), section 4, from the README.
4. Commit everything: the run folders without `traces.jsonl`, [`README.md`](results/README.md), the archive move, and the plan and models changes. The commit message describes the change in plain words and names no model.
5. Delete nothing yourself. Tell the human that the branch `snapshots/round-<date>` can be deleted (a cloud session cannot). Push the session branch, open a pull request, merge it with a merge commit (not squash) and check that `main` holds [`benchmark/results/README.md`](results/README.md). Do all of this in the same session.
6. Reply to the human with the Final score table and the Reading lines of the README, the actual time and cost against the projection, and anything the human must decide.

## Approve up front

Give these before the round, so that nothing waits for a click.

- Shell, run in the background for up to 2 hours each:
  - `python3 benchmark/runner/round_executor.py *`, `python3 benchmark/runner/round_sample_check.py *`, `python3 benchmark/runner/round_summary.py *`;
  - `python3 project/tools/rules_check.py`, `python3 -m unittest harness/test_harness.py`, `python3 -m unittest benchmark/runner/test_runner.py`;
  - reading: `cat`, `ls`, `tail`, `head`, `test -n "$AI_GATEWAY_API_KEY"`, `git status`, `git diff`, `git log`;
  - `git add`, `git commit`, `git push -u origin <session branch>`, `git fetch`, `git merge origin/main` (only if `main` moved).
- Edit and write: [`project/plan.md`](../project/plan.md), [`benchmark/models.md`](models.md), `benchmark/results/**`.
- GitHub pull request tools: create, list, read and merge (`mcp__github__create_pull_request`, `mcp__github__list_pull_requests`, `mcp__github__pull_request_read`, `mcp__github__merge_pull_request`, `mcp__github__update_pull_request`).
- Scheduling: `send_later` (`mcp__claude-code-remote__send_later`) or `ScheduleWakeup`, for the 15-minute check.
- Network from the session: `ai-gateway.vercel.sh` (models, embeddings, search) and public web pages (in the Opus `web` mode the model chooses which pages to fetch).
- Money: the credits and the key budget under "Before you start". The runner spends nothing else.

## Needs the human

Only these stop the round.
- credits or key budget used up (exit 6), or credits too low at the start (exit 4);
- the round spent its limit of US$ 25 (exit 9). The limit is set by DESIGN-31, within the author's US$ 100 (CONSTRAINT-1). Only after the author raises `release.max_cost_usd`, `round_executor.py --resume --max-minutes 110` continues where the round stopped;
- no clean request setting for a model, or invalid answers on its last setting (exits 4, 5);
- a failure the table above does not recover (exit 7, second crash);
- a merge conflict that is not in [`project/plan.md`](../project/plan.md) or [`benchmark/models.md`](models.md).

## Why the preflight and the health check exist

- The first full benchmark was accepted on "0 errors". No call had failed, but the reasoning models spent their 4,000 tokens thinking. Qwen answered 85% of its baseline questions with a cut-off text, 549 of its 1,350 multiple-choice answers had no readable letter, and the run took 512 minutes.
- A valid answer (one that can be scored) is not the same as a correct answer. Validity is checked on a sample before the long run and again while it goes. Correctness is the score.
- The sample chooses every setting that decides validity (reasoning, `max_tokens`) and saves it in the run folder's `config.json`.

## A smaller run

- One model, one mode: `python3 benchmark/runner/run_executor.py --models google/gemma-4-31b-it --modes agent-e2 --runs 1 --questions L4-004`.
- A smaller run also copies unchanged answers from the folders in [`benchmark/results/`](results); `--no-reuse` asks every answer.
- `run_executor.py --dry-run` prints the answers and a rough cost. It undercounts a model that thinks, so trust `round_sample_check.py --models <id>` instead.
- `python3 benchmark/runner/round_executor.py --dry-run` prints the plan of the round without any call.
