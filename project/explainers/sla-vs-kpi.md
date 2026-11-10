# SLA vs KPI: a worked example

For people, not for Agent E2. Not indexed. Agent E2 reads the rules in `knowledge/sp5-framework/performance/kpi-vs-sla.md`; this file shows them with numbers.

## The rules
| | SLA | KPI |
|---|---|---|
| What it measures | Whether the contract was kept | Reality: the absolute value, how bad |
| Per 5-minute interval | SLI: pass or fail against the promised threshold. A fail is a fail: 1.01% and 50% count the same | A score from 0 to 100, lower as the metric gets worse |
| Actual | Share of passed intervals in the calendar month. Volatile, per VM | The VM's score. Volatile, per VM |
| Target | Per class of service: Gold 99.9%, Silver 99.8%, Bronze 99.6%. Steady, for many VMs | Per class of service: Gold 99.5%, Silver 99%, Bronze 98%. Steady, for many VMs. The colour levels are the same for every class |
| Cadence | Monthly, a business meeting with stakeholders | Daily, a technical meeting. A month is far too late |

- SLA and KPI are not mathematically related. One cannot be computed from the other.

## Setup
- Two Gold VMs, June 2026: 30 days, 8,640 five-minute intervals.
- SLI: VM Memory Contention, 5-minute average, fails above 1%. Gold SLA target 99.9%.
- KPI: VM Performance (%), Gold target 99.5%.
  - Its memory sub-metric is Peak RAM Contention. It scores 100 at 0%, 75 at 0.5%, 50 at 1%, 25 at 2% and 0 at 4% and above, in a straight line between those points.
  - The VM Performance (%) score is the weighted average of the sub-metric scores, with weight 2 ^ ((100 - score) / 25), so a bad sub-metric weighs more (`knowledge/sp5-framework/performance/performance-kpi-design.md`, Scoring).
- Simplifications:
  - the other 8 sub-metrics stay at 100 all month;
  - the 20-second peak equals the 5-minute average (in reality the peak is at least the average, so the KPI could only be worse);
  - a normal interval has 0% contention (a Gold VM runs at 1:1 memory).

| | VM 01 | VM 02 |
|---|---|---|
| Bad intervals | 5 at 50% (25 minutes, one episode on 12 June) | 100 at 1.01%, spread over the month: 3 or 4 a day |

## SLA, monthly
| | VM 01 | VM 02 |
|---|---|---|
| SLI fails | 5 | 100 |
| SLA actual | 8,635 / 8,640 = 99.94% | 8,540 / 8,640 = 98.84% |
| Against Gold 99.9% | Pass | Fail |

- VM 02 is in breach of contract; VM 01 is not. The SLI did not care that VM 01 failed at 50% and VM 02 at 1.01%.

## KPI, per interval
| Memory contention | Memory sub-metric score | Its weight | VM Performance (%) | Colour of the score |
|---|---|---|---|---|
| 0% | 100 | 1 | 100 | Green |
| 1.01% | 50 - 25 × 0.01 = 49.75 | 2 ^ 2.01 = 4.03 | (8 × 100 + 49.75 × 4.03) / (8 + 4.03) = 83.17 | Green (75-100), though the memory sub-metric is orange |
| 50% | 0 (past 4%) | 16 | (8 × 100 + 0) / (8 + 16) = 33.33 | Orange (25-50) |

## KPI, daily
Daily actual taken here as the average of the day's 288 interval scores (to confirm: Q161).

| Day | VM 01 | VM 02 |
|---|---|---|
| 12 June | (283 × 100 + 5 × 33.33) / 288 = 98.84 | 99.77 or 99.82 |
| Any other day | 100 | 99.77 (4 bad intervals) or 99.82 (3) |
| Against Gold 99.5 | Fails on 12 June | Passes every day |

- On 12 June the technical meeting sees VM 01 below its Gold KPI target and starts troubleshooting. 98.84 would also fail Silver (99) and only pass Bronze (98).
- VM 02 never misses its KPI target, yet it breaches the contract.

## What the example shows
- The two rankings are opposite. On the SLA, VM 01 is better (99.94% against 98.84%). On the KPI, VM 01 is worse: 25 minutes where memory was so short that the application stalled.
- SLA answers "did we keep the promise?" for the business, once a month. KPI answers "how did the VM actually perform?" for the technical team, every day.
- Fixing only what breaches the SLA would leave VM 01's stall unexplained. Fixing only the KPI would leave VM 02's breach and its penalty unseen.
- A Gold VM must keep a higher KPI score than a Silver VM: the target differs by class, the colour levels do not.
