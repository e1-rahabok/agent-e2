# VM Memory Balloon Target

## Meaning
- Memory the hypervisor wants the balloon driver to reclaim from this VM.
- Non-zero: the hypervisor has asked the VM to give back memory.
- The Guest OS performs the reallocation. So Balloon Target can be 0 while Ballooned is above 0.

## Traps
- "Balloon Target 0, so Ballooned must be 0" → the guest releases pages on its own schedule.

## Metadata
```yaml
id: vsphere/memory/metrics/virtual-machine/balloon-target
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
metric_class: context
internal_derive:
- vsphere/memory/concepts/ballooning
same_name: []
same_meaning: []
related:
- vsphere/memory/metrics/virtual-machine/ballooned
source:
  document: PART 3 - Counters.docx
  path: Memory > VM > Contention Metrics > Balloon
corrections: []
review_notes: []
status: draft
```
