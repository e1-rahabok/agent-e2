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
- A limit causes ballooning, also on a host with free memory. A limit lowers the VM's memory target. ESXi reclaims what is above it with the balloon first, then compression, then host swap. See [`vsphere/technology/memory/concepts/memory-limit`](../../concepts/memory-limit.md).
- The 4 memory layers explain why Consumed grows under a limit: the Guest OS uses more memory, the VM layer makes that Consumed, and ESXi reclaims when Consumed would pass the limit. They do not stop the balloon: the balloon is how ESXi takes memory back when the driver runs.
- Compressed and Swapped join when the balloon cannot take enough: driver missing, switched off or too slow, or at its ceiling (Mem.CtlMaxPercent, default 65% of configured memory).
- Example: 8 GB CentOS VM running MySQL with a 2 GB limit was heavily ballooned. 6 GB must leave; the balloon takes at most 5.2 GB.
- See [`vsphere/technology/memory/concepts/ballooning`](../../concepts/ballooning.md).

## Misconceptions
- "Ballooned > 0, so the host is under memory pressure now" → not necessarily. Ballooned, Compressed and Swapped are past tense: memory reclaimed earlier. VM memory contention decides whether the VM waits now.
- "Ballooning means VMs are contending for RAM" → check Contention.
- "A limit cannot cause ballooning, only Compressed or Swapped" → the balloon is first when the driver runs. Compression and swap take over when the balloon cannot reclaim enough.

## Metadata
```yaml
id: vsphere/technology/memory/metrics/virtual-motherboard/ballooned
retriever_guide: metric-meaning
up_front: 'Ballooned > 0, so the host is under memory pressure now'
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
same_name:
- vsphere/technology/memory/metrics/host/ballooned
same_meaning: []
related:
- vsphere/technology/memory/metrics/comparisons/vm-memory-metrics
- vsphere/technology/memory/decision-tree/is-overcommit-affecting-vm
- vsphere/technology/memory/concepts/memory-layers
- vsphere/technology/memory/concepts/ballooning
- vsphere/technology/memory/metrics/virtual-motherboard/balloon-target
- vsphere/technology/memory/concepts/memory-limit
source:
  document: Knowledge base
  path: The World of Metrics > Metrics Nuances > Complexity > Other Nuances; Memory > Architecture > Virtual Memory; Relationship; Memory > VM > Contention Metrics > Balloon; Consumption Metrics > Ballooned
corrections: []
review_notes:
- 'To check: metric_class: set to contention.'
- 'Section ''Mechanism'': from Memory > Architecture.'
- 'Sections Behaviour: from Memory > VM.'
status: draft
```
