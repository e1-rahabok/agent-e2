# Memory limit

## Mechanism
- A memory limit (`sched.mem.max`, Edit Settings, Memory, Limit) caps the physical memory ESXi backs the VM with. Consumed cannot grow past it. Granted can: it counts VM pages, shared and zero pages included.
- Shares and reservations act when demand exceeds supply. A limit is enforced at all times, also on a host in the High state with free memory.
- The Guest OS does not see the limit. It sees the configured memory, fills it with cache and free pages, and Consumed climbs until it meets the limit.
- A resource pool caps its VMs the same way. A VM that shows Unlimited can sit under a limit on its parent or an ancestor pool.
- Lowering a limit below the current Consumed starts the reclamation at once.

## Enforcement order
- The memory scheduler gives the VM a memory target that cannot exceed the limit. A VM whose Consumed is above its target is reclaimed in this order:
  1. Balloon, when the driver runs. The scheduler sets the Balloon Target to the excess. The guest picks the pages: free pages first, then clean cache, then guest swap. See [`vsphere/technology/memory/concepts/ballooning`](ballooning.md).
  2. Compression, when the driver is missing, switched off, not running yet, at its ceiling or too slow. ESXi picks pages without asking the guest.
  3. Host swapping, for pages that do not compress below 2 KB. See [`vsphere/technology/memory/concepts/swap-and-compression`](swap-and-compression.md).
- Page sharing runs whatever the limit. The limit does not trigger it.
- The balloon ceiling is 65% of configured memory by default (Mem.CtlMaxPercent on the host; `sched.mem.maxmemctl`, in MB, per VM). Everything above the ceiling goes by compression and swap.
- Example: 8 GB VM, 2 GB limit, all pages touched. 6 GB must leave. The balloon takes at most 5.2 GB (65%); at least 0.8 GB is compressed or swapped. Ballooned heavy, Compressed and Swapped small but above 0, is the normal picture.
- The vendor troubleshooting text reads it the same way: free host memory with high swap or balloon on a VM or pool means it reached its resource limit (vSphere 9.1, Monitoring and Performance, memory performance problems).

## Signs in the counters
- Consumed flat at or a little under the limit. Granted above it.
- Ballooned, Compressed or Swapped above 0 while the host has free memory and no other VM is reclaimed.
- A balloon flat near 65% of configured memory on a host with free memory: look for a limit on the VM, its pool and the ancestor pools.
- Swapped and Compressed can move in opposite directions: the guest reads swapped pages back while ESXi compresses others to stay under the limit. See the example in [`vsphere/technology/memory/concepts/swap-and-compression`](swap-and-compression.md).
- Swapped or compressed pages cost a wait only when the guest touches them again: that wait is memory contention. See [`vsphere/technology/memory/metrics/virtual-motherboard/latency`](../metrics/virtual-motherboard/latency.md).

## Fix
- Remove the limit, or raise it to what the guest needs. More memory on the host or the VM changes nothing while the limit stays.
- Size the VM to the memory it needs instead of capping a larger one. The guest cannot see a limit, so it behaves worse than a VM configured smaller.
- Check the pool and its ancestors, not only the VM.

## Misconceptions
- "A limit acts only when the host is short of memory" → a limit is absolute and is enforced on a host with free memory too.
- "A limit causes only Compressed or Swapped, never Balloon" → the balloon is first when the driver runs. Compression and swap take over when it cannot reclaim enough.
- "Switching the balloon off (`sched.mem.maxmemctl` 0) stops the reclamation" → the memory above the limit must still go: ESXi compresses and swaps instead, blind to which pages the guest uses.
- "Moving the VM to a host with more free memory ends the swapping" → the limit belongs to the VM or its pool and follows it to any host.

## Metadata
```yaml
id: vsphere/technology/memory/concepts/memory-limit
retriever_guide: how-it-works
scope: vsphere
technology:
- memory
pillar:
- performance
- capacity
product:
- vsphere
object:
- VirtualMachine
- ResourcePool
internal_derive:
- vsphere/technology/memory/concepts/ballooning
- vsphere/technology/memory/concepts/swap-and-compression
- vsphere/technology/memory/concepts/host-memory-states
related:
- vsphere/technology/memory/metrics/virtual-motherboard/ballooned
- vsphere/technology/memory/metrics/virtual-motherboard/balloon-target
- vsphere/technology/memory/metrics/virtual-motherboard/swapped
- vsphere/technology/memory/metrics/virtual-motherboard/compressed
- vsphere/architecture/resource-controls
- vsphere/object-types/resource-pool/resource-pool-design
source:
  document: Knowledge base; vSphere 9.1 documentation
  path: Memory > VM > Contention Metrics > Balloon; vSphere Monitoring and Performance, Solutions for Memory Performance Problems (p. 2037); Resource Management, Mem.CtlMaxPercent (p. 600)
corrections: []
review_notes:
- 'Section ''Enforcement order'': the order balloon, compression, swap under a limit, and that the Balloon Target is the excess above the limit. Vendor text found: the memory performance table of vSphere 9.1 (p. 2037) and Broadcom KB 326270; no vendor text states the Balloon Target formula. Check against https://knowledge.broadcom.com/external/article/326270.'
- 'To check: Section ''Mechanism'': the limit caps Consumed and not the VM overhead (overhead is bounded by sched.mem.overheadMax); the VCF Operations Effective limit would then be the limit plus overhead (Q205). Check against the VCF Operations 9.1 metric definition of Memory|Effective limit.'
- 'To check: whether VMkernel lowers the balloon ceiling when the guest reports little free memory. No vendor text found.'
status: draft
```
