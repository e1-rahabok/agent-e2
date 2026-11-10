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
Daily KPI actual for performance: the 95th percentile of the day's 288 scores, the score that 95% of the intervals reach or exceed. The worst 5% (14 intervals, 70 minutes) are ignored.

| Day | VM 01 | VM 02 |
|---|---|---|
| 12 June | 5 of 288 intervals at 33.33, all inside the ignored 14: daily KPI 100 | 3 or 4 intervals at 83.17, ignored: 100 |
| Any other day | 100 | 100 |
| Against Gold 99.5 | Pass | Pass |

- The daily KPI does not move for a 25-minute episode. It shows sustained degradation, not a single burst: that is the design.
- Had VM 01's episode lasted 2 hours (24 intervals), the worst 14 would be ignored and the 15th worst, 33.33, would be the daily KPI: far below 99.5. The technical meeting would see it the next morning.

## The alert, the same day
- The 25-minute episode at 50% is caught by the VM memory contention alert, not by the KPI. The red alert needs VM Memory Contention above 6% (5-minute), Peak Memory Contention above 24% and CPU Usage above 1 GHz, all together (`knowledge/vsphere/technology/memory/configuration/memory-alerts.md`).
- At 50%, all hold (assuming the VM is busy), so the alert fires after its wait cycle: one 5-minute collection. The admin acts within 1-2 hours.
- VM 02 at 1.01% stays far below the orange alert (3%): no alert, correctly. Nothing urgent happened to it.

## What the example shows
- Three instruments, three questions:

| Instrument | VM 01 (5 intervals at 50%) | VM 02 (100 intervals at 1.01%) | Question it answers |
|---|---|---|---|
| SLA, monthly | Pass (99.94%) | Fail (98.84%) | Did we keep the promise? A fail is a fail |
| KPI, daily 95th percentile | Pass (100) | Pass (100) | Is the VM performing, day after day? |
| Alert, intra-day | Red, on 12 June | None | Must someone act now? |

- The SLA ranks VM 02 worse; the alert ranks VM 01 worse; the daily KPI sees neither, because neither degraded for more than 70 minutes in a day.
- None of them can be computed from another. Each needs its own threshold, its own time span and its own spike filter: the SLI's pass or fail, the KPI's 95th percentile, the alert's wait cycle.
- A Gold VM must keep a higher KPI score than a Silver VM: the target differs by class, the colour levels do not.
