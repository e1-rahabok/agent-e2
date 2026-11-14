# KPI design

## KPI definition
- KPI is strictly about performance: "performance" has a specific meaning in enterprise IT infrastructure.
- While capacity and availability can impact performance, they should not be mixed up. One name per pillar keeps monitoring unambiguous.
- A KPI is one metric that quantifies the true performance of an object.
- A KPI is a baseline, the standard expectation maintained with effort, not a target still to reach. Provider and consumer each have their own KPI. The ideal, an ESXi host at 100% while no VM sees contention, is not realistic.
- The KPIs per object (business application, Guest OS, VM, ESXi, cluster): [`sp5-framework/performance/performance-management`](README.md), section KPIs. Each KPI file lists its sub-metrics, its limits and what it leaves out.

## Reason for a KPI
- 5,000 VMs every 5 minutes over 24 hours is too many trend charts. One score per object makes monitoring at scale possible.

## One KPI per realm
- A realm is a layer that its owner controls and the layer below cannot see into. The VM is a virtual motherboard; the Guest OS runs on it. So VM Performance (%) and Guest OS Performance (%) are two KPIs, not one.
- Pros: the direction of troubleshooting is clear; each score is higher (a single number dilutes less).
- Cons: twice the metrics; application teams see both as infrastructure and ask for one number.
- For the application team the two are one entity: report the VM GOS KPI, the average of VM Performance (%) and Guest OS Performance (%).
![Guest OS and VM metrics used in the KPIs](images/guest-os-and-vm-performance-kpi-metrics.png)

## Metric qualification
- A metric qualifies only if its values map to the 4 ranges (green, yellow, orange, red) for every object of the type. Otherwise it distorts the KPI.
- So most utilization metrics (disk IOPS, network throughput) are excluded: no universal mapping fits all objects.
- A consumer KPI reads only the consumer's own metrics. Provider metrics (ESXi, resource pool, datastore, cluster) are averages of their consumers: less visibility, and derivable from the consumer metrics. You troubleshoot VMs, not infrastructure.
- A provider KPI reads the contention of its consumers (section Depth and breadth), plus what only the provider sees, such as the host physical network.
- A metric whose threshold cannot be defended is left out ([`sp5-framework/concepts/modelling`](../concepts/modelling.md), section Setting thresholds).

## Depth and breadth
- A provider KPI (ESXi host, cluster) reads the contention of its consumers with two questions:
  - how deep? The worst VM: a problem that hits one VM hard;
  - how broad? The 90th percentile across the VMs: a problem that many VMs have.
- Aggregate directly from the VMs, not from hosts first: a two-level aggregation misrepresents the VM population.
- Breadth uses the 90th percentile: the average reacts too late; the 95th percentile suffers from host imbalance.
- The worst-VM rows have higher limits than the 90th-percentile rows: one VM with a limit in a large cluster is an outlier, not a cluster problem.
- Not the average of the VM KPIs: a cluster serves VMs, so guest contention matters little to it, and the host physical network matters to it but not to a VM.
- VM stats are 20-second peaks, not 5-minute averages, to catch short bursts: that makes the KPI a leading indicator.

## Reading a KPI over time
- Two numbers each KPI has:
  - actual: volatile, per object (the VM's score);
  - target: steady, for many objects. One set of levels and one target for every object of a type: the KPI is never per class of service.
  - Daily KPI actual: the 99th percentile of the day's 288 scores counted from the worst (higher is better, so statistically the 1st percentile): the score that 99% of the intervals reach or exceed; the worst 2 intervals (10 minutes) are ignored. The 95th percentile (70 minutes ignored) is too lenient for large organisations. For capacity, the summary over time is part of each model.
- The class of service shows in the result, not in the target. Gold has less contention by design (less overcommit, more reservation and shares), so a Gold VM tends to score higher than a Silver VM. To check the promise, group the VMs per class and compare each group's KPI: Gold should score above Silver, Silver above Bronze ([`sp5-framework/performance/kpi-vs-sla`](kpi-vs-sla.md), section Two steps of maturity). The promise is relative, contention 1x, 2x, 3x ([`sp5-framework/capacity/class-of-service-planning`](../capacity/class-of-service-planning.md)), not a minimum KPI per class.
- Cadence: daily, in a technical meeting; a month is far too late ([`sp5-framework/performance/kpi-vs-sla`](kpi-vs-sla.md)).

## Scoring
- Each metric maps to a score: green 100-75, yellow 75-50, orange 50-25, red 25-0.
- Five limits per metric: the values where the score is 100, 75, 50, 25 and 0. Inside a range the score falls in a straight line. Past the 0 limit it stays 0; before the best limit it stays 100. In `catalog/thresholds-performance`, section `kpi`, each cell holds them as [green, yellow, orange, red, zero]: where each colour starts, and where red ends. Red is a range, not open ended: without the zero limit no score can be computed.
- Direction: lower is better for most metrics (CPU Ready), so the limits go up. Higher is better for a few (Guest OS free memory), so the limits go down. One calculation handles both.
- The best limit is not always 0. For ESXi CPU Imbalance it is 1, one running thread per running core, so every value up to 1 scores 100.
- Combine as a weighted average where a worse score weighs more:

```text
KPI = sum(score × weight) / sum(weight)
weight = 2 ^ ((100 - score) / 25)
```

- The weight is 1 at score 100, 2 at 75, 4 at 50, 8 at 25 and 16 at 0, and changes smoothly in between, so the KPI does not jump when a value crosses a range limit.
- Reason: with a plain average one red metric among nine healthy ones is hidden. Nine at 100 and one at 18.75: plain average about 91.9; weighted (9 × 100 + 18.75 × 9.51) / (9 + 9.51) ≈ 58.3.
- Why a weighted average and not the worst colour or a sum: [`sp5-framework/concepts/modelling`](../concepts/modelling.md), section Three ways to combine the colours.
- Values are rounded to two decimals before scoring, so the KPI matches the numbers the user sees. Noise below 0.005 counts as 0.
- Green given as a single value (for example 0%): only that value scores 100; any other value starts in yellow at 75.
- Excluded green: a metric whose green range says nothing about health (rare dropped packets, low utilization) is left out of the KPI while green, so it does not add a free 100. Once it leaves green it counts. The test reads the value against the green limit, not the weight. If every metric with data is excluded, the KPI is 100.
- Missing data: a metric with no data is left out, never counted as 0, because 0 usually means perfect. With no data at all, the KPI is not published.
- Limitation: because the weight grows as the score falls, a metric that gets worse can move the KPI the wrong way when other metrics are already worse. Example and effect: [`vsphere/object-types/cluster/models/cluster-risk`](../../vsphere/object-types/cluster/models/cluster-risk.md), section Sub-metric weight in Cluster Risk.
- The same scoring serves the capacity models (Cluster Consumption, Cluster Risk), which publish 100 minus the weighted average.
- Why four equal ranges, thresholds and validation: [`sp5-framework/concepts/modelling`](../concepts/modelling.md).

## Misconceptions
- "Add IOPS to the KPI" → no universal range; it masks real problems.
- "Put the datastore or ESXi metric in the VM KPI" → a provider metric is an average of VMs; the consumer KPI reads the consumer's own metrics.
- "The KPI target is higher for Gold" → the KPI has no class of service. Gold scores higher because it has less contention by design; compare the class groups.
- "Gold VMs must keep VM Performance above 99.5%" → no minimum KPI per class; the class promise is relative contention (1x, 2x, 3x), read by comparing class groups.
- "A KPI of 75% is a failure" → one 5-minute score of 75% on a development VM is acceptable; the KPI is not a contract with a penalty.
- "KPI means any key indicator, availability included" → KPI is performance only: the P is performance. Availability has KAI (key availability indicator); security, compliance included, has KSI (key security indicator). In daily speech users say availability KPI, business KPI or marketing KPI for any key indicator: translate by the pillar it measures.
- "Cluster Performance is the average of its VM KPIs" → a provider KPI reads depth (worst VM) and breadth (90th percentile) of VM contention, plus the host network.
- "Average the daily KPI" → read the 99th percentile of the day's 288 scores; an average hides the bad intervals.

## Metadata
```yaml
id: sp5-framework/performance/performance-kpi-design
retriever_guide: how-it-works
scope: sp5-framework
technology:
- cpu
- memory
- storage
- network
- system
pillar:
- performance
product:
- vcf-operations
object:
- VirtualMachine
- HostSystem
- ClusterComputeResource
internal_derive:
- sp5-framework/observability/thresholds
related:
- sp5-framework/performance/performance-management
- sp5-framework/performance/kpi-vs-sla
- sp5-framework/concepts/modelling
- vsphere/object-types/vm/vm-performance
- guest-os/system/guest-os-performance
- vsphere/object-types/esxi/esxi-performance
- vsphere/object-types/cluster/cluster-performance
- vcf-operations/features/peak-20-second-metrics
images:
  - path: images/guest-os-and-vm-performance-kpi-metrics.png
    product: [vcf-operations]
    object: [VirtualMachine]
    metric: ['VM Performance', 'Guest OS Performance']
    image_type: table
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: 'Consumer Objects > Performance: VM & Guest OS > Approach; Implementation'
corrections:
- 'Section ''One KPI per realm'': VM GOS KPI = average of the two, for the application team. Part 1 of the book, which combines them in one KPI, is outdated.'
- 'Section ''Scoring'': the book gives step weights 1x, 2x, 4x, 8x. The knowledge base uses the smooth weight 2^((100 - score)/25) with the excluded green, single-value green, rounding and missing-data rules.'
review_notes: []
status: draft
```
