# VM Memory Entitlement

## Formula
```text
Entitlement = Granted + Overhead
```

## Meaning
- ESXi memory the VM deserves, as determined by the ESXi scheduler.

## Observed behaviour
- On a 9.1 lab VM (8 GiB configured), Entitlement tracked Consumed sample by sample at about 1.104 times Consumed (6.10 GiB against 5.53 GiB), while Granted stayed at 6,356,764 KB and Overhead consumed at 58,460 KB. Granted plus Overhead (6.12 GiB) did not move with it, so the formula above did not describe this VM (Q230).
- A reservation did not change it: Entitlement stayed near 6.1 GiB with an 8 GiB reservation set and after it was removed ([VM memory metrics compared](../comparisons/vm-memory-metrics.md), section VM reservation across counters).

## Misconceptions
- "Entitlement is what the VM uses" → it is a scheduler value.
- "Entitlement rises to the VM's reservation" → it stayed below an 8 GiB reservation on the lab VM (6.1 GiB).

## Metadata
```yaml
id: vsphere/technology/memory/metrics/virtual-motherboard/entitlement
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
- vsphere/architecture/resource-controls
- vsphere/technology/memory/concepts/memory-overhead
same_name: []
same_meaning: []
related:
- vsphere/technology/memory/metrics/comparisons/vm-memory-metrics
- vsphere/technology/memory/metrics/virtual-motherboard/granted
- vsphere/technology/memory/metrics/virtual-motherboard/overhead
source:
  document: Knowledge base
  path: Memory > VM > Consumption Metrics
corrections: []
review_notes:
- 'To check: Section ''Meaning'': the limit behaviour; unconfirmed.'
- 'To check: whether Entitlement excludes memory above a limit (the VM is not entitled beyond its limit).'
status: draft
```
