# VM Memory Swapped

## Meaning
- Memory of the VM swapped out at host level.
- The ESXi equivalent is called Swap Used. Different names for different vantage points.

## Behaviour
- Pages that do not compress below 2 KB are swapped. Compressed and Swapped are mutually exclusive and move together.
- ESXi swaps pages at random: it cannot see guest free memory.
- Swapped is not Swap in - Swap out: both run in parallel on different pages.
- vMotion can make Swapped larger than swap out minus swap in: a VM that arrives with memory already swapped brings those pages with it.
- Swapped pages stay out until the guest requests them.
- A limit causes swapping and compression.

## What a non-zero value means
- Compressed or Swapped happens for one of two reasons:
  - ESXi Consumed is very high.
  - The VM hit its limit.
- It does not mean the host failed to serve the VM. The Consumed pages taken can hold a lot of cache.
- So it does not always result in VM Memory Latency. Check Latency for unmet demand.

## Misconceptions
- "Swapped > 0, so the host cannot satisfy the VM's memory" → not always. The pages taken can be guest cache. Check Latency.
- See `vsphere/technology/memory/concepts/swap-and-compression`.

## Metadata
```yaml
id: vsphere/technology/memory/metrics/virtual-motherboard/swapped
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
layer:
- virtual-motherboard
metric_class: contention
internal_derive:
- vsphere/technology/memory/concepts/host-memory-states
same_name: []
same_meaning:
- vsphere/technology/memory/metrics/host/swap-used
related:
- vsphere/technology/memory/concepts/swap-and-compression
- vsphere/technology/memory/metrics/virtual-motherboard/compressed
- vsphere/technology/memory/metrics/virtual-motherboard/swap-in-rate
- vsphere/technology/memory/metrics/virtual-motherboard/swap-out-rate
- vsphere/technology/memory/metrics/virtual-motherboard/swap-target
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity; Memory > VM > Swap + Compress
corrections: []
review_notes:
- 'The vSphere 9.1 documentation (vSphere Monitoring and Performance > Virtual Machines > Memory (MB), p. 2105) defines Swapped = swapout - swapin. The documentation is wrong here; the book is right. The vMotion line in section ''Behaviour'' follows the book.'
- 'To check: metric_class: set to contention.'
- 'Sections Behaviour: from Memory > VM.'
status: draft
```
