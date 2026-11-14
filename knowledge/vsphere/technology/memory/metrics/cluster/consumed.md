# Cluster Memory Consumed

## Meaning
- Includes only memory consumed by VMs.
- Includes VM overhead.
- Excludes memory consumed by ESXi itself.

## Metadata
```yaml
id: vsphere/technology/memory/metrics/cluster/consumed
retriever_guide: metric-meaning
scope: vsphere
technology:
- memory
pillar:
- capacity
product:
- vsphere
object:
- ClusterComputeResource
metric_class: consumption
internal_derive:
- vsphere/architecture/provider-consumer
same_name:
- vsphere/technology/memory/metrics/host/consumed
- vsphere/technology/memory/metrics/virtual-motherboard/consumed
same_meaning: []
related: []
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity
corrections: []
review_notes:
- 'To check: vSphere 9.1 documentation disagrees with itself on cluster Consumed: the cluster memory chart text says VM consumed plus overhead and not the VMkernel, the Memory (MB) counter table says it includes service console and VMkernel memory; the catalog rows (kb = this file) follow the second. Check on a live cluster: cluster Consumed against the sum of host Consumed.'
status: draft
```
