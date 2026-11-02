---
id: vsphere/memory/metrics/host/consumed
retriever_guide: metric-meaning
scope: vsphere
technology:
- memory
pillar:
- capacity
product:
- vsphere
object:
- HostSystem
metric_class: consumption
internal_derive:
- vsphere/foundations/provider-consumer
same_name:
- vsphere/memory/metrics/cluster/consumed
- vsphere/memory/metrics/virtual-machine/consumed
same_meaning: []
related: []
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity
corrections: []
review_notes: []
status: draft
---

# ESXi Memory Consumed

## Meaning
- Includes memory consumed by ESXi itself.

## Traps
- Summing VM Consumed and expecting ESXi Consumed.
