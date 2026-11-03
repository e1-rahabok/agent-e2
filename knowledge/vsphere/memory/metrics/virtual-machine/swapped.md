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

## What a non-zero value means
- Compressed or Swapped happens for one of two reasons:
  - ESXi Consumed is very high.
  - The VM hit its limit.
- It does not mean the host failed to serve the VM. The Consumed pages taken can hold a lot of cache.
- So it does not always result in VM Memory Latency. Check Latency for unmet demand.

## Traps
- "Swapped > 0, so the host cannot satisfy the VM's memory" → not always. The pages taken can be guest cache. Check Latency.
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
- 'The vSphere 9.1 documentation defines Swapped = swapout - swapin, and notes that vMotion can make Swapped larger than swapout - swapin (vSphere Monitoring and Performance > Virtual Machines > Memory (MB), p. 2103). This contradicts section ''Behaviour''. Open question Q045.'
- metric_class set to contention. Author to confirm.
- 'Sections Behaviour: from Memory > VM.'
- "Section 'What a non-zero value means': author (2026-11-03), Q016: VM Compressed happens when ESXi Consumed is very high or the VM hit its limit. Consumed pages can hold a lot of cache, so it does not always translate to VM latency. The Architecture statement holds; the VM-section statement is superseded."
status: draft
```
