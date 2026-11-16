# Benchmark report: 20261116-muse-glimmer-30b

- Index version: `c364e1cc4c8f`. Retrieval: hybrid. Sampling: {"meta/muse-glimmer-30b": {"temperature": 1.0, "top_p": 0.95, "top_k": 64}}. Runs: 5.
- Questions: 291 (deterministic 291, judged 0; text 210, table 74, screenshot 8; level 100: 7, level 200: 11, level 300: 111, level 400: 162). Skipped: none.
- Answers: 2910 scored, 0 failed.

## Final score

| Model | Mode | Final | ± margin | Worst run | Luck | Confident wrong | Override |
|---|---|---|---|---|---|---|---|
| meta/muse-glimmer-30b | agent-e2 | 84% | 4% | 69% | 25% | 15% | 2% |
| meta/muse-glimmer-30b | baseline | 41% | 6% | 21% | 42% | 58% | - |

## Consensus of 3, projected

What the shipped setting `consensus_samples: 3` would give: multiple-choice letters stand only when 3 samples agree; otherwise Unsure. Projected from the recorded runs, no new model call (`report.py`, function `consensus`). Judged answers unchanged.

| Model | Mode | Final | Final, consensus | Confident wrong | Confident wrong, consensus | Multiple choice: confident wrong, consensus | Multiple choice: Unsure, consensus |
|---|---|---|---|---|---|---|---|
| meta/muse-glimmer-30b | agent-e2 | 84% | 75% | 15% | 5% | 5% | 20% |

## Release gate

Agent E2. Reference: anthropic/claude-opus-5.5, web mode (not in this benchmark: gap not read).

| Model | Gate | Value | Limit | Pass |
|---|---|---|---|---|
| meta/muse-glimmer-30b | Final score | 84% | at least 85% | no |
| meta/muse-glimmer-30b | Level 400 | 83% | at least 80% | yes |
| meta/muse-glimmer-30b | Confident wrong | 15% | at most 3% | no |

- Not read here: no up-front misconception (lines marked `up_front`) stated as true (author check), and the held-out set at most 11 points below the development set (separate run). Method: `benchmark/design.md`, section 7.5.

## Sub-scores

| Model | Mode | Deterministic | Judged | Text | Table | Screenshot | Level 100 | Level 200 | Level 300 | Level 400 |
|---|---|---|---|---|---|---|---|---|---|---|
| meta/muse-glimmer-30b | agent-e2 | 84% | - | 84% | 85% | 92% | 100% | 96% | 85% | 83% |
| meta/muse-glimmer-30b | baseline | 41% | - | 36% | 51% | 60% | 71% | 64% | 43% | 37% |

- Final: mean question credit over all questions, 0-100%. Every question weighs the same.
- Question credit = the mean of its runs. Deterministic: share of runs with the exact letters. Judged: mean judge score / 3. Worst run: the same score with each question on its lowest run (consistency; not a gate).
- Sub-scores: the same mean within one group. By answer type, by input type (a question counts for every input it includes), by level.
- Luck: share of questions whose credit differs between runs. Confident wrong: share of answers that are wrong and not Unsure (judged: score 0, not unsure).
- Override: share of Agent E2 answers that state the misconception although every needed file was in the context: the model kept its own belief over the knowledge base. Target: 0. See `benchmark/models.md`, section 1.
- Method: `benchmark/design.md`, sections 3 and 7.4.

## Deterministic answers: luck-free scores

| Model | Mode | Track | Stable correct | ± margin | Luck | Stable unsure | Confident wrong | Unsure | Accuracy when answered |
|---|---|---|---|---|---|---|---|---|---|
| meta/muse-glimmer-30b | agent-e2 | text | 69% | 5% | 26% | 0% | 16% | 0% | 84% |
| meta/muse-glimmer-30b | baseline | text | 20% | 5% | 42% | 0% | 59% | 1% | 41% |
| meta/muse-glimmer-30b | agent-e2 | vision | 88% | 23% | 12% | 0% | 8% | 0% | 92% |
| meta/muse-glimmer-30b | baseline | vision | 50% | 35% | 25% | 0% | 40% | 0% | 60% |

- Stable correct: share of questions answered correctly in every run: a known answer, not a guess. Consistency, not the final score (the final score is the mean of the runs).
- Luck: share of questions correct in some runs but not all. Counted as not known.
- Stable unsure: share of questions where the model chose Unsure in every run.
- Confident wrong: share of answers that are wrong and not Unsure (wrong letters, partly right, Unsure mixed with other letters, unparseable). The answers that mislead an operator. Target: near 0.
- Accuracy when answered: exact share among answers that were not Unsure.

## Deterministic answers: scores

| Model | Mode | Track | Exact | Partial | Majority | ± margin | Consistency | Misconception | Parse fail | Recall | Steps | Tokens | Latency s | Cost US$ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| meta/muse-glimmer-30b | agent-e2 | text | 84% | 95% | 87% | 4% | 72% | 2% | 0% | 97% | 2.0 | 34055 | 28.3 | 19.853 |
| meta/muse-glimmer-30b | baseline | text | 40% | 73% | 45% | 6% | 27% | 14% | 0% | - | 1.0 | 2199 | 7.8 | 2.216 |
| meta/muse-glimmer-30b | agent-e2 | vision | 92% | 96% | 88% | 23% | 88% | 0% | 0% | 84% | 2.0 | 35554 | 26.6 | 0.568 |
| meta/muse-glimmer-30b | baseline | vision | 60% | 73% | 62% | 34% | 50% | 25% | 0% | - | 1.0 | 4462 | 9.7 | 0.096 |

- Exact and Partial: mean over all runs. Majority: most common answer per question. Margin: 95% interval on Majority from the number of questions.
- Consistency: share of questions answered identically in every run. Recall: share of the question `knowledge` ids whose text reached the model (Agent E2 only: the reading set and any gap follow-up). Steps: model calls per answer.

## Deterministic answers: exact score by technology

| Model | Mode | cpu | gpu | memory | network | storage | system |
|---|---|---|---|---|---|---|---|
| meta/muse-glimmer-30b | agent-e2 | 83% | 100% | 86% | 88% | 84% | 86% |
| meta/muse-glimmer-30b | baseline | 34% | 0% | 41% | 48% | 46% | 38% |

## Deterministic answers: exact score by task

| Model | Mode | decide-capacity | explain-mechanism | judge-setting | read-metric | troubleshoot |
|---|---|---|---|---|---|---|
| meta/muse-glimmer-30b | agent-e2 | 79% | 87% | 89% | 86% | 82% |
| meta/muse-glimmer-30b | baseline | 35% | 37% | 34% | 45% | 45% |

## Hardest questions (Agent E2, or web for the frontier reference)

| Question | Mean credit | Common wrong answers or missed points |
|---|---|---|
| 0019 | 0% | A,B,C,D,E,G ×5 |
| 0110 | 0% | A,C,I ×5 |
| 0383 | 0% | A,D,F,G ×5 |
| 0405 | 0% | A,B,D,E,G,H ×5 |
| 0422 | 0% | A,C,D,G ×5 |
| 0433 | 0% | B,D,E ×5 |
| 0012 | 0% | A,C,F ×3, B,C,F ×1, C,F ×1 |
| 0104 | 0% | A,B,C,D,E,F,L ×2, A,B,C,D,E,F,K,L ×2, A,B,C,D,E,K ×1 |
| 0148 | 0% | A,D,E ×5 |
| 0215 | 0% | C,D,F,G,H ×4, D,F,H ×1 |

Traces: `traces.jsonl` in this folder (one line per answer).
