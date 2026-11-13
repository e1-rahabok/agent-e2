# Benchmark report: 20261113-002119

- Index version: `772630b04a97`. Retrieval: hybrid. Temperature: 0.2. Runs: 2.
- Questions: 150 (deterministic 87, judged 55; text 108, table 33, screenshot 1; level 100: 5, level 200: 15, level 300: 40, level 400: 82). Skipped: 0034, 0037, 0042, 0051, 0050. Judge: openai/gpt-5.6-sol.
- Answers: 282 scored, 18 failed.

## Final score

| Model | Mode | Final | ± margin | Luck | Confident wrong | Override |
|---|---|---|---|---|---|---|
| anthropic/claude-opus-5.5 | web | 77% | 7% | 13% | 13% | - |

## Sub-scores

| Model | Mode | Deterministic | Judged | Text | Table | Screenshot | Level 100 | Level 200 | Level 300 | Level 400 |
|---|---|---|---|---|---|---|---|---|---|---|
| anthropic/claude-opus-5.5 | web | 89% | 59% | 77% | 78% | 100% | 100% | 84% | 74% | 76% |

- Final: mean question credit over all questions, 0-100%. Every question weighs the same.
- Question credit = the worst of its runs. Deterministic: 1 if the letters are exact in every run, else 0. Judged: lowest judge score / 3.
- Sub-scores: the same mean within one group. By answer type, by input type (a question counts for every input it includes), by level.
- Luck: share of questions whose credit differs between runs. Confident wrong: share of answers that are wrong and not Unsure (judged: score 0, not unsure).
- Override: share of answers in knowledge base modes that state the misconception although every needed file was in the context: the model kept its own belief over the knowledge base. Target: 0. See `benchmark/models.md`, section 1.
- Method: `benchmark/design.md`, sections 3 and 7.4.

## Judged answers

| Model | Mode | Mean score 0-3 | Score 3 | Score 0 | Misconception | Unsure |
|---|---|---|---|---|---|---|
| anthropic/claude-opus-5.5 | web | 2.04 | 58% | 27% | 6% | 6% |

## Deterministic answers: luck-free scores

| Model | Mode | Track | Stable correct | ± margin | Luck | Stable unsure | Confident wrong | Unsure | Accuracy when answered |
|---|---|---|---|---|---|---|---|---|---|
| anthropic/claude-opus-5.5 | web | text | 88% | 7% | 2% | 0% | 9% | 2% | 91% |
| anthropic/claude-opus-5.5 | web | vision | 100% | 0% | 0% | 0% | 0% | 0% | 100% |

- Stable correct: share of questions answered correctly in every run. The headline score: a known answer, not a guess.
- Luck: share of questions correct in some runs but not all. Counted as not known.
- Stable unsure: share of questions where the model chose Unsure in every run.
- Confident wrong: share of answers that are wrong and not Unsure (wrong letters, partly right, Unsure mixed with other letters, unparseable). The answers that mislead an operator. Target: near 0.
- Accuracy when answered: exact share among answers that were not Unsure.

## Deterministic answers: scores

| Model | Mode | Track | Exact | Partial | Majority | ± margin | Consistency | Misconception | Parse fail | Recall | Fallback | Steps | Tokens | Latency s | Cost US$ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| anthropic/claude-opus-5.5 | web | text | 89% | 94% | 91% | 6% | 93% | 2% | 0% | 0% | 0% | 0.5 | 3687 | 8.6 | 4.340 |
| anthropic/claude-opus-5.5 | web | vision | 100% | 100% | 100% | 0% | 100% | 0% | 0% | 0% | 0% | 1.0 | 9253 | 15.4 | 0.110 |

- Exact and Partial: mean over all runs. Majority: most common answer per question. Margin: 95% interval on Majority from the number of questions.
- Consistency: share of questions answered identically in every run. Recall: share of the question `knowledge` ids the mode retrieved or read.

## Deterministic answers: exact score by technology

| Model | Mode | cpu | memory | network | storage | system |
|---|---|---|---|---|---|---|
| anthropic/claude-opus-5.5 | web | 92% | 83% | 96% | 91% | 95% |

## Deterministic answers: exact score by task

| Model | Mode | decide-capacity | explain-mechanism | judge-setting | read-metric | troubleshoot |
|---|---|---|---|---|---|---|
| anthropic/claude-opus-5.5 | web | 97% | 87% | 40% | 92% | 93% |

## Hardest questions (knowledge base modes)

| Question | Mean credit | Common wrong answers or missed points |
|---|---|---|
| 0052 | 0% | A flat balloon can persist after host pressure has passed and, by itself, indicates neither current pressure nor waiting; VM Memory Latency/VCF Operations Memory Contention should also be checked. ×1, A flat balloon only means the reclaimed amount is unchanged and may reflect past pressure; memory waits can also appear as VM Memory Latency, ESXi swap-in, or decompression without guest swapping or O ×1 |
| 0011 | 0% | A,B,C,D,G ×1, A,C,D,G ×1 |
| 0017 | 0% | VM log files are mandatory virtualization overhead, alongside ESXi kernel and VMM overhead. ×1, VM log files are mandatory virtualization overhead, not merely VM consumption. ×1 |
| 0016 | 0% | Host Ready is only the VMs' Ready summed, and host Demand excludes VMkernel/system work; kernel work appears in Usage, not Demand. ×1, ESXi CPU Demand excludes VMkernel/system worlds; kernel work appears in Usage, while a host with no VMs has Demand at 0. ×1 |
| 0022 | 0% | B,D,E ×2 |
| 0027 | 0% | The 10–15 ms guidance is specifically at the SQL layer, so Windows and VM-layer thresholds must be lower; a universal 15 ms vSphere threshold is inappropriate, and a 5-minute window can generate many  ×1, The vSphere VM-layer threshold must be lower than the SQL-layer 10–15 ms guidance, and a 5-minute window represents 300 per-second samples that commonly creates alerts without user complaints. ×1 |
| 0089 | 0% | The peak is the single highest 20-second value across all disks and both directions, not the highest read plus the highest write; the 248 ms average also implies more than one affected point or disk. ×1, The peak is the single highest 20-second latency across every virtual disk and both read/write directions, not highest read plus highest write. ×1 |
| 0232 | 0% | A ×1, UN ×1 |
| 0002 | 0% | A definitive conclusion that the VM is running more slowly due to lower CPU frequency but is not waiting for CPU service; flat Ready and Co-Stop indicate no contention. ×1, The contrast that Linux Steal Time includes only CPU Ready, while VM CPU Latency includes frequency and other factors. ×1 |
| 0006 | 0% | Capacity is fixed hardware space measured here as 40 threads for ESXi 01 and 20 threads for ESXi 02; GHz values are fluctuating performance/throughput figures. ×1, Capacity is fixed hardware space expressed here as 40 threads for ESXi 01 and 20 threads for ESXi 02; GHz values are fluctuating performance figures, not capacity. ×1 |

Traces: `traces.jsonl` in this folder (one line per answer).
