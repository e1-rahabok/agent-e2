# Cluster Consumption (%)

## What it measures
- One 0-100% value for a vSphere cluster: actual utilization and saturation of the cluster as a whole, against its usable capacity. Higher is worse: 0 is nothing consumed, 100 is fully consumed. The same direction as Cluster Risk (%).
- Against usable capacity, not total: Usable = Total − HA − Buffer. The capacity kept for a host failure and the policy buffer are not available to VMs ([`sp5-framework/capacity/supply`](../../../../sp5-framework/capacity/supply.md)). A cluster at 80% of its total capacity is full when 20% is HA and buffer.
- Cluster-wide, not the worst host. Every sub-metric adds up the hosts of the cluster, so a big host counts more than a small one. Cluster Risk (%) is the opposite: it takes the worst host ([`vsphere/object-types/cluster/models/cluster-risk`](cluster-risk.md)).
- Why cluster-wide: DRS moves VMs to balance the hosts, so the capacity of the cluster is the sum of its hosts; HA and the buffer are reserved across the cluster, not on any one host.
- Saturation is not contention. Ballooned, swapped and compressed memory do not mean anything is slow yet. They are real consumption, so they have their own sub-metrics.
- Published on the cluster under `vCommunity|Cluster Consumption`; the score is `vCommunity|Cluster Consumption|Cluster Consumption Score`. One of the three inputs of Close for Business ([`vsphere/object-types/cluster/models/close-for-business`](close-for-business.md)).

## Sub-metrics
| Group | Sub-metric | Cluster-wide value |
|---|---|---|
| Utilization | ESXi CPU Thread Utilization | Threads in use on all hosts ÷ CPU usable capacity in threads |
| Utilization | ESXi Memory Consumed, hosts without tiering | Consumed memory of all hosts ÷ usable DRAM |
| Utilization | ESXi DRAM Consumed, tiered hosts | Tier 0 consumed of all tiered hosts ÷ their usable DRAM. Memory Consumed covers both tiers and passes 100% of DRAM by design; tiering starts at 80% of DRAM, so green runs to 80 |
| Saturation | Memory Tiering Consumption | NVMe tier in use on all hosts ÷ usable NVMe tier |
| Saturation | ESXi Memory Ballooned | Ballooned memory of all hosts ÷ usable DRAM |
| Saturation | ESXi Memory Zip Swap | Compressed plus swapped memory of all hosts ÷ usable DRAM |

- Colour bands: `catalog/thresholds-capacity`, rows with this file as `kb`. No green range is excluded: every row with data counts.
- Threads in use per host = `cpu|utilization_average` % × threads. Memory: `mem|consumed_average`, `mem|vmmemctl_average`, `mem|compressed_average`, `mem|swapout_average`; NVMe tier `mem:NVMe|tier.usage` against `mem:NVMe|memory_tier_size`.
- DRAM is the host's DRAM only, never DRAM plus a memory tier. DRAM and the NVMe tier are kept apart: each memory row reads one of them.
- CPU usable capacity is counted in threads, not MHz. Capacity is quantity: how many VMs fit, not how fast they run.

## Usable capacity in the pack
- VCF Operations computes usable capacity per cluster from HA admission control and the Capacity Buffer (Demand) of the policy, in MHz for CPU and KB for memory.
- The pack takes it as a percentage of total capacity (`cpu|demand|usableCapacity` ÷ `cpu|capacity_provisioned`; `mem|demand|usableCapacity` ÷ `mem|host_provisioned`) and applies that percentage to the threads, DRAM and NVMe tier of the running hosts.
- Hosts left out: not responding, disconnected, powered off or in standby (DPM), in maintenance mode, or with no value in the last 10 minutes. A left-out host stays in total capacity but adds nothing to usable capacity. A host still entering maintenance mode counts as running: its VMs are still on it.

## Scoring
- The same scoring as every KPI and model of the pack ([`sp5-framework/performance/performance-kpi-design`](../../../../sp5-framework/performance/performance-kpi-design.md), section Scoring), then flipped: Cluster Consumption = 100 − weighted average.
- Bands: green 0-25, yellow 25-50, orange 50-75, red 75-100.
- Worked example: a host of 64 threads and 512 GB at 40% thread utilization, and a host of 32 threads and 256 GB at 70%; HA and buffer take 20%. Threads in use: 25.6 + 22.4 = 48 of 96 (50% of total; the average of 40% and 70% would be 55%). Against usable (76.8 threads): 62.5%. Memory consumed 486.4 of 614.4 GB usable: 79.17%. Cluster Consumption = 34.53.
- A worse sub-metric can lower Cluster Consumption: its weight rises as its score falls, so a row that gets worse but stays below the rows driving the score lowers the weighted average. Same mechanism as Cluster Risk ([`vsphere/object-types/cluster/models/cluster-risk`](cluster-risk.md), section A worse sub-metric can lower Cluster Risk).
- Missing data: a row with no data is left out, never counted as 0, because 0 means nothing consumed.

## Reading it
- Read it with Cluster Performance (%). High consumption with green performance: the cluster is busy and serving its VMs; it closes on consumption only when red, or when consumption and performance are both orange and risk is high ([`vsphere/object-types/cluster/models/close-for-business`](close-for-business.md)).
- Memory consumed high with green saturation rows is a cache doing its job: Windows and Linux keep pages they once touched. A memory shortage shows in the saturation rows first, then in VM memory contention.
- On a host with memory tiering, compression and swap read 0: memory beyond DRAM goes to the NVMe tier first. The tier's consumption is then the saturation signal ([`vsphere/technology/memory/concepts/memory-tiering`](../../../technology/memory/concepts/memory-tiering.md)).
- Its bands are linear, 25, 50, 75, 100% of the usable NVMe tier: the metric sits between utilization and saturation. A utilization row starts green at a high number; a saturation row starts green at a low number and doubles quickly. Tier pages are cold by design, yet each one is memory beyond DRAM; linear quarter steps blend the two natures.
- Low consumption with red performance: contention comes from imbalance, limits, resource pools or storage, not from load ([`vsphere/object-types/cluster/health-check/cluster-health-check`](../health-check/cluster-health-check.md)).
- Low consumption that stays low for months: wastage, unless the cluster is new or holds DR protection ([`sp5-framework/capacity/demand`](../../../../sp5-framework/capacity/demand.md), section Consumption).

## Limitations
- CPU usable capacity in threads comes from a ratio in MHz. Exact only when every host has the same clock speed and the same Hyper-Threading setting. Example: host A 32 cores with Hyper-Threading (64 threads), host B 32 cores without (32 threads), each half of the MHz; HA and buffer take 50%: the pack counts 48 usable threads, while 32 or 64 remain depending on which host fails.
- The memory percentage is applied to the NVMe tier too: it assumes HA and the buffer remove the same part of DRAM and tier.
- Usable capacity 0 has two cases. Hosts run but HA and buffer leave nothing to VMs: Cluster Consumption is 100 and the rows of that resource are not published. No host runs: nothing is consumed and nothing is published.
- Memory Tiering Consumption is not yet confirmed on a live system.
- To validate: whether a host in maintenance mode lowers usable capacity twice, once in the VCF Operations percentage and once as a left-out host.

## Misconceptions
- "Saturation means VMs are slow" → saturation is consumption; check Cluster Performance (%).
- "Cluster Consumption is the average of the hosts" → it adds up the hosts: a big host counts more. In the example the average is 55%, the cluster-wide value 50% of total.
- "Cluster Consumption is measured against total capacity" → against usable capacity, after HA and buffer.
- "Cluster Consumption is orange, so the cluster is closed" → it closes on consumption only when red, or when consumption and performance are both orange and risk is orange or red.
- "Cluster Consumption shows the hottest host" → the hottest host is Cluster Risk (%).
- "CPU usable capacity is in MHz" → the pack counts threads: capacity is quantity, not speed.

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
same_name: []
same_meaning: []
related:
- vsphere/object-types/cluster/models/cluster-risk
- vsphere/object-types/cluster/kpis/cluster-performance
- vsphere/object-types/cluster/models/close-for-business
- sp5-framework/performance/performance-kpi-design
- sp5-framework/capacity/capacity-management
images:
source:
  document: VCF-vCommunity-Adapter documentation, Cluster Consumption KPI and Capacity Management Model (read 2026-11-11); Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: https://github.com/e1-rahabok/VCF-vCommunity-Adapter/blob/main/docs/reference/metrics/cluster-consumption.md; docs/concepts/capacity-management.md; Provider Objects > Other Metrics > Cluster Consumption (%)
corrections:
- 'Section ''Sub-metrics'': the adapter documentation gives Memory Tiering Consumption bands 4, 8, 16, 32; the author set 25, 50, 75, 100 and added the tiered-host DRAM Consumed row, 80, 85, 90, 100 (2026-11-12, Q179). The pack follows after it is updated.'
review_notes:
status: draft
```
