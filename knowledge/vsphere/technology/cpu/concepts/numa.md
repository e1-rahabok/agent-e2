# NUMA on ESXi

## Activation
- ESX NUMA scheduling and memory placement are active by default only on systems with:
  - at least 4 total CPU cores,
  - at least 2 CPU cores per NUMA node.
- BIOS node interleaving:
  - interleaving deactivated: ESX detects the system as NUMA and applies NUMA optimizations,
  - interleaving activated: ESX does not detect the system as NUMA.
- Recommendation: in most cases, deactivate node interleaving. This leaves NUMA active. The source gives this as the best-performance setting (p. 21).

## VM categories
| Category | vCPU placement | Memory placement | Memory access |
|---|---|---|---|
| VM with vCPUs ≤ cores per physical NUMA node | All vCPUs in one NUMA node | Preferentially local to that node | All accesses local. Lowest memory access latency. |
| "Wide" VM: vCPUs > cores per physical NUMA node | Two or more NUMA nodes | Preferentially local to those nodes | Some vCPUs may access remote memory. Higher average memory access latency. |

- A VM with no more vCPUs than cores per NUMA node can have a slight performance advantage.
- Wide VM latency increase can be reduced with vNUMA. See [`vsphere/technology/cpu/concepts/virtual-numa`](virtual-numa.md).

## Scheduler mechanics
- Each VM gets a home node at power-on, chosen to balance CPU and memory load across nodes. Its vCPUs run only on that node; new memory comes from that node.
- Wide VMs are split into NUMA clients, each managed as a normal single-node client. ESXi measures inter-node latency at boot and places a wide VM's clients on nodes close to each other.
- Every 2 seconds (default) the rebalancer checks node loads. It can move a VM to a less loaded node, preferring a VM that already has memory there, or swap VMs between nodes to improve locality.
- After a move, ESXi migrates the VM's memory to the new home node page by page (4 KB), at a controlled rate. Memory is not moved if the VM stays only briefly.
- Until migration completes, the VM runs with remote memory: esxtop N%L below 100%, NRMEM above 0. NMIG counts the moves. See [`vsphere/tools/esxtop/memory`](../../../tools/esxtop/memory.md).
- After a large workload change (many VMs started) placement settles within seconds to minutes.
- Page sharing is per node: each node keeps its own copy of a shared page, so shared pages never force remote access.
- A VM with manual CPU affinity or memory affinity is no longer managed by the NUMA scheduler: no rebalancing, no memory migration. NUMA node affinity (numa.nodeAffinity) keeps NUMA management but limits the nodes.
- Memory affinity without CPU affinity breaks automatic rebalancing.

## Virtual topology (ESXi 8.0 and later)
- ESXi 8.0 enhanced virtual topology:
  - selects optimal coresPerSocket values for VMs,
  - selects optimal virtual L3 sizes,
  - exposes NUMA for virtual devices, and vNUMA topology, when CPU hot plug is enabled.

## Hardware locality (9.1 p. 30)
- NICs, NVMe drives and GPUs are usually associated with a specific NUMA node.
- To reduce data traffic across NUMA boundaries:
  - distribute devices across NUMA nodes,
  - place workloads on the NUMA node local to the devices they use.
- Find device locality:
  - Linux: `lspci -v`, look for the NUMA node output,
  - Windows Server, PowerShell: `Get-NetAdapterRss -Name <AdapterName>`, shows the closest NUMA node.

## Settings
- NUMA controls, sizing, snoop modes and processor-specific settings: see [`vsphere/technology/cpu/configuration/numa-settings`](../configuration/numa-settings.md).

## Misconceptions
- "A VM with more vCPUs than cores per node is as fast as one that fits" → wide VMs can access remote memory and have higher average memory latency.

## Metadata
```yaml
id: vsphere/technology/cpu/concepts/numa
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
- HostSystem
- VirtualMachine
- ClusterComputeResource
internal_derive: []
related:
- vsphere/technology/cpu/concepts/virtual-numa
- vsphere/technology/cpu/concepts/hyper-threading
- vsphere/technology/cpu/concepts/idle-and-unused-vcpus
- vsphere/technology/cpu/concepts/cpu-topology
source:
  document: Performance Best Practices for VMware vSphere 9.1 (revision 20260624)
  path: ESX CPU Considerations > Non-Uniform Memory Access (NUMA) (pp. 29-30); Hardware BIOS Settings > General BIOS Settings (p. 21)
corrections: []
review_notes:
- 'Section ''Scheduler mechanics'': from the vSphere 9.1 documentation, vSphere Resource Management > How ESX NUMA Scheduling Works, Home Nodes and Initial Placement, Dynamic Load Balancing and Page Migration, Transparent Page Sharing Optimized for NUMA, Specifying NUMA Controls (pp. 1936-1942).'
- 'To check: Section ''Scheduler mechanics'': the esxtop counter mapping; not in the documentation.'
- Checked against 9.1 (revision 20260624). Snoop mode list removed in 9.1 (p. 30). Hardware locality and Intel Granite Rapids guidance added (p. 30).
- 'Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-9-1-performance-best-practices'
- 'To check: the ''Using NUMA Systems with ESX'' section of the vSphere Resource Management guide, referenced by the source; not read.'
status: draft
```
