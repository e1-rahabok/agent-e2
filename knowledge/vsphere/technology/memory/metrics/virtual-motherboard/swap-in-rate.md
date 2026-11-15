# VM Memory Swap In Rate

## Meaning
- Rate of pages moved from the swap file back into DIMM (KBps; vSphere Web Services API 9.1, `mem.swapinRate`). Swap In (KB) is the cumulative amount.
- Host cache has its own counter: Host cache swap in rate.
- Relevance for operations: performance troubleshooting: the source of a VM memory wait, read with VM Memory Latency ([`vsphere/technology/memory/vm-memory-latency-high`](../../vm-memory-latency-high.md), step 2). Not for capacity.

## Impact
- Swap in is contention: the guest requested a swapped page and waited.
- Correlates highly with Memory Latency.
- It does not mean the host is under pressure now. The pressure happened in the past.
- The rate tells the shape: a burst of several MB in one second is acute; a few KB per second over many minutes is chronic, with the same total ([`vsphere/technology/memory/concepts/swap-and-compression`](../../concepts/swap-and-compression.md), section Transition).

## Misconceptions
- "No current host pressure, so swap in is harmless" → the guest still waits for each page.
- "Swap In Rate is 0, so the VM never waits for memory" → a decompression is a wait too; VM Memory Latency counts both.

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
  document: Knowledge base; vSphere Web Services API 9.1
  path: Memory > VM > Swap + Compress > Transition; API 9.1 memory counters, swapinRate (https://developer.broadcom.com/xapis/vsphere-web-services-api/9.1/memory_counters.html)
corrections: []
review_notes: []
status: draft
```
