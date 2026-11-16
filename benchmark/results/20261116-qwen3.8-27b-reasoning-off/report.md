# Benchmark report: 20261116-qwen3.8-27b-invalid-0

- Index version: `fd7212115546`. Retrieval: hybrid. Sampling: {"alibaba/qwen3.8-27b": {"temperature": 1.0, "top_p": 0.95, "top_k": 20}}. Runs: 5.
- Questions: 291 (deterministic 291, judged 0; text 210, table 74, screenshot 8; level 100: 7, level 200: 11, level 300: 111, level 400: 162). Skipped: none.
- Answers: 2910 scored, 22 failed.

## Final score

| Model | Mode | Final | ± margin | Worst run | Luck | Confident wrong | Override |
|---|---|---|---|---|---|---|---|
| alibaba/qwen3.8-27b | agent-e2 | 67% | 5% | 33% | 62% | 32% | 4% |
| alibaba/qwen3.8-27b | baseline | 20% | 5% | 3% | 44% | 71% | - |

## Consensus of 3, projected

What the shipped setting `consensus_samples: 3` would give: multiple-choice letters stand only when 3 samples agree; otherwise Unsure. Projected from the recorded runs, no new model call (`report.py`, function `consensus`). Judged answers unchanged.

| Model | Mode | Final | Final, consensus | Confident wrong | Confident wrong, consensus | Multiple choice: confident wrong, consensus | Multiple choice: Unsure, consensus |
|---|---|---|---|---|---|---|---|
| alibaba/qwen3.8-27b | agent-e2 | 67% | 43% | 32% | 2% | 2% | 54% |

## Release gate

Agent E2. Reference: anthropic/claude-opus-5.5, web mode (not in this benchmark: gap not read).

| Model | Gate | Value | Limit | Pass |
|---|---|---|---|---|
| alibaba/qwen3.8-27b | Final score | 67% | at least 85% | no |
| alibaba/qwen3.8-27b | Level 400 | 61% | at least 80% | no |
| alibaba/qwen3.8-27b | Confident wrong | 32% | at most 3% | no |

- Not read here: no up-front misconception (lines marked `up_front`) stated as true (author check), and the held-out set at most 11 points below the development set (separate run). Method: `benchmark/design.md`, section 7.5.

## Sub-scores

| Model | Mode | Deterministic | Judged | Text | Table | Screenshot | Level 100 | Level 200 | Level 300 | Level 400 |
|---|---|---|---|---|---|---|---|---|---|---|
| alibaba/qwen3.8-27b | agent-e2 | 67% | - | 68% | 63% | 80% | 97% | 85% | 72% | 61% |
| alibaba/qwen3.8-27b | baseline | 20% | - | 18% | 24% | 45% | 51% | 35% | 20% | 18% |

- Final: mean question credit over all questions, 0-100%. Every question weighs the same.
- Question credit = the mean of its runs. Deterministic: share of runs with the exact letters. Judged: mean judge score / 3. Worst run: the same score with each question on its lowest run (consistency; not a gate).
- Sub-scores: the same mean within one group. By answer type, by input type (a question counts for every input it includes), by level.
- Luck: share of questions whose credit differs between runs. Confident wrong: share of answers that are wrong and not Unsure (judged: score 0, not unsure).
- Override: share of Agent E2 answers that state the misconception although every needed file was in the context: the model kept its own belief over the knowledge base. Target: 0. See `benchmark/models.md`, section 1.
- Method: `benchmark/design.md`, sections 3 and 7.4.

## Deterministic answers: luck-free scores

| Model | Mode | Track | Stable correct | ± margin | Luck | Stable unsure | Confident wrong | Unsure | Accuracy when answered |
|---|---|---|---|---|---|---|---|---|---|
| alibaba/qwen3.8-27b | agent-e2 | text | 33% | 5% | 61% | 0% | 33% | 1% | 67% |
| alibaba/qwen3.8-27b | baseline | text | 2% | 2% | 45% | 1% | 71% | 9% | 21% |
| alibaba/qwen3.8-27b | baseline | vision | 38% | 34% | 25% | 0% | 52% | 2% | 46% |
| alibaba/qwen3.8-27b | agent-e2 | vision | 38% | 34% | 62% | 0% | 20% | 0% | 80% |

- Stable correct: share of questions answered correctly in every run: a known answer, not a guess. Consistency, not the final score (the final score is the mean of the runs).
- Luck: share of questions correct in some runs but not all. Counted as not known.
- Stable unsure: share of questions where the model chose Unsure in every run.
- Confident wrong: share of answers that are wrong and not Unsure (wrong letters, partly right, Unsure mixed with other letters, unparseable). The answers that mislead an operator. Target: near 0.
- Accuracy when answered: exact share among answers that were not Unsure.

## Deterministic answers: scores

| Model | Mode | Track | Exact | Partial | Majority | ± margin | Consistency | Misconception | Parse fail | Recall | Steps | Tokens | Latency s | Cost US$ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| alibaba/qwen3.8-27b | agent-e2 | text | 67% | 87% | 76% | 5% | 34% | 4% | 0% | 97% | 2.0 | 38396 | 9.2 | 6.904 |
| alibaba/qwen3.8-27b | baseline | text | 19% | 52% | 25% | 5% | 4% | 14% | 2% | - | 1.0 | 2870 | 5.2 | 2.696 |
| alibaba/qwen3.8-27b | agent-e2 | vision | 80% | 87% | 100% | 0% | 38% | 2% | 0% | 91% | 2.1 | 41971 | 9.4 | 0.179 |
| alibaba/qwen3.8-27b | baseline | vision | 45% | 54% | 50% | 35% | 38% | 22% | 0% | - | 1.0 | 4301 | 2.6 | 0.019 |

- Exact and Partial: mean over all runs. Majority: most common answer per question. Margin: 95% interval on Majority from the number of questions.
- Consistency: share of questions answered identically in every run. Recall: share of the question `knowledge` ids whose text reached the model (Agent E2 only: the reading set and any gap follow-up). Steps: model calls per answer.

## Deterministic answers: exact score by technology

| Model | Mode | cpu | gpu | memory | network | storage | system |
|---|---|---|---|---|---|---|---|
| alibaba/qwen3.8-27b | agent-e2 | 64% | 80% | 66% | 71% | 65% | 67% |
| alibaba/qwen3.8-27b | baseline | 15% | 20% | 22% | 28% | 23% | 21% |

## Deterministic answers: exact score by task

| Model | Mode | decide-capacity | explain-mechanism | judge-setting | read-metric | troubleshoot |
|---|---|---|---|---|---|---|
| alibaba/qwen3.8-27b | agent-e2 | 56% | 69% | 72% | 70% | 68% |
| alibaba/qwen3.8-27b | baseline | 12% | 13% | 14% | 22% | 29% |

## Hardest questions (Agent E2, or web for the frontier reference)

| Question | Mean credit | Common wrong answers or missed points |
|---|---|---|
| 0263 | 0% | B ×5 |
| 0376 | 0% | A,B,C,E,H ×5 |
| 0383 | 0% | A,D,F,G ×2, A,B,D,F,G ×2, A,D,E,F,G,H ×1 |
| 0408 | 0% | A,B,F ×5 |
| 0409 | 0% | D,E,G ×4, A,C,D,E,G ×1 |
| 0422 | 0% | A,C,D ×3, A,C ×1, A,C,D,G ×1 |
| 0012 | 0% | C,F,H ×1, B,F ×1, B,C,F ×1 |
| 0058 | 0% | A,F,G,J ×3, A,F,G,I,J ×1, F,G,J ×1 |
| 0146 | 0% | A,B,C,J,M ×1, A,B,C,M,O ×1, A,B,C ×1 |
| 0188 | 0% | A,C,E,F,H,L ×4, A,C,H,L ×1 |

Traces: `traces.jsonl` in this folder (one line per answer).
