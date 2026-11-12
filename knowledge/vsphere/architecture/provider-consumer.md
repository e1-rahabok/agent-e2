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
- kind: sum-of-consumers metric: the sum over the VMs of what they would use with no contention, an internal metric of the CPU scheduler.
- Not the sum of all VM worlds + VMkernel worlds: kernel work is in Usage, not in Demand. A host with no VMs shows Demand flat at 0 while Usage is not 0.

## CPU Ready on ESXi
- A VM is a consumer. Multiple VMs can share the same physical core, at a performance cost.
- Ready measures a consumer waiting to be scheduled.
- A physical core or thread is always ready. Ready does not apply to ESXi.
- src: Complexity > Architecture Complexity

## ESXi vs VMs plus kernel
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

## Misconceptions
- "ESXi CPU Ready is high, so the host waits for CPU" → Ready measures a consumer waiting to be scheduled; a physical core or thread is always ready. A Ready value on ESXi is an aggregate of its VMs: read the VMs, starting with the worst.
- "ESXi CPU Demand = VM usage + kernel usage" → wrong. It is VM demand only; kernel work is in Usage. See [`vsphere/technology/cpu/metrics/host/demand`](../technology/cpu/metrics/host/demand.md).

## Metadata
```yaml
id: vsphere/architecture/provider-consumer
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
- vsphere/architecture/metric-sources
- vsphere/architecture/object-relationships
- vsphere/architecture/vm-vs-guest-os
- vsphere/technology/cpu/metrics/comparisons/consumption-metrics
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: The World of Metrics > Metrics Nuances > Virtualization Impact
corrections:
- 'Section ''ESXi CPU Demand'': sum of VM demand, kernel not included; a host with no VMs shows 0 (Part 1). Replaces the 2026-11-02 reading as a provider metric.'
review_notes: []
status: draft
```
