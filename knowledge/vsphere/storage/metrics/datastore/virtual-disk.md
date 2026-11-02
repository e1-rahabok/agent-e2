# Datastore Virtual Disk

## Meaning
- Excludes RDM. The RDM data sits on an external LUN, not on the datastore.

## Metadata
```yaml
id: vsphere/storage/metrics/datastore/virtual-disk
retriever_guide: metric-meaning
scope: vsphere
technology:
- storage
pillar:
- capacity
- performance
product:
- vsphere
object:
- Datastore
metric_class: consumption
internal_derive:
- vsphere/foundations/object-relationships
same_name:
- vsphere/storage/metrics/virtual-machine/virtual-disk
same_meaning: []
related: []
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity
corrections: []
review_notes: []
status: draft
```
