# VM Memory Compressed

## Meaning
- VM memory held in compressed form. The output of compression, not the input.
- Compression saved: ESXi memory reclaimed by compression.

## Behaviour
- Pages that compress below 2 KB stay compressed (4:1 or 2:1). Others are swapped.
- Compressed and Swapped are mutually exclusive and move together.
- Under a limit, pages are compressed to make room for newly requested pages. Example: limit 2 GB, Consumed fell 0.4 GB in 20 minutes; Compressed spiked to 0.6 GB.
- ESXi compresses pages at random: it cannot see guest free memory.
- Excluded from Granted: the page is not directly accessible.
- Not counted as savings: decompression costs performance.
- Windows also compresses its In Use pages inside the guest. Different counter.

## Traps
- "Compressed > 0 means the VM is slow now" → only decompression on access causes latency.

## Metadata
```yaml
id: vsphere/memory/metrics/virtual-machine/compressed
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
metric_class: contention
internal_derive:
- vsphere/memory/concepts/swap-and-compression
same_name: []
same_meaning: []
related:
- vsphere/memory/metrics/virtual-machine/swapped
- vsphere/memory/metrics/virtual-machine/latency
- vsphere/memory/metrics/virtual-machine/swap-target
source:
  document: PART 3 - Counters.docx
  path: Memory > VM > Swap + Compress; Consumption Metrics > Compressed; Consumed > Ballooned
corrections: []
review_notes:
- metric_class set to contention, matching Swapped and Ballooned. Author to confirm.
status: draft
```
