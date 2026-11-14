# Cluster Memory Usage

## Meaning
- Maps to Consumed (VM overhead included).

## Metadata
```yaml
id: vsphere/technology/memory/metrics/cluster/usage
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
- sp5-framework/observability/resource-nature
same_name:
- vsphere/technology/memory/metrics/virtual-motherboard/usage
- vsphere/technology/memory/metrics/host/usage
same_meaning: []
related:
- vsphere/technology/memory/metrics/cluster/consumed
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity
corrections: []
review_notes: []
status: draft
```
