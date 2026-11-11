# VM memory latency (contention) is high

## Checks, in order
1. Latency (VCF Operations: VM Memory Contention).
2. Swap in rate and decompression rate: the source of the wait.
3. Limit on the VM, and the resource pool's resources.
4. Shares and reservation, compared with other VMs.
5. Host memory pressure: Swap out, Compressed, Ballooned on other VMs.

## Actions
- Put the VM swap file (vswp) on faster, lower-latency storage, such as host swap cache.
- Raise memory shares or reservation to reduce swapping. In a resource pool, make sure the pool has enough for all its VMs.
- Reduce assigned memory (right-size). Less to reclaim, lower risk.
- Remove the VM limit.
- Unswap the swapped pages. Not possible via API; possible with a manual command (article by Duncan Epping and Valentin Bondzio).
- Reboot the VM in regular maintenance. This removes the swap file and future swap-in waits on those pages. A page can be swapped out again later.

## How to read the result
- Swap out without swap in: past pressure, no wait yet.
- Latency with a flat Consumed near the limit: the limit is the cause.

## Misconceptions
- "Balloon is in Latency" → Latency excludes balloon.

## Metadata
```yaml
id: vsphere/technology/memory/troubleshooting/vm-memory-latency-high
retriever_guide: troubleshooting
scope: vsphere
technology:
- memory
pillar:
- performance
product:
- vsphere
- vcf-operations
object:
- VirtualMachine
internal_derive:
- vsphere/technology/memory/metrics/virtual-motherboard/latency
- vsphere/technology/memory/concepts/swap-and-compression
related:
- vsphere/technology/memory/metrics/virtual-motherboard/swap-in-rate
- vsphere/technology/memory/metrics/virtual-motherboard/swapped
- vsphere/technology/memory/metrics/virtual-motherboard/compressed
- vsphere/technology/memory/decision-tree/is-overcommit-affecting-vm
source:
  document: PART 3 - Counters.docx
  path: Memory > VM > Contention Metrics > Latency
corrections: []
review_notes:
- 'To check: unswap article cited by the book, third-party, not read (https://www.yellow-bricks.com/2016/06/02/memory-pages-swapped-can-unswap/).'
status: draft
```
