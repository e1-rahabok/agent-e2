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

## Base of a millisecond value
- The VM CPU counters in ms (Run, Ready, Co-stop, Wait, Idle, Used, System, Overlap, Max limited, Swap wait) are summation counters: each 20-second sample holds the ms that one vCPU spent in the state, or was charged, during those 20 seconds (vSphere Web Services API 9.1, CPU counters: stats type delta, rollup type summation).
- 100% of one vCPU is the length of the sample in ms. A VM value adds up its vCPUs, so the VM's 100% is that length times the vCPU count.
- VCF Operations stores the average of the 15 20-second values of a 5-minute cycle, not their sum (Broadcom KB 315941; KB 444403 for VCF Operations 9.x). A VCF Operations ms value of a summation counter is therefore a value per 20 seconds: 100% is 20,000 ms per vCPU, 80,000 ms for a 4-vCPU VM.
- The states of a VM at one VCF Operations 5-minute point (Run + Ready + Co-stop + Wait) add up to about 20,000 ms × vCPUs, the same total as one vCenter real-time sample ([`vsphere/technology/cpu/concepts/vcpu-states`](../../vsphere/technology/cpu/concepts/vcpu-states.md), section State across time).
- A VCF Operations 5-minute value of a summation counter is a whole multiple of 1/15 ms, within display rounding, because each 20-second value is a whole number of ms: a Co-stop of 1,151.6 ms is 17,274 / 15. A sum of the 15 values would be a whole number.
- VCF Operations 9.1 defines CPU Contention (%) as a percentage of the 20-second collection interval (VCF Operations 9.1 documentation, Virtual Machine Metrics).
- A VCF Operations view or chart that rolls 5-minute points up by average (one point per hour or per day) keeps the 20,000 ms base. A rollup by sum multiplies the base by the number of points summed.
- vCenter rolls summation counters up by sum, so the base grows with the chart interval: real time 20,000 ms, Past Day (5-minute points) 300,000 ms, Past Week (30 minutes) 1,800,000 ms, Past Month (2 hours) 7,200,000 ms, Past Year (1 day) 86,400,000 ms per vCPU (Broadcom KB 306576).
- The same 5 minutes of the same VM read about 15 times higher in ms on the vCenter Past Day chart than in VCF Operations, because vCenter sums the 15 samples and VCF Operations averages them. Converted to %, both agree.
- Percent from a VCF Operations ms value: value / (20,000 × vCPUs) × 100. CPU Ready of 3,000 ms is 15% on a 1-vCPU VM and 3.75% on a 4-vCPU VM.
- Broadcom KB 394770 and KB 398528 compute CPU Contention (%) from the ms of the 15 raw 20-second samples divided by 300,000 ms (times the vCPU count in KB 398528). That 300,000 ms base fits the sum of the raw samples, not the stored 5-minute ms value, which is their average.

## Short problems in 5-minute collection
- VCF Operations collects every 5 minutes by default. A problem shorter than 5 minutes can be missed.
- Example: idle 08:00:00-08:02:30, busy 08:02:30-08:07:30, idle again. The points at 08:05 and 08:10 each average half busy, half idle; the 08:00 point covers 07:55-08:00 and is idle. To appear whole in one point, a spike may have to last 10 minutes.
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
- "CPU Ready 3,000 ms in a 5-minute VCF Operations point of a 1-vCPU VM is 1%" → VCF Operations averages the 15 20-second values, so the base is 20,000 ms per vCPU: 15%.
- "A VCF Operations 5-minute point sums its 15 samples, so a 4-vCPU VM's 100% is 1,200,000 ms" → that is the vCenter Past Day sum; VCF Operations stores the average, so the VM's 100% is 80,000 ms.
- "VCF Operations shows 15 times less Ready in ms than the vCenter Past Day chart, so one tool is wrong" → vCenter sums the 15 samples and VCF Operations averages them; the % agrees.
- "KB 398528 divides Contention by 300,000 ms × vCPUs, so VCF Operations ms values have a 300,000 ms base" → the KB divides the sum of the 15 raw 20-second samples; the stored 5-minute value is their average, base 20,000 ms per vCPU.
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
- vsphere/technology/cpu/concepts/vcpu-states
source:
  document: Knowledge base; Broadcom KB 315941, Aria Operations (formerly vRealize Operations) Data Collection; Broadcom KB 444403, Understanding "Peak" or "Worst" Performance Metrics in VMware VCF / Aria Operations (VCF Operations 9.x); Broadcom KB 306576 (legacy 2002181), Converting between CPU summation and CPU % ready values; Broadcom KB 394770, How is CPU Contention (%) calculated; Broadcom KB 398528 (Aria Operations 8.18 and later); VCF Operations 9.1 documentation (TechDocs, last updated 2026-11-12), Virtual Machine Metrics; vSphere Web Services API 9.1, CPU Counters
  path: Metric Mastery > Collection Interval; Why Milliseconds as Unit?; Rollup Type; Real Time Collection; Performance Troubleshooting; Base of a millisecond value from KB 315941 (15 samples averaged into the stored value), KB 444403 (standard metrics are the average of the 15 samples), KB 306576 (vCenter chart intervals), KB 394770 and KB 398528 (Contention over 300,000 ms), Virtual Machine Metrics (CPU Contention (%) as a percentage of the 20-second collection interval), API 9.1 CPU Counters (delta, millisecond, summation)
corrections: []
review_notes: []
status: draft
```
