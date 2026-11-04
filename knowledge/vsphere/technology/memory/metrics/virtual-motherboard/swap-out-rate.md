# VM Memory Swap Out Rate

## Meaning
- Rate of pages moved from DIMM to the swap file (KBps). Swap Out (KB) is the amount.

## Why it matters
- Swap out means ESXi was under memory pressure or the VM hit a limit.
- Not contention by itself: the swapped page may never be requested.
- Shape matters: an acute burst differs from a slow, sustained rate with the same total.
- Example: summed rate × 300 s ≈ 4,059 MB, close to 4,157 MB Swapped.

## Traps
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
  document: PART 3 - Counters.docx
  path: Memory > VM > Swap + Compress > Transition; Example
corrections: []
review_notes:
- 'metric_class set to context: swap out is not contention per the book. Author to confirm.'
status: draft
```
