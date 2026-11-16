# Benchmark report: 20261116-claude-opus-5.5

- Index version: `6c422ed54d44`. Retrieval: hybrid. Sampling: {"anthropic/claude-opus-5.5": {}}. Runs: 5.
- Questions: 291 (deterministic 291, judged 0; text 210, table 74, screenshot 8; level 100: 7, level 200: 11, level 300: 111, level 400: 162). Skipped: none.
- Answers: 1455 scored, 1 failed.

## Final score

| Model | Mode | Final | ± margin | Worst run | Luck | Confident wrong | Override |
|---|---|---|---|---|---|---|---|
| anthropic/claude-opus-5.5 | web | 79% | 5% | 68% | 21% | 17% | - |

## Sub-scores

| Model | Mode | Deterministic | Judged | Text | Table | Screenshot | Level 100 | Level 200 | Level 300 | Level 400 |
|---|---|---|---|---|---|---|---|---|---|---|
| anthropic/claude-opus-5.5 | web | 79% | - | 77% | 82% | 90% | 100% | 93% | 77% | 78% |

- Final: mean question credit over all questions, 0-100%. Every question weighs the same.
- Question credit = the mean of its runs. Deterministic: share of runs with the exact letters. Judged: mean judge score / 3. Worst run: the same score with each question on its lowest run (consistency; not a gate).
- Sub-scores: the same mean within one group. By answer type, by input type (a question counts for every input it includes), by level.
- Luck: share of questions whose credit differs between runs. Confident wrong: share of answers that are wrong and not Unsure (judged: score 0, not unsure).
- Override: share of Agent E2 answers that state the misconception although every needed file was in the context: the model kept its own belief over the knowledge base. Target: 0. See `benchmark/models.md`, section 1.
- Method: `benchmark/design.md`, sections 3 and 7.4.

## Deterministic answers: luck-free scores

| Model | Mode | Track | Stable correct | ± margin | Luck | Stable unsure | Confident wrong | Unsure | Accuracy when answered |
|---|---|---|---|---|---|---|---|---|---|
| anthropic/claude-opus-5.5 | web | text | 67% | 5% | 22% | 1% | 17% | 4% | 82% |
| anthropic/claude-opus-5.5 | web | vision | 88% | 23% | 12% | 0% | 10% | 0% | 90% |

- Stable correct: share of questions answered correctly in every run: a known answer, not a guess. Consistency, not the final score (the final score is the mean of the runs).
- Luck: share of questions correct in some runs but not all. Counted as not known.
- Stable unsure: share of questions where the model chose Unsure in every run.
- Confident wrong: share of answers that are wrong and not Unsure (wrong letters, partly right, Unsure mixed with other letters, unparseable). The answers that mislead an operator. Target: near 0.
- Accuracy when answered: exact share among answers that were not Unsure.

## Deterministic answers: scores

| Model | Mode | Track | Exact | Partial | Majority | ± margin | Consistency | Misconception | Parse fail | Recall | Steps | Tokens | Latency s | Cost US$ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| anthropic/claude-opus-5.5 | web | text | 78% | 91% | 80% | 5% | 75% | 2% | 0% | - | 1.7 | 5802 | 12.0 | 55.946 |
| anthropic/claude-opus-5.5 | web | vision | 90% | 96% | 88% | 23% | 88% | 0% | 0% | - | 1.4 | 7578 | 9.0 | 1.635 |

- Exact and Partial: mean over all runs. Majority: most common answer per question. Margin: 95% interval on Majority from the number of questions.
- Consistency: share of questions answered identically in every run. Recall: share of the question `knowledge` ids whose text reached the model (Agent E2 only: the reading set and any gap follow-up). Steps: model calls per answer.

## Deterministic answers: exact score by technology

| Model | Mode | cpu | gpu | memory | network | storage | system |
|---|---|---|---|---|---|---|---|
| anthropic/claude-opus-5.5 | web | 78% | 0% | 76% | 83% | 84% | 78% |

## Deterministic answers: exact score by task

| Model | Mode | decide-capacity | explain-mechanism | judge-setting | read-metric | troubleshoot |
|---|---|---|---|---|---|---|
| anthropic/claude-opus-5.5 | web | 75% | 74% | 76% | 79% | 83% |

## Hardest questions (Agent E2, or web for the frontier reference)

| Question | Mean credit | Common wrong answers or missed points |
|---|---|---|
| 0017 | 0% | A,F,K ×5 |
| 0028 | 0% | B,F,G ×5 |
| 0110 | 0% | A,C,I ×5 |
| 0231 | 0% | A,E ×3, UN ×2 |
| 0232 | 0% | A,C,F ×5 |
| 0273 | 0% | UN ×4, B,C,D,F ×1 |
| 0279 | 0% | UN ×5 |
| 0362 | 0% | UN ×4, B,C,F,H,J ×1 |
| 0387 | 0% | B,C,E ×5 |
| 0406 | 0% | E,F,G ×4, A,F,G ×1 |

Traces: `traces.jsonl` in this folder (one line per answer).
