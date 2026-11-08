# Aggregation: summarizing many objects

## No lossless summary
- Aggregating to a parent object represents many values with one. Every technique loses detail: mean, median, maximum, minimum, percentile, sum, count.
- Average works across time. Across members of a group it hides the outlier until the problem is widespread: by the time the average of 1,000 VMs is bad, about a hundred are already bad.

## Divide summed counters correctly
- ESXi CPU Ready (ms) = sum of VM CPU Ready; VM CPU Ready = sum of its vCPU Ready.
- Example: a host with 149,116 ms Ready runs 67 VMs with 195 vCPUs. Each vCPU can reach 20,000 ms, so the number means nothing until divided:

```text
ESXi CPU Ready (%) = ESXi CPU Ready (ms) / (20,000 ms × vCPUs of running VMs)
```

- Divide by running vCPUs, not by physical cores.
- Ready is not spread evenly: larger VMs tend to show more, as they have more vCPUs.

## Leading and lagging
- Performance is read on contention, which jumps at the point of overcommit; consumption climbs toward 100% gradually.
- A VDI system built for 1,000 users serves the first 1,000 well and then degrades suddenly. An average across the group reacts late: it is a lagging indicator.
- The absolute maximum reacts early but carries outliers. A worst percentile (5th or 1st) sits between.

## Techniques
| Technique | Returns | Fits | Limit |
|---|---|---|---|
| Worst | The worst member | Few members (hosts in a cluster, containers in a pod); 12 points of an hour | Frequent outliers |
| Percentile | The member after cutting the worst share | Many members | One member only: no sign of a population problem |
| Average of worsts | Mean of all members above a percentile (95th-100th) | More stable than one percentile | Skewed by outliers; then use 90th or 92.5th |
| Count | Members in a band (red, orange) | Very large groups; expected near 0 | A threshold must be defined first |
| Sum | Total over members | Green threshold at 0 | Threshold depends on member count |
| Disparity | Highest minus lowest | Members meant to share load equally | - |

- Percentile choice: the worst 5th percentile below about 100 members; above 250, the 97th percentile (about 3 standard deviations).
- Worst 5th percentile excludes: 10 members 0.5; 20 1; 50 2.5; 100 5; 200 10; 500 25.
- Count reads as real life: 5 affected users out of 100,000 is 0.005% as an average, but 5 as a count. Track the red count (expected 0) and the orange count as an earlier warning.
- Sum: when every member can be green while the parent sum is red, the threshold was not scaled to the member count.
- Use two together when one is not enough: worst for depth, percentile for breadth. Make one primary, the other secondary. Worst far above the 95th percentile: the worst is an outlier. Close together: a real problem.

## Two kinds of peak
- Peak across time of one metric, and peak among members at one time.
- A cluster of 8 hosts has 288 five-minute points per host per day: 2,304 values. The true peak is the highest of the 2,304.
- To get it: at each time point take the busiest host, then take the highest over the day. The busiest host changes over time.
- The true peak is sensitive to one value. The 99th percentile drops the highest 23 of 2,304.
- The common approach averages the 8 hosts at each point, then takes the peak over time. It under-reports: for the cluster average to reach 80%, at least one host passed 80% and one may be near 100%.
- Same inside one VM: a 64-vCPU VM at 90% has vCPUs at 100%.

## Depth and breadth
| Dimension | Question | Threshold |
|---|---|---|
| Depth | How bad is the worst? | High: one VM very slow is worth a look, and it can be mission critical |
| Breadth | How widespread? | Lower: many VMs moderately slow is worth a look before it gets worse |

- The first questions about a slow VM: how bad (depth), how long and in what pattern, how many others (breadth). Nobody asks for the average.
- Isolated: look at the affected object. Widespread: look at what the affected VMs share (cluster, datastore, resource pool, host).
- Breadth by threshold (share of members above it) requires a threshold per metric. Breadth by percentile works for any metric; the author recommends the 90th percentile.
- Pattern of a cluster that cannot cope: maximum more than 10x the average, average flat, while one or two VMs at a time are not served. With equal treatment, VMs take turns to be hit; the worst VM line can be 60x the average.
- Applied: Cluster Performance (%) uses worst VM for depth and 90th percentile for breadth (`vsphere/object-types/cluster/kpis/cluster-performance`).

## Disparity
- Members meant to share load should be balanced: vCPUs of one VM, hosts in a cluster, RDS hosts in a farm, Horizon Connection Servers in a pod, disks in a vSAN disk group, web servers in a farm.

```text
Disparity (%) = (highest - lowest) / total capacity
```

- Divided by total, not by the highest value. Dividing by the highest gives a large number when the gap is small in absolute terms (useful only in application profiling).
- VM example: `vsphere/technology/cpu/metrics/virtual-motherboard/usage-disparity`.

## Traps
- "Cluster average CPU Ready is low, so no VM is waiting" → average hides the few that wait; read the worst VM and the 90th percentile.
- "ESXi CPU Ready of 149,116 ms is very high" → it is a sum over 195 vCPUs: divide by 20,000 ms × running vCPUs.
- "Cluster peak utilization 80%, so every host stayed below 80%" → the average of hosts at each point hides a host near 100%.
- "Use the maximum: it catches everything" → it catches outliers too; pair it with a percentile.
- "Average performance of the VDI farm is fine, so users are fine" → count users in red; 5 of 100,000 vanish in an average.

## Metadata
```yaml
id: observability/aggregation
retriever_guide: how-it-works
scope: vendor-neutral
technology:
- cpu
- system
pillar:
- performance
- capacity
product: []
internal_derive: []
related:
- observability/collection-interval
- observability/thresholds
- vsphere/object-types/cluster/kpis/cluster-performance
- vsphere/technology/cpu/metrics/virtual-motherboard/usage-disparity
- vsphere/technology/cpu/metrics/virtual-motherboard/ready
source:
  document: 'PART 3 - Counters.docx, Metric Mastery (author update, 2026-11-08)'
  path: Metric Mastery > Aggregation; The Problem with Average; Lagging vs Leading Indicators; "Peak" Utilization; Depth vs Breadth; Usage Disparity
corrections: []
review_notes:
- 'Section ''Summed counters'': the 20,000 ms factor in the formula is Claude''s; the book writes ESXi CPU Ready (%) = ESXi CPU Ready (ms) / Sum (vCPU of running VMs) (Q137).'
- 'Section ''Techniques'': the book table "Count / Worst 5th Percentile / Exclusion" lists 10 → 9.50, 0.50 and so on; written as members excluded.'
status: draft
```
