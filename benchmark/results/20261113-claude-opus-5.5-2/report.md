# Benchmark report: 20261113-claude-opus-5.5-2

- Index version: `de2551c8d790`. Retrieval: hybrid. Sampling: {"anthropic/claude-opus-5.5": {}}. Runs: 5.
- Questions: 196 (deterministic 119, judged 77; text 155, table 35, screenshot 6; level 100: 8, level 200: 17, level 300: 40, level 400: 131). Skipped: none. Judge: openai/gpt-6.1-terra.
- Answers: 1960 scored, 0 failed.

## Final score

| Model | Mode | Final | ± margin | Worst run | Luck | Confident wrong | Override |
|---|---|---|---|---|---|---|---|
| anthropic/claude-opus-5.5 | baseline | 84% | 5% | 74% | 19% | 11% | - |
| anthropic/claude-opus-5.5 | web | 81% | 5% | 69% | 22% | 12% | - |

## Sub-scores

| Model | Mode | Deterministic | Judged | Text | Table | Screenshot | Level 100 | Level 200 | Level 300 | Level 400 |
|---|---|---|---|---|---|---|---|---|---|---|
| anthropic/claude-opus-5.5 | baseline | 92% | 71% | 83% | 81% | 100% | 100% | 89% | 83% | 82% |
| anthropic/claude-opus-5.5 | web | 90% | 67% | 80% | 81% | 100% | 98% | 87% | 81% | 79% |

- Final: mean question credit over all questions, 0-100%. Every question weighs the same.
- Question credit = the mean of its runs. Deterministic: share of runs with the exact letters. Judged: mean judge score / 3. Worst run: the same score with each question on its lowest run (consistency; not a gate).
- Sub-scores: the same mean within one group. By answer type, by input type (a question counts for every input it includes), by level.
- Luck: share of questions whose credit differs between runs. Confident wrong: share of answers that are wrong and not Unsure (judged: score 0, not unsure).
- Override: share of answers in knowledge base modes that state the misconception although every needed file was in the context: the model kept its own belief over the knowledge base. Target: 0. See `benchmark/models.md`, section 1.
- Method: `benchmark/design.md`, sections 3 and 7.4.

## Judged answers

| Model | Mode | Mean score 0-3 | Score 3 | Score 0 | Misconception | Unsure |
|---|---|---|---|---|---|---|
| anthropic/claude-opus-5.5 | baseline | 2.13 | 70% | 28% | 3% | 12% |
| anthropic/claude-opus-5.5 | web | 2.01 | 66% | 32% | 4% | 9% |

## Deterministic answers: luck-free scores

| Model | Mode | Track | Stable correct | ± margin | Luck | Stable unsure | Confident wrong | Unsure | Accuracy when answered |
|---|---|---|---|---|---|---|---|---|---|
| anthropic/claude-opus-5.5 | baseline | text | 88% | 6% | 5% | 0% | 7% | 2% | 93% |
| anthropic/claude-opus-5.5 | web | text | 85% | 7% | 8% | 2% | 6% | 5% | 94% |
| anthropic/claude-opus-5.5 | baseline | vision | 100% | 0% | 0% | 0% | 0% | 0% | 100% |
| anthropic/claude-opus-5.5 | web | vision | 100% | 0% | 0% | 0% | 0% | 0% | 100% |

- Stable correct: share of questions answered correctly in every run. The headline score: a known answer, not a guess.
- Luck: share of questions correct in some runs but not all. Counted as not known.
- Stable unsure: share of questions where the model chose Unsure in every run.
- Confident wrong: share of answers that are wrong and not Unsure (wrong letters, partly right, Unsure mixed with other letters, unparseable). The answers that mislead an operator. Target: near 0.
- Accuracy when answered: exact share among answers that were not Unsure.

## Deterministic answers: scores

| Model | Mode | Track | Exact | Partial | Majority | ± margin | Consistency | Misconception | Parse fail | Recall | Seen | Fallback | Steps | Tokens | Latency s | Cost US$ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| anthropic/claude-opus-5.5 | baseline | text | 91% | 95% | 91% | 5% | 92% | 2% | 0% | - | - | 0% | 0.0 | 1356 | 7.4 | 7.073 |
| anthropic/claude-opus-5.5 | web | text | 90% | 93% | 90% | 5% | 89% | 2% | 0% | 0% | - | 0% | 0.6 | 4167 | 10.8 | 15.379 |
| anthropic/claude-opus-5.5 | baseline | vision | 100% | 100% | 100% | 0% | 100% | 0% | 0% | - | - | 0% | 0.0 | 4256 | 4.5 | 0.619 |
| anthropic/claude-opus-5.5 | web | vision | 100% | 100% | 100% | 0% | 100% | 0% | 0% | 0% | - | 0% | 0.1 | 5232 | 8.2 | 0.788 |

- Exact and Partial: mean over all runs. Majority: most common answer per question. Margin: 95% interval on Majority from the number of questions.
- Consistency: share of questions answered identically in every run. Recall: share of the question `knowledge` ids whose text reached the model (classic: the context; agentic: the first lookup and the files it read). Seen: the same share counting search results too; Seen above Recall means files found but not read.

## Deterministic answers: exact score by technology

| Model | Mode | cpu | memory | network | storage | system |
|---|---|---|---|---|---|---|
| anthropic/claude-opus-5.5 | baseline | 94% | 83% | 96% | 93% | 94% |
| anthropic/claude-opus-5.5 | web | 89% | 87% | 95% | 91% | 91% |

## Deterministic answers: exact score by task

| Model | Mode | decide-capacity | explain-mechanism | judge-setting | read-metric | troubleshoot |
|---|---|---|---|---|---|---|
| anthropic/claude-opus-5.5 | baseline | 100% | 90% | 80% | 92% | 92% |
| anthropic/claude-opus-5.5 | web | 95% | 89% | 80% | 89% | 94% |

## Hardest questions (knowledge base modes)

| Question | Mean credit | Common wrong answers or missed points |
|---|---|---|
| 0045 | 0% | The most likely cause is a snapshot chain: extra datastore reads return no data and are excluded from virtual disk counters. ×1, The most likely cause is a snapshot: chain checks add datastore read I/Os that return no data, and virtual disk counters exclude snapshot I/O. ×1, A snapshot is the most likely cause: snapshot-chain checks add datastore read IOPS that return no data, while virtual disk counters exclude snapshot I/O. ×1 |
| 0011 | 0% | A,B,C,D,G ×3, A,C,D,G ×2 |
| 0017 | 0% | VM log files are virtualization overhead. ×3, VM log files are overhead. ×1, vSAN FTT is optional protection, not overhead; VM log files are overhead. ×1 |
| 0022 | 0% | B,D,E ×5 |
| 0089 | 0% | The peak is the highest single 20-second point across disks and directions, not peak read latency plus peak write latency. ×1, The peak is the maximum of a single disk and direction, and the 248 ms write latency requires more than one such point or disk. ×1, The peak is the highest single 20-second read or write point across all disks, not the sum of the highest read and write latencies. ×1 |
| 0232 | 0% | A ×3, UN ×2 |
| 0002 | 0% | The contrast with Linux Steal Time. ×1, The frequency-driven latency increase does not mean the VM is waiting for CPU or necessarily has a performance problem. ×1, Linux Steal Time includes only CPU Ready, whereas VM CPU Latency also includes frequency effects. ×1 |
| 0006 | 0% | Capacity is fixed and expressed as 40 threads for ESXi 01 and 20 threads for ESXi 02; GHz measures throughput, not capacity. ×2, Capacity is the fixed thread count: 40 threads for ESXi 01 and 20 threads for ESXi 02; GHz measures throughput, not capacity. ×1, Capacity is fixed space measured here in threads: E (40 threads) for ESXi 01 and E (20 threads) for ESXi 02; GHz measures throughput. ×1 |
| 0297 | 0% | The swap file is copied between different locations during vMotion; if it cannot be created, the VM does not power on. ×1, A VM whose swap file cannot be created does not power on. ×1, A VM whose swap file cannot be created does not power on; local capacity is insufficient after one host is lost. ×1 |
| 0024 | 0% | A,B,D,E ×5 |

Traces: `traces.jsonl` in this folder (one line per answer).
