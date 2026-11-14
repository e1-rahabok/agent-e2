# ESXi Performance (%)

## Definition
- One score per ESXi host, 0-100%. 100 is perfect.
- It measures actual contention, not potential. It quantifies the problem; it does not explain the root cause.
- ESXi is a provider: it has no contention of its own. The KPI reads the contention of the powered-on VMs running on the host, plus the host's own physical network. See [`vsphere/architecture/provider-consumer`](../../architecture/provider-consumer.md).
- Not a built-in VCF Operations metric. 9 sub-metrics.
- Use: the first step of the ESXi health check ([`vsphere/object-types/esxi/esxi-health-check`](esxi-health-check.md)). When the score drops, open the 9 sub-metrics of that host.

## Design
- Same 9 sub-metrics and the same limits as Cluster Performance ([`vsphere/object-types/cluster/cluster-performance`](../cluster/cluster-performance.md)), measured over the VMs of one host instead of the whole cluster: depth (the worst VM) and breadth (the 90th percentile), at 20-second peaks ([`sp5-framework/performance/performance-kpi-design`](../../../sp5-framework/performance/performance-kpi-design.md), section Depth and breadth).
- A VM belongs to the host named in its `summary|parentHost` property; it counts only when `summary|runtime|powerState` is Powered On.

## Thresholds
- Colour levels (green, yellow, orange, red, zero for 5 minutes, 20 seconds and 2 seconds): `catalog/thresholds-performance`, section `kpi`. They are shown with this file; this file holds the reasons.

- The red range ends where the sub-metric scores 0.
- Excluded: while bad packets are exactly 0, the row is left out of the KPI, so it does not add a free 100. Any bad packet is yellow and counts.

## Sub-metric formulas
| Sub-metric | Source (VCF Operations) |
|---|---|
| Ready (worst, 90th percentile) | VM `cpu\|20_sec_peak_readyPct` |
| Co-stop (worst, 90th percentile) | VM `cpu\|20_sec_peak_costopPct` |
| Memory latency (worst, 90th percentile) | VM `mem\|20_sec_peak_host_contentionPct` |
| Disk latency (worst, 90th percentile) | VM `virtualDisk\|20_sec_peak_totalLatency_average` |
| Bad network packets | Host: (errorsRx + errorsTx + droppedRx + droppedTx) / (packetsRx + packetsTx) × 100 in the last 5-minute cycle |

- Bad packets are never averaged over a longer time: that hides a spike. Packets Received and Transmitted totals are deactivated by default in VCF Operations; activate them in the policy first.
- It replaces the former "ESXi Bad Network Packets" super metric.

## Scoring
- Each sub-metric scores 100-0 against its limits; the KPI is a weighted average where a worse score weighs more. Rule shared by every KPI: [`sp5-framework/performance/performance-kpi-design`](../../../sp5-framework/performance/performance-kpi-design.md), section Scoring.
- Nothing wrong: bad packets 0 (excluded), the other 8 score 100. KPI = 100.
- One VM with 200 ms disk latency: the worst-VM disk row is a quarter into red (160-320 ms) and scores 18.75 with weight 9.51. The 90th percentile stays 0: one VM is not a broad problem. KPI = (7 × 100 + 18.75 × 9.51) / (7 + 9.51) ≈ 53.2.
- A host with no powered-on VMs: no VM sub-metric has data; bad packets 0 are left out. KPI = 100.
- Missing data: a sub-metric with no data, or a stat older than 10 minutes, is left out, never counted as 0. A host that is not connected gets no KPI.

## Misconceptions
- "ESXi CPU Ready is the host's contention" → host Ready sums its VMs and hides the one that suffers; this KPI takes the worst VM and the 90th percentile.
- "ESXi Performance is low, so the host is overloaded" → it scores VM contention and bad packets, not utilization. A host can be busy and score 100.
- "Host with no VMs scores 100, so the host is fine" → the KPI has nothing to score; availability and configuration are separate health check steps.
- "ESXi KPI = average of its VM Performance KPIs" → different metrics: depth and breadth across the VMs, plus the host network.

## Metadata
```yaml
id: vsphere/object-types/esxi/esxi-performance
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
- HostSystem
metric_class: contention
internal_derive:
- sp5-framework/performance/performance-kpi-design
- vsphere/object-types/cluster/cluster-performance
same_name: []
same_meaning: []
related:
- sp5-framework/performance/performance-management
- vsphere/object-types/esxi/esxi-health-check
- vsphere/object-types/vm/vm-performance
- vsphere/architecture/provider-consumer
images:
source:
  document: Knowledge base
  path: 'ESXi Performance (%): the Cluster Performance design applied to the VMs of one host'
corrections: []
review_notes:
- 'To check: Section Thresholds, interval: the Cluster Performance memory rows carry interval 5m in the catalog; every VM sub-metric here is a 20-second peak, including mem|20_sec_peak_host_contentionPct.'
- 'To check: Section Misconceptions: derived from the design text.'
status: draft
```
