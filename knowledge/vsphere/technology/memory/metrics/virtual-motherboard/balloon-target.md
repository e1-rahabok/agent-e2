# VM Memory Balloon Target

## Meaning
- Memory the hypervisor wants the balloon driver to reclaim from this VM.
- Non-zero: the hypervisor has asked the VM to give back memory.
- The Guest OS performs the reallocation. So Balloon Target can be 0 while Ballooned is above 0.

## Misconceptions
- "Balloon Target 0, so Ballooned must be 0" → the guest releases pages on its own schedule.

## Metadata
```yaml
id: vsphere/technology/memory/metrics/virtual-motherboard/balloon-target
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
- vsphere/technology/memory/concepts/ballooning
same_name: []
same_meaning: []
related:
- vsphere/technology/memory/metrics/virtual-motherboard/ballooned
source:
  document: Knowledge base
  path: Memory > VM > Contention Metrics > Balloon
corrections: []
review_notes: []
status: draft
```
