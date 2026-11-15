# VM Memory Entitlement

## Meaning
- Host physical memory the VM is entitled to, as the ESXi scheduler determines it (vSphere API 9.1, `mem.entitlement`).
- The scheduler's allocation rests on the estimated demand and on the reservation, limit and shares of the VMs on the host (API 9.1, `mem.mementitlement`, the host-level counter).
- A value of VMkernel memory management, not an operations counter. vCenter shows it among the VM memory counters, so administrators meet it and misuse it.
- Relevance for operations: none for capacity, sizing or alerting. Do not size, alert or report on it.
- Troubleshooting use: a value below the VM's configured memory. Alone it is not a fault: on a host without memory pressure it follows the VM's estimated demand, and a lab VM at rest showed a value below its configured memory with nothing reclaimed. Read it with Ballooned, Swapped, Compressed and Latency.
- It does not follow a reservation: setting and removing a reservation left it where it was ([VM memory metrics compared](../comparisons/vm-memory-metrics.md), section VM reservation across counters).

## Misconceptions
- "Entitlement is what the VM uses" → it is a scheduler value.
- "Entitlement rises to the VM's reservation" → it stayed below a reservation that was above Consumed on the lab VM.
- "Entitlement = Granted + Overhead" → the API gives no formula; the scheduler computes it from demand and the resource policies.
- "Entitlement below configured memory means the VM is short of memory" → only with reclamation or Latency beside it; at rest it can sit below configured memory with no pressure.

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
