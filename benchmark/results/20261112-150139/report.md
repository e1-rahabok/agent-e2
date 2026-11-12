# Benchmark report: 20261112-150139

- Index version: `31c2d87209c0`. Retrieval: hybrid. Temperature: 0.2. Runs: 5.
- Questions: 150 (deterministic 90, judged 60; text 114, table 35, screenshot 1; level 100: 5, level 200: 15, level 300: 40, level 400: 90). Skipped: 0034, 0037, 0042, 0051, 0050. Judge: openai/gpt-5.6-sol.
- Answers: 2250 scored, 0 failed.

## Final score

| Model | Mode | Final | ± margin | Luck | Confident wrong | Override |
|---|---|---|---|---|---|---|
| alibaba/qwen3.8-27b | agentic | 51% | 8% | 40% | 28% | 1% |
| alibaba/qwen3.8-27b | classic | 39% | 8% | 33% | 43% | 1% |
| alibaba/qwen3.8-27b | baseline | 4% | 3% | 22% | 87% | - |

## Release gate

Agentic mode. Reference: anthropic/claude-opus-5.5, baseline mode (not in this benchmark: gap not read).

| Model | Gate | Value | Limit | Pass |
|---|---|---|---|---|
| alibaba/qwen3.8-27b | Final score | 51% | at least 85% | no |
| alibaba/qwen3.8-27b | Level 400 | 38% | at least 80% | no |
| alibaba/qwen3.8-27b | Confident wrong | 28% | at most 3% | no |

- Not read here: no misconception of `knowledge/misconceptions.md` stated as true (author check), and the held-out set within 5 points (separate run). Method: `benchmark/design.md`, section 7.5.

## Sub-scores

| Model | Mode | Deterministic | Judged | Text | Table | Screenshot | Level 100 | Level 200 | Level 300 | Level 400 |
|---|---|---|---|---|---|---|---|---|---|---|
| alibaba/qwen3.8-27b | agentic | 69% | 24% | 59% | 27% | 0% | 100% | 73% | 66% | 38% |
| alibaba/qwen3.8-27b | classic | 53% | 17% | 45% | 17% | 100% | 80% | 60% | 40% | 32% |
| alibaba/qwen3.8-27b | baseline | 6% | 1% | 5% | 0% | 0% | 40% | 18% | 2% | 0% |

- Final: mean question credit over all questions, 0-100%. Every question weighs the same.
- Question credit = the worst of its runs. Deterministic: 1 if the letters are exact in every run, else 0. Judged: lowest judge score / 3.
- Sub-scores: the same mean within one group. By answer type, by input type (a question counts for every input it includes), by level.
- Luck: share of questions whose credit differs between runs. Confident wrong: share of answers that are wrong and not Unsure (judged: score 0, not unsure).
- Override: share of answers in knowledge base modes that state the misconception although every needed file was in the context: the model kept its own belief over the knowledge base. Target: 0. See `benchmark/models.md`, section 1.
- Method: `benchmark/design.md`, sections 3 and 7.4.

## Judged answers

| Model | Mode | Mean score 0-3 | Score 3 | Score 0 | Misconception | Unsure |
|---|---|---|---|---|---|---|
| alibaba/qwen3.8-27b | agentic | 1.41 | 40% | 49% | 4% | 1% |
| alibaba/qwen3.8-27b | baseline | 0.32 | 8% | 88% | 0% | 2% |
| alibaba/qwen3.8-27b | classic | 1.12 | 36% | 62% | 1% | 0% |

## Deterministic answers: luck-free scores

| Model | Mode | Track | Stable correct | ± margin | Luck | Stable unsure | Confident wrong | Unsure | Accuracy when answered |
|---|---|---|---|---|---|---|---|---|---|
| alibaba/qwen3.8-27b | agentic | text | 70% | 10% | 27% | 0% | 14% | 1% | 86% |
| alibaba/qwen3.8-27b | classic | text | 53% | 10% | 30% | 0% | 31% | 0% | 69% |
| alibaba/qwen3.8-27b | baseline | text | 6% | 5% | 18% | 0% | 87% | 0% | 13% |
| alibaba/qwen3.8-27b | classic | vision | 100% | 0% | 0% | 0% | 0% | 0% | 100% |
| alibaba/qwen3.8-27b | baseline | vision | 0% | 0% | 0% | 0% | 100% | 0% | 0% |
| alibaba/qwen3.8-27b | agentic | vision | 0% | 0% | 100% | 0% | 60% | 0% | 40% |

- Stable correct: share of questions answered correctly in every run. The headline score: a known answer, not a guess.
- Luck: share of questions correct in some runs but not all. Counted as not known.
- Stable unsure: share of questions where the model chose Unsure in every run.
- Confident wrong: share of answers that are wrong and not Unsure (wrong letters, partly right, Unsure mixed with other letters, unparseable). The answers that mislead an operator. Target: near 0.
- Accuracy when answered: exact share among answers that were not Unsure.

## Deterministic answers: scores

| Model | Mode | Track | Exact | Partial | Majority | ± margin | Consistency | Misconception | Parse fail | Recall | Fallback | Steps | Tokens | Latency s | Cost US$ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| alibaba/qwen3.8-27b | agentic | text | 86% | 90% | 88% | 7% | 70% | 1% | 7% | 62% | 0% | 6.4 | 33306 | 26.3 | 4.863 |
| alibaba/qwen3.8-27b | classic | text | 69% | 70% | 74% | 9% | 67% | 0% | 30% | 78% | 0% | 1.0 | 27130 | 45.0 | 5.360 |
| alibaba/qwen3.8-27b | baseline | text | 13% | 14% | 10% | 6% | 80% | 0% | 85% | - | 0% | 0.0 | 4712 | 30.2 | 3.628 |
| alibaba/qwen3.8-27b | classic | vision | 100% | 100% | 100% | 0% | 100% | 0% | 0% | 100% | 0% | 1.0 | 19997 | 69.1 | 0.017 |
| alibaba/qwen3.8-27b | agentic | vision | 40% | 40% | 100% | 0% | 0% | 20% | 40% | 20% | 0% | 2.8 | 22646 | 38.2 | 0.060 |
| alibaba/qwen3.8-27b | baseline | vision | 0% | 0% | 0% | 0% | 100% | 0% | 100% | - | 0% | 0.0 | 6466 | 32.1 | 0.045 |

- Exact and Partial: mean over all runs. Majority: most common answer per question. Margin: 95% interval on Majority from the number of questions.
- Consistency: share of questions answered identically in every run. Recall: share of the question `knowledge` ids the mode retrieved or read.

## Deterministic answers: exact score by technology

| Model | Mode | cpu | memory | network | storage | system |
|---|---|---|---|---|---|---|
| alibaba/qwen3.8-27b | agentic | 78% | 90% | 83% | 89% | 84% |
| alibaba/qwen3.8-27b | baseline | 5% | 12% | 11% | 19% | 12% |
| alibaba/qwen3.8-27b | classic | 61% | 71% | 79% | 73% | 64% |

## Deterministic answers: exact score by task

| Model | Mode | decide-capacity | explain-mechanism | judge-setting | read-metric | troubleshoot |
|---|---|---|---|---|---|---|
| alibaba/qwen3.8-27b | agentic | 86% | 88% | 80% | 81% | 89% |
| alibaba/qwen3.8-27b | baseline | 10% | 20% | 0% | 18% | 6% |
| alibaba/qwen3.8-27b | classic | 59% | 74% | 68% | 75% | 71% |

## Hardest questions (knowledge base modes)

| Question | Mean credit | Common wrong answers or missed points |
|---|---|---|
| 0041 | 0% | VMXNET3 reports 10 Gbps as a guest-visible label regardless of physical uplink speed; it does not reflect the vmnic behind the port group. ×1, VMXNET3 reports 10 Gbps by default regardless of physical uplink; a VMX setting can only raise that reported value and still imposes no limit, and a Network I/O Control limit applies even when the upl ×1, The VMXNET3-reported speed is a fixed label independent of the vmnic/port group; a VMX setting can only raise the reported value from 10 Gbps and still imposes no limit, and same-host VM traffic can e ×1 |
| 0016 | 0% | ESXi CPU Demand is a true provider metric: the scheduler's internal ideal total demand without contention, not a sum of VM demand. ×2, ESXi CPU Demand is a true provider metric: the scheduler's internal ideal total demand without contention, not a sum of VM Demand or VMkernel worlds. ×2, ESXi CPU Demand is a true provider metric: the scheduler's internal ideal total demand without contention, not a sum of VM or consumer demand. ×1 |
| 0006 | 0% | The answer should select E for both hosts: 40 threads for ESXi 01 and 20 threads for ESXi 02, because capacity is fixed hardware space rather than fluctuating GHz throughput. ×2, The answer should select E for ESXi 01 (40 threads) and E for ESXi 02 (20 threads), explaining that capacity is fixed hardware space while GHz is fluctuating throughput. ×1, E for ESXi 01 (40 threads) and E for ESXi 02 (20 threads); capacity is fixed space, while GHz figures describe fluctuating throughput. ×1 |
| 0012 | 0% | (unparsed) ×9, UN ×1 |
| 0080 | 0% | All key points were missed. ×2, All key points were missed, including thin-growth risk, snapshot risk, vSAN policy overhead, and the overcommit-ratio method. ×1, No answer was provided; it missed thin-growth risk, snapshot risk, vSAN policy overhead and headroom, and the policy-aware overcommit calculation. ×1 |
| 0083 | 0% | No answer was provided; it missed using Used plus System, Ready, and Co-stop to derive 13.75 GHz and at least 7 vCPUs in cluster B. ×1, All key points, including using Used + Ready + Co-stop + System to derive 13.75 GHz and at least 7 vCPUs in cluster B. ×1, The answer omits the conclusion, the Used + Ready + Co-stop + System calculation, the 13.75 GHz footprint, and the requirement for at least 7 vCPUs in cluster B. ×1 |
| 0084 | 0% | All key points were missed because no answer was provided. ×3, All key points were missed. ×2, All key points are missing. ×1 |
| 0102 | 0% | All key points were missed. ×4, All key points were missed because no answer was provided. ×4, All key points were omitted. ×2 |
| 0103 | 0% | (unparsed) ×9, A,C,E ×1 |
| 0106 | 0% | All key points were missed because no answer was provided. ×3, All key points were omitted, including comparing Ready to Net Run and explaining why the flat 5% threshold misses interactive web VMs. ×1, All key points: Ready must be compared with Net Run, which identifies the web VMs as losing the most proportionally and explains why the flat 5% alert missed them. ×1 |

Traces: `traces.jsonl` in this folder (one line per answer).
