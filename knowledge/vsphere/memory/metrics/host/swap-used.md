# ESXi Memory Swap Used

## Meaning
- The host-level counterpart of VM Swapped. Different names for different vantage points.

## Metadata
```yaml
id: vsphere/memory/metrics/host/swap-used
retriever_guide: metric-meaning
scope: vsphere
technology:
- memory
pillar:
- performance
product:
- vsphere
object:
- HostSystem
metric_class: contention
internal_derive:
- vsphere/memory/concepts/overcommit-techniques
same_name: []
same_meaning:
- vsphere/memory/metrics/virtual-machine/swapped
related: []
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity
corrections: []
review_notes:
- metric_class set to contention. Author to confirm.
status: draft
```
