# Cluster Performance (%)

## What it is
- One score per vSphere cluster, 0-100%. 100 is perfect.
- It measures actual contention, not potential. It quantifies the problem; it does not explain the root cause.
- Not built into VCF Operations: it is a metric of the vCommunity management pack, published on the cluster object under `vCommunity|Cluster Performance|Cluster Performance Score`, with its 9 sub-metrics beside it.
- Use: watch many clusters at once; when the score drops, open the 9 sub-metrics of that cluster.
- Leading indicator of how close the cluster is to contention: [`vsphere/object-types/cluster/models/cluster-risk`](models/cluster-risk.md). Ballooning and swapping are scored there, not here.

## Design
- Depth (the worst VM) and breadth (the 90th percentile) of the contention of the cluster's powered-on VMs, aggregated directly from the VMs, with VM stats at their 20-second peaks. Why this design, and why not the average of the VM KPIs: [`sp5-framework/performance/performance-kpi-design`](../../../sp5-framework/performance/performance-kpi-design.md), section Depth and breadth.
- Drill to hosts only when troubleshooting.
- One ESXi row: the physical network matters to the cluster, not to a VM.
- Limitation: outliers, for example one VM with a limit in a large cluster; the worst-VM rows have higher limits than the 90th-percentile rows for that reason.

## Thresholds
- Colour levels (yellow, orange, red for 5 minutes, 20 seconds and 2 seconds): `catalog/thresholds-performance`, section `kpi`. They are shown with this file; this file holds the reasons.

- The red range ends where the sub-metric scores 0.
- Excluded: while bad packets are exactly 0, the row is left out of the KPI, so it does not add a free 100 that hides the other rows. Any bad packet is yellow and counts.

## How each sub-metric is calculated
| Sub-metric | Source (VCF Operations) |
|---|---|
| Ready (worst, 90th percentile) | VM `cpu\|20_sec_peak_readyPct` |
| Co-stop (worst, 90th percentile) | VM `cpu\|20_sec_peak_costopPct` |
| Memory wait (worst, 90th percentile) | Memory latency, VM `mem\|20_sec_peak_host_contentionPct`, plus NVMe wait on hosts with memory tiering (below) |
| Disk latency (worst, 90th percentile) | VM `virtualDisk\|20_sec_peak_totalLatency_average` |
| Bad network packets | Per host: (errorsRx + errorsTx + droppedRx + droppedTx) / (packetsRx + packetsTx) × 100 in the last 5-minute cycle; the highest host |

- VMs counted: powered-on VMs on the cluster's hosts. A powered-off VM is left out: its last stats are old.
- 90th percentile: sort the VMs; take the one at position 90% of the count, rounded up. With fewer than 10 VMs it equals the worst VM.
- Bad packets are never averaged or summed over a longer time: that hides a spike. Packets Received and Transmitted totals are deactivated by default in VCF Operations; activate them in the policy first.
- One VM with 200 ms disk latency and the others at 0: the worst-VM row is orange to red; the 90th percentile stays 0. One VM is not a broad problem.

- NVMe wait: the share of vCPU time a VM waits for pages fetched from the NVMe tier, by Little's law. NVMe wait (%) = VM tier-1 read bandwidth (MB/s) × 256 pages per MB × host NVMe read latency (s) ÷ VM vCPUs × 100. The VM does not care where it waits for memory, so the bands stay those of memory latency. On a host without tiering, NVMe wait is 0.
- Before NVMe wait is scored, validate on a tiered host: one 4 KB page per fetch blocking one vCPU, no prefetch, and memory latency not already counting the fetches. Until then it is shown and left out of the score.

## Scoring
- Each sub-metric scores 100-0 against its limits, then the scores are combined in a weighted average where a worse score weighs more. Rule shared by every KPI of the pack: [`sp5-framework/performance/performance-kpi-design`](../../../sp5-framework/performance/performance-kpi-design.md), section Scoring.
- Worked example: 8 sub-metrics at 0 (bad packets excluded), except 90th percentile Ready = 5% (a quarter into red). That row scores 18.75 with weight about 9.51. KPI = (7 × 100 + 18.75 × 9.51) / (7 + 9.51) ≈ 53.2. A plain average gives about 89.8 and hides the problem.
- Missing data: a sub-metric with no data, or data older than 10 minutes, is left out. It is never counted as 0, because 0 means perfect. With no sub-metric data, the KPI is not published.

## Threshold reasons
- Co-stop, Overlap and Other Wait have the same VM impact as Ready, but practically lower values. The same range would inflate the score.
- Dropped and error packets are rare. Take the worst host, not a sum (a sum becomes an average). Low threshold, as many hosts have 25 Gb NICs.

## Not used
| Metric | Reason |
|---|---|
| % VMs with CPU Ready > 1%, % VMs with memory contention > 0% | Same purpose as the percentile. |
| VM utilization | Irrelevant. Use host metrics. |
| ESXi Consumed | Higher consumed is better. Ballooned and swapped + compressed are in Cluster Risk. |
| ESXi CPU utilization | Does not impact performance. Highest host thread utilization is in Cluster Risk. |
| VM DRS Score | About demand, not contention. Example: 23 VMs on a host; 15 low-memory VMs scored 68, 8 high-memory VMs scored below 25, at 117% memory over-provisioning. Cluster DRS score is a weighted average of VM DRS scores. |
| % VMs facing disk latency | Belongs to the datastore KPI. |
| CPU Other Wait | False positives seen. |
| CPU Overlap | Values so low they could mask other problems. |
| Storage bus resets and aborts | - |
| vMotion count | Counts migrations, not downtime. See below |

### vMotion Count
- The vMotion counter counts migrations. It does not measure the downtime of each one.
- In a healthy environment each vMotion stuns the VM for less than 0.2 seconds, which the Guest OS does not notice.
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
same_name: []
same_meaning: []
related:
- sp5-framework/performance/performance-management
- vsphere/object-types/cluster/concepts/cluster-utilization-vs-contention
- vsphere/object-types/vm/vm-performance
images:
source:
  document: VCF-vCommunity-Adapter documentation, Cluster Performance KPI; Private Cloud Management by Iwan Rahabok (https://isvara.io/download) for the design and threshold reasons
  path: https://github.com/e1-rahabok/VCF-vCommunity-Adapter/blob/main/docs/reference/metrics/cluster-performance.md; formula/cluster-performance.png; Provider Objects > Performance > Cluster Performance (%)
corrections:
- 'Sections ''Thresholds'', ''How each sub-metric is calculated'', ''Scoring'': the book table and text are outdated. Current source is the adapter documentation: disk latency is used; packet green is Excluded; balloon and swap moved to Cluster Risk.'
- 'Section ''vMotion Count'': vMotion is excluded; the book text says both included and not included.'
review_notes:
- 'To check: Sections ''Design'', ''Threshold reasons'' and ''Not used'': still from the book, whose text is outdated; check against the adapter documentation. Rows that conflict with it were removed (disk latency, balloon reason).'
status: draft
```
