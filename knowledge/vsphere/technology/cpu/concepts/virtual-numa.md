# Virtual NUMA (vNUMA)

## Definition
- vNUMA exposes the NUMA topology of the host to the guest OS.
- A NUMA-aware guest OS and applications can use the hardware NUMA architecture more efficiently.
- Benefit: can be significant for wide VMs. See [`vsphere/technology/cpu/concepts/numa`](numa.md).
- Size of the benefit depends on how far the guest OS and applications are NUMA-optimized.

## Requirements and defaults
- Requires virtual hardware version 8 or later.
- Default: vNUMA is active only for VMs with more than 8 vCPUs.
- Older releases set vNUMA with VMX options: `numa.vcpu.min` (activate it for a smaller VM), `numa.vcpu.maxPerVirtualNode` (vCPUs per virtual node).
- vSphere 9.1, virtual hardware version 20 and later: set a manual layout in Edit Settings > Virtual Hardware > CPU, menu vNUMA Topology. Do not add `numa.*` attributes in the VM's Advanced Parameters: they are no longer offered there or supported for this use.

## Topology initialization
- The vNUMA topology is built at power-on from the NUMA topology of the host the VM starts on, and from the VM's vCPU count and memory.
- vSphere 9.1, virtual hardware version 20 and later: ESXi rebuilds the topology at every power cycle, so it matches the host the VM powers on. A change of the vCPU count also rebuilds it.
- Older behaviour: the topology was calculated at the first power-on and then kept (`numa.autosize.once` TRUE). That avoided a guest topology change at reboot, but a VM later moved to a host with a different NUMA layout kept a layout that no longer fit.
- To keep the old behaviour in 9.1 (the same topology across reboots, so the guest OS sees no change): the vCenter cluster advanced setting `VPXD_PersistVnuma` = True (Cluster > Configure > Advanced Settings), not a per-VM VMX option.
- vMotion does not rebuild the topology: the guest cannot take a NUMA change while it runs. A VM first powered on a host with large NUMA nodes keeps that layout after a move to a host with smaller nodes: ESXi spreads it over two physical nodes while the guest keeps placing threads and memory for one. The next power cycle on the smaller host rebuilds the layout for that host (unless `VPXD_PersistVnuma` is set).
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
- Size wide VMs to fit within one physical NUMA node where possible. A VM that fits one node is presented to the guest as one node, a uniform (UMA) machine, even when it spans two L3 domains: for example 64 vCPUs in a 128-core node ([`sp5-framework/capacity/vm-size`](../../../../sp5-framework/capacity/vm-size.md), Example: AMD EPYC 9996 in NPS2).
- Memory must split evenly across the VM's virtual nodes, so configure it as a multiple of the number of virtual nodes. A VM spread over every node of an NPS4 host (4 nodes per socket) takes memory divisible by 4; over SNC3, by 3; over NPS2, by 2. An uneven split gives the guest unequal nodes and uneven memory latency.
- Memory per node: keep the VM's memory within the memory of the nodes it uses. A VM in one NPS2 node of an AMD EPYC 9996 has at most half of the socket's memory as local memory; above that ESXi fetches the rest from the other IOD's node.
- Example from the source: a host with six cores per NUMA node suits VMs of no more than six vCPUs.
- If a VM must be larger than one node, size it to split evenly across as few physical NUMA nodes as possible.
- A VM vCPU count above the physical core count uses hyper-threads. This can create contention. See [`vsphere/technology/cpu/concepts/hyper-threading`](hyper-threading.md).

## CPU Hot Add
- Adding vCPUs with CPU Hot Add deactivates vNUMA for that VM.
- The guest then sees one vNUMA node.
- See [`vsphere/technology/cpu/concepts/idle-and-unused-vcpus`](idle-and-unused-vcpus.md).

## Misconceptions
- "vMotion rebuilds the vNUMA layout for the new host" → it does not. The layout stays through the move; the next power cycle on the new host rebuilds it.
- "The vNUMA layout is fixed at the first power-on" → in vSphere 9.1 (virtual hardware 20 and later) it is rebuilt at every power cycle, unless the cluster setting `VPXD_PersistVnuma` keeps it.
- "Set `numa.autosize.once` or other `numa.*` options in the VM's advanced parameters" → in 9.1 use the vNUMA Topology menu in Edit Settings > CPU; to keep a layout across reboots, use the cluster setting `VPXD_PersistVnuma`.
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
  document: Knowledge base (vSphere NUMA Architecture and Sizing Guide, vSphere 9.1); Performance Best Practices for VMware vSphere 9.1 (revision 20260624); vSphere 9.1 Resource Management, Virtual NUMA Controls and Using Virtual NUMA (Broadcom TechDocs, last updated 2026-11-09)
  path: Guest Operating System CPU Considerations > Virtual NUMA (vNUMA) (p. 57); Using NUMA Systems with ESXi > Virtual NUMA Controls (option numa.autosize.once)
corrections: []
review_notes:
- 'To check: Section ''Topology initialization'': the 9.1 Virtual NUMA Controls page (last updated 2026-11-09) still lists numa.autosize.once (default FALSE in its table, TRUE in its text) and does not name VPXD_PersistVnuma or the vNUMA Topology menu; the file follows the knowledge base (Q192). Check the cluster setting name against a vCenter 9.1 instance or a KB. URL: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-1/vsphere-resource-management/using-numa-systems-with-esxi/virtual-numa-controls.html'
- 'Source URL for the vCPU count sentence: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-1/vsphere-resource-management/using-numa-systems-with-esxi/using-virtual-numa.html'
- Checked against 9.1 (revision 20260624). Page 57 unchanged. Page reference updated.
- 'Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-9-1-performance-best-practices'
- 'To check: KB 81383, the ''Virtual Machine vCPU and vNUMA Rightsizing'' blog and the Virtual Machine Compute Optimizer tool, referenced by the source; not read.'
status: draft
```
