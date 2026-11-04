# Cluster Memory Usage

## Meaning
- Maps to Consumed + Overhead.

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
- foundations/resource-nature
same_name:
- vsphere/technology/memory/metrics/virtual-motherboard/usage
- vsphere/technology/memory/metrics/host/usage
same_meaning: []
related:
- vsphere/technology/memory/metrics/cluster/consumed
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity
corrections: []
review_notes: []
status: draft
```
