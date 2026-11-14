# Retrieval check

What it measures, why it is needed, how to read the result, and what to do when the score is low. For the author and for whoever changes the knowledge base or the harness. Not indexed.
Script: [benchmark/runner/retrieval_eval.py](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/retrieval_eval.py). Benchmark design: [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), section 9.

## Why it is needed
- A wrong answer has three possible causes: the knowledge base lacks the fact, retrieval did not bring the file to the model, or the model misread a file it had. The benchmark score mixes all three.
- The retrieval check isolates the second cause. No model is called, so it costs nothing and runs in seconds.
- It caps Agent E2. A model cannot use a file it never sees: if 75% of the needed files reach the reading set, Agent E2 answers from at most those files (plus a gap follow-up), however good the model is.
- It catches regressions. Every new knowledge file changes word statistics and ranking. A file added for one chapter can push another question's file out of the top results. Without this check, the drop would surface only in the next benchmark, mixed with model noise.
- It keeps changes honest. Rule (`CLAUDE.md`, Validation): a change to structure or retrieval needs a before and after number. This check gives that number for every change set.
- Runs on the run set as it is (author, 2026-11-13, Q206), re-baselined when the question set changes.

## What it does
- Input: every benchmark question that lists `knowledge` ids, the files a correct answer depends on ([benchmark/README.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/README.md)).
- For each question it builds Agent E2's reading set ([harness/planner.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/planner.py)) from the code-only reading of the question (no model call), on the same `## Prompt` text the model sees, options included:
  1. Search: the top 6 files (`--k`, default 6).
  2. Reading set: the tiers of [harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md), section 4.2 (flow, named files, search, mechanism links, one search per claim, the rest), cut to the context budget (`context_tokens: 16000`). Settings: [benchmark/runner/config.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/config.yaml).
- It never drops an unknown id: a needed file that no longer exists (moved, renamed) stops the check, because dropping it would raise recall falsely. Moved files go in [project/tools/moved.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/project/tools/moved.yaml).

```bash
python3 benchmark/runner/retrieval_eval.py                       # keyword (BM25), offline
python3 benchmark/runner/retrieval_eval.py --questions 0062,0067  # some questions
python3 benchmark/runner/retrieval_eval.py --set plan_section_tokens=250   # try a setting
python3 benchmark/runner/retrieval_eval.py --no-options                    # the stem only, as an operator asks: the field reading
AI_GATEWAY_API_KEY=... python3 benchmark/runner/retrieval_eval.py --embeddings   # hybrid, as in benchmark runs
```

## How to read the result
- One row per question:

| Column | Meaning |
|---|---|
| Needed | Number of `knowledge` files the question lists |
| Search top 6 | Needed files among the 6 best search results |
| Reading set | Needed files in the reading set the model receives |
| Missed in the reading set | The needed files that did not arrive |

- Summary line, four numbers, and a line of complete questions by number of needed files:
  - **Recall@6 search**: share of all needed files found by search alone. It measures ranking.
  - **Recall reading set**: share of all needed files that reach the model. The number that caps Agent E2.
  - **Questions with every needed file in context**: questions where nothing is missing. A question missing one of three files can still be answered wrong.
  - **Main file missing from the reading set**: questions whose `knowledge_main` did not arrive, out of the questions that have one. Each is a defect.
- Read the reading-set numbers first. A search drop with no reading-set drop means the plan still brings the file through a link, a name or a claim; the model sees the same files.
- Compare against the previous run, question by question, not only the totals. Two questions can swap (one gains, one loses) with no change in the total. Save both outputs and `diff` them.
- Limits:
  - the needed files are the question writer's judgment; a missing id in a question makes recall look better than it is;
  - a file counted as in the reading set can be there as its best sections only (tiers 4-6), or cut by the budget;
  - the model's case (stage 1) can add files the code-only reading does not; it is not in this check yet (`--case-model`, planned);
  - BM25 and hybrid give different numbers. Compare like with like, and record the mode.
- Current numbers and history: [project/plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md), M3.

## What is a good number
- Levels agreed by the author (Q130, 2026-11-12). Baseline of the Agent E2 generation (2026-11-14, 196 questions): BM25 recall 76%, 109 of 196 complete (56%), main file missing on 25; hybrid recall 80%, 117 of 196 complete (60%), main file missing on 19: bad. After Q211 (2026-11-14) BM25 reads 77%, 110 of 196; current numbers: [project/plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md), M3. Output: [benchmark/results/retrieval-2026-11-14/](../benchmark/results/retrieval-2026-11-14/hybrid.md). Earlier generations are archived and not compared.

### Why the retrieval number must be higher than the release score
- Release gate ([benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), section 7.5): final score at least 85% on Agent E2, Level 400 at least 80%, confident-wrong at most 3%.
- The answer can be no better than its reading set. Roughly: answer accuracy ≈ (questions with every needed file) × (share the model gets right when it has them) + a little from the model's own knowledge.
- The model is not perfect even with the right files. If it gets 95% right with complete context, 85% needs about 90% of questions complete (0.90 × 0.95 ≈ 0.85).
- So the retrieval bar sits above the release bar, not at it.
- A missing file also drives confident-wrong answers: the model answers from Level 300 public knowledge, the very misconception the knowledge base exists to correct.

### Levels (the reading set, BM25 and hybrid both reported)
| Level | Main file in context | Complete questions | Context recall | Meaning |
|---|---|---|---|---|
| Bad | below 100% | below 80% | below 90% | The model is starved; a benchmark mostly measures retrieval |
| Good enough to release | 100% (each miss fixed or explained) | at least 90% | at least 95% | Leaves room for the 85% gate after model errors |
| Target | 100% | at least 97% | at least 98% | Matches the 99% answer target |
| Perfect | 100% | 100% | 100% | Not a goal; see below |

- Percent, not counts: the number of questions moves.
- Main file: the question's `knowledge_main` ([benchmark/README.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/README.md)), the file that holds the answer or the misconception. The check prints it as the fourth number, over the questions that have one.
- Held-out set ([benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), section 7.5): at most 11 points below the visible set.

- Search recall@6 has no gate: it is a diagnostic for ranking. The reading set is what the model reads.
- The gap follow-up of stage 6 can add a file after the draft; it is measured by the benchmark, not here.

### Is perfect applicable?
- No, as a target. 100% is possible on paper and still not the aim:
  - The key is a human judgment: each question's `knowledge` list is what its writer thought necessary. Some lists name a file the answer does not strictly need; some miss one. 100% against an imperfect key is not 100% of what matters.
  - Overfitting: the last few percent are reached by tuning files and links to the visible questions. That raises this number without helping a real user's question. The held-out set ([benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), section 7.5) would expose it.
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
