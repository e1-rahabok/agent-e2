# Virtual NUMA (vNUMA)

## Definition
- vNUMA exposes the NUMA topology of the host to the guest OS.
- A NUMA-aware guest OS and applications can use the hardware NUMA architecture more efficiently.
- Benefit: can be significant for wide VMs. See [`vsphere/technology/cpu/concepts/numa`](numa.md).
- Size of the benefit depends on how far the guest OS and applications are NUMA-optimized.

## Requirements and defaults
- Requires virtual hardware version 8 or later.
- Default: vNUMA is active only for VMs with more than 8 vCPUs.
- Activate for a smaller VM: add `numa.vcpu.min = X` to the VMX file, where X is the vCPU count of the VM.
- Full manual control: the `maxPerVirtualNode` option.

## Topology initialization
- The vNUMA topology is set at first power-on. It is based partly on the NUMA topology of the host.
- The topology does not change unless the VM vCPU count changes.
- If a vNUMA VM moves to a host with a different NUMA topology, its vNUMA topology may no longer suit the host.
- The result can be reduced performance.
- Best results: clusters made entirely of hosts with matching NUMA architecture.

## corespersocket
- From vSphere 6.5, changing corespersocket no longer changes the vNUMA topology.
- corespersocket only changes how vCPUs are presented to the guest OS. This can matter for software licensing.
- vNUMA determines its topology from the underlying ESX host.
- Example from the source:
  - host: dual socket, 16 cores per socket,
  - VM: four sockets, four cores per socket (16 vCPUs), corespersocket = 4.
  - Before vSphere 6.5: vNUMA created four NUMA nodes.
  - From vSphere 6.5: vNUMA creates one 16-vCPU node, because the VM fits in one physical NUMA node. The guest still sees four sockets with four cores each.
- Revert to the older behaviour: `numa.vcpu.followcorespersocket`.
- Some corespersocket values still give sub-optimal guest topologies, and can reduce performance.

## Sizing
- Size wide VMs to fit within one physical NUMA node where possible.
- Example from the source: a host with six cores per NUMA node suits VMs of no more than six vCPUs.
- If a VM must be larger than one node, size it to split evenly across as few physical NUMA nodes as possible.
- A VM vCPU count above the physical core count uses hyper-threads. This can create contention. See [`vsphere/technology/cpu/concepts/hyper-threading`](hyper-threading.md).

## CPU Hot Add
- Adding vCPUs with CPU Hot Add deactivates vNUMA for that VM.
- The guest then sees one vNUMA node.
- See [`vsphere/technology/cpu/concepts/idle-and-unused-vcpus`](idle-and-unused-vcpus.md).

## Misconceptions
- "corespersocket sets the NUMA layout" → from vSphere 6.5 it does not. It sets the guest socket presentation.
- "vNUMA is on for every VM" → by default it is on only for VMs with more than 8 vCPUs.

## Metadata
```yaml
id: vsphere/technology/cpu/concepts/virtual-numa
retriever_guide: how-it-works
scope: vsphere
technology:
- cpu
- memory
pillar:
- performance
product:
- vsphere
object:
- VirtualMachine
internal_derive: []
related:
- vsphere/technology/cpu/concepts/numa
- vsphere/technology/cpu/concepts/idle-and-unused-vcpus
source:
  document: Performance Best Practices for VMware vSphere 9.1 (revision 20260624)
  path: Guest Operating System CPU Considerations > Virtual NUMA (vNUMA) (p. 57)
corrections: []
review_notes:
- Checked against 9.1 (revision 20260624). Page 57 unchanged. Page reference updated.
- 'Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-9-1-performance-best-practices'
- 'To check: KB 81383, the ''Virtual Machine vCPU and vNUMA Rightsizing'' blog and the Virtual Machine Compute Optimizer tool, referenced by the source; not read.'
status: draft
```
