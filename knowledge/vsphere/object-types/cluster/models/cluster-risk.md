# Cluster Risk (%)

## Purpose
- A leading indicator.
- The name is not Capacity Risk or Performance Risk as it covers both.
- It quantifies the risk factor of VMs feel contention or ESXi consumption rise.
- Risk measures potential. It complements actual. 
- Cluster Performance shows actual contention ([`vsphere/object-types/cluster/cluster-performance`](../cluster-performance.md)). Cluster Risk shows potential contention.
- Higher is worse: 0 is no risk, 100 is maximum risk. Cluster Consumption reads the same way; Cluster Performance is higher-is-better.
- Every sub-metric takes the worst ESXi host. One full host hurts its VMs while the cluster average looks fine. Many clusters have 8 hosts or fewer, so the worst warns early. Different sub-metrics can come from different hosts: fine for monitoring, not for troubleshooting.
- A risk model, not a KPI: a KPI scores performance only. Users also call it the Cluster Risk KPI.
- Not a built-in VCF Operations metric. 12 sub-metrics.

## Thresholds
- Limits: `catalog/thresholds-risk`, section `model` (the sub-metrics) and `score` (Cluster Risk itself), lines with this file as `kb`. They are shown with this file; this file holds the reasons.

- Excluded: six green ranges (thread utilization, active memory, CPU and memory reservation, CPU and memory overcommit). A host that is not busy, has little reserved or is not overcommitted says nothing about risk. While green, these rows are left out instead of scoring 100; they count once they leave green.
- The excluded green ends where yellow starts: thread utilization below 60%, active memory below 50%, reservation below 10%, overcommit below 1.
- CPU imbalance is green only at exactly 1 (one running thread per running core). Any imbalance is yellow.

## Sub-metric formulas
Per host, then the worst host is kept.

| Sub-metric | Per host | Source (VCF Operations) |
|---|---|---|
| Highest ESXi CPU thread utilization (%) | % of the host's threads in use, Hyper-Threading aware | `cpu\|utilization_average` |
| Worst ESXi CPU imbalance (ratio) | Running threads / running cores. Running threads = utilization % × threads; running cores = core utilization % × cores | `cpu\|utilization_average`, `cpu\|coreUtilization_average`, `hardware\|cpuInfo\|numCpuCores` |
| Worst ESXi memory ballooned (%) | Ballooned, as % of host DRAM | `mem\|vmmemctl_average` |
| Worst ESXi swapped + zipped memory (%) | (Compressed + swapped), as % of host DRAM | `mem\|compressed_average`, `mem\|swapout_average` |
| Worst ESXi active memory, tiered hosts (% of DRAM) | Active memory as % of host DRAM. Excluded while green (below 50%). Left out on hosts without memory tiering | `mem\|active_average`; DRAM `mem:DRAM\|memory_tier_total_capacity`; tier `mem:NVMe\|memory_tier_size` |
| Worst ESXi NVMe read latency (µs) | Read latency of the NVMe memory tier, at all times: a device waking from a power-saving state explains a high reading, it does not remove the wait. Left out on hosts without memory tiering | `mem:NVMe\|latency.read_latest` (µs) |
| Highest ESXi CPU reservation (%) | Reserved CPU, as % of host CPU capacity | `cpu\|reservedCapacity_average` / `cpu\|totalCapacity_average` |
| Highest ESXi memory reservation (%) | Reserved memory, as % of host DRAM | `mem\|reservedCapacity_average` |
| Highest ESXi CPU overcommit ratio | vCPUs of powered-on VMs per physical thread | `cpu\|vcpus_allocated_on_all_powered_on_vms`, `hardware\|cpuInfo\|numCpuCores` (threads as below) |
| Highest ESXi memory overcommit ratio | Memory of powered-on VMs / host DRAM | `mem\|memory_allocated_on_all_powered_on_vms` |
| Highest CPU monster VM : host ratio | vCPUs of the largest powered-on VM / CPU monster size of its host | VM `config\|hardware\|numCpu` |
| Highest memory monster VM : host ratio | Memory of the largest powered-on VM / memory monster size of its host | VM `config\|hardware\|memoryKB` |

- Threads = 2 × cores when Hyper-Threading is available and active, else the cores.

## DRAM as the memory base
- Cluster Risk has no memory consumed row, by the author's decision: Memory Consumed (DRAM and NVMe) ÷ DRAM passes 100% on a tiered host by design, so it would read orange or red on a healthy tiered host, and the memory rows overlap. Ballooned, swapped + zipped and active memory cover the pressure.
- Every memory % and ratio is against the host's DRAM (the DIMMs). A memory tier such as NVMe is never added.
- Reason: VMs run in DRAM; NVMe holds only cold pages. A % of DRAM + NVMe looks smaller than the real pressure. There is no use case in Cluster Risk for the expanded capacity. Cluster Consumption uses it for capacity ([`vsphere/object-types/cluster/models/cluster-consumption`](cluster-consumption.md)).
- Source: host `mem:DRAM\|memory_tier_total_capacity`; fallback `mem\|host_provisioned`. With neither, the host's memory rows are left out, never scored against a guess.

## CPU overcommit: per thread
- The CPU overcommit ratio is per thread, because the CPU executes per thread. With Hyper-Threading, 4 vCPUs per thread is 8 per core.
- A Bronze cluster run at its planned 3:1 per thread reads 3 on this row, the start of red, by design: the planning ratio is set by the price of the class, while Cluster Risk reads the running cluster, so Bronze scores a higher risk than Gold ([`sp5-framework/capacity/class-of-service-planning`](../../../../sp5-framework/capacity/class-of-service-planning.md)).

## Monster VM
| Resource | A VM is a monster when it has more than | Example |
|---|---|---|
| CPU | 50% of the host's physical cores. Cores, not threads. | 64 cores, 128 threads: above 32 vCPU |
| Memory | 40% of the host's DRAM, or 256 GB, whichever is smaller. NVMe tiering does not count. | 768 GB DRAM + 768 GB NVMe: 40% is 307 GB, so 256 GB |

- The ratio compares the largest VM with that size: 1 is exactly the monster size; above 1 it is a monster.
- The three numbers (50%, 40%, 256 GB) are defaults, settable per adapter instance. The ratio limits (1, 2, 3, 4) do not change.
- Horizontal risk: more monster VMs, unevenly spread across hosts. Vertical risk: bigger VMs. One 96-vCPU VM is riskier than four 24-vCPU VMs.
- Factors: NUMA and L3 domains (their size depends on the CPU generation: AMD CCDs hold 8 to 32 cores, Intel Xeon has compute tiles; a fixed 16-vCPU threshold would flag too many VMs), Hyper-Threading, hypervisor overhead (vSAN + NSX + VMkernel can take more than 10% CPU).
- Monster VMs cause contention despite low utilization, reservation and allocation.

## Scoring
- The sub-metrics are scored and combined as for every KPI and model ([`sp5-framework/performance/performance-kpi-design`](../../../../sp5-framework/performance/performance-kpi-design.md), section Scoring), where 100 is best. The published value is flipped: Cluster Risk = 100 − weighted average.
- Bands are the mirror of the performance KPIs: green 0-25, yellow 25-50, orange 50-75, red 75-100. An alert or widget on Cluster Risk must treat high as bad: red from 75.
- Worked example: two hosts of 32 cores, 512 GB DRAM, four VMs of 4 vCPUs and 16 GB each; host 1 at 90% thread and 100% core utilization, host 2 at 30% and 60%. Thread utilization 90% enters at the start of red (25, weight 8). Imbalance of host 1 is 57.6 running threads / 32 running cores = 1.8, halfway through red (12.5, weight 11.31). Ballooned and swapped + zipped read 0 (100); monster ratios 0.25 and 0.08 (93.75, 98); excluded rows left out; no tiering. Weighted average 32.11; Cluster Risk = 67.89.
- Missing data: a sub-metric with no data, or data older than 10 minutes, is left out; never counted as 0, because 0 means no risk.

## Sub-metric weight in Cluster Risk
- The weight of a sub-metric rises as its score falls. When the score is already high, a sub-metric that gets worse but is still better than the ones driving the score pulls the weighted average up, so Cluster Risk goes down.
- An Excluded row that leaves green enters at weight 2 at once: the same effect.
- Example: Cluster Risk 67.89 (section Scoring); new idle VMs raise the CPU overcommit ratio from 0.5 to 1.12. The row enters yellow (72.00, weight 2.17) and Cluster Risk falls to 64.52. Only from about 2.7 does it raise it above 67.89.
- Read the sub-metrics before acting on a falling Cluster Risk. A cluster just above orange (50) can drop to yellow after VMs are deployed.
- It happens only when Cluster Risk is already high. When the other sub-metrics are green, a worse sub-metric always raises it.

## Reasons
- CPU reservation is against base clock speed: All-Core Turbo is unknown.
- Allocation is per host, not cluster-wide: the metric is about performance as well as capacity.

## Not used
- Inter-host imbalance: partly covered by highest host utilization; complex; field validation that it changes remediation is pending.
- vMotion: involves the network across top-of-rack switches. Track the maximum vMotion stun time across the environment separately, as basic health ([`vsphere/object-types/cluster/cluster-performance`](../cluster-performance.md), section vMotion Count).

## Use in troubleshooting
- Risk can rise for days while performance stays green, until a trigger (a busy morning, a host failure, a maintenance window) turns it into contention.
- Read the rows, not the score: a worse sub-metric can leave the score flat or lower it (section Sub-metric weight in Cluster Risk).

## Misconceptions
- "Cluster Performance was green all week, so nothing was building up" → Cluster Risk reads potential contention; its sub-metrics can step up days before the VMs wait.
- "The CPU overcommit row reads 3, so the Bronze 3:1 plan is met" → the row is per thread, as the class plans are: Bronze 3:1 reads 3; on Hyper-Threading hosts that is 6 vCPUs per core.
- "Cluster average utilization shows risk" → use the worst host.
- "Cluster Risk fell, so the cluster is safer" → a worse sub-metric can lower it when the score is already high; read the sub-metrics.
- "Memory consumed is low against DRAM + NVMe" → risk is measured against DRAM only.
- "A monster VM is one above half the host threads" → half the physical cores, not threads; memory above 40% of DRAM or 256 GB, whichever is smaller.

## Metadata
```yaml
id: vsphere/object-types/cluster/models/cluster-risk
retriever_guide: metric-meaning
scope: vsphere
technology:
- cpu
- memory
- system
pillar:
- capacity
- performance
product:
- vcf-operations
object:
- ClusterComputeResource
metric_class: context
internal_derive:
- sp5-framework/concepts/modelling
- sp5-framework/capacity/class-of-service-planning
- sp5-framework/performance/performance-kpi-design
- sp5-framework/capacity/overcommit
- vsphere/technology/cpu/metrics/cluster/inter-host-imbalance
- vsphere/technology/memory/concepts/memory-tiering
- vsphere/architecture/resource-controls
same_name: []
same_meaning: []
related:
- vsphere/object-types/cluster/models/cluster-consumption
- vsphere/technology/cpu/metrics/host/imbalance
- vsphere/object-types/cluster/concepts/cluster-operations
- vsphere/technology/cpu/concepts/cpu-measurement-levels
images:
source:
  document: Knowledge base
  path: Provider Objects > Other Metrics > Cluster Risk (%); Monster VM
corrections: []
review_notes: []
status: draft
```
