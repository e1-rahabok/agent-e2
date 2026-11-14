# Collection interval and granularity

## Three ways to collect
| Choice | What is kept | Use |
|---|---|---|
| Point in time | The value at the collection moment | Space and free memory, where the latest value matters |
| Average of the cycle | Mean of every value in the cycle | Complete picture; most metrics |
| Maximum or minimum of the cycle | Worst value in the cycle | Pairs with the average for contention |

- A point-in-time value every 5 minutes keeps second 300 and misses 299 seconds. Over time it swings wider than the average: higher maxima, lower minima.
- Example: VMware Tools reports Guest OS memory as a point in time; Telegraf reports the average. The pattern is similar for stable metrics such as memory and disk space; the values differ.
- Some use cases require two numbers per metric: the average and the worst.
- Most metrics reset to 0 every cycle. A running total is less useful in operations.

## Time as the raw unit of CPU
- vSphere shows CPU in milliseconds, MHz and %. Milliseconds is the source; MHz and % are derived from it.
- The kernel scheduler counts time and the cycles done in that time. A 2 GHz core completes twice the cycles of a 1 GHz core in the same time; a thread with a busy Hyper-Threading sibling completes fewer.
- Read utilization, usage, demand and used as cycles completed in a time window.
- The raw counter is a running total in microseconds (vsish: `cpu-latency:798578245914 usec`). A 20-second value is the difference between two readings; % divides it by 20,000 ms.
- When a collection runs late or the host is busy, the states of one vCPU can sum to slightly above 20,000 ms.
- A CPU value at 9:00:00 is the average of the previous cycle, not the state at that second.
- MHz values only compare across hosts with the same static frequency. Mixed CPU generations in one cluster make MHz metrics hard to use as DRS moves VMs. One reason the cluster is the unit of capacity.

## Short problems in 5-minute collection
- VCF Operations collects every 5 minutes by default. A problem shorter than 5 minutes can be missed.
- Example: idle 08:00:00-08:02:30, busy 08:02:30-08:07:30, idle again. Collections at 08:00, 08:05 and 08:10 each average half busy, half idle. To appear whole in one point, a spike may have to last 10 minutes.
- The 100% of any millisecond value in VCF Operations is 20,000 ms, not 300,000 ms: it averages the 15 20-second values. CPU Ready of 3,000 ms is 15%, not 1%.
- Storing all 15 20-second values costs 15x the data. Usually only the peak is used: [`vcf-operations/features/peak-20-second-metrics`](../../vcf-operations/features/peak-20-second-metrics.md).
- vCenter statistics levels do not apply to VCF Operations. It collects from vCenter through its own filter, set in the policy ([`vsphere/tools/vsphere-client/vcenter-statistics`](../../vsphere/tools/vsphere-client/vcenter-statistics.md)).
- The vSAN API returns the latest value, not the average or peak. At a 5-minute cycle that is second 300 only.
- Collection frequency is not granularity: VCF Operations collects every 5 minutes but takes 15 20-second points per cycle.

## Granularity by use case
| Use case | Granularity |
|---|---|
| Performance profiling | 1-20 seconds for every counter |
| Performance troubleshooting | 1-20 seconds for raw contention; 5 minutes for the rest |
| Performance KPI | 20-second peak and 5-minute average |
| Capacity | 15 minutes, the average, not the peak |

- Capacity does not require 15-minute points functionally. Operationally it is safer: a failed collection loses 15 minutes, not more.
- Per-second data everywhere is not the goal:
  - the source may not produce it, or pays a performance or capacity cost to produce it;
  - the monitoring system can grow as large as the system it monitors; the money may be better spent on hardware;
  - each extra point adds less: the first one carries the most information;
  - the fix is the same: there are few remedies for many problems.
- Start from the fix (add hardware, change a setting), list the metrics it requires, then the granularity each requires.
- 1-20 seconds is required for contention metrics only. Consumption and context: 5 minutes.
- Higher resolution also helps where a contention metric does not exist. A VM has no network latency or retransmit metric, only dropped packets; read packets per second and throughput at high resolution instead.
- 2-second data in VCF Operations 9.1: [`vcf-operations/features/real-time-metrics`](../../vcf-operations/features/real-time-metrics.md).

## Misconceptions
- "CPU Ready 3,000 ms in a 5-minute VCF Operations point is 1%" → the base is 20,000 ms: 15%.
- "No alert in VCF Operations, so there was no 5-minute spike" → a spike split across two collections may never show whole; it may have to last 10 minutes.
- "Raise the vCenter statistics level to get more in VCF Operations" → the level does not apply; VCF Operations uses its policy.
- "The vSAN value is the 5-minute average" → the vSAN API gives the last value only.
- "Collect everything every second" → only contention requires 1-20 seconds; the rest costs more than it tells.
- "CPU MHz compares across hosts" → only at the same static frequency.

## Metadata
```yaml
id: sp5-framework/observability/collection-interval
retriever_guide: how-it-works
scope: sp5-framework
technology:
- cpu
- system
pillar:
- performance
- capacity
product:
- vsphere
- vcf-operations
internal_derive: []
related:
- vcf-operations/vcf-operations-role
- vsphere/tools/vsphere-client/vcenter-statistics
- vcf-operations/features/peak-20-second-metrics
- sp5-framework/observability/aggregation
- sp5-framework/observability/measurement-precision
- vcf-operations/features/real-time-metrics
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download), Metric Mastery (update of 2026-11-08)
  path: Metric Mastery > Collection Interval; Why Milliseconds as Unit?; Rollup Type; Real Time Collection; Performance Troubleshooting
corrections: []
review_notes: []
status: draft
```
