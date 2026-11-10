# VM Memory Consumed

## Meaning
- Excludes overhead.
- Includes reserved memory only once the VM has touched it: a reservation alone does not raise Consumed. See `vsphere/architecture/resource-controls`.

## vMotion effect
- After vMotion, Consumed on the destination can increase. Swapped or compressed pages can become regular pages. See `vsphere/architecture/overhead`.

## View
- ESXi view (ESXi pages) of the VM: memory that has been active.
- Shared pages count once: 3 VM pages shared into 1 ESXi page count as 1.
- Ballooned and swapped VM pages have no ESXi page here.
- Consumed can hold a lot of guest cache.
- Does not exist in Windows. No Guest OS counterpart.

## Formula
```text
Consumed = Granted - savings (sharing)
```
- ESXi memory mapped to the VM.
- ESXi backs VM memory with 2 MB pages whenever possible, even if the guest does not request them. Fewer TLB misses, but the VM consumes more than the guest uses.
- Excludes overhead (transparent to the guest) and swapped memory (not readily usable).
- Compressed: the freed part of a compressed page (for example 0.75 KB of a 4 KB page compressed to 1 KB) is excluded.
- Includes touched reserved memory; untouched reserved memory is not counted.
- Capped by a limit. Can reach, not exceed, configured memory.
- vCenter Guest | Memory Usage is the same as Consumed. Do not use it.

## Why Consumed stays high
- A guest that frees a page only updates its free list. The hypervisor does not see the list, so the ESXi page stays mapped.
- So Consumed is higher than Guest OS In Use and stays high after Active has dropped.
- Consumed and Guest OS In Use are managed independently. They do not match.
- Consumed below Guest OS Used: check Shared and Zero pages.

## Metadata
```yaml
id: vsphere/technology/memory/metrics/virtual-motherboard/consumed
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
layer:
- virtual-motherboard
metric_class: consumption
internal_derive:
- vsphere/architecture/resource-controls
- vsphere/architecture/overhead
same_name:
- vsphere/technology/memory/metrics/host/consumed
- vsphere/technology/memory/metrics/cluster/consumed
same_meaning: []
related:
- vsphere/technology/memory/concepts/memory-layers
- vsphere/technology/memory/concepts/guest-os-vs-vm-memory
- vsphere/technology/memory/metrics/virtual-motherboard/granted
- vsphere/technology/memory/metrics/virtual-motherboard/shared
- vsphere/technology/memory/metrics/virtual-motherboard/zero-pages
- vsphere/technology/memory/metrics/virtual-motherboard/active
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity; Memory > Architecture > Guest OS vs VM; Memory > VM > Consumption Metrics > Consumed
corrections: []
review_notes:
- 'Section ''View'': from Memory > Architecture.'
- 'Sections Formula, Why Consumed stays high: from Memory > VM.'
- 'To check: Section ''Formula'': whether Consumed includes the compressed remainder that stays in DIMM; the book is unsure.'
status: draft
```
