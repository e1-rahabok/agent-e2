# VM Memory Swapped

## Meaning
- Memory of the VM swapped out at host level.
- The ESXi equivalent is called Swap Used. Different names for different vantage points.
- Relevance for operations: performance troubleshooting and capacity context: pages the VM waits for when it touches them. The wait shows in VM Memory Latency.

## Behaviour
- Pages that do not compress to 2 KB or smaller are swapped. Compressed and Swapped are mutually exclusive per page. Both grow while ESXi reclaims; afterwards they can move apart: when the guest reads swapped pages back while ESXi compresses others, for example under a limit, Swapped falls as Compressed rises ([`vsphere/technology/memory/concepts/swap-and-compression`](../../concepts/swap-and-compression.md), section Example: limit, swap and compress in opposite directions).
- ESXi swaps pages at random: it cannot see guest free memory.
- VM Memory Swapped is not Swap Out minus Swap In: Swapped is what sits in the swap file now, while Swap Out and Swap In count transfers since the counters started on this host, so a vMotion arrival or a counter reset breaks the difference.
- vMotion can make Swapped larger than swap out minus swap in: a VM that arrives with memory already swapped brings those pages with it.
- Swapped pages stay out until the guest requests them.
- A limit causes ballooning first, then compression and swapping, for what the balloon cannot take. See [`vsphere/technology/memory/concepts/memory-limit`](../../concepts/memory-limit.md).

## Non-zero value
- Compressed or Swapped happens for one of two reasons:
  - ESXi Consumed is very high.
  - The VM hit its limit.
- It does not mean the host failed to serve the VM. The Consumed pages taken can hold a lot of cache.
- So it does not always result in VM Memory Latency. Check Latency for unmet demand.

## Misconceptions
- "Swapped > 0, so the host cannot satisfy the VM's memory" → not always. The pages taken can be guest cache. Check Latency.

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
metric_class: consumption
internal_derive:
- vsphere/technology/memory/concepts/host-memory-states
same_name: []
same_meaning:
- vsphere/technology/memory/metrics/host/swap-used
related:
- vsphere/technology/memory/metrics/comparisons/vm-memory-metrics
- vsphere/technology/memory/concepts/swap-and-compression
- vsphere/technology/memory/metrics/virtual-motherboard/compressed
- vsphere/technology/memory/metrics/virtual-motherboard/swap-in-rate
- vsphere/technology/memory/metrics/virtual-motherboard/swap-out-rate
- vsphere/technology/memory/metrics/virtual-motherboard/swap-target
source:
  document: Knowledge base; vSphere 9.1 documentation (PDF built 2026-11-02)
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity; Memory > VM > Swap + Compress; Monitoring and Performance, Virtual Machines, Memory (MB), Swapped (p. 2105); Memory Compression (p. 1841)
corrections:
- 'Section ''Behaviour'': vSphere 9.1 documentation, Monitoring and Performance > Virtual Machines > Memory (MB) (p. 2105), defines Swapped = swapout - swapin. Swapped is the VM''s current swapped memory, not that difference; kept until the documentation is fixed.'
review_notes: []
status: draft
```
