# Cluster Performance (%)

## Definition
- One score per vSphere cluster, 0-100%. 100 is perfect.
- It measures actual contention, not potential. It quantifies the problem; it does not explain the root cause.
- Not a built-in VCF Operations metric. 9 sub-metrics.
- Use: watch many clusters at once; when the score drops, open the 9 sub-metrics of that cluster.
- Leading indicator of how close the cluster is to contention: [`vsphere/object-types/cluster/models/cluster-risk`](models/cluster-risk.md). Ballooning and swapping are scored there, not here.

## Design
- Depth (the worst VM) and breadth (the 90th percentile) of the contention of the cluster's powered-on VMs, aggregated directly from the VMs, with VM stats at their 20-second peaks. Why this design, and why not the average of the VM KPIs: [`sp5-framework/performance/performance-kpi-design`](../../../sp5-framework/performance/performance-kpi-design.md), section Depth and breadth.
- Drill to hosts only when troubleshooting.
- One ESXi row: the physical network matters to the cluster, not to a VM.
- Limitations of the design and of NVMe wait: section Limitations.

## Thresholds
- Limits (best, green, yellow, orange, zero-at, for 5 minutes, 20 seconds and 2 seconds): `catalog/thresholds-performance`, section `kpi`. They are shown with this file; this file holds the reasons.

- The red range ends where the sub-metric scores 0.
- Excluded: while bad packets are exactly 0, the row is left out of the KPI, so it does not add a free 100 that hides the other rows. Any bad packet is yellow and counts.

## Sub-metric formulas
| Sub-metric | Source (VCF Operations) | Catalog row (KPI) |
|---|---|---|
| Ready (worst, 90th percentile) | VM `cpu\|20_sec_peak_readyPct` | Worst peak vCPU Ready among all VMs (%); 90th percentile peak vCPU Ready among VMs (%) |
| Co-stop (worst, 90th percentile) | VM `cpu\|20_sec_peak_costopPct` | Worst peak vCPU Co-stop among all VMs (%); 90th percentile peak vCPU Co-stop among VMs (%) |
| Memory wait (worst, 90th percentile) | Memory Wait of each VM (vm-performance, section Memory Wait): Memory Contention, VM `mem\|20_sec_peak_host_contentionPct`, plus NVMe wait on hosts with memory tiering | Worst memory wait among all VMs (%); 90th percentile memory wait among VMs (%) |
| Disk latency (worst, 90th percentile) | VM `virtualDisk\|20_sec_peak_totalLatency_average` | Worst peak disk latency among all VM virtual disks (ms); 90th percentile peak disk latency among VM virtual disks (ms) |
| Bad network packets | Per host: (errorsRx + errorsTx + droppedRx + droppedTx) / (packetsRx + packetsTx) × 100 in the last 5-minute cycle; the highest host | Highest ESXi (error + dropped) network packets (%) |

- VMs counted: powered-on VMs on the cluster's hosts. A powered-off VM is left out: its last stats are old.
- 90th percentile: sort the VMs; take the one at position 90% of the count, rounded up. With fewer than 10 VMs it equals the worst VM.
- Bad packets are never averaged or summed over a longer time: that hides a spike. Packets Received and Transmitted totals are deactivated by default in VCF Operations; activate them in the policy first.
- One VM with 200 ms disk latency and the others at 0: the worst-VM row is red, a quarter into the band; the 90th percentile stays 0. One VM is not a broad problem.

## NVMe wait formula
- NVMe wait: the share of vCPU time a VM waits for pages fetched from the NVMe tier, by Little's law. NVMe wait (%) = VM NVMe read bandwidth (MB/s) × 256 pages per MB × host NVMe read latency (s) ÷ VM vCPUs × 100. The VM does not care where it waits for memory, so the bands stay those of Memory Contention. On a host without tiering, NVMe wait is 0.
- How the formula works (Little's law: items in flight = arrival rate × time each takes): MB/s × 256 is the fetches per second, since 1 MB holds 256 pages of 4 KB; × the read latency is the vCPUs frozen at any moment; ÷ the vCPUs is the share of the VM's vCPU time spent waiting, read like CPU Ready.
- Example: a VM of 8 vCPUs reads 6 MB/s from NVMe at 290 µs. 6 × 256 = 1,536 fetches per second; × 0.00029 s = 0.445 vCPU frozen on average; ÷ 8 = 5.57% of its vCPU time.
- Memory Contention does not count the NVMe fetches: the counter is unaware of memory tiering. Adding the two counts no wait twice.
- NVMe wait is scored here, in ESXi Performance (%) and in VM Performance (%), as part of Memory Wait. Its limits, and which way each bends the value: section Limitations.

## Scoring
- Each sub-metric scores 100-0 against its limits, then the scores are combined in a weighted average where a worse score weighs more. Rule shared by every KPI: [`sp5-framework/performance/performance-kpi-design`](../../../sp5-framework/performance/performance-kpi-design.md), section Scoring.
- Worked example: 8 sub-metrics at 0 (bad packets excluded), except 90th percentile Ready = 5% (a quarter into red). That row scores 18.75 with weight about 9.51. KPI = (7 × 100 + 18.75 × 9.51) / (7 + 9.51) ≈ 53.2. A plain average gives about 89.8 and hides the problem.
- Missing data: a sub-metric with no data, or data older than 10 minutes, is left out. It is never counted as 0, because 0 means perfect. With no sub-metric data, the KPI is not published.

## Threshold reasons
- Co-stop has the same VM impact as Ready, but practically lower values: the same range would inflate the score, so the Co-stop rows have tighter limits. Overlap and Other Wait are not used (section Not used).
- Dropped and error packets are rare. Take the worst host, not a sum (a sum becomes an average). Low threshold, as many hosts have 25 Gb NICs.

## Limitations
- Outliers: one VM with a limit in a large cluster pulls the worst-VM rows down, so they have higher limits than the 90th-percentile rows.
- NVMe wait is computed, not measured: no counter gives the time spent waiting for NVMe fetches.
- One 4 KB page per fetch. Prefetch or a large page means fewer fetches than MB/s × 256: the formula overstates the wait.
- Each fetch stalls the vCPU that touched the page for the whole read latency ([`vsphere/technology/memory/concepts/memory-tiering`](../../technology/memory/concepts/memory-tiering.md), section Touching a page on NVMe). If that vCPU runs during part of a fetch, the formula overstates the wait.
- vMotion precopy reads the cold pages of a migrating VM from NVMe (memory-tiering, section Interactions). If these reads count in the VM's NVMe read bandwidth, nothing in the guest waits on them and the worst-VM row can turn red during a host evacuation. Not known whether they count.
  - Until known: on high NVMe wait, check the VM's migration events in the same collection cycle first.
  - If they count, the pack leaves NVMe wait out, marked, for each VM moved to another host in the cycle (vCenter migration events, read once per vCenter per cycle). Never 0 and never scaled: the guest also faults on cold pages during a vMotion, and no counter separates the two reads.
- The host's NVMe read latency stands in for the VM's: no counter gives it per VM.
- Mixed time base: memory latency is a 20-second peak, the NVMe wait inputs are Latest values. The NVMe part understates a burst.
- Release: memory latency does not count NVMe fetches in vSphere 9.1. If a later release counts them, the sum counts the wait twice.
- Collection: NVMe `latency.read` is level 3, `bandwidth.read` level 2. If either is not collected, the Memory Wait rows hold Memory Contention alone and understate the wait on a tiered host: say NVMe wait is missing.

## Not used
| Metric | Reason |
|---|---|
| % VMs with CPU Ready > 1%, % VMs with memory contention > 0% | Same purpose as the percentile. |
| VM utilization | Irrelevant. Use host metrics. |
| ESXi Consumed | Higher consumed is better. Ballooned and swapped + compressed are in Cluster Risk. |
| ESXi CPU utilization | Does not impact performance. Highest host thread utilization is in Cluster Risk. |
| VM DRS Score | Execution efficiency (VM happiness), not contention. Example: 23 VMs on a host; 15 low-memory VMs scored 68, 8 high-memory VMs scored below 25, at 117% memory over-provisioning. Cluster DRS score is a weighted average of VM DRS scores. |
| % VMs facing disk latency | Belongs to the datastore KPI. |
| CPU Other Wait | False positives seen. |
| CPU Overlap | Values so low they could mask other problems. |
| Storage bus resets and aborts | - |
| vMotion count | Counts migrations, not downtime. See below |

### vMotion Count
- The vMotion counter counts migrations. It does not measure the downtime of each one.
- Healthy stun time and downtime of a vMotion: [`vsphere/object-types/vm/vmotion`](../vm/vmotion.md).
- Monitor vMotion separately, with the other broad infrastructure capabilities: NSX Edge, vSAN resync, the physical network.
- For vMotion, track the maximum stun time across all vMotions in the whole environment. A rising maximum is a leading indicator of performance degradation.

## Misconceptions
- "Cluster KPI = average VM KPI" → different purpose and metrics: depth and breadth across VMs, plus the host network.
- "Cluster Performance is green, so no VM suffers" → the worst-VM rows tolerate more than the percentile rows; open the sub-metrics.
- "Many vMotions lowered Cluster Performance" → vMotion is not in the KPI; check the maximum stun time instead.
- "No bad packets scores 100 and lifts the KPI" → while exactly 0 the row is excluded.

## Metadata
```yaml
id: vsphere/object-types/cluster/cluster-performance
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
- ClusterComputeResource
metric_class: contention
internal_derive:
- sp5-framework/performance/performance-kpi-design
- vsphere/object-types/vm/vmotion
same_name: []
same_meaning: []
related:
- vsphere/object-types/cluster/cluster-health-check
- sp5-framework/performance/performance-management
- vsphere/object-types/cluster/concepts/cluster-utilization-vs-contention
- vsphere/object-types/vm/vm-performance
images:
source:
  document: Knowledge base
  path: Provider Objects > Performance > Cluster Performance (%)
corrections: []
review_notes:
- 'To check: Section ''NVMe wait formula'': the VCF Operations key of the VM NVMe read bandwidth used by the pack (`mem:NVMe|bandwidth.read_latest`, MBps, from the VM counter mem.bandwidth.read, instance NVMe) and that the host key `mem:NVMe|latency.read_latest` is in µs; read both on a live tiered 9.1 host (VCF-vCommunity-Adapter, memory_wait.py).'
- 'To check: Section ''Limitations'': one 4 KB page per NVMe fetch, no prefetch or large page; compare a VM''s NVMe read bandwidth with its fault count on a tiered 9.1 host.'
- 'To check: Section ''Limitations'': each NVMe fetch freezes the touching vCPU for the whole read latency; measure on a tiered 9.1 host.'
- 'To check: Section ''Limitations'': whether vMotion precopy reads count in the migrating VM''s NVMe read bandwidth; vMotion an idle tiered VM with NVMe consumed above 0 and compare the VM and host NVMe read bandwidth at 20-second samples.'
- 'To check: Section ''Limitations'': whether VCF Operations collects the host NVMe latency.read (level 3) and VM bandwidth.read (level 2) at the default statistics level; vSphere 9.1 documentation, Monitoring and Performance > Data Collection Levels.'
status: draft
```
