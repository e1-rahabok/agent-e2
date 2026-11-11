# VM Memory Swap Target

## Meaning
- Amount of memory ESXi aims to reclaim from the VM by compression and swapping.
- Input, not result. ESXi need not reach it if it does not have to.
- Read it as compress-swap target.

## Example
- Swap Target about 6.8 million KB, changing every 20 seconds.
- Swapped constant for the hour (max = min). No limit, no resource pool: likely historical.
- Granted constant: the VM did not request more.
- Consumed fluctuated slightly. Consumed and Swap Target mirror each other: when Consumed rises, Swap Target falls.
![Swap Target, Swapped, Granted and Consumed table](../../images/vm-memory-swap-target-swapped-granted-consumed-quiz-table.png)

## Misconceptions
- "Swap Target = Swapped" → the target is an input; Swapped is the result.

## Metadata
```yaml
id: vsphere/technology/memory/metrics/virtual-motherboard/swap-target
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
- vsphere/technology/memory/metrics/virtual-motherboard/swapped
- vsphere/technology/memory/metrics/virtual-motherboard/compressed
- vsphere/technology/memory/metrics/virtual-motherboard/consumed
images:
  - path: ../../images/vm-memory-swap-target-swapped-granted-consumed-quiz-table.png
    product: [vsphere]
    object: [VirtualMachine]
    metric: ['VM Memory Swap Target', 'VM Memory Swapped', 'VM Memory Granted', 'VM Memory Consumed']
    image_type: table
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: Memory > VM > Swap + Compress > Transition; Quiz!
corrections: []
review_notes: []
status: draft
```
