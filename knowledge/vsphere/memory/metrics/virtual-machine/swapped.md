# VM Memory Swapped

## Meaning
- Memory of the VM swapped out at host level.
- The ESXi equivalent is called Swap Used. Different names for different vantage points.

## Metadata
```yaml
id: vsphere/memory/metrics/virtual-machine/swapped
retriever_guide: metric-meaning
scope: vsphere
technology:
- memory
pillar:
- performance
product:
- vsphere
object:
- VirtualMachine
metric_class: contention
internal_derive:
- vsphere/memory/concepts/overcommit-techniques
same_name: []
same_meaning:
- vsphere/memory/metrics/host/swap-used
related: []
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity
corrections: []
review_notes:
- metric_class set to contention. Author to confirm.
status: draft
```
