# VM Memory Balloon Target

## Meaning
- Memory the hypervisor wants the balloon driver to reclaim from this VM.
- Non-zero: the hypervisor has asked the VM to give back memory.
- The Guest OS performs the reallocation. So Balloon Target can be 0 while Ballooned is above 0.
- Two causes of a non-zero target: host memory pressure, and a VM above its limit (the target covers the excess; see [`vsphere/technology/memory/concepts/memory-limit`](../../concepts/memory-limit.md)). The driver stops at its ceiling, 65% of configured memory by default; a target above it leaves the rest to compression and swap.

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
