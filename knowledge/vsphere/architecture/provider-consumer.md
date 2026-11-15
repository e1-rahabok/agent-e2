# Provider vs consumer

## Definition
- Virtualization splits the IT stack into provider and consumer.
- Provider example: ESXi. Consumer example: VM.
- vSphere counters are more complex than physical machine counters: more components, plus inconsistencies caused by virtualization.
- When virtualized, CPU, memory, disk and network each behave differently than on a physical machine.

## Two kinds of provider metric
| Kind | Meaning | Example |
|---|---|---|
| provider metric | Exists only at the provider. No consumer equivalent. | ESXi physical network (vmnic). |
| sum-of-consumers metric | Aggregates the consumers' metric. | Sum of VM network at ESXi; ESXi CPU Demand. |

- The metric name does not say which kind it is.
- Before reading a provider value, decide which kind it is. A sum of consumers says nothing about provider-only work (kernel, vSAN, NSX).

## ESXi CPU Demand
- A sum-of-consumers metric: the demand of the VMs, an internal metric of the CPU scheduler. Kernel work is in Usage, not in Demand. The vSphere API 9.1 defines `cpu.demand` on the host with the same VM-centric text as on the VM: the CPU a virtual machine would use with no contention and no limit.
- vCenter and VCF Operations compute it differently: a host with no VMs reads 0 in vCenter and the kernel's CPU reservation in VCF Operations. Formulas and examples: [`vsphere/technology/cpu/metrics/host/demand`](../technology/cpu/metrics/host/demand.md), section vCenter vs VCF Operations.

## CPU Ready on ESXi
- A VM is a consumer. Multiple VMs can share the same physical core, at a performance cost.
- Ready measures a consumer waiting to be scheduled.
- A physical core or thread is always ready. Ready does not apply to ESXi as a provider: the ESXi Ready counter (`cpu.ready` on the host) sums its VMs.

## ESXi vs VMs plus kernel
- ESXi metrics are more complex than the sum of its VMs plus the kernel: some counters are provider metrics, some sums of consumers, and the name does not say which.

## Three layers
- Adding a virtualization layer changes the layers directly above and below it.
- Interpreting VM metrics therefore requires three layers: Guest OS, virtualization (ESXi), physical.
- Containers and Kubernetes add a layer with a less strict boundary. Resource-pool-style troubleshooting problems then apply at process granularity. More knowledge is required, not less.

## VMkernel kernel space vs user space
- VMkernel is an operating system. It has kernel space and user space ([`vsphere/architecture/kernel-worlds`](kernel-worlds.md)).
- Some counters include both. Others include only one.

## Tools not built for vSphere
- Monitoring tools not purpose-built for vSphere often understand its characteristics only partially.
- Partial understanding leads to a wrong interpretation, and a wrong interpretation to a wrong action.

## Misconceptions
- "ESXi CPU Ready is high, so the host waits for CPU" → Ready measures a consumer waiting to be scheduled; a physical core or thread is always ready. A Ready value on ESXi is an aggregate of its VMs: read the VMs, starting with the worst.
- "The host's vmnic throughput equals the sum of its VMs' network" → vmnic throughput is a provider metric: it also carries VMkernel traffic (vMotion, vSAN, management, IP storage), which no VM counter holds. Decide the kind of the provider metric before comparing it with a sum of consumers.

## Metadata
```yaml
id: vsphere/architecture/provider-consumer
retriever_guide: how-it-works
up_front: 'ESXi CPU Ready is high, so the host waits for CPU'
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
internal_derive:
- vsphere/technology/cpu/metrics/host/demand
related:
- vsphere/architecture/kernel-worlds
- vsphere/architecture/metric-sources
- vsphere/architecture/object-relationships
- vsphere/architecture/vm-vs-guest-os
- vsphere/technology/cpu/metrics/comparisons/consumption-metrics
source:
  document: Knowledge base; vSphere Web Services API 9.1 reference, CPU counters (cpu.demand)
  path: The World of Metrics > Metrics Nuances > Virtualization Impact; Complexity > Architecture Complexity
corrections: []
review_notes: []
status: draft
```
