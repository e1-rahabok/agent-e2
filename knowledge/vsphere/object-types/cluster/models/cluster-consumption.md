# Cluster Consumption (%)

## Measurement
- One 0-100% value for a vSphere cluster: actual utilization and saturation of the cluster as a whole, against its usable capacity. Higher is worse: 0 is nothing consumed, 100 is fully consumed. The same direction as Cluster Risk (%).
- Against usable capacity, not total: Usable = Total − HA − Buffer. The capacity kept for a host failure and the policy buffer are not available to VMs ([`sp5-framework/capacity/supply`](../../../../sp5-framework/capacity/supply.md)). A cluster at 80% of its total capacity is full when 20% is HA and buffer.
- Cluster-wide, not the worst host. Every sub-metric adds up the hosts of the cluster, so a big host counts more than a small one. Cluster Risk (%) is the opposite: it takes the worst host ([`vsphere/object-types/cluster/models/cluster-risk`](cluster-risk.md)).
- Why cluster-wide: DRS moves VMs to balance the hosts, so the capacity of the cluster is the sum of its hosts; HA and the buffer are reserved across the cluster, not on any one host.
- Saturation is not contention. Ballooned, swapped and compressed memory do not mean anything is slow yet. They are real consumption, so they have their own sub-metrics.
- A capacity model, not a KPI: a KPI scores performance only. Users also call it the Cluster Consumption KPI.
- Not a built-in VCF Operations metric. One of the three inputs of Close for Business ([`vsphere/object-types/cluster/models/close-for-business`](close-for-business.md)).

## Sub-metrics
| Group | Sub-metric | Cluster-wide value |
|---|---|---|
| Utilization | Cluster-wide ESXi CPU thread utilization (%) | Threads in use on all hosts ÷ CPU usable capacity in threads |
| Utilization | Cluster-wide ESXi memory consumed (%) | Consumed memory of all hosts ÷ usable memory: DRAM, plus the NVMe tier on a tiered host. The raw vCenter metric, unchanged: on a tiered host vSphere counts DRAM and NVMe as host memory, and Consumed covers both |
| Utilization | Cluster-wide ESXi DRAM Consumed (%) | DRAM in use on all tiered hosts ÷ their usable DRAM. A separate metric, not Memory Consumed: DRAM in use = Memory Consumed − NVMe tier in use, per host. Never above 100%; tiering starts at about 80% of DRAM, so green runs to 80. Cluster Risk has no memory consumed row. |
| Saturation | Cluster memory tiering consumption (%) | NVMe tier in use on all tiered hosts ÷ their usable DRAM: how much memory sits beyond DRAM, against the DRAM it spilled from |
| Saturation | Cluster-wide ESXi memory ballooned (%) | Ballooned memory of all hosts ÷ usable DRAM |
| Saturation | Cluster-wide ESXi swapped + zipped memory (%) | Compressed plus swapped memory of all hosts ÷ usable DRAM |

- Limits: `catalog/thresholds-capacity`, section `model` (the sub-metrics) and `score` (Cluster Consumption itself), lines with this file as `kb`. No green band is excluded: every sub-metric with data counts.
- Threads in use per host = `cpu|utilization_average` % × threads. Memory: `mem|consumed_average`, `mem|vmmemctl_average`, `mem|compressed_average`, `mem|swapout_average`; NVMe tier in use `mem:NVMe|tier.usage`; a host with `mem:NVMe|memory_tier_size` above 0 is a tiered host.
- Memory reads ESXi Memory Consumed, not ESXi Memory Utilization: Utilization mixes realms, because its VM term comes from Guest OS counters; Consumed stays in one realm and is conservative, and the reclamation it leaves out counts as saturation ([`vsphere/technology/memory/metrics/host/utilization`](../../../technology/memory/metrics/host/utilization.md), section Reason).
- Memory Consumed is against the host memory vSphere reports: DRAM, plus the NVMe tier on a tiered host (`mem:NVMe|memory_tier_size`). Every other memory row is against DRAM only, never DRAM plus a memory tier. ESXi DRAM Consumed per host = `mem|consumed_average` − `mem:NVMe|tier.usage`.
- CPU usable capacity is counted in threads, not MHz. Capacity is quantity: how many VMs fit, not how fast they run.

## Usable capacity
- VCF Operations computes usable capacity per cluster from HA admission control and the Capacity Buffer (Demand) of the policy, in MHz for CPU and KB for memory.
- The model takes it as a percentage of total capacity (`cpu|demand|usableCapacity` ÷ `cpu|capacity_provisioned`; `mem|demand|usableCapacity` ÷ `mem|host_provisioned`) and applies that percentage to the threads, the DRAM and, for Memory Consumed, the DRAM plus NVMe tier of the running hosts. DRAM Consumed, Memory Tiering Consumption, Ballooned and Zip Swap divide by usable DRAM.
- Hosts left out: not responding, disconnected, powered off or in standby (DPM), in maintenance mode, or with no value in the last 10 minutes. A left-out host stays in total capacity but adds nothing to usable capacity. A host still entering maintenance mode counts as running: its VMs are still on it.

## Scoring
- The same scoring as every KPI and model ([`sp5-framework/performance/performance-kpi-design`](../../../../sp5-framework/performance/performance-kpi-design.md), section Scoring), then flipped: Cluster Consumption = 100 − weighted average.
- Bands: green 0-25, yellow 25-50, orange 50-75, red 75-100.
- Worked example, inputs: a host of 64 threads and 512 GB at 40% thread utilization and 60% memory consumed, and a host of 32 threads and 256 GB at 70% and 70%; HA and buffer take 20%; no ballooned, compressed or swapped memory; no memory tiering.
- Worked example, CPU: threads in use 25.6 + 22.4 = 48 of 96 (50% of total; the average of 40% and 70% would be 55%). Against usable (76.8 threads): 62.5%, in yellow, score 62.5, weight 2.83.
- Worked example, memory: consumed 307.2 + 179.2 = 486.4 GB of 614.4 GB usable: 79.17%, near the end of yellow, score 52.08, weight 3.78.
- Worked example, saturation: Ballooned and Zip Swap read 0, green, score 100, weight 1 each; they count, because no green range of this model is excluded.
- Worked example, result: weighted average (62.5 × 2.83 + 52.08 × 3.78 + 100 + 100) ÷ (2.83 + 3.78 + 1 + 1) = 66.64; Cluster Consumption = 100 − 66.64 = 33.36. The limits of each sub-metric: `catalog/thresholds-capacity`, section `model`.
- A worse sub-metric can lower Cluster Consumption: its weight rises as its score falls, so a row that gets worse but stays below the rows driving the score lowers the weighted average. Same mechanism as Cluster Risk ([`vsphere/object-types/cluster/models/cluster-risk`](cluster-risk.md), section Sub-metric weight in Cluster Risk).
- Missing data: a row with no data is left out, never counted as 0, because 0 means nothing consumed.

## Interpretation
- Read it with Cluster Performance (%). High consumption with green performance: the cluster is busy and serving its VMs; it closes on consumption only when red, or when consumption and performance are both orange and risk is high ([`vsphere/object-types/cluster/models/close-for-business`](close-for-business.md)).
- Memory consumed high with green saturation rows is a cache doing its job: Windows and Linux keep pages they once touched. A memory shortage shows in the saturation rows first, then in VM memory contention.
- On a tiered cluster, Memory Consumed can read green while DRAM is full: at the 1:1 tier ratio, DRAM at 85% and 20% of DRAM on NVMe read (85 + 20) ÷ 200 = 52.5%. That is how vSphere counts host memory, not a choice of the model. How full DRAM is shows in ESXi DRAM Consumed, the spill in Memory Tiering Consumption, and active memory against DRAM in Cluster Risk. Memory Consumed is yellow at 70% only when about 55% of DRAM has spilled, near the red of Memory Tiering Consumption.
- On a host with memory tiering, compression and swap read 0: memory beyond DRAM goes to the NVMe tier first. The tier's consumption is then the saturation signal ([`vsphere/technology/memory/concepts/memory-tiering`](../../../technology/memory/concepts/memory-tiering.md)).
- Memory Tiering Consumption divides by usable DRAM, not by the NVMe tier. The overcommit ratio and the class-of-service plan are against DRAM, and Ballooned and Zip Swap, the saturation rows tiering replaces, divide by usable DRAM too. The value does not change with the DRAM:NVMe ratio: 30% is 30% of DRAM spilled, whatever the tier size. Only tiered hosts count, so the DRAM of non-tiered hosts in a mixed cluster does not dilute it.
- Its bands are linear, 15, 30, 45, 60% of usable DRAM, set by the class-of-service plan ([`sp5-framework/capacity/class-of-service-planning`](../../../../sp5-framework/capacity/class-of-service-planning.md)). Spill ≈ memory ratio × 85% concurrent peak − about 80% of DRAM, where tiering starts: Gold (1:1) about 5%, green; Silver (1.2:1) about 20%, yellow; Bronze (1.4:1) about 40%, orange; red is beyond every class. At 60% spill and 30% active memory, active memory reaches 50% of DRAM, the end of green in Cluster Risk.
- Not doubling steps like Ballooned: tier pages are cold by design, and the vendor design point, the 1:1 tier ratio at 2x density, costs 0-10%. Not 25/50/75/100 either: red at 75% means VM memory near 1.75x DRAM, beyond the highest class.
- Low consumption with red performance: contention comes from imbalance, limits, resource pools or storage, not from load ([`vsphere/object-types/cluster/cluster-health-check`](../cluster-health-check.md)).
- Low consumption that stays low for months: wastage, unless the cluster is new or holds DR protection ([`sp5-framework/capacity/demand`](../../../../sp5-framework/capacity/demand.md), section Consumption).

## Limitations
- CPU usable capacity in threads comes from a ratio in MHz. Exact only when every host has the same clock speed and the same Hyper-Threading setting. Example: host A 32 cores with Hyper-Threading (64 threads), host B 32 cores without (32 threads), each half of the MHz; HA and buffer take 50%: the model counts 48 usable threads, while 32 or 64 remain depending on which host fails.
- Memory Consumed changes with the DRAM:NVMe ratio on a tiered host: the same VMs read lower with a bigger tier. Read Memory Tiering Consumption beside it, which does not.
- A tier smaller than DRAM caps Memory Tiering Consumption: with a 0.25:1 tier, a full tier reads 25%, in yellow, and the host swaps next. Ballooned and Zip Swap catch it, one step late.
- Usable capacity 0 has two cases. Hosts run but HA and buffer leave nothing to VMs: Cluster Consumption is 100 and the rows of that resource are not published. No host runs: nothing is consumed and nothing is published.

## Misconceptions
- "Saturation means VMs are slow" → saturation is consumption; check Cluster Performance (%).
- "Cluster Consumption is the average of the hosts" → it adds up the hosts: a big host counts more. In the example the average is 55%, the cluster-wide value 50% of total.
- "Cluster Consumption is measured against total capacity" → against usable capacity, after HA and buffer.
- "On a tiered host, Memory Consumed should be against DRAM" → it is the raw vCenter metric; vSphere counts DRAM and NVMe as host memory, so its capacity is both. The DRAM view is the separate metric ESXi DRAM Consumed.
- "Cluster Consumption is orange, so the cluster is closed" → it closes on consumption only when red, or when consumption and performance are both orange and risk is orange or red.
- "Cluster Consumption shows the hottest host" → the hottest host is Cluster Risk (%).
- "CPU usable capacity is in MHz" → the model counts threads: capacity is quantity, not speed.

## Metadata
```yaml
id: vsphere/object-types/cluster/models/cluster-consumption
retriever_guide: metric-meaning
scope: vsphere
technology:
- cpu
- memory
- system
pillar:
- capacity
product:
- vcf-operations
object:
- ClusterComputeResource
metric_class: consumption
internal_derive:
- sp5-framework/capacity/supply
- sp5-framework/capacity/demand
- sp5-framework/performance/performance-kpi-design
same_name: []
same_meaning: []
related:
- vsphere/object-types/cluster/models/cluster-risk
- vsphere/object-types/cluster/cluster-performance
- vsphere/object-types/cluster/models/close-for-business
- sp5-framework/performance/performance-kpi-design
- sp5-framework/capacity/capacity-management
images:
source:
  document: Knowledge base
  path: Provider Objects > Other Metrics > Cluster Consumption (%)
corrections: []
review_notes:
- 'To check: Section ''Sub-metrics'': the Memory Tiering Consumption row (`mem:NVMe|tier.usage`, in MB) on a live host with memory tiering.'
- 'To check: Section ''Sub-metrics'': ESXi DRAM Consumed as `mem|consumed_average` − `mem:NVMe|tier.usage`; on a live tiered 9.1 host, compare with the DRAM instance of `mem.tier.consumed` (vSphere 9.1 documentation, Monitoring and Performance > Hosts > Memory (MB), p. 2038).'
- 'To check: Section ''Interpretation'': the band anchors assume DRAM holds at about 80% once tiering runs; on a live tiered 9.1 host, compare DRAM consumed with `mem:NVMe|tier.usage` under load. At about 90%, every band end moves down about 10 points.'
- 'To check: Section ''Usable capacity'': whether a host in maintenance mode lowers usable capacity twice, once in the VCF Operations usable-capacity percentage and once as a left-out host; a live cluster with one host in maintenance mode.'
status: draft
```
