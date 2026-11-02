# Cluster Memory Consumed

## Meaning
- Includes only memory consumed by VMs.
- Includes VM overhead.
- Excludes memory consumed by ESXi itself.

## Metadata
```yaml
id: vsphere/memory/metrics/cluster/consumed
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
- vsphere/foundations/provider-consumer
same_name:
- vsphere/memory/metrics/host/consumed
- vsphere/memory/metrics/virtual-machine/consumed
same_meaning: []
related: []
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity
corrections: []
review_notes: []
status: draft
```
