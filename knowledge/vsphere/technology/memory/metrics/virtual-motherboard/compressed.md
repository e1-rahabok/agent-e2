# VM Memory Compressed

## Meaning
- VM memory held in compressed form. The output of compression, not the input.
- Compression saved: ESXi memory reclaimed by compression.
- Relevance for operations: performance troubleshooting and capacity context: past reclamation by host pressure or a limit. Not a wait: only a decompression on access counts in VM Memory Latency.

## Behaviour
- Pages that compress to 2 KB or smaller stay compressed (4:1 or 2:1). Others are swapped (vSphere 9.1 documentation, Memory Compression, p. 1841).
- Compressed and Swapped are mutually exclusive per page. Both grow while ESXi reclaims; afterwards they can move apart: when the guest reads swapped pages back while ESXi compresses others, for example under a limit, Swapped falls as Compressed rises ([`vsphere/technology/memory/concepts/swap-and-compression`](../../concepts/swap-and-compression.md), section Example: limit, swap and compress in opposite directions).
- Under a limit, pages are compressed to make room for newly requested pages. Example: limit 2 GB, Consumed fell 0.4 GB in 20 minutes; Compressed spiked to 0.6 GB.
- ESXi compresses pages at random: it cannot see guest free memory.
- Excluded from Granted: the page is not directly accessible.
- Not counted as savings: decompression costs performance.
- Windows also compresses its In Use pages inside the guest. Different counter.

## Non-zero value
- VM Compressed happens for one of two reasons:
  - ESXi Consumed is very high.
  - The VM hit its limit.
- The Consumed pages taken can hold a lot of cache. So it does not always result in VM Memory Latency.

## Misconceptions
- "Compressed > 0 means the VM is slow now" → only decompression on access causes latency.
- "Compressed > 0 means the host cannot satisfy the VM" → the cause is high ESXi Consumed or a limit, and the pages can be cache.

## Metadata
```yaml
id: vsphere/technology/memory/metrics/virtual-motherboard/compressed
retriever_guide: metric-meaning
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
layer:
- virtual-motherboard
metric_class: consumption
internal_derive:
- vsphere/technology/memory/concepts/swap-and-compression
same_name: []
same_meaning: []
related:
- vsphere/technology/memory/metrics/comparisons/vm-memory-metrics
- vsphere/technology/memory/metrics/virtual-motherboard/swapped
- vsphere/technology/memory/metrics/virtual-motherboard/latency
- vsphere/technology/memory/metrics/virtual-motherboard/swap-target
source:
  document: Knowledge base
  path: Memory > VM > Swap + Compress; Consumption Metrics > Compressed; Consumed > Ballooned
corrections: []
review_notes: []
status: draft
```
