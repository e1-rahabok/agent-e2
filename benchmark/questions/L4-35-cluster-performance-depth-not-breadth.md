# Cluster Performance: depth without breadth

## Prompt
The attached screenshot is the VCF Operations metric view of one cluster: Cluster Performance Score and its 9 sub-metrics (vCommunity management pack).

- Worst VM Disk Latency is in the red range.
- 90th Percentile VM Disk Latency is green.
- All other sub-metrics are green.

Which statement is correct?

- A. One VM, or a few, is hit hard: open the worst VM and its virtual disks; the storage of the cluster as a whole is not the first suspect.
- B. The datastore or array is overloaded for the whole cluster.
- C. The KPI is wrong: a green 90th percentile means the worst VM must be green too.
- D. The disk rows are 5-minute averages, so the red value is an old sample.

## Input to supply
- Tool: VCF Operations 9.1, cluster object > Metrics, folder `vCommunity|Cluster Performance`, the 10 metrics in one view (or the pack's dashboard).
- Condition for the key: Worst VM Disk Latency at or above 160 ms; 90th Percentile VM Disk Latency below 20 ms; all other sub-metrics green; the cluster has at least 20 powered-on VMs.
- Mask cluster names if they reveal the customer.
- Save as `benchmark/questions/75/vcf-operations-cluster-performance-submetrics.png`.

## Likely wrong answer
B: reading the worst VM as a cluster-wide storage problem.

## Expected key points
- Answer: A.
- The worst-VM rows answer how deep; the 90th-percentile rows answer how broad. Red depth with green breadth means a problem that hits one VM hard, not many VMs.
- The knowledge base example: one VM with 200 ms disk latency and the others at 0 makes the worst-VM row orange to red while the 90th percentile stays 0.
- D is wrong: the VM rows are 20-second peaks, not 5-minute averages.
- Next: open the worst VM, check per virtual disk, read vs write, outstanding IO and the host KAVG and DAVG.

## Notes
- Previous id: question-0075 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0075"
title: "Cluster Performance: depth without breadth"
product: [vcf-operations]
technology: [storage, system]
task: read-metric
level: 400
answer_type: deterministic
input: [screenshot]
knowledge:
  - vsphere/object-types/cluster/metrics/cluster-performance
  - vsphere/object-types/vm/metrics/comparisons/peak-20-second-metrics
attachments:
  - 0075/vcf-operations-cluster-performance-submetrics.png
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
answer: [A]
trap: [B]
status: awaiting-input
```
