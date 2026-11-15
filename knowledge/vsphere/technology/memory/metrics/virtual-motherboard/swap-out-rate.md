# VM Memory Swap Out Rate

## Meaning
- Rate of pages moved from DIMM to the swap file (KBps; vSphere Web Services API 9.1, `mem.swapoutRate`). Swap Out (KB) is the cumulative amount.
- Relevance for operations: performance troubleshooting and capacity context: ESXi reclaiming from the VM now, by host pressure or a limit. Not a wait.

## Impact
- Swap out means ESXi was under memory pressure or the VM hit a limit.
- Not contention by itself: the swapped page may never be requested.
- Shape matters: an acute burst differs from a slow, sustained rate with the same total.
- Example: summed rate × 300 s ≈ 4,059 MB, close to 4,157 MB Swapped ([`vsphere/technology/memory/concepts/swap-and-compression`](../../concepts/swap-and-compression.md), section Example).
- A limit swaps on a host with free memory, after the balloon ([`vsphere/technology/memory/concepts/memory-limit`](../../concepts/memory-limit.md)).

## Misconceptions
- "Swap out means the VM is slow" → only swap in makes the guest wait.

## Metadata
```yaml
id: vsphere/technology/memory/metrics/virtual-motherboard/swap-out-rate
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
metric_class: context
internal_derive:
- vsphere/technology/memory/concepts/swap-and-compression
same_name: []
same_meaning: []
related:
- vsphere/technology/memory/metrics/virtual-motherboard/swap-in-rate
- vsphere/technology/memory/metrics/virtual-motherboard/swapped
source:
  document: Knowledge base; vSphere Web Services API 9.1
  path: Memory > VM > Swap + Compress > Transition; Example; API 9.1 memory counters, swapoutRate (https://developer.broadcom.com/xapis/vsphere-web-services-api/9.1/memory_counters.html)
corrections: []
review_notes: []
status: draft
```
