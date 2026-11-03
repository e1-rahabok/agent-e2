# Cluster Inter-Host Imbalance

## Definitions
- High host: Core Utilization > 90% AND Thread Utilization > 80%.
- Low host: Core Utilization < 50% AND Thread Utilization < 40%.
- 90% for core, not 100%: sustained 100% for 300 s is too late, and NUMA keeps some cores busy while others idle.
- 80% for thread, not lower: lower would include hosts that still have many idle threads.
- Focus is imbalance at high utilization. Imbalance at low utilization is not operationally important.
![High and low hosts in a cluster](../../images/cluster-cpu-imbalance-count-of-high-vs-low-utilization-hosts.png)

## Formula
```text
Imbalance = High hosts / Low hosts
```
- Relative, so clusters of different sizes compare.

## Values
| Colour | Meaning | Value |
|---|---|---|
| Red (worst) | 1 or more high hosts, no low host to move VMs to. Moving VMs to another cluster may be required. | 100, 200, 300, ... (raised to avoid overlap with pink) |
| Pink (bad) | More high hosts than low hosts. Maybe not enough capacity to balance. | Between 1 and 63 (decimal) |
| Orange (bad) | High hosts = low hosts. | 1 |
| Yellow (warning) | Fewer high hosts than low hosts. | Between 0 and 1 |
| Green (good) | Utilized and balanced. | 0 |
| Grey (waste) | Low hosts, no high host. Underutilized. | -1, -2, ... (whole numbers) |
- Pink can reach 63: maximum 64 hosts minus 1 low host.
![Imbalance colours for a 6-host cluster](../../images/cluster-cpu-imbalance-score-colors-for-6-host-cluster.png)

## Limitation
- Summarizing loses detail: 1 high over 2 low and 4 high over 8 low both give 0.5.
- Concatenation (1.2, 4.8) keeps the detail but makes sorting less meaningful.
- A 12-host cluster has 169 possible values.

## Traps
- "Imbalance 0 means every host is idle" → 0 also means no high hosts while some hosts are well used.

## Metadata
```yaml
id: vsphere/cpu/metrics/cluster/inter-host-imbalance
retriever_guide: metric-meaning
scope: vsphere
technology:
- cpu
pillar:
- performance
- capacity
product:
- vcf-operations
object:
- ClusterComputeResource
metric_class: context
internal_derive:
- vsphere/cpu/metrics/host/core-utilization
- vsphere/cpu/metrics/host/utilization
same_name: []
same_meaning: []
related:
- vsphere/cpu/metrics/host/imbalance
- vsphere/system/concepts/cluster-operations
source:
  document: PART 3 - Counters.docx
  path: Provider Objects > Overview > Inter-Host Imbalance
corrections: []
review_notes:
- 'Section ''Values'': the book''s grey range reads ''-1, -2, -3, ...., 64''. Read as down to -64.'
- 'Section ''Definitions'': whether this is a built-in VCF Operations metric or the author''s own super metric is not stated. Related to Q011.'
status: draft
```
