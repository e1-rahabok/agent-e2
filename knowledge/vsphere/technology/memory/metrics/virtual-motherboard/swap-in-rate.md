# VM Memory Swap In Rate

## Meaning
- Rate of pages moved from the swap file back into DIMM (KBps). Swap In (KB) is the amount.
- Host cache has its own counter: Host cache swap in rate.

## Why it matters
- Swap in is contention: the guest requested a swapped page and waited.
- Correlates highly with Memory Latency.
- It does not mean the host is under pressure now. The pressure happened in the past.

## Misconceptions
- "No current host pressure, so swap in is harmless" → the guest still waits for each page.

## Metadata
```yaml
id: vsphere/technology/memory/metrics/virtual-motherboard/swap-in-rate
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
- vsphere/technology/memory/concepts/swap-and-compression
same_name: []
same_meaning: []
related:
- vsphere/technology/memory/metrics/virtual-motherboard/swap-out-rate
- vsphere/technology/memory/metrics/virtual-motherboard/latency
- vsphere/technology/memory/metrics/virtual-motherboard/swapped
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: Memory > VM > Swap + Compress > Transition
corrections: []
review_notes: []
status: draft
```
