# Benchmark report: 20261113-muse-glimmer-30b-2

- Index version: `de2551c8d790`. Retrieval: hybrid. Sampling: {"meta/muse-glimmer-30b": {"temperature": 1.0, "top_p": 0.95, "top_k": 64}}. Runs: 5.
- Questions: 196 (deterministic 119, judged 77; text 155, table 35, screenshot 6; level 100: 8, level 200: 17, level 300: 40, level 400: 131). Skipped: none. Judge: openai/gpt-6.1-terra.
- Answers: 2940 scored, 0 failed.

## Final score

| Model | Mode | Final | ± margin | Worst run | Luck | Confident wrong | Override |
|---|---|---|---|---|---|---|---|
| meta/muse-glimmer-30b | agentic | 78% | 6% | 59% | 36% | 20% | 1% |
| meta/muse-glimmer-30b | classic | 77% | 6% | 60% | 34% | 21% | 3% |
| meta/muse-glimmer-30b | baseline | 54% | 7% | 36% | 37% | 42% | - |

## Release gate

Agentic mode. Reference: anthropic/claude-opus-5.5, web mode (not in this benchmark: gap not read).

| Model | Gate | Value | Limit | Pass |
|---|---|---|---|---|
| meta/muse-glimmer-30b | Final score | 78% | at least 85% | no |
| meta/muse-glimmer-30b | Level 400 | 75% | at least 80% | no |
| meta/muse-glimmer-30b | Confident wrong | 20% | at most 3% | no |

- Not read here: no misconception of `knowledge/misconceptions.md` stated as true (author check), and the held-out set at most 11 points below the development set (separate run). Method: `benchmark/design.md`, section 7.5.

## Sub-scores

| Model | Mode | Deterministic | Judged | Text | Table | Screenshot | Level 100 | Level 200 | Level 300 | Level 400 |
|---|---|---|---|---|---|---|---|---|---|---|
| meta/muse-glimmer-30b | agentic | 87% | 65% | 80% | 68% | 93% | 92% | 80% | 86% | 75% |
| meta/muse-glimmer-30b | classic | 86% | 63% | 79% | 68% | 83% | 88% | 83% | 82% | 74% |
| meta/muse-glimmer-30b | baseline | 66% | 35% | 55% | 44% | 70% | 71% | 57% | 54% | 52% |

- Final: mean question credit over all questions, 0-100%. Every question weighs the same.
- Question credit = the mean of its runs. Deterministic: share of runs with the exact letters. Judged: mean judge score / 3. Worst run: the same score with each question on its lowest run (consistency; not a gate).
- Sub-scores: the same mean within one group. By answer type, by input type (a question counts for every input it includes), by level.
- Luck: share of questions whose credit differs between runs. Confident wrong: share of answers that are wrong and not Unsure (judged: score 0, not unsure).
- Override: share of answers in knowledge base modes that state the misconception although every needed file was in the context: the model kept its own belief over the knowledge base. Target: 0. See `benchmark/models.md`, section 1.
- Method: `benchmark/design.md`, sections 3 and 7.4.

## Judged answers

| Model | Mode | Mean score 0-3 | Score 3 | Score 0 | Misconception | Unsure |
|---|---|---|---|---|---|---|
| meta/muse-glimmer-30b | agentic | 1.94 | 61% | 34% | 4% | 1% |
| meta/muse-glimmer-30b | baseline | 1.05 | 32% | 63% | 17% | 4% |
| meta/muse-glimmer-30b | classic | 1.88 | 55% | 34% | 4% | 0% |

## Deterministic answers: luck-free scores

| Model | Mode | Track | Stable correct | ± margin | Luck | Stable unsure | Confident wrong | Unsure | Accuracy when answered |
|---|---|---|---|---|---|---|---|---|---|
| meta/muse-glimmer-30b | classic | text | 77% | 8% | 15% | 1% | 12% | 2% | 88% |
| meta/muse-glimmer-30b | agentic | text | 76% | 8% | 19% | 0% | 13% | 1% | 87% |
| meta/muse-glimmer-30b | baseline | text | 50% | 9% | 28% | 0% | 32% | 3% | 68% |
| meta/muse-glimmer-30b | classic | vision | 83% | 30% | 0% | 0% | 17% | 0% | 83% |
| meta/muse-glimmer-30b | agentic | vision | 83% | 30% | 17% | 0% | 7% | 0% | 93% |
| meta/muse-glimmer-30b | baseline | vision | 67% | 38% | 17% | 0% | 30% | 0% | 70% |

- Stable correct: share of questions answered correctly in every run. The headline score: a known answer, not a guess.
- Luck: share of questions correct in some runs but not all. Counted as not known.
- Stable unsure: share of questions where the model chose Unsure in every run.
- Confident wrong: share of answers that are wrong and not Unsure (wrong letters, partly right, Unsure mixed with other letters, unparseable). The answers that mislead an operator. Target: near 0.
- Accuracy when answered: exact share among answers that were not Unsure.

## Deterministic answers: scores

| Model | Mode | Track | Exact | Partial | Majority | ± margin | Consistency | Misconception | Parse fail | Recall | Seen | Fallback | Steps | Tokens | Latency s | Cost US$ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| meta/muse-glimmer-30b | agentic | text | 87% | 92% | 88% | 6% | 78% | 3% | 1% | 60% | 80% | 0% | 7.1 | 42147 | 25.2 | 9.322 |
| meta/muse-glimmer-30b | classic | text | 86% | 91% | 87% | 6% | 81% | 4% | 0% | 78% | 78% | 0% | 1.0 | 13907 | 9.0 | 3.168 |
| meta/muse-glimmer-30b | baseline | text | 65% | 78% | 67% | 9% | 60% | 10% | 0% | - | - | 0% | 0.0 | 1289 | 6.9 | 0.618 |
| meta/muse-glimmer-30b | agentic | vision | 93% | 93% | 100% | 0% | 83% | 0% | 0% | 29% | 46% | 0% | 6.7 | 56176 | 26.2 | 0.630 |
| meta/muse-glimmer-30b | classic | vision | 83% | 83% | 83% | 30% | 100% | 0% | 0% | 53% | 53% | 0% | 1.0 | 16372 | 5.5 | 0.181 |
| meta/muse-glimmer-30b | baseline | vision | 70% | 70% | 67% | 38% | 83% | 13% | 0% | - | - | 0% | 0.0 | 3970 | 5.3 | 0.052 |

- Exact and Partial: mean over all runs. Majority: most common answer per question. Margin: 95% interval on Majority from the number of questions.
- Consistency: share of questions answered identically in every run. Recall: share of the question `knowledge` ids whose text reached the model (classic: the context; agentic: the first lookup and the files it read). Seen: the same share counting search results too; Seen above Recall means files found but not read.

## Deterministic answers: exact score by technology

| Model | Mode | cpu | memory | network | storage | system |
|---|---|---|---|---|---|---|
| meta/muse-glimmer-30b | agentic | 89% | 89% | 88% | 82% | 88% |
| meta/muse-glimmer-30b | baseline | 60% | 61% | 64% | 70% | 73% |
| meta/muse-glimmer-30b | classic | 82% | 91% | 89% | 86% | 87% |

## Deterministic answers: exact score by task

| Model | Mode | decide-capacity | explain-mechanism | judge-setting | read-metric | troubleshoot |
|---|---|---|---|---|---|---|
| meta/muse-glimmer-30b | agentic | 79% | 86% | 87% | 89% | 90% |
| meta/muse-glimmer-30b | baseline | 64% | 57% | 64% | 62% | 77% |
| meta/muse-glimmer-30b | classic | 79% | 85% | 81% | 84% | 96% |

## Hardest questions (knowledge base modes)

| Question | Mean credit | Common wrong answers or missed points |
|---|---|---|
| 0041 | 0% | VMXNET3 reports 10 Gbps by default regardless of uplink speed; a VMX setting can change the reported speed upward without limiting throughput. ×2, VMXNET3 reports 10 Gbps by default regardless of uplink speed; a VMX setting can raise the reported speed without limiting throughput. ×2, VMXNET3 reports 10 Gbps by default regardless of physical uplink speed; its reported speed is not a throughput limit. ×1 |
| 0046 | 0% | A,B,C ×10 |
| 0006 | 0% | GHz figures measure performance, not capacity. ×3, GHz figures are performance figures, not host capacity. ×1, GHz figures measure performance, not total capacity. ×1 |
| 0330 | 0% | B ×10 |
| 0235 | 0% | Capacity Remaining is the smallest gap over the next three days; also add the project’s demand to the projection and check CPU Ready and Co-stop at month-end. ×1, Capacity Remaining is the smallest remaining capacity over the next three days, corresponding to the highest projected demand. ×1, Capacity Remaining is the smallest gap to usable capacity over the next three days. ×1 |
| 0240 | 0% | A,C ×8, UN ×2 |
| 0279 | 0% | Add a dynamic Virtual Machine custom group directly or nested in the business application, with a name rule that excludes test VMs; check both vCenters with Preview and do not promise a refresh time. ×1, A dynamic VM custom group can be added to the business application, with name rules that exclude test VMs. ×1, A dynamic VM custom group can be added directly or nested in the business application, with a name rule that excludes test VMs and applies across both vCenter adapters. ×1 |
| 0310 | 10% | UN ×7, (unparsed) ×2 |
| 0297 | 10% | Swap files are copied between different locations during vMotion even when no pages are swapped; the one-host-down capacity shortfall is also missed. ×1, SAN space is reclaimed gradually for VMs moved to configured hosts, though hosts 7 and 8 retain swap files on SAN; vMotion copies swap files when locations differ. ×1, The swap file is copied between differing locations during vMotion, even when no pages are swapped. ×1 |
| 0062 | 10% | High DAVG despite low array latency can point to the HBA or fabric. ×2, DAVG can be high despite low array-reported latency, pointing to the HBA or FC fabric. ×1, High DAVG despite low array latency points to the HBA or fabric; elevated KAVG points to kernel queues. ×1 |

Traces: `traces.jsonl` in this folder (one line per answer).
