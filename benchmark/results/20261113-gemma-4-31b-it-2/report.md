# Benchmark report: 20261113-gemma-4-31b-it-2

- Index version: `de2551c8d790`. Retrieval: hybrid. Sampling: {"google/gemma-4-31b-it": {"temperature": 1.0, "top_p": 0.95, "top_k": 64}}. Runs: 5.
- Questions: 196 (deterministic 119, judged 77; text 155, table 35, screenshot 6; level 100: 8, level 200: 17, level 300: 40, level 400: 131). Skipped: none. Judge: openai/gpt-6.1-terra.
- Answers: 2940 scored, 0 failed.

## Final score

| Model | Mode | Final | ± margin | Worst run | Luck | Confident wrong | Override |
|---|---|---|---|---|---|---|---|
| google/gemma-4-31b-it | classic | 78% | 6% | 63% | 33% | 19% | 2% |
| google/gemma-4-31b-it | agentic | 76% | 6% | 58% | 38% | 21% | 4% |
| google/gemma-4-31b-it | baseline | 57% | 7% | 36% | 45% | 40% | - |

## Release gate

Agentic mode. Reference: anthropic/claude-opus-5.5, web mode (not in this benchmark: gap not read).

| Model | Gate | Value | Limit | Pass |
|---|---|---|---|---|
| google/gemma-4-31b-it | Final score | 76% | at least 85% | no |
| google/gemma-4-31b-it | Level 400 | 71% | at least 80% | no |
| google/gemma-4-31b-it | Confident wrong | 21% | at most 3% | no |

- Not read here: no misconception of `knowledge/misconceptions.md` stated as true (author check), and the held-out set at most 11 points below the development set (separate run). Method: `benchmark/design.md`, section 7.5.

## Sub-scores

| Model | Mode | Deterministic | Judged | Text | Table | Screenshot | Level 100 | Level 200 | Level 300 | Level 400 |
|---|---|---|---|---|---|---|---|---|---|---|
| google/gemma-4-31b-it | classic | 89% | 62% | 80% | 68% | 83% | 83% | 89% | 87% | 74% |
| google/gemma-4-31b-it | agentic | 85% | 61% | 77% | 65% | 97% | 89% | 91% | 83% | 71% |
| google/gemma-4-31b-it | baseline | 67% | 41% | 59% | 43% | 77% | 73% | 69% | 59% | 54% |

- Final: mean question credit over all questions, 0-100%. Every question weighs the same.
- Question credit = the mean of its runs. Deterministic: share of runs with the exact letters. Judged: mean judge score / 3. Worst run: the same score with each question on its lowest run (consistency; not a gate).
- Sub-scores: the same mean within one group. By answer type, by input type (a question counts for every input it includes), by level.
- Luck: share of questions whose credit differs between runs. Confident wrong: share of answers that are wrong and not Unsure (judged: score 0, not unsure).
- Override: share of answers in knowledge base modes that state the misconception although every needed file was in the context: the model kept its own belief over the knowledge base. Target: 0. See `benchmark/models.md`, section 1.
- Method: `benchmark/design.md`, sections 3 and 7.4.

## Judged answers

| Model | Mode | Mean score 0-3 | Score 3 | Score 0 | Misconception | Unsure |
|---|---|---|---|---|---|---|
| google/gemma-4-31b-it | agentic | 1.83 | 49% | 32% | 6% | 1% |
| google/gemma-4-31b-it | baseline | 1.24 | 36% | 54% | 15% | 2% |
| google/gemma-4-31b-it | classic | 1.85 | 53% | 34% | 3% | 1% |

## Deterministic answers: luck-free scores

| Model | Mode | Track | Stable correct | ± margin | Luck | Stable unsure | Confident wrong | Unsure | Accuracy when answered |
|---|---|---|---|---|---|---|---|---|---|
| google/gemma-4-31b-it | classic | text | 82% | 7% | 14% | 1% | 9% | 1% | 91% |
| google/gemma-4-31b-it | agentic | text | 75% | 8% | 18% | 1% | 14% | 1% | 86% |
| google/gemma-4-31b-it | baseline | text | 48% | 9% | 34% | 0% | 33% | 1% | 67% |
| google/gemma-4-31b-it | classic | vision | 83% | 30% | 0% | 0% | 17% | 0% | 83% |
| google/gemma-4-31b-it | agentic | vision | 83% | 30% | 17% | 0% | 3% | 0% | 97% |
| google/gemma-4-31b-it | baseline | vision | 67% | 38% | 17% | 0% | 23% | 0% | 77% |

- Stable correct: share of questions answered correctly in every run. The headline score: a known answer, not a guess.
- Luck: share of questions correct in some runs but not all. Counted as not known.
- Stable unsure: share of questions where the model chose Unsure in every run.
- Confident wrong: share of answers that are wrong and not Unsure (wrong letters, partly right, Unsure mixed with other letters, unparseable). The answers that mislead an operator. Target: near 0.
- Accuracy when answered: exact share among answers that were not Unsure.

## Deterministic answers: scores

| Model | Mode | Track | Exact | Partial | Majority | ± margin | Consistency | Misconception | Parse fail | Recall | Seen | Fallback | Steps | Tokens | Latency s | Cost US$ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| google/gemma-4-31b-it | classic | text | 89% | 93% | 90% | 5% | 84% | 2% | 0% | 78% | 78% | 0% | 1.0 | 14577 | 9.5 | 1.168 |
| google/gemma-4-31b-it | agentic | text | 85% | 91% | 86% | 6% | 79% | 4% | 0% | 46% | 56% | 0% | 4.8 | 32836 | 19.4 | 2.640 |
| google/gemma-4-31b-it | baseline | text | 67% | 79% | 71% | 8% | 58% | 13% | 0% | - | - | 0% | 0.0 | 991 | 3.7 | 0.090 |
| google/gemma-4-31b-it | agentic | vision | 97% | 97% | 100% | 0% | 83% | 0% | 0% | 25% | 30% | 0% | 4.1 | 27269 | 17.6 | 0.116 |
| google/gemma-4-31b-it | baseline | vision | 77% | 77% | 83% | 30% | 83% | 7% | 0% | - | - | 0% | 0.0 | 549 | 4.5 | 0.003 |
| google/gemma-4-31b-it | classic | vision | 83% | 83% | 83% | 30% | 100% | 0% | 0% | 53% | 53% | 0% | 1.0 | 13878 | 9.1 | 0.059 |

- Exact and Partial: mean over all runs. Majority: most common answer per question. Margin: 95% interval on Majority from the number of questions.
- Consistency: share of questions answered identically in every run. Recall: share of the question `knowledge` ids whose text reached the model (classic: the context; agentic: the first lookup and the files it read). Seen: the same share counting search results too; Seen above Recall means files found but not read.

## Deterministic answers: exact score by technology

| Model | Mode | cpu | memory | network | storage | system |
|---|---|---|---|---|---|---|
| google/gemma-4-31b-it | agentic | 82% | 88% | 83% | 87% | 90% |
| google/gemma-4-31b-it | baseline | 60% | 64% | 82% | 81% | 75% |
| google/gemma-4-31b-it | classic | 85% | 91% | 95% | 93% | 87% |

## Deterministic answers: exact score by task

| Model | Mode | decide-capacity | explain-mechanism | judge-setting | read-metric | troubleshoot |
|---|---|---|---|---|---|---|
| google/gemma-4-31b-it | agentic | 81% | 89% | 79% | 87% | 87% |
| google/gemma-4-31b-it | baseline | 62% | 68% | 67% | 61% | 77% |
| google/gemma-4-31b-it | classic | 76% | 88% | 88% | 90% | 98% |

## Hardest questions (knowledge base modes)

| Question | Mean credit | Common wrong answers or missed points |
|---|---|---|
| 0310 | 0% | UN ×10 |
| 0079 | 0% | Use memory contention to check whether a VM is already waiting for memory; exclude rpt-batch-08 and check contention after changes. ×1, rpt-batch-08 has 3.4% memory contention and zero page-outs; check contention as well as page-out. ×1, Keep resized memory above Guest Needed Memory with headroom; reclaim in steps and recheck page-out and contention. ×1 |
| 0150 | 0% | The new VMs fit under admission control, which remains green because the existing VMs have no reservations. ×1, HA admission control counts reservations, not configured memory or usage, and stays green; the new VMs fit in normal operation. ×1, Normal operation fits at current usage, and admission control stays green because the existing VMs have no reservations. ×1 |
| 0230 | 0% | A,C,E ×6, C,E ×4 |
| 0140 | 3% | Consumed is approximately 39.58 GB, just under the 40.44 GB effective limit; 14.7 GB is approximately Swapped. ×1, Consumed is approximately 39.58 GB, just under the 40.44 GB effective limit. ×1, Consumed is approximately 39.58 GB, just below the limit; swapped-page readbacks cause vCPU waits and contention. ×1 |
| 0353 | 7% | HA admission control behavior, capacity options including a fifth host, and checking the busiest days for peaks. ×1, At 96% after one host fails, contention is expected; admission control based on reservations does not establish that performance will remain acceptable. Check peak days and the performance-degradation ×1, Contention is expected after a host loss at 96% CPU utilization; HA admission control does not assess usage under its percentage policy. ×1 |
| 0279 | 7% | A dynamic custom group can be added directly to the existing business application, with rules that include production VMs and exclude test VMs. ×1, A dynamic custom group can be added to the business application without being placed in a tier. ×1, A dynamic VM custom group can be added directly to the business application, with criteria that exclude test VMs. ×1 |
| 0183 | 10% | From VCF 9.0, SIOC storage policies honor only limits; shares and reservations are ignored. ×1, SIOC storage-policy shares and reservations are ignored from VCF 9.0; check DAVG versus KAVG to locate the wait. ×1, Shares and reservations are ignored in VCF 9.0+; check DAVG versus KAVG to locate the wait. ×1 |
| 0041 | 10% | The reported VMXNET3 link speed is a label, defaulting to 10 Gbps regardless of physical uplink speed. ×1, VMXNET3 reports 10 Gbps by default regardless of uplink speed; a VMX setting can raise the reported speed without limiting throughput. ×1, The reported VMXNET3 speed is a label independent of the physical uplink; the NIOC limit applies to transmit traffic only, even when the uplink is idle. ×1 |
| 0297 | 10% | Hosts 7 and 8 fall back to SAN; swap-file copying during vMotion; gradual SAN recovery; N-1 capacity shortfall. ×1, Hosts 7 and 8 fall back to storing swap files with the VMs on the SAN; the 14 TB requirement and one-host-failure capacity shortfall were not calculated. ×1, vMotion copies the swap file when locations differ; hosts 7 and 8 retain swap files on the SAN, and reclamation is gradual. ×1 |

Traces: `traces.jsonl` in this folder (one line per answer).
