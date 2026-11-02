# VM Memory Swapped

## Meaning
- Memory of the VM swapped out at host level.
- The ESXi equivalent is called Swap Used. Different names for different vantage points.

## Behaviour
- Pages that do not compress below 2 KB are swapped. Compressed and Swapped are mutually exclusive and move together.
- ESXi swaps pages at random: it cannot see guest free memory.
- Swapped is not Swap in - Swap out: both run in parallel on different pages.
- Swapped pages stay out until the guest requests them.
- A limit causes swapping and compression.
- See `vsphere/memory/concepts/swap-and-compression`.

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
related:
- vsphere/memory/concepts/swap-and-compression
- vsphere/memory/metrics/virtual-machine/compressed
- vsphere/memory/metrics/virtual-machine/swap-in-rate
- vsphere/memory/metrics/virtual-machine/swap-out-rate
- vsphere/memory/metrics/virtual-machine/swap-target
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity; Memory > VM > Swap + Compress
corrections: []
review_notes:
- metric_class set to contention. Author to confirm.
- 'Sections Behaviour: from Memory > VM.'
- 'Section ''Behaviour'': the VM section says any Compressed or Swapped value means the host could not satisfy the VM; the Architecture section says it does not mean VMs contended for RAM. Open question in docs/todo.md.'
status: draft
```
