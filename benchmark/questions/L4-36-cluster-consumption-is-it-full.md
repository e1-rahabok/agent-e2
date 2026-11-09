# Cluster Consumption orange: is the cluster full?

## Prompt
The attached screenshot is the VCF Operations view of one cluster: Cluster Consumption and its sub-metrics, and Cluster Performance beside it.

- Cluster-wide ESXi memory consumed is in the orange range.
- Ballooned, swapped + zipped and memory tiering consumption are green.
- Cluster Performance is green.
- The cluster has 12 hosts and is sized for 11 (one host for HA or maintenance).

The capacity manager wants to stop placing VMs on this cluster. Do you agree? Explain what the screenshot shows and what decides it.

## Input to supply
- Tool: VCF Operations 9.1, cluster object > Metrics, folders `vCommunity|Cluster Consumption` and `vCommunity|Cluster Performance` (or the pack's dashboard).
- Condition for the key: memory consumed between 80% and 90%; ballooned, swapped + zipped and tiering consumption green; Cluster Performance green; 12 hosts in the cluster.
- Mask cluster names if they reveal the customer.
- Save as `benchmark/questions/76/vcf-operations-cluster-consumption.png`.

## Likely wrong answer
"Agree: memory consumed is orange, so the cluster is full."

## Expected key points
- Not yet. Consumed memory is utilization, not contention: Cluster Performance green says the VMs are not slow.
- The saturation rows (ballooned, swapped + zipped, tiering) are green: no reclamation pressure.
- Ballooning starts only after about 99% of host memory is used. With 12 hosts sized for 11, a 99% target during HA or maintenance gives about 90.75% in normal operation (99% × 11 / 12).
- So the decision depends on the HA headroom: below about 90% consumed per host the cluster can still take VMs; watch the saturation rows and Cluster Performance as it grows.
- The answer would change if any saturation row left green or Cluster Performance fell.

## Notes
- Previous id: question-0076 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0076"
title: "Cluster Consumption orange: is the cluster full?"
product: [vcf-operations]
technology: [memory, system]
task: decide-capacity
level: 400
answer_type: judged
input: [screenshot]
knowledge:
  - vsphere/object-types/cluster/models/cluster-consumption
  - vsphere/technology/memory/concepts/host-memory-states
  - sp5-framework/capacity/capacity-model
attachments:
  - 0076/vcf-operations-cluster-consumption.png
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
status: awaiting-input
```
