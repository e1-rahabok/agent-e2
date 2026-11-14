# VM Performance (%)

## Definition
- One 0-100% score per VM. 100 is perfect.
- It scores the VM as a virtual motherboard: is ESXi giving it the CPU, memory, disk and network it asks for? What happens inside Windows or Linux is scored by Guest OS Performance (%) ([`guest-os/system/guest-os-performance`](../../../guest-os/system/guest-os-performance.md)).
- Not a built-in VCF Operations metric. Scored on every powered-on VM; a powered-off VM gets no score: its stats are old.
- VM Guest OS KPI: the average of VM Performance (%) and Guest OS Performance (%), one score per VM for the application team. A VM without VMware Tools has no Guest OS Performance, so its VM Guest OS KPI is its VM Performance alone.
- Use: step 2 of the VM health check ([`vsphere/object-types/vm/vm-health-check`](vm-health-check.md)); when it drops, open the sub-metric that pulls it down.

## Sub-metrics
| Group | Sub-metric | Source (VCF Operations) | Catalog row (KPI) |
|---|---|---|---|
| VM contention | CPU Co-stop | `cpu\|20_sec_peak_costopPct` | Peak CPU Co-stop among any vCPU (%) |
| VM contention | CPU Ready | `cpu\|20_sec_peak_readyPct` | Peak CPU Ready among any vCPU (%) |
| VM contention | CPU Overlap | `cpu\|20_sec_peak_overlap` | Peak CPU Overlap (%) |
| VM contention | Memory Contention | `mem\|20_sec_peak_host_contentionPct` | Peak RAM Contention (%) |
| VM contention | Disk Latency | `virtualDisk\|20_sec_peak_totalLatency_average` | Peak read/write latency among vDisks (ms) |
| VM contention | Network Dropped Tx | `net\|droppedTxPct_max` | Peak network TX dropped packets (%) |
| VM utilization | CPU Run | `cpu\|net_run` | CPU Net Run (%) |
| IaaS high utilization | Memory Ballooned | `mem\|balloonPct` | VM Memory Ballooned (%) |
| IaaS high utilization | Memory Zip Swap | (`mem\|compressed_average` + `mem\|swapped_average`) ÷ `guest\|used_memory` × 100 | VM Memory Compressed + Swapped (%) |

- 20-second peaks where they exist, not 5-minute averages: the KPI is a leading indicator ([`vcf-operations/features/peak-20-second-metrics`](../../../vcf-operations/features/peak-20-second-metrics.md)).
- Colour levels: `catalog/thresholds-performance`, section `kpi`, rows with this file as `kb`.
- Excluded while green, so they do not add a free 100: CPU Overlap below 0.5% (some overlap is normal), Network Dropped Tx at exactly 0 (drops are rare; any drop is yellow), CPU Run below 95% (a VM that is not busy says nothing about its performance; above 95% the VM itself is too small).

## Reasons
- CPU uses 4 metrics (Co-stop, Ready, Overlap, Net Run). They do not peak in the same 20-second period, so they cannot be combined. Known limitation: CPU weight is larger.
- Ready, Co-stop and Overlap have different thresholds: different sensitivity. Ready tends to be 2x Co-stop.
- High CPU utilization threshold: high utilization means work is done; only above 95% does the VM's own size limit it.
- Memory Contention is the only counter that shows a VM memory problem. VM and Guest OS can have memory problems independently.
- Ballooned and Zip Swap are leading indicators, not real performance problems.
- Compressed and Swapped are combined: both result from the same action (reclaiming a page), so together they tell the complete picture.
- Zip Swap has a tighter band than Memory Contention (green 0-0.25% vs 0-0.5%) although it is less serious: it is measured on 5-minute samples, Memory Contention on 20-second peaks. A 5-minute average reads lower than a 20-second peak, so its band must be lower too.
- Zip Swap is divided by Guest OS used memory, not configured memory: configured memory includes memory the Guest OS does not use, so the % would under-report the risk.
- Network: vCenter has no latency or retransmit counter, so transmit dropped packets are used. Drops are retransmitted and often unnoticed, so the threshold is not low.

## Not used
| Area | Metric | Reason |
|---|---|---|
| CPU | Other Wait | Too many CPU metrics inflate CPU weight. A rare bug gives false positives. |
| Memory | Consumed, Active, Granted | Do not indicate performance problems. |
| Storage | Outstanding IO | A function of IOPS and latency: duplicate. |
| Storage | Snapshot latency | Covered by CPU Other Wait. |
| Storage | Datastore latency | An average of the VMs on the datastore; the VM's own disk latency is in the KPI. |
| Network | Broadcast, multicast | Undesirable, but do not cause performance problems. |
| Network | Error packets | VMware Tools does not provide them. |
| Network | Network queue | No such metric. |
| Network | Receive dropped | Too many false positives. |
| Network | Packets per second | 100% cannot be quantified. |
| Ratio | Guest OS IOPS : VM IOPS | Should be near 1 or stable. The Guest OS reports the last value, the VM the average. No data yet. |
| Cluster | VM DRS Score | About execution efficiency and cluster performance; reuses KPI metrics. |
| vMotion | Downtime, stun time | Not enough data for ranges beyond green (0.2 s). |

- VM DRS Score = Performance Goodness × 0.8 / CPU Demand. 0.8 is the performance degradation threshold. It considers CPU, memory (including tiering), network, Fault Tolerance, vSAN, storage and maintenance. A low score does not mean the VM runs badly: it reflects execution efficiency ([`vsphere/object-types/cluster/configuration/drs-migration-levels`](../cluster/configuration/drs-migration-levels.md), section Cluster DRS Score).

## Scoring
- The scoring shared by every KPI: [`sp5-framework/performance/performance-kpi-design`](../../../sp5-framework/performance/performance-kpi-design.md), section Scoring.
- Nothing wrong: Overlap, Dropped Tx and Run are in their excluded green and left out; the other 6 score 100. KPI = 100.
- CPU Ready 10%: a quarter into red (8 to 16) scores 18.75, weight 9.51. KPI = (5 × 100 + 18.75 × 9.51) / (5 + 9.51) ≈ 46.74.
- CPU Run 98%: halfway through orange (97 to 99) scores 37.5, weight 5.66. KPI ≈ 69.67.
- 0.25% dropped packets: halfway through yellow (0 to 0.5) scores 62.5, weight 2.83. KPI ≈ 87.99.
- Missing data: a sub-metric with no data, or a stat older than 10 minutes, is left out, never counted as perfect. A VM without VMware Tools has no Zip Swap (it needs `guest|used_memory`). With no data at all, the KPI is not published.

## Misconceptions
- "CPU Run 70% lowers the score" → below 95% the row is left out of the KPI; only a VM busy above 95% is scored on it.
- "VM Performance is green, so the application is fine" → it stops at the virtual motherboard; read Guest OS Performance (%) for what runs inside.
- "One dropped packet barely moves the KPI" → any drop leaves the excluded green and counts, at least at yellow.
- "Ballooned memory means the VM is slow" → ballooning is a leading indicator; Memory Contention shows the wait.
- "A KPI of 100 on a VM with no data is healthy" → with no data the KPI is not published at all.
- "Use datastore latency in the VM KPI" → it is an average of the VMs on the datastore; the KPI reads the VM's own disk latency.
- "A low VM DRS Score means the VM runs badly" → it reflects execution efficiency, not contention; read VM Performance (%).

## Metadata
```yaml
id: vsphere/object-types/vm/vm-performance
retriever_guide: metric-meaning
scope: vsphere
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
layer:
- virtual-motherboard
metric_class: contention
internal_derive:
- sp5-framework/performance/performance-kpi-design
same_name: []
same_meaning: []
related:
- guest-os/system/guest-os-performance
- vcf-operations/features/peak-20-second-metrics
- vsphere/object-types/vm/vm-health-check
- sp5-framework/performance/performance-management
- vsphere/object-types/cluster/configuration/drs-migration-levels
images:
source:
  document: Knowledge base; Private Cloud Management by Iwan Rahabok (https://isvara.io/download) for the reasons and the metrics not used
  path: 'Consumer Objects > Performance: VM & Guest OS > VM Performance (%); Metrics Not Used'
corrections:
- 'Section ''Reasons'': the source document says the Compressed + Swapped threshold is 2x memory contention. The table (half) is correct; the text is superseded. Keep until the source document is updated.'
- 'Sections ''Sub-metrics'' and ''Reasons'': the source document is outdated. Network Dropped Tx: green only at exactly 0 (source document: up to 0.25%); CPU Run and CPU Overlap excluded while green; Ballooned read from mem|balloonPct, only Zip Swap divided by Guest OS used memory.'
review_notes:
- 'To check: Section ''Sub-metrics'': the denominator of mem|balloonPct (configured memory or Guest OS used memory); the earlier text divided Ballooned by Guest OS used memory too.'
- 'To check: Section ''Not used'': VM DRS Score formula from the source document (vSphere 7 blog), not read (https://blogs.vmware.com/vsphere/2020/05/vsphere-7-a-closer-look-at-the-vm-drs-score.html).'
status: draft
```
