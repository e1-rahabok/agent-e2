# NUMA on ESXi

## Activation
- ESX NUMA scheduling and memory placement are active by default only on systems with:
  - at least 4 total CPU cores,
  - at least 2 CPU cores per NUMA node.
- BIOS node interleaving:
  - interleaving deactivated: ESX detects the system as NUMA and applies NUMA optimizations,
  - interleaving activated: ESX does not detect the system as NUMA.
- Recommendation: in most cases, deactivate node interleaving. This leaves NUMA active. Performance Best Practices for vSphere 9.1 gives this as the best-performance setting (p. 21).

## VM categories
| Category | vCPU placement | Memory placement | Memory access |
|---|---|---|---|
| VM with vCPUs ≤ cores per physical NUMA node | All vCPUs in one NUMA node | Preferentially local to that node | All accesses local. Lowest memory access latency. |
| "Wide" VM: vCPUs > cores per physical NUMA node | Two or more NUMA nodes | Preferentially local to those nodes | Some vCPUs may access remote memory. Higher average memory access latency. |

- vCPUs fit one node, memory does not: the VM stays one NUMA client with one home node, and new memory comes from that node until the node's memory is used; the rest lands on another node. That remote memory is steady: no rebalancing makes it local, because the home node cannot hold it. Typical cause: memory raised past one node's capacity. Fix by sizing the memory to fit one node, from what the guest needs, or by splitting the VM into NUMA clients that each fit a node ([`vsphere/technology/cpu/configuration/numa-settings`](../configuration/numa-settings.md)).
- A VM with no more vCPUs than cores per NUMA node can have a slight performance advantage.
- Wide VM latency increase can be reduced with vNUMA. See [`vsphere/technology/cpu/concepts/virtual-numa`](virtual-numa.md).

## Scheduler mechanics
- Each VM gets a home node at power-on, chosen to balance CPU and memory load across nodes. Its vCPUs run only on that node; new memory comes from that node.
- Wide VMs are split into NUMA clients, each managed as a normal single-node client. ESXi measures inter-node latency at boot and places a wide VM's clients on nodes close to each other.
- Every 2 seconds (default) the rebalancer checks node loads. It can move a VM to a less loaded node, preferring a VM that already has memory there, or swap VMs between nodes to improve locality.
- After a move, ESXi migrates the VM's memory to the new home node page by page (4 KB), at a controlled rate. Memory is not moved if the VM stays only briefly.
- Until migration completes, the VM runs with remote memory: esxtop N%L (current percentage of the VM's memory that is local) below 100%, NRMEM (current remote memory) above 0, NHN the current home node (vSphere 9.1 documentation, esxtop memory panel, p. 2157). NMIG counts the moves. See [`vsphere/tools/esxtop/memory`](../../../tools/esxtop/memory.md).
- After a large workload change (many VMs started) placement settles within seconds to minutes.
- Page sharing is per node: each node keeps its own copy of a shared page, so shared pages never force remote access.
- A VM with manual CPU affinity or memory affinity is no longer managed by the NUMA scheduler: no rebalancing, no memory migration. NUMA node affinity (numa.nodeAffinity) keeps NUMA management but limits the nodes.
- Memory affinity without CPU affinity breaks automatic rebalancing.
- Action affinity: the scheduler places NUMA clients that communicate often on one node. That usually helps, but can overload some nodes while others idle, so VMs on the busy nodes show higher Ready and some VMs move back and forth. Setting the host advanced option /Numa/LocalityWeightActionAffinity to 0 turns it off; vMotion or power-cycle the VMs so placement is redone (Broadcom KB 314059, ESXi 7.x and 8.x).

## Virtual topology (ESXi 8.0 and later)
- ESXi 8.0 enhanced virtual topology:
  - selects optimal coresPerSocket values for VMs,
  - selects optimal virtual L3 sizes,
  - can expose NUMA for virtual devices, and a vNUMA topology, on a VM with CPU hot plug enabled.
- The enhanced virtual topology needs virtual hardware version 20 or later. On older virtual hardware, CPU Hot Add still gives the guest one NUMA node.
- Even on virtual hardware 20 and later, a VM with CPU hot plug gets one NUMA node by default; a vNUMA layout with hot plug needs a manual NUMA configuration ([`vsphere/technology/cpu/concepts/virtual-numa`](virtual-numa.md), section CPU Hot Add).

## Hardware locality (ESXi 9.1)
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
- "Remote memory means the VM is wide, or ESXi keeps moving it between nodes" → a VM with one home node whose memory exceeds the node has steady remote memory. Steady NRMEM over samples is placement, not migration.
- "Pin the VM to its node with CPU and memory affinity to make memory local" → affinity takes the VM out of NUMA management (no rebalancing, no memory migration) and cannot make memory larger than the node local.

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
  document: Performance Best Practices for VMware vSphere 9.1 (revision 20260624); VMware vSphere 9.1 product documentation (PDF built 2026-11-02; the copyright page carries no revision number); Broadcom KB 314059
  path: 'ESX CPU Considerations > Non-Uniform Memory Access (NUMA) (pp. 29-30); Hardware BIOS Settings > General BIOS Settings (p. 21). vSphere 9.1, vSphere Resource Management > Using NUMA Systems with ESX: How ESX NUMA Scheduling Works, Home Nodes and Initial Placement, Dynamic Load Balancing and Page Migration, Transparent Page Sharing Optimized for NUMA, Specifying NUMA Controls (pp. 1936-1942); Virtual Topology in ESX (pp. 1939-1940), hardware version 20 or later; by default a VM with CPU hotplug enforces a single NUMA node; vSphere Monitoring and Performance > resxtop and esxtop > Memory Panel, NHN, NRMEM, N%L (p. 2157). KB 314059 (NUMA nodes are heavily load imbalanced causing high contention for some virtual machines)'
corrections: []
review_notes:
- 'To check: Section ''Scheduler mechanics'': the esxtop field NMIG (count of NUMA migrations); not in the vSphere 9.1 documentation esxtop memory panel (p. 2157).'
- 'To check: Section ''VM categories'': a VM whose vCPUs fit one node but whose memory exceeds it stays one NUMA client with steady remote memory; vSphere 9.1 Home Nodes and Initial Placement (p. 1938) says only that new memory comes from the home node. Needs a lab test on a 9.1 host (esxtop N%L, NRMEM).'
status: draft
```
