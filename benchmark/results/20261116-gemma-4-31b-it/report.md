# Benchmark report: 20261116-gemma-4-31b-it

- Index version: `89ffa8d47073`. Retrieval: hybrid. Sampling: {"google/gemma-4-31b-it": {"temperature": 1.0, "top_p": 0.95, "top_k": 64}}. Runs: 5.
- Questions: 291 (deterministic 291, judged 0; text 210, table 74, screenshot 8; level 100: 7, level 200: 11, level 300: 111, level 400: 162). Skipped: none.
- Answers: 2910 scored, 17 failed.

## Final score

| Model | Mode | Final | ± margin | Worst run | Luck | Confident wrong | Override |
|---|---|---|---|---|---|---|---|
| google/gemma-4-31b-it | agent-e2 | 79% | 5% | 59% | 33% | 21% | 2% |
| google/gemma-4-31b-it | baseline | 40% | 6% | 20% | 40% | 60% | - |

## Consensus of 3, projected

What the shipped setting `consensus_samples: 3` would give: multiple-choice letters stand only when 3 samples agree; otherwise Unsure. Projected from the recorded runs, no new model call (`report.py`, function `consensus`). Judged answers unchanged.

| Model | Mode | Final | Final, consensus | Confident wrong | Confident wrong, consensus | Multiple choice: confident wrong, consensus | Multiple choice: Unsure, consensus |
|---|---|---|---|---|---|---|---|
| google/gemma-4-31b-it | agent-e2 | 79% | 66% | 21% | 7% | 7% | 27% |

## Release gate

Agent E2. Reference: anthropic/claude-opus-5.5, web mode (not in this benchmark: gap not read).

| Model | Gate | Value | Limit | Pass |
|---|---|---|---|---|
| google/gemma-4-31b-it | Final score | 79% | at least 85% | no |
| google/gemma-4-31b-it | Level 400 | 74% | at least 80% | no |
| google/gemma-4-31b-it | Confident wrong | 21% | at most 3% | no |

- Not read here: no up-front misconception (lines marked `up_front`) stated as true (author check), and the held-out set at most 11 points below the development set (separate run). Method: `benchmark/design.md`, section 7.5.

## Sub-scores

| Model | Mode | Deterministic | Judged | Text | Table | Screenshot | Level 100 | Level 200 | Level 300 | Level 400 |
|---|---|---|---|---|---|---|---|---|---|---|
| google/gemma-4-31b-it | agent-e2 | 79% | - | 81% | 72% | 95% | 100% | 98% | 82% | 74% |
| google/gemma-4-31b-it | baseline | 40% | - | 37% | 46% | 62% | 60% | 69% | 41% | 36% |

- Final: mean question credit over all questions, 0-100%. Every question weighs the same.
- Question credit = the mean of its runs. Deterministic: share of runs with the exact letters. Judged: mean judge score / 3. Worst run: the same score with each question on its lowest run (consistency; not a gate).
- Sub-scores: the same mean within one group. By answer type, by input type (a question counts for every input it includes), by level.
- Luck: share of questions whose credit differs between runs. Confident wrong: share of answers that are wrong and not Unsure (judged: score 0, not unsure).
- Override: share of Agent E2 answers that state the misconception although every needed file was in the context: the model kept its own belief over the knowledge base. Target: 0. See `benchmark/models.md`, section 1.
- Method: `benchmark/design.md`, sections 3 and 7.4.

## Deterministic answers: luck-free scores

| Model | Mode | Track | Stable correct | ± margin | Luck | Stable unsure | Confident wrong | Unsure | Accuracy when answered |
|---|---|---|---|---|---|---|---|---|---|
| google/gemma-4-31b-it | agent-e2 | text | 58% | 6% | 33% | 0% | 21% | 0% | 79% |
| google/gemma-4-31b-it | baseline | text | 19% | 5% | 41% | 0% | 60% | 0% | 39% |
| google/gemma-4-31b-it | agent-e2 | vision | 75% | 30% | 25% | 0% | 2% | 2% | 97% |
| google/gemma-4-31b-it | baseline | vision | 50% | 35% | 25% | 0% | 38% | 0% | 62% |

- Stable correct: share of questions answered correctly in every run: a known answer, not a guess. Consistency, not the final score (the final score is the mean of the runs).
- Luck: share of questions correct in some runs but not all. Counted as not known.
- Stable unsure: share of questions where the model chose Unsure in every run.
- Confident wrong: share of answers that are wrong and not Unsure (wrong letters, partly right, Unsure mixed with other letters, unparseable). The answers that mislead an operator. Target: near 0.
- Accuracy when answered: exact share among answers that were not Unsure.

## Deterministic answers: scores

| Model | Mode | Track | Exact | Partial | Majority | ± margin | Consistency | Misconception | Parse fail | Recall | Steps | Tokens | Latency s | Cost US$ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| google/gemma-4-31b-it | agent-e2 | text | 78% | 93% | 82% | 4% | 64% | 2% | 0% | 97% | 2.0 | 36900 | 65.0 | 7.614 |
| google/gemma-4-31b-it | baseline | text | 39% | 73% | 42% | 6% | 30% | 14% | 0% | - | 1.0 | 2145 | 3.1 | 0.453 |
| google/gemma-4-31b-it | agent-e2 | vision | 95% | 97% | 100% | 0% | 75% | 2% | 0% | 89% | 2.1 | 34135 | 39.3 | 0.197 |
| google/gemma-4-31b-it | baseline | vision | 62% | 74% | 62% | 34% | 50% | 22% | 0% | - | 1.0 | 1108 | 3.8 | 0.007 |

- Exact and Partial: mean over all runs. Majority: most common answer per question. Margin: 95% interval on Majority from the number of questions.
- Consistency: share of questions answered identically in every run. Recall: share of the question `knowledge` ids whose text reached the model (Agent E2 only: the reading set and any gap follow-up). Steps: model calls per answer.

## Deterministic answers: exact score by technology

| Model | Mode | cpu | gpu | memory | network | storage | system |
|---|---|---|---|---|---|---|---|
| google/gemma-4-31b-it | agent-e2 | 77% | 100% | 76% | 81% | 83% | 77% |
| google/gemma-4-31b-it | baseline | 33% | 0% | 43% | 50% | 49% | 33% |

## Deterministic answers: exact score by task

| Model | Mode | decide-capacity | explain-mechanism | judge-setting | read-metric | troubleshoot |
|---|---|---|---|---|---|---|
| google/gemma-4-31b-it | agent-e2 | 74% | 80% | 76% | 79% | 83% |
| google/gemma-4-31b-it | baseline | 32% | 33% | 27% | 42% | 53% |

## Hardest questions (Agent E2, or web for the frontier reference)

| Question | Mean credit | Common wrong answers or missed points |
|---|---|---|
| 0151 | 0% | B,C,F ×5 |
| 0187 | 0% | B,C,D,F ×5 |
| 0263 | 0% | B ×5 |
| 0383 | 0% | A,D,F,G ×5 |
| 0403 | 0% | A,C,D,G ×5 |
| 0413 | 0% | A,C,G ×5 |
| 0422 | 0% | A,C,D,G ×3, A,C,D ×2 |
| 0433 | 0% | B,D,E ×5 |
| 0012 | 0% | B,C,F ×5 |
| 0085 | 0% | A,C,E,F,K,M,P ×4, A,C,E,F,G,I,K,M,P,Q ×1 |

Traces: `traces.jsonl` in this folder (one line per answer).
