# Benchmark report: 20261113-000312

- Index version: `772630b04a97`. Retrieval: hybrid. Temperature: 0.2. Runs: 5.
- Questions: 150 (deterministic 90, judged 60; text 114, table 35, screenshot 1; level 100: 5, level 200: 15, level 300: 40, level 400: 90). Skipped: 0034, 0037, 0042, 0051, 0050. Judge: openai/gpt-5.6-sol.
- Answers: 750 scored, 0 failed.

## Final score

| Model | Mode | Final | ± margin | Luck | Confident wrong | Override |
|---|---|---|---|---|---|---|
| anthropic/claude-opus-5.5 | baseline | 67% | 8% | 28% | 10% | - |

## Sub-scores

| Model | Mode | Deterministic | Judged | Text | Table | Screenshot | Level 100 | Level 200 | Level 300 | Level 400 |
|---|---|---|---|---|---|---|---|---|---|---|
| anthropic/claude-opus-5.5 | baseline | 84% | 41% | 68% | 64% | 100% | 100% | 60% | 73% | 63% |

- Final: mean question credit over all questions, 0-100%. Every question weighs the same.
- Question credit = the worst of its runs. Deterministic: 1 if the letters are exact in every run, else 0. Judged: lowest judge score / 3.
- Sub-scores: the same mean within one group. By answer type, by input type (a question counts for every input it includes), by level.
- Luck: share of questions whose credit differs between runs. Confident wrong: share of answers that are wrong and not Unsure (judged: score 0, not unsure).
- Override: share of answers in knowledge base modes that state the misconception although every needed file was in the context: the model kept its own belief over the knowledge base. Target: 0. See `benchmark/models.md`, section 1.
- Method: `benchmark/design.md`, sections 3 and 7.4.

## Judged answers

| Model | Mode | Mean score 0-3 | Score 3 | Score 0 | Misconception | Unsure |
|---|---|---|---|---|---|---|
| anthropic/claude-opus-5.5 | baseline | 1.99 | 60% | 30% | 4% | 18% |

## Deterministic answers: luck-free scores

| Model | Mode | Track | Stable correct | ± margin | Luck | Stable unsure | Confident wrong | Unsure | Accuracy when answered |
|---|---|---|---|---|---|---|---|---|---|
| anthropic/claude-opus-5.5 | baseline | text | 84% | 8% | 9% | 0% | 9% | 2% | 91% |
| anthropic/claude-opus-5.5 | baseline | vision | 100% | 0% | 0% | 0% | 0% | 0% | 100% |

- Stable correct: share of questions answered correctly in every run. The headline score: a known answer, not a guess.
- Luck: share of questions correct in some runs but not all. Counted as not known.
- Stable unsure: share of questions where the model chose Unsure in every run.
- Confident wrong: share of answers that are wrong and not Unsure (wrong letters, partly right, Unsure mixed with other letters, unparseable). The answers that mislead an operator. Target: near 0.
- Accuracy when answered: exact share among answers that were not Unsure.

## Deterministic answers: scores

| Model | Mode | Track | Exact | Partial | Majority | ± margin | Consistency | Misconception | Parse fail | Recall | Fallback | Steps | Tokens | Latency s | Cost US$ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| anthropic/claude-opus-5.5 | baseline | text | 89% | 94% | 90% | 6% | 90% | 2% | 0% | - | 0% | 0.0 | 1393 | 5.8 | 5.626 |
| anthropic/claude-opus-5.5 | baseline | vision | 100% | 100% | 100% | 0% | 100% | 0% | 0% | - | 0% | 0.0 | 3895 | 8.3 | 0.125 |

- Exact and Partial: mean over all runs. Majority: most common answer per question. Margin: 95% interval on Majority from the number of questions.
- Consistency: share of questions answered identically in every run. Recall: share of the question `knowledge` ids the mode retrieved or read.

## Deterministic answers: exact score by technology

| Model | Mode | cpu | memory | network | storage | system |
|---|---|---|---|---|---|---|
| anthropic/claude-opus-5.5 | baseline | 93% | 83% | 99% | 93% | 93% |

## Deterministic answers: exact score by task

| Model | Mode | decide-capacity | explain-mechanism | judge-setting | read-metric | troubleshoot |
|---|---|---|---|---|---|---|
| anthropic/claude-opus-5.5 | baseline | 96% | 85% | 44% | 92% | 93% |

## Hardest questions (knowledge base modes)

| Question | Mean credit | Common wrong answers or missed points |
|---|---|---|

Traces: `traces.jsonl` in this folder (one line per answer).
