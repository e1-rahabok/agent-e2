# VM Memory Ballooned

## Meaning
- Past tense: the balloon holds pages reclaimed earlier, possibly days ago. A non-zero value does not mean ballooning is happening now.
- Ballooned stays while the Balloon Target stays: the VMkernel deflates the balloon when the target falls below it, not when the guest wants memory back. An idle VM on a host that stays overcommitted keeps a low allocation target, because idle memory is taxed, so its balloon stays ([`vsphere/technology/memory/concepts/ballooning`](../../concepts/ballooning.md), section Inflate and deflate, step by step).
- Some ballooning is normal. See [`vsphere/technology/memory/decision-tree/is-overcommit-affecting-vm`](../../decision-tree/is-overcommit-affecting-vm.md).
- Relevance for operations: capacity and performance troubleshooting context: a sign of reclamation by host pressure or a limit. Not a wait: VM Memory Latency does not count the balloon.

## Mechanism
- Proactive: starts before ESXi fails to meet demand.
- Reduces guest cache.
- Ballooned pages exist only in the VM view. They map to no ESXi page.
- The first sign of memory pressure, not of unmet demand. Demand is unmet only when Contention occurs.

## Behaviour
- Ballooned pages are removed from Granted: not functionally used.
- Guest OS memory counters still include them: the driver's pinned pages count as In Use. Guest OS sizing keeps them, with no deduction ([`guest-os/system/concepts/guest-os-sizing`](../../../../../guest-os/system/concepts/guest-os-sizing.md), section Ballooned memory in sizing).
- A flat Ballooned value for weeks: the Balloon Target held for weeks, and the guest ran within the rest of its memory.
- A limit causes ballooning, also on a host with free memory. A limit lowers the VM's memory target. ESXi reclaims what is above it with the balloon first, then compression, then host swap. See [`vsphere/technology/memory/concepts/memory-limit`](../../concepts/memory-limit.md).
- The 4 memory layers explain why Consumed grows under a limit: the Guest OS uses more memory, the VM layer makes that Consumed, and ESXi reclaims when Consumed would pass the limit. They do not stop the balloon: the balloon is how ESXi takes memory back when the driver runs.
- Compressed and Swapped join when the balloon cannot take enough: driver missing, switched off or too slow, or at its ceiling (Mem.CtlMaxPercent, default 65% of configured memory).
- Example: 8 GB CentOS VM running MySQL with a 2 GB limit was heavily ballooned. 6 GB must leave; the balloon takes at most 5.2 GB.
- See [`vsphere/technology/memory/concepts/ballooning`](../../concepts/ballooning.md).

## Misconceptions
- "Ballooned > 0, so the host is under memory pressure now" → not necessarily. Ballooned, Compressed and Swapped are past tense: memory reclaimed earlier, and a limit inflates the balloon on a host with free memory. VM memory contention decides whether the VM waits now.
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
metric_class: consumption
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
  document: Knowledge base; vSphere 9.1 documentation (PDF built 2026-11-02)
  path: The World of Metrics > Metrics Nuances > Complexity > Other Nuances; Memory > Architecture > Virtual Memory; Relationship; Memory > VM > Contention Metrics > Balloon; Consumption Metrics > Ballooned; Resource Management, How ESX Hosts Allocate Memory, Memory Tax for Idle Virtual Machines (pp. 1838-1839); Monitoring and Performance, Virtual Machines, Memory (MB), Balloon Target (p. 2104)
corrections: []
review_notes: []
status: draft
```
