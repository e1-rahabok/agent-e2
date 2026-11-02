# VM Memory Consumed

## Meaning
- Excludes overhead.
- Includes reserved memory, even if the Guest OS has not used it yet. See `vsphere/foundations/resource-management`.

## vMotion effect
- After vMotion, Consumed on the destination can increase. Swapped or compressed pages can become regular pages. See `vsphere/foundations/overhead`.

## Metadata
```yaml
id: vsphere/memory/metrics/virtual-machine/consumed
retriever_guide: metric-meaning
scope: vsphere
technology:
- memory
pillar:
- capacity
product:
- vsphere
object:
- VirtualMachine
metric_class: consumption
internal_derive:
- vsphere/foundations/resource-management
- vsphere/foundations/overhead
same_name:
- vsphere/memory/metrics/host/consumed
- vsphere/memory/metrics/cluster/consumed
same_meaning: []
related: []
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity
corrections: []
review_notes: []
status: draft
```
