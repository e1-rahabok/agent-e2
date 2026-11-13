# Benchmark report: 20261112-150135

- Index version: `31c2d87209c0`. Retrieval: hybrid. Temperature: 0.2. Runs: 5.
- Questions: 150 (deterministic 90, judged 60; text 114, table 35, screenshot 1; level 100: 5, level 200: 15, level 300: 40, level 400: 90). Skipped: 0034, 0037, 0042, 0051, 0050. Judge: openai/gpt-5.6-sol.
- Answers: 2250 scored, 0 failed.

## Final score

| Model | Mode | Final | ± margin | Luck | Confident wrong | Override |
|---|---|---|---|---|---|---|
| google/gemma-4-31b-it | classic | 67% | 8% | 30% | 18% | 4% |
| google/gemma-4-31b-it | agentic | 54% | 8% | 39% | 22% | 1% |
| google/gemma-4-31b-it | baseline | 32% | 7% | 43% | 43% | - |

## Release gate

Agentic mode. Reference: anthropic/claude-opus-5.5, baseline mode (not in this benchmark: gap not read).

| Model | Gate | Value | Limit | Pass |
|---|---|---|---|---|
| google/gemma-4-31b-it | Final score | 54% | at least 85% | no |
| google/gemma-4-31b-it | Level 400 | 48% | at least 80% | no |
| google/gemma-4-31b-it | Confident wrong | 22% | at most 3% | no |

- Not read here: no misconception of `knowledge/misconceptions.md` stated as true (author check), and the held-out set within 5 points (separate run). Method: `benchmark/design.md`, section 7.5.

## Sub-scores

| Model | Mode | Deterministic | Judged | Text | Table | Screenshot | Level 100 | Level 200 | Level 300 | Level 400 |
|---|---|---|---|---|---|---|---|---|---|---|
| google/gemma-4-31b-it | classic | 84% | 40% | 69% | 59% | 100% | 100% | 87% | 71% | 60% |
| google/gemma-4-31b-it | agentic | 67% | 34% | 58% | 38% | 100% | 80% | 67% | 58% | 48% |
| google/gemma-4-31b-it | baseline | 46% | 12% | 34% | 27% | 0% | 80% | 47% | 34% | 26% |

- Final: mean question credit over all questions, 0-100%. Every question weighs the same.
- Question credit = the worst of its runs. Deterministic: 1 if the letters are exact in every run, else 0. Judged: lowest judge score / 3.
- Sub-scores: the same mean within one group. By answer type, by input type (a question counts for every input it includes), by level.
- Luck: share of questions whose credit differs between runs. Confident wrong: share of answers that are wrong and not Unsure (judged: score 0, not unsure).
- Override: share of answers in knowledge base modes that state the misconception although every needed file was in the context: the model kept its own belief over the knowledge base. Target: 0. See `benchmark/models.md`, section 1.
- Method: `benchmark/design.md`, sections 3 and 7.4.

## Judged answers

| Model | Mode | Mean score 0-3 | Score 3 | Score 0 | Misconception | Unsure |
|---|---|---|---|---|---|---|
| google/gemma-4-31b-it | agentic | 1.67 | 35% | 32% | 10% | 2% |
| google/gemma-4-31b-it | baseline | 1.06 | 23% | 56% | 18% | 5% |
| google/gemma-4-31b-it | classic | 1.75 | 40% | 32% | 9% | 2% |

## Deterministic answers: luck-free scores

| Model | Mode | Track | Stable correct | ± margin | Luck | Stable unsure | Confident wrong | Unsure | Accuracy when answered |
|---|---|---|---|---|---|---|---|---|---|
| google/gemma-4-31b-it | classic | text | 84% | 8% | 12% | 0% | 9% | 0% | 91% |
| google/gemma-4-31b-it | agentic | text | 66% | 10% | 28% | 0% | 18% | 0% | 82% |
| google/gemma-4-31b-it | baseline | text | 46% | 10% | 29% | 0% | 38% | 0% | 62% |
| google/gemma-4-31b-it | classic | vision | 100% | 0% | 0% | 0% | 0% | 0% | 100% |
| google/gemma-4-31b-it | agentic | vision | 100% | 0% | 0% | 0% | 0% | 0% | 100% |
| google/gemma-4-31b-it | baseline | vision | 0% | 0% | 100% | 0% | 20% | 0% | 80% |

- Stable correct: share of questions answered correctly in every run. The headline score: a known answer, not a guess.
- Luck: share of questions correct in some runs but not all. Counted as not known.
- Stable unsure: share of questions where the model chose Unsure in every run.
- Confident wrong: share of answers that are wrong and not Unsure (wrong letters, partly right, Unsure mixed with other letters, unparseable). The answers that mislead an operator. Target: near 0.
- Accuracy when answered: exact share among answers that were not Unsure.

## Deterministic answers: scores

| Model | Mode | Track | Exact | Partial | Majority | ± margin | Consistency | Misconception | Parse fail | Recall | Fallback | Steps | Tokens | Latency s | Cost US$ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| google/gemma-4-31b-it | classic | text | 91% | 95% | 91% | 6% | 85% | 2% | 0% | 78% | 0% | 1.0 | 14126 | 8.3 | 0.890 |
| google/gemma-4-31b-it | agentic | text | 82% | 91% | 85% | 7% | 71% | 5% | 0% | 45% | 0% | 4.9 | 23077 | 19.9 | 1.472 |
| google/gemma-4-31b-it | baseline | text | 62% | 78% | 64% | 10% | 58% | 14% | 0% | - | 0% | 0.0 | 1066 | 3.8 | 0.074 |
| google/gemma-4-31b-it | baseline | vision | 80% | 80% | 100% | 0% | 0% | 20% | 0% | - | 0% | 0.0 | 1000 | 7.6 | 0.001 |
| google/gemma-4-31b-it | classic | vision | 100% | 100% | 100% | 0% | 100% | 0% | 0% | 100% | 0% | 1.0 | 17582 | 7.5 | 0.012 |
| google/gemma-4-31b-it | agentic | vision | 100% | 100% | 100% | 0% | 100% | 0% | 0% | 60% | 0% | 7.0 | 34563 | 22.6 | 0.025 |

- Exact and Partial: mean over all runs. Majority: most common answer per question. Margin: 95% interval on Majority from the number of questions.
- Consistency: share of questions answered identically in every run. Recall: share of the question `knowledge` ids the mode retrieved or read.

## Deterministic answers: exact score by technology

| Model | Mode | cpu | memory | network | storage | system |
|---|---|---|---|---|---|---|
| google/gemma-4-31b-it | agentic | 70% | 83% | 91% | 96% | 87% |
| google/gemma-4-31b-it | baseline | 53% | 59% | 77% | 73% | 71% |
| google/gemma-4-31b-it | classic | 83% | 92% | 93% | 100% | 84% |

## Deterministic answers: exact score by task

| Model | Mode | decide-capacity | explain-mechanism | judge-setting | read-metric | troubleshoot |
|---|---|---|---|---|---|---|
| google/gemma-4-31b-it | agentic | 82% | 88% | 40% | 78% | 92% |
| google/gemma-4-31b-it | baseline | 58% | 68% | 28% | 55% | 76% |
| google/gemma-4-31b-it | classic | 81% | 91% | 72% | 94% | 99% |

## Hardest questions (knowledge base modes)

| Question | Mean credit | Common wrong answers or missed points |
|---|---|---|
| 0041 | 0% | VMXNET3 reports 10 Gbps by default regardless of physical uplink; NIOC limits transmit traffic only and applies even when the uplink is idle. ×1, VMXNET3 reports 10 Gbps by default as a label regardless of physical uplink speed; a VMX setting can only raise that reported value and does not limit throughput. ×1, VMXNET3 reports 10 Gbps by default regardless of physical uplink; a VMX setting can only raise this label and never limits throughput; NIOC limits transmit even when uplinks are idle. ×1 |
| 0016 | 0% | ESXi CPU Demand is a true provider metric: the scheduler's internal ideal total demand without contention, not a sum of VM or VMkernel demand. ×3, ESXi CPU Demand is a true provider metric: the scheduler's internal ideal total demand without contention, not a sum of VM Demand metrics. ×2, ESXi CPU Demand is a true provider metric, not a sum of VM metrics; it is the scheduler's internal estimate of ideal total demand without contention. ×1 |
| 0080 | 0% | DS-APP-04, DS-APP-09, and DS-WEB-02 are the top risks; DS-ARCH-01 is thick-provisioned and cannot grow, and vSAN overcommit must count RAID-1's doubled provisioned size. ×1, DS-ARCH-01 is all thick and therefore not the first to run out; the top risks are DS-APP-04, DS-APP-09, and DS-WEB-02, and vSAN RAID-1 must double provisioned capacity when setting the ratio. ×1, DS-WEB-02 as a top thin-growth risk, DS-DEV-11 snapshot risk, and RAID-1 doubling in the vSAN overcommit calculation. ×1 |
| 0113 | 0% | A power-off/restart on an old host does not recalculate vNUMA; the topology changes only when the vCPU count changes, so running on old hosts requires resizing to fit a 12-core node or otherwise match ×1, The vNUMA layout changes only when the vCPU count changes; a power cycle alone does not rebuild it, and the VM should be constrained to new hosts with a DRS VM/Host rule or separate homogeneous cluste ×1, The vNUMA layout changes only when the vCPU count changes; merely powering the VM off does not rebuild it. ×1 |
| 0150 | 0% | Normal operation fits and HA admission control remains green because it counts reservations rather than current usage; the existing VMs have no reservations. ×1, HA admission control counts reservations rather than current consumed usage, so the 1.5 TB reservation fits within the 3 TB admission-control capacity and remains green; normal operation also fits at  ×1, HA admission control remains green because it counts reservations, not the existing VMs' unreserved configured memory. ×1 |
| 0235 | 0% | The peaks are month-end closes, and the aggressive policy underweights them; change to a conservative setting. ×1, Capacity Remaining is the smallest remaining capacity from the highest projected demand over the next three days, and aggressive risk weighting suppresses month-end peaks; the policy should be changed ×1, Capacity Remaining’s 3-day window in mid-November does not include the month-end close, and contention must be checked with VM CPU Ready and Co-stop. ×1 |
| 0269 | 0% | Neither Windows In Use/working set nor VM Active establishes SQL Server's actual memory requirement; lower max server memory incrementally and monitor SQL Server counters and query performance over a  ×1, Neither Windows In Use nor VM Active establishes SQL Server's required memory; lower max server memory incrementally and observe SQL Server counters and query performance over a full business cycle be ×1, Neither Windows In Use nor VM Active shows SQL Server's actual memory need; SQL Server retains allowed RAM as cache, so sizing must be tested by lowering max server memory in steps and monitoring SQL  ×1 |
| 0052 | 10% | A balloon can reflect current or past host pressure, or a VM/resource-pool limit; adding VM memory does not stop it. ×1, It omits that ballooning can reflect current or past host pressure or a VM/resource-pool limit, and that adding VM memory will not stop it. ×1, A balloon can reflect current or past host pressure or a VM/resource-pool limit, and adding VM memory does not stop it. ×1 |
| 0012 | 10% | B ×8, A,B ×1 |
| 0024 | 10% | A,B,E ×3, A,B,D,E ×3, A,B,D ×3 |

Traces: `traces.jsonl` in this folder (one line per answer).
