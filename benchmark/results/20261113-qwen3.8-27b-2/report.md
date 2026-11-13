# Benchmark report: 20261113-qwen3.8-27b-2

- Index version: `de2551c8d790`. Retrieval: hybrid. Sampling: {"alibaba/qwen3.8-27b": {"temperature": 1.0, "top_p": 0.95, "top_k": 20}}. Runs: 5.
- Questions: 196 (deterministic 119, judged 77; text 155, table 35, screenshot 6; level 100: 8, level 200: 17, level 300: 40, level 400: 131). Skipped: none. Judge: openai/gpt-6.1-terra.
- Answers: 2940 scored, 0 failed.

## Final score

| Model | Mode | Final | ± margin | Worst run | Luck | Confident wrong | Override |
|---|---|---|---|---|---|---|---|
| alibaba/qwen3.8-27b | classic | 69% | 6% | 46% | 48% | 29% | 4% |
| alibaba/qwen3.8-27b | agentic | 63% | 7% | 28% | 63% | 30% | 3% |
| alibaba/qwen3.8-27b | baseline | 41% | 7% | 15% | 52% | 51% | - |

## Release gate

Agentic mode. Reference: anthropic/claude-opus-5.5, web mode (not in this benchmark: gap not read).

| Model | Gate | Value | Limit | Pass |
|---|---|---|---|---|
| alibaba/qwen3.8-27b | Final score | 63% | at least 85% | no |
| alibaba/qwen3.8-27b | Level 400 | 55% | at least 80% | no |
| alibaba/qwen3.8-27b | Confident wrong | 30% | at most 3% | no |

- Not read here: no misconception of `knowledge/misconceptions.md` stated as true (author check), and the held-out set at most 11 points below the development set (separate run). Method: `benchmark/design.md`, section 7.5.

## Sub-scores

| Model | Mode | Deterministic | Judged | Text | Table | Screenshot | Level 100 | Level 200 | Level 300 | Level 400 |
|---|---|---|---|---|---|---|---|---|---|---|
| alibaba/qwen3.8-27b | classic | 81% | 49% | 71% | 54% | 90% | 91% | 75% | 84% | 62% |
| alibaba/qwen3.8-27b | agentic | 71% | 50% | 65% | 49% | 97% | 92% | 76% | 78% | 55% |
| alibaba/qwen3.8-27b | baseline | 53% | 21% | 43% | 26% | 63% | 66% | 58% | 49% | 34% |

- Final: mean question credit over all questions, 0-100%. Every question weighs the same.
- Question credit = the mean of its runs. Deterministic: share of runs with the exact letters. Judged: mean judge score / 3. Worst run: the same score with each question on its lowest run (consistency; not a gate).
- Sub-scores: the same mean within one group. By answer type, by input type (a question counts for every input it includes), by level.
- Luck: share of questions whose credit differs between runs. Confident wrong: share of answers that are wrong and not Unsure (judged: score 0, not unsure).
- Override: share of answers in knowledge base modes that state the misconception although every needed file was in the context: the model kept its own belief over the knowledge base. Target: 0. See `benchmark/models.md`, section 1.
- Method: `benchmark/design.md`, sections 3 and 7.4.

## Judged answers

| Model | Mode | Mean score 0-3 | Score 3 | Score 0 | Misconception | Unsure |
|---|---|---|---|---|---|---|
| alibaba/qwen3.8-27b | agentic | 1.51 | 46% | 47% | 7% | 5% |
| alibaba/qwen3.8-27b | baseline | 0.62 | 19% | 77% | 22% | 3% |
| alibaba/qwen3.8-27b | classic | 1.48 | 45% | 48% | 9% | 1% |

## Deterministic answers: luck-free scores

| Model | Mode | Track | Stable correct | ± margin | Luck | Stable unsure | Confident wrong | Unsure | Accuracy when answered |
|---|---|---|---|---|---|---|---|---|---|
| alibaba/qwen3.8-27b | classic | text | 62% | 9% | 34% | 0% | 18% | 1% | 82% |
| alibaba/qwen3.8-27b | agentic | text | 34% | 9% | 61% | 1% | 24% | 7% | 75% |
| alibaba/qwen3.8-27b | baseline | text | 21% | 8% | 57% | 1% | 36% | 11% | 59% |
| alibaba/qwen3.8-27b | classic | vision | 83% | 30% | 17% | 0% | 10% | 0% | 90% |
| alibaba/qwen3.8-27b | agentic | vision | 83% | 30% | 17% | 0% | 0% | 3% | 100% |
| alibaba/qwen3.8-27b | baseline | vision | 50% | 40% | 17% | 0% | 33% | 3% | 66% |

- Stable correct: share of questions answered correctly in every run. The headline score: a known answer, not a guess.
- Luck: share of questions correct in some runs but not all. Counted as not known.
- Stable unsure: share of questions where the model chose Unsure in every run.
- Confident wrong: share of answers that are wrong and not Unsure (wrong letters, partly right, Unsure mixed with other letters, unparseable). The answers that mislead an operator. Target: near 0.
- Accuracy when answered: exact share among answers that were not Unsure.

## Deterministic answers: scores

| Model | Mode | Track | Exact | Partial | Majority | ± margin | Consistency | Misconception | Parse fail | Recall | Seen | Fallback | Steps | Tokens | Latency s | Cost US$ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| alibaba/qwen3.8-27b | classic | text | 81% | 89% | 88% | 6% | 63% | 5% | 0% | 78% | 78% | 0% | 1.0 | 14584 | 3.3 | 0.768 |
| alibaba/qwen3.8-27b | agentic | text | 70% | 81% | 82% | 7% | 35% | 7% | 1% | 69% | 81% | 0% | 7.5 | 57126 | 9.3 | 2.637 |
| alibaba/qwen3.8-27b | baseline | text | 53% | 66% | 60% | 9% | 22% | 10% | 0% | - | - | 0% | 0.0 | 1466 | 5.9 | 0.727 |
| alibaba/qwen3.8-27b | agentic | vision | 97% | 97% | 100% | 0% | 83% | 0% | 0% | 30% | 40% | 0% | 5.5 | 67330 | 16.9 | 0.152 |
| alibaba/qwen3.8-27b | classic | vision | 90% | 90% | 83% | 30% | 83% | 0% | 0% | 53% | 53% | 0% | 1.0 | 17670 | 4.6 | 0.037 |
| alibaba/qwen3.8-27b | baseline | vision | 63% | 63% | 67% | 38% | 50% | 17% | 0% | - | - | 0% | 0.0 | 4307 | 3.4 | 0.013 |

- Exact and Partial: mean over all runs. Majority: most common answer per question. Margin: 95% interval on Majority from the number of questions.
- Consistency: share of questions answered identically in every run. Recall: share of the question `knowledge` ids whose text reached the model (classic: the context; agentic: the first lookup and the files it read). Seen: the same share counting search results too; Seen above Recall means files found but not read.

## Deterministic answers: exact score by technology

| Model | Mode | cpu | memory | network | storage | system |
|---|---|---|---|---|---|---|
| alibaba/qwen3.8-27b | agentic | 69% | 69% | 71% | 70% | 80% |
| alibaba/qwen3.8-27b | baseline | 42% | 52% | 57% | 60% | 67% |
| alibaba/qwen3.8-27b | classic | 77% | 82% | 82% | 84% | 82% |

## Deterministic answers: exact score by task

| Model | Mode | decide-capacity | explain-mechanism | judge-setting | read-metric | troubleshoot |
|---|---|---|---|---|---|---|
| alibaba/qwen3.8-27b | agentic | 67% | 73% | 67% | 76% | 71% |
| alibaba/qwen3.8-27b | baseline | 44% | 46% | 56% | 61% | 55% |
| alibaba/qwen3.8-27b | classic | 72% | 77% | 85% | 82% | 87% |

## Hardest questions (knowledge base modes)

| Question | Mean credit | Common wrong answers or missed points |
|---|---|---|
| 0041 | 0% | The VMXNET3 link speed is a reported label, 10 Gbps by default, not the speed of the physical uplink. ×1, The reported VMXNET3 speed is a label, not the physical uplink speed; a VMX setting can raise the reported speed without limiting throughput. ×1, The reported VMXNET3 speed is a label independent of physical uplink speed; a VMX setting can change it upward without limiting throughput. ×1 |
| 0006 | 0% | Capacity is the fixed thread count: 40 threads for ESXi 01 and 20 threads for ESXi 02; GHz measures performance, not capacity. ×1, Capacity is fixed space measured in physical threads: 40 for ESXi 01 and 20 for ESXi 02; GHz measures throughput. ×1, ESXi 02 capacity is E, 20 threads; GHz measures performance, not capacity. ×1 |
| 0141 | 0% | A,C ×7, A,D ×2, D ×1 |
| 0150 | 0% | Admission control remains green, and normal operation fits at current consumption without reclamation. ×1, HA admission control counts reservations, not configured memory or usage, and stays green; the new VMs fit in normal operation at current consumption. ×1, Normal operation fits at current consumption, and HA admission control stays green because it counts reservations rather than existing VM usage. ×1 |
| 0239 | 0% | The 40 GHz limit was applied to RP-Web, not RP-Batch; verify both pool limits and Max Limited, then remove the web limit. ×1, The 40 GHz limit was most likely applied to RP-Web; verify both pool limits, the script and Max Limited, then remove the web limit. ×1, The likely 40 GHz limit on RP-Web, its confirmation with pool settings and Max Limited, and its removal. ×1 |
| 0240 | 0% | A,C ×3, UN ×3, A ×2 |
| 0297 | 3% | Swap files are created at power-on; copying occurs even without swapped pages; the one-host-loss capacity shortfall and gradual SAN-space recovery. ×1, Swap-file copying even without swapped pages, hosts 7–8 fallback and gradual SAN release, and insufficient N-1 capacity for HA restarts. ×1, Hosts 7 and 8 fall back to VM-directory swap on the SAN; vMotion copies the swap file when locations differ, even without swapped pages. ×1 |
| 0353 | 7% | Post-failure Core Utilization is 96%, and a fifth host is a defensible cluster-capacity response; check the busiest days for peak load. ×1, HA admission control compares reservations, not usage, and gives no warning here; the default performance degradation tolerance of 100% never warns. ×1, HA admission-control behavior, peak-load verification, and the option to accept degraded performance ×1 |
| 0361 | 7% | Raise the LUN device queue depth first; raising PVSCSI depth alone shifts the guest wait to the VMkernel queue without improving the I/O rate. ×1, Raise the LUN device queue depth first; raising PVSCSI depth alone only moves the wait into the VMkernel queue and does not increase throughput. ×1, The 16 ms comprises 7.8 ms in the VMkernel device queue, 0.2 ms in the VMkernel stack, and 8 ms at the device. ×1 |
| 0079 | 7% | Do not reclaim from the Java/DB tier; use contention and page-out as safety checks; reclaim at least 256 GB with headroom from the six identified candidates. ×1, The six identified VMs can yield at least 256 GB with headroom above Guest Needed Memory and no page-out or contention. ×1, Do not size VMs without guest data using Consumed; use page-out as a check and keep headroom above Guest Needed Memory. ×1 |

Traces: `traces.jsonl` in this folder (one line per answer).
