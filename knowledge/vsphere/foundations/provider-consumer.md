# Provider vs consumer

## Definition
- Virtualization splits the IT stack into provider and consumer.
- Provider example: ESXi. Consumer example: VM.
- vSphere counters are more complex than physical machine counters: more components, plus inconsistencies caused by virtualization.
- When virtualized, CPU, memory, disk and network each behave differently than on a physical machine.

## Two kinds of provider metric
| Kind | Meaning | Example |
|---|---|---|
| provider metric | Exists only at the provider. No consumer equivalent. | Physical network in ESXi. |
| sum-of-consumers metric | Aggregates the consumers' metric. | Sum of VM network in ESXi. |

- The metric name does not say which kind it is.

## ESXi CPU Demand
- kind: provider metric.
- Not the sum of all VM worlds + VMkernel worlds.
- It is an internal metric of the CPU scheduler: the ideal total demand had there been no contention at all.
- trap: "Demand comes from consumers, so ESXi CPU Demand must be a sum of consumer demand" → wrong.

## CPU Ready does not apply to ESXi
- A VM is a consumer. Multiple VMs can share the same physical core, at a performance cost.
- Ready measures a consumer waiting to be scheduled.
- A physical core or thread is always ready. Ready does not apply to ESXi.
- src: Complexity > Architecture Complexity

## ESXi ≠ VMs + kernel
- ESXi metrics are more complex than the sum of its VMs plus the kernel.
- src: Complexity > Architecture Complexity

## Three layers
- Adding a virtualization layer changes the layers directly above and below it.
- Interpreting VM metrics therefore requires three layers: Guest OS, virtualization (ESXi), physical.
- Containers and Kubernetes add a layer with a less strict boundary. Resource-pool-style troubleshooting problems then apply at process granularity. More knowledge is required, not less.

## VMkernel kernel space vs user space
- VMkernel is an operating system. It has kernel space and user space.
- Some counters include both. Others include only one.

## Tools not built for vSphere
- Monitoring tools not purpose-built for vSphere often understand its characteristics only partially.
- Partial understanding → wrong interpretation → wrong action.

## Provider metric types
- Provider metric: exists only at the provider. Example: ESXi physical network (vmnic).
- Sum of consumer metric: the provider aggregates its consumers. Example: sum of VM network at ESXi; ESXi CPU Demand.
- Before reading a provider value, decide which kind it is. A sum of consumers says nothing about provider-only work (kernel, vSAN, NSX).

## Metadata
```yaml
id: vsphere/foundations/provider-consumer
retriever_guide: how-it-works
scope: vsphere
technology:
- cpu
- memory
- storage
- network
pillar:
- performance
- capacity
product:
- vsphere
object:
- VirtualMachine
- HostSystem
internal_derive: []
related:
- vsphere/foundations/metric-sources
- vsphere/foundations/object-relationships
- vsphere/foundations/vm-vs-guest-os
- vsphere/cpu/metrics/comparisons/consumption-metrics
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Virtualization Impact
corrections:
- '2026-11-02: ESXi CPU Demand is a provider metric. Not answered in uploaded document.'
review_notes:
- "Section 'Provider metric types': author (2026-11-03), Q009."
status: draft
```
