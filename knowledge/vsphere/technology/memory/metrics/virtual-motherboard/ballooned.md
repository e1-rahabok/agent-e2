# VM Memory Ballooned

## Meaning
- Past tense. A non-zero value does not mean ballooning is happening now.
- Ballooning may have happened days ago. The page stays ballooned while idle, because the Guest OS has not asked for it.
- Some ballooning is normal. See [`vsphere/technology/memory/decision-tree/is-overcommit-affecting-vm`](../../decision-tree/is-overcommit-affecting-vm.md).

## Mechanism
- Proactive: starts before ESXi fails to meet demand.
- Reduces guest cache.
- Ballooned pages exist only in the VM view. They map to no ESXi page.
- The first sign of memory pressure, not of unmet demand. Demand is unmet only when Contention occurs.

## Behaviour
- Ballooned pages are removed from Granted: not functionally used.
- Guest OS memory counters still include them. Exclude them when working out Guest OS utilization.
- A flat Ballooned value for weeks: the guest never requested those pages again.
- A limit does not cause ballooning directly. The 4 memory layers act at different levels:
  - Process and Guest OS layer: the Guest OS uses more memory. The user can be the balloon driver or any other process.
  - VM layer: that use makes Consumed grow.
  - ESXi layer: when Consumed tries to grow beyond the limit, ESXi compresses or swaps.
- So under a limit, the direct result is Compressed or Swapped. Balloon is not.
- Example: 8 GB CentOS VM running MySQL with a 2 GB limit was heavily ballooned. The book notes a default maximum of around 63%.
- See [`vsphere/technology/memory/concepts/ballooning`](../../concepts/ballooning.md).

## Misconceptions
- "Ballooned > 0, so the host is under memory pressure now" → not necessarily.
- "Ballooning means VMs are contending for RAM" → check Contention.
- "A limit causes ballooning" → not directly. A limit causes Compressed or Swapped when Consumed tries to grow beyond it.

## Metadata
```yaml
id: vsphere/technology/memory/metrics/virtual-motherboard/ballooned
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
metric_class: contention
internal_derive:
- vsphere/technology/memory/concepts/host-memory-states
same_name: []
same_meaning: []
related:
- vsphere/technology/memory/decision-tree/is-overcommit-affecting-vm
- vsphere/technology/memory/concepts/memory-layers
- vsphere/technology/memory/concepts/ballooning
- vsphere/technology/memory/metrics/virtual-motherboard/balloon-target
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: The World of Metrics > Metrics Nuances > Complexity > Other Nuances; Memory > Architecture > Virtual Memory; Relationship; Memory > VM > Contention Metrics > Balloon; Consumption Metrics > Ballooned
corrections: []
review_notes:
- 'To check: metric_class: set to contention.'
- 'Section ''Mechanism'': from Memory > Architecture.'
- 'Sections Behaviour: from Memory > VM.'
- 'To check: Section ''Behaviour'': the balloon maximum is the Mem.CtlMaxPercent setting, default 65%; the book states around 63%.'
status: draft
```
