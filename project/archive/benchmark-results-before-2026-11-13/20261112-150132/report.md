# Benchmark report: 20261112-150132

- Index version: `31c2d87209c0`. Retrieval: hybrid. Temperature: 0.2. Runs: 5.
- Questions: 150 (deterministic 90, judged 60; text 114, table 35, screenshot 1; level 100: 5, level 200: 15, level 300: 40, level 400: 90). Skipped: 0034, 0037, 0042, 0051, 0050. Judge: openai/gpt-5.6-sol.
- Answers: 2250 scored, 0 failed.

## Final score

| Model | Mode | Final | ± margin | Luck | Confident wrong | Override |
|---|---|---|---|---|---|---|
| meta/muse-glimmer-30b | classic | 64% | 8% | 33% | 18% | 4% |
| meta/muse-glimmer-30b | agentic | 56% | 8% | 38% | 22% | 2% |
| meta/muse-glimmer-30b | baseline | 37% | 8% | 37% | 43% | - |

## Release gate

Agentic mode. Reference: anthropic/claude-opus-5.5, baseline mode (not in this benchmark: gap not read).

| Model | Gate | Value | Limit | Pass |
|---|---|---|---|---|
| meta/muse-glimmer-30b | Final score | 56% | at least 85% | no |
| meta/muse-glimmer-30b | Level 400 | 51% | at least 80% | no |
| meta/muse-glimmer-30b | Confident wrong | 22% | at most 3% | no |

- Not read here: no misconception of `knowledge/misconceptions.md` stated as true (author check), and the held-out set within 5 points (separate run). Method: `benchmark/design.md`, section 7.5.

## Sub-scores

| Model | Mode | Deterministic | Judged | Text | Table | Screenshot | Level 100 | Level 200 | Level 300 | Level 400 |
|---|---|---|---|---|---|---|---|---|---|---|
| meta/muse-glimmer-30b | classic | 81% | 38% | 68% | 50% | 100% | 100% | 73% | 69% | 58% |
| meta/muse-glimmer-30b | agentic | 72% | 32% | 60% | 43% | 100% | 100% | 67% | 57% | 51% |
| meta/muse-glimmer-30b | baseline | 49% | 19% | 39% | 31% | 0% | 80% | 33% | 42% | 33% |

- Final: mean question credit over all questions, 0-100%. Every question weighs the same.
- Question credit = the worst of its runs. Deterministic: 1 if the letters are exact in every run, else 0. Judged: lowest judge score / 3.
- Sub-scores: the same mean within one group. By answer type, by input type (a question counts for every input it includes), by level.
- Luck: share of questions whose credit differs between runs. Confident wrong: share of answers that are wrong and not Unsure (judged: score 0, not unsure).
- Override: share of answers in knowledge base modes that state the misconception although every needed file was in the context: the model kept its own belief over the knowledge base. Target: 0. See `benchmark/models.md`, section 1.
- Method: `benchmark/design.md`, sections 3 and 7.4.

## Judged answers

| Model | Mode | Mean score 0-3 | Score 3 | Score 0 | Misconception | Unsure |
|---|---|---|---|---|---|---|
| meta/muse-glimmer-30b | agentic | 1.86 | 56% | 35% | 4% | 1% |
| meta/muse-glimmer-30b | baseline | 1.17 | 32% | 57% | 13% | 6% |
| meta/muse-glimmer-30b | classic | 1.92 | 52% | 30% | 5% | 0% |

## Deterministic answers: luck-free scores

| Model | Mode | Track | Stable correct | ± margin | Luck | Stable unsure | Confident wrong | Unsure | Accuracy when answered |
|---|---|---|---|---|---|---|---|---|---|
| meta/muse-glimmer-30b | classic | text | 81% | 8% | 15% | 0% | 10% | 0% | 90% |
| meta/muse-glimmer-30b | agentic | text | 72% | 9% | 25% | 0% | 14% | 0% | 86% |
| meta/muse-glimmer-30b | baseline | text | 49% | 10% | 26% | 0% | 37% | 1% | 63% |
| meta/muse-glimmer-30b | classic | vision | 100% | 0% | 0% | 0% | 0% | 0% | 100% |
| meta/muse-glimmer-30b | agentic | vision | 100% | 0% | 0% | 0% | 0% | 0% | 100% |
| meta/muse-glimmer-30b | baseline | vision | 0% | 0% | 0% | 0% | 100% | 0% | 0% |

- Stable correct: share of questions answered correctly in every run. The headline score: a known answer, not a guess.
- Luck: share of questions correct in some runs but not all. Counted as not known.
- Stable unsure: share of questions where the model chose Unsure in every run.
- Confident wrong: share of answers that are wrong and not Unsure (wrong letters, partly right, Unsure mixed with other letters, unparseable). The answers that mislead an operator. Target: near 0.
- Accuracy when answered: exact share among answers that were not Unsure.

## Deterministic answers: scores

| Model | Mode | Track | Exact | Partial | Majority | ± margin | Consistency | Misconception | Parse fail | Recall | Fallback | Steps | Tokens | Latency s | Cost US$ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| meta/muse-glimmer-30b | classic | text | 90% | 95% | 92% | 6% | 83% | 3% | 1% | 78% | 0% | 1.0 | 15519 | 20.2 | 3.403 |
| meta/muse-glimmer-30b | agentic | text | 86% | 89% | 90% | 6% | 72% | 1% | 8% | 57% | 0% | 8.1 | 28987 | 33.6 | 6.060 |
| meta/muse-glimmer-30b | baseline | text | 63% | 75% | 64% | 10% | 62% | 9% | 10% | - | 0% | 0.0 | 2996 | 21.9 | 1.598 |
| meta/muse-glimmer-30b | classic | vision | 100% | 100% | 100% | 0% | 100% | 0% | 0% | 100% | 0% | 1.0 | 19397 | 15.6 | 0.042 |
| meta/muse-glimmer-30b | agentic | vision | 100% | 100% | 100% | 0% | 100% | 0% | 0% | 72% | 0% | 8.8 | 34511 | 24.1 | 0.070 |
| meta/muse-glimmer-30b | baseline | vision | 0% | 0% | 0% | 0% | 0% | 60% | 40% | - | 0% | 0.0 | 6447 | 33.8 | 0.031 |

- Exact and Partial: mean over all runs. Majority: most common answer per question. Margin: 95% interval on Majority from the number of questions.
- Consistency: share of questions answered identically in every run. Recall: share of the question `knowledge` ids the mode retrieved or read.

## Deterministic answers: exact score by technology

| Model | Mode | cpu | memory | network | storage | system |
|---|---|---|---|---|---|---|
| meta/muse-glimmer-30b | agentic | 84% | 88% | 90% | 81% | 83% |
| meta/muse-glimmer-30b | baseline | 56% | 59% | 63% | 70% | 72% |
| meta/muse-glimmer-30b | classic | 87% | 91% | 97% | 88% | 84% |

## Deterministic answers: exact score by task

| Model | Mode | decide-capacity | explain-mechanism | judge-setting | read-metric | troubleshoot |
|---|---|---|---|---|---|---|
| meta/muse-glimmer-30b | agentic | 80% | 90% | 84% | 84% | 91% |
| meta/muse-glimmer-30b | baseline | 66% | 60% | 24% | 62% | 69% |
| meta/muse-glimmer-30b | classic | 87% | 92% | 80% | 88% | 96% |

## Hardest questions (knowledge base modes)

| Question | Mean credit | Common wrong answers or missed points |
|---|---|---|
| 0041 | 0% | VMXNET3 reports a default 10 Gbps label independent of the physical uplink; a VMX setting can only raise that reported value and does not limit throughput. ×1, VMXNET3 reports 10 Gbps by default regardless of the physical uplink; a VMX setting can only raise that reported value and does not limit throughput. ×1, The VMXNET3-reported 10 Gbps speed is only a label independent of the physical uplink; a VMX setting can raise that reported value but does not limit throughput, and same-host VM traffic can exceed it ×1 |
| 0016 | 0% | ESXi CPU Demand is a true provider metric: the scheduler's internal ideal total demand without contention, not a sum of VM Demand. ×2, ESXi CPU Demand is a true provider metric representing the scheduler's ideal total demand without contention, not a sum of VM demand. ×1, ESXi CPU Demand is a true provider metric: the scheduler's internal ideal total demand without contention, not a sum of VM demand or VMkernel worlds. ×1 |
| 0022 | 0% | B,D,E ×8, B,D ×1, UN ×1 |
| 0080 | 0% | DS-ARCH-01 is all thick, so its existing disks cannot grow; it should be watched for new snapshots and swap but is not among the first to run out. ×1, DS-ARCH-01 is all thick and cannot grow from existing VMDKs, so it is not the first datastore likely to run out; DS-APP-04, DS-APP-09, and DS-WEB-02 are the top risks. ×1, DS-ARCH-01 is all thick, so existing disks cannot grow; despite 95% used it is not the first datastore likely to run out and should mainly be watched for new snapshots and swap files. ×1 |
| 0183 | 0% | From VCF 9.0, storage policies honor only limits; shares and reservations are ignored, so High shares cannot protect db-11. ×1, In VCF 9.0 and later, storage-policy shares and reservations are ignored; only limits are honored. ×1, In VCF 9.0 and later, shares and reservations are ignored; confirm array/fabric contention by finding high DAVG with low KAVG. ×1 |
| 0235 | 0% | Capacity Remaining is the smallest remaining capacity at the highest projected demand in the next three days, and CPU Ready/Co-stop should be checked at month-end. ×1, Capacity Remaining is the smallest remaining capacity at the highest projected demand in the next three days; the answer reverses this and also omits checking CPU Ready and Co-stop at month-end. ×1, Capacity Remaining is the smallest remaining capacity at the highest projected demand in the next three days, and CPU Ready/Co-stop should be checked during the last month-end close. ×1 |
| 0240 | 0% | A,C ×4, (unparsed) ×3, UN ×1 |
| 0150 | 7% | Admission control counts reservations, not configured memory or current usage; after failure the 1.5 TB reservation fits in 3 TB, while existing VMs are forced into heavy reclamation. ×1, Admission control remains green because it counts the 1.5 TB of reservations but not the unreserved existing VMs' usage. ×1, HA admission control stays green because it counts reservations, not the unreserved configured memory of existing VMs; after failure the VMs can run but existing VMs suffer heavy reclamation. ×1 |
| 0049 | 10% | B,D ×7, (unparsed) ×2 |
| 0113 | 10% | The vNUMA layout changes only when the vCPU count changes, not merely after powering off and restarting on an old host. ×1, The vNUMA layout changes only when the vCPU count changes; merely powering off and restarting on an old host does not rebuild it for that host. ×1, The vNUMA layout changes only when the vCPU count changes; powering off and restarting on an old host alone does not rebuild it. ×1 |

Traces: `traces.jsonl` in this folder (one line per answer).
