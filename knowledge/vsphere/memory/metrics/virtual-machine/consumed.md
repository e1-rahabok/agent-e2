# VM Memory Consumed

## Meaning
- Excludes overhead.
- Includes reserved memory, even if the Guest OS has not used it yet. See `vsphere/foundations/resource-management`.

## vMotion effect
- After vMotion, Consumed on the destination can increase. Swapped or compressed pages can become regular pages. See `vsphere/foundations/overhead`.

## View
- ESXi view (ESXi pages) of the VM: memory that has been active.
- Shared pages count once: 3 VM pages shared into 1 ESXi page count as 1.
- Ballooned and swapped VM pages have no ESXi page here.
- Consumed can hold a lot of guest cache.
- Does not exist in Windows. No Guest OS counterpart.

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
related:
- vsphere/memory/concepts/memory-layers
- vsphere/memory/concepts/guest-os-vs-vm-memory
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity; Memory > Architecture > Guest OS vs VM
corrections: []
review_notes:
- 'Section ''View'': from Memory > Architecture.'
status: draft
```
