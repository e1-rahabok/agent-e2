# Retrieval check

What it measures, why it is needed, how to read the result, and what to do when the score is low. For the author and for whoever changes the knowledge base or the harness. Not indexed.
Script: [benchmark/runner/retrieval_eval.py](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/retrieval_eval.py). Benchmark design: [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), section 9.

## Why it is needed
- A wrong answer has three possible causes: the knowledge base lacks the fact, retrieval did not bring the file to the model, or the model misread a file it had. The benchmark score mixes all three.
- The retrieval check isolates the second cause. No model is called, so it costs nothing and runs in seconds.
- It caps classic mode. A model cannot use a file it never sees: if 75% of the needed files reach the context, classic mode answers from at most those files, however good the model is.
- It catches regressions. Every new knowledge file changes word statistics and ranking. A file added for one chapter can push another question's file out of the top results. Without this check, the drop would surface only in the next benchmark, mixed with model noise.
- It keeps changes honest. Rule (`CLAUDE.md`, Validation): a change to structure or retrieval needs a before and after number. This check gives that number for every change set.
- Paused (author, 2026-11-12) until the whole question bank is revamped: the questions and their needed files are changing. Reactivated after the revamp, with a new baseline.

## What it does
- Input: every benchmark question that lists `knowledge` ids, the files a correct answer depends on ([benchmark/README.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/README.md)).
- For each question it runs the same retrieval classic mode uses, on the same `## Prompt` text the model sees, options included:
  1. Search: the top 6 files (`--k`, default 6).
  2. Classic context: the search hits (`classic_k: 6`), plus the troubleshooting flow first when the question reads as troubleshooting (`route_troubleshooting`), plus the `same_name`, `related` and `internal_derive` links of the top 2 hits, cut to the context budget (`context_tokens: 16000`). Settings: [benchmark/runner/config.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/config.yaml).
- It never drops an unknown id: a needed file that no longer exists (moved, renamed) stops the check, because dropping it would raise recall falsely. Moved files go in [project/tools/moved.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/project/tools/moved.yaml).

```bash
python3 benchmark/runner/retrieval_eval.py                       # keyword (BM25), offline
python3 benchmark/runner/retrieval_eval.py --questions 0062,0067  # some questions
python3 benchmark/runner/retrieval_eval.py --set expand_derive=false   # try a setting
AI_GATEWAY_API_KEY=... python3 benchmark/runner/retrieval_eval.py --embeddings   # hybrid, as in benchmark runs
```

## How to read the result
- One row per question:

| Column | Meaning |
|---|---|
| Needed | Number of `knowledge` files the question lists |
| Search top 6 | Needed files among the 6 best search results |
| Classic context | Needed files in the context the model receives |
| Missed in context | The needed files that did not arrive |

- Summary line, four numbers:
  - **Recall@6 search**: share of all needed files found by search alone. It measures ranking.
  - **Recall classic context**: share of all needed files that reach the model. The number that caps classic mode.
  - **Questions with every needed file in context**: questions where nothing is missing. A question missing one of three files can still be answered wrong.
  - **Main file missing from context**: questions whose `knowledge_main` did not arrive, out of the questions that have one. Each is a defect.
- Read the context numbers first. A search drop with no context drop means link expansion still brings the file; the model sees the same files. Example 2026-11-07: search recall@6 fell from 65% to 64% (questions 0062 and 0067 each lost one file from the top 6), context stayed at 75% and 55 of 90: no effect on answers.
- Compare against the previous run, question by question, not only the totals. Two questions can swap (one gains, one loses) with no change in the total. Save both outputs and `diff` them.
- Agentic mode is not measured: the agent searches several times with its own queries. A file missed here can still be found there, but classic mode is the floor.
- Limits:
  - the needed files are the question writer's judgment; a missing id in a question makes recall look better than it is;
  - a file counted as in context can be cut by the budget, so only its start reaches the model;
  - BM25 and hybrid give different numbers. Compare like with like, and record the mode.
- Current numbers and history: [project/plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md), M3.

## What is a good number
- Levels agreed by the author (Q130, 2026-11-12). Last numbers before the pause (2026-11-11, 95 questions): classic context recall 78%, 61 of 95 complete (64%): bad.

### Why the retrieval number must be higher than the release score
- Release gate ([benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), section 7.5): final score at least 85% in agentic mode, Level 400 at least 80%, confident-wrong at most 3%.
- In classic mode the answer can be no better than its context. Roughly: answer accuracy ≈ (questions with every needed file) × (share the model gets right when it has them) + a little from the model's own knowledge.
- The model is not perfect even with the right files. If it gets 95% right with complete context, 85% needs about 90% of questions complete (0.90 × 0.95 ≈ 0.85).
- So the retrieval bar sits above the release bar, not at it.
- A missing file also drives confident-wrong answers: the model answers from Level 300 public knowledge, the very misconception the knowledge base exists to correct.

### Levels (classic mode, BM25 and hybrid both reported)
| Level | Main file in context | Complete questions | Context recall | Meaning |
|---|---|---|---|---|
| Bad | below 100% | below 80% | below 90% | The model is starved; a benchmark mostly measures retrieval |
| Good enough to release | 100% (each miss fixed or explained) | at least 90% | at least 95% | Leaves room for the 85% gate after model errors |
| Target | 100% | at least 97% | at least 98% | Matches the 99% answer target |
| Perfect | 100% | 100% | 100% | Not a goal; see below |

- Percent, not counts: the number of questions moves.
- Main file: the question's `knowledge_main` ([benchmark/README.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/README.md)), the file that holds the answer or the misconception. The check prints it as the fourth number, over the questions that have one.
- Held-out set ([benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), section 10): within 5 points of the visible set.

- Search recall@6 has no gate: it is a diagnostic for ranking. Context is what the model reads.
- Agentic mode, the shipped mode, searches again and can fetch what classic missed. It is measured by the benchmark, not here. Classic mode is the floor and the fallback, so it carries these levels; they are conservative for the agentic score.
- Read the last numbers this way: 61 of 95 complete (64%) means about 1 question in 3 lacks at least one needed file: the Bad band, about 25 points short of release.

### Is perfect applicable?
- No, as a target. 100% is possible on paper and still not the aim:
  - The key is a human judgment: each question's `knowledge` list is what its writer thought necessary. Some lists name a file the answer does not strictly need; some miss one. 100% against an imperfect key is not 100% of what matters.
  - Overfitting: the last few percent are reached by tuning files and links to these 90 prompts. That raises this number without helping a real user's question. The held-out set ([benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), section 10) would expose it.
  - The budget is finite: a question that needs 7 files competes for 16K tokens; cutting other context to fit it can hurt elsewhere.
  - Real users phrase questions in ways no set covers; a perfect score here does not carry over.
- Perfect is the right goal for one thing, and it is the gate: no question misses its main file (`knowledge_main`). A miss of a supporting file is tolerable; a miss of the main file is a defect to fix every time.
- Watch the held-out set: when it scores clearly below the visible set, retrieval is being fitted, not improved.

## When the score is bad
- First decide what kind of bad:
  - **A drop after a change**: compare the per-question rows of before and after. Which questions lost a file, and which new file took its place?
  - **A low level overall**: list the files in "Missed in context" across all questions. Files missed again and again point to a structural cause.
- Then find the cause of each miss, from the cheapest fix:

| Cause | Sign | Fix |
|---|---|---|
| Wrong or stale `knowledge` id in the question | The listed file does not hold the fact; a better file is in context | Fix the question's `knowledge` list |
| The file does not use the user's words | Prompt words absent from the file (a counter name, an esxtop field, a screen label) | Add the term to the file, a misconception line in the user's words, or a glossary synonym |
| The fact sits in a long file on another topic | Right file, rank 7-15 | Move the fact to the file whose topic matches, or split the file |
| A new file outranks the right one | Miss started after a change set; the new file is in context instead | Make the new file specific, or link the right file from it (`related`, `internal_derive`) |
| Files that belong together are not linked | One file in context, its partner missing | Add `same_name`, `related` or `internal_derive` links |
| Budget too small | File ranked inside the list but cut | Shorten the files ahead of it; test a larger `context_tokens` |
| Ranking problem across many questions | Same pattern in many rows | A harness experiment: query expansion, hybrid search, re-ranker, routing |

- Measure each fix with the check before keeping it. Keep a fix only when context recall or complete questions go up, or stay the same while the content becomes more correct (record that reason in the plan).
- Never fit the knowledge base to one question: a fix must be a general fact, term or link that helps every question on the topic. The held-out set guards against fitting ([benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), section 10).
- Record every run in [project/plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md) (M3): date, change, mode, context recall, complete questions, and the questions that gained or lost.
