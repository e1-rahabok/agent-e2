# NUMA settings

## Controls
| Control | Scope | Effect |
|---|---|---|
| `maxPerMachineNode` | VM | Limits vCPUs placed per NUMA node. Splits a VM that would fit in one node across nodes. |
| `numa.vcpu.preferHT` | VM | On hyper-threaded systems, a VM with vCPUs > cores per node and < logical processors per node uses logical processors with local memory, instead of full cores with remote memory. |
| `numa.nodeAffinity` | VM | Manual NUMA placement. Overrides the default behaviour. |

- `maxPerMachineNode` use case: some memory-bandwidth-bottlenecked workloads gain aggregate memory bandwidth when a VM is split across NUMA nodes.
- `maxPerMachineNode` impacts vNUMA. Consider vNUMA when setting it.

## Sizing guidance
- Size a VM to stay within one physical NUMA node.
- If a VM must be larger than one node, size it to split evenly across as few nodes as possible.
- Example in Performance Best Practices for vSphere 9.1 (p. 57): six cores per NUMA node means a VM of six vCPUs or fewer fits one node.
- vCPU counts above the physical core count use hyper-threads. See [`vsphere/technology/cpu/concepts/hyper-threading`](../concepts/hyper-threading.md).

## Snoop modes
- 9.1 document (p. 30): no mode list. The best mode depends on the workload and the hardware.
- Follow the server manufacturer's guidance.
- 9.0 document (p. 28) listed five modes. Kept for reference. Verify before use:
  - Early Snoop (ES),
  - Home Snoop (HS),
  - Home snoop with Directory and Opportunistic Snoop Broadcast (HS with DIS + OSB),
  - Cluster-on-Die (COD),
  - Sub-NUMA Cluster (SNC).
- COD partitions a processor at boot into one or more NUMA nodes.
- SNC is similar to COD. It differs in how it uses the last-level cache.

## Intel Granite Rapids (ESXi 9.1)
- Size VMs to align with NUMA node and SNC domain boundaries.
- Design workloads to maximize NUMA locality. Consider vCPU placement, memory allocation, and NUMA node and SNC domain boundaries.
- Reduce unnecessary VM movement to stabilize NUMA locality: set the NUMA migration threshold to 50 or greater, `numa.migThreshold = XX`.
- Performance Best Practices for vSphere 9.1 names these workloads as especially relevant: in-memory databases, HPC, low-latency and real-time services, and high I/O applications.

## AMD EPYC
- NUMA Nodes per Socket (NPS) sets the memory channel interleave policy. Not all EPYC processors offer all values:
  - NPS-1: each CPU is one NUMA node; memory interleaves over every channel of the socket,
  - NPS-2: each CPU is two NUMA nodes,
  - NPS-4: each CPU is four NUMA nodes.
- CCX as NUMA Domain (LLC as NUMA Node in AMD documents):
  - activated: each Core Cache Complex (CCX) is a NUMA domain,
  - deactivated: CPUs are presented as set by NPS.
- The CCX setting does not change the memory channel interleave policy. NPS controls that.
- General-purpose cluster: NPS-1 with CCX as NUMA Domain deactivated, the BIOS defaults. Performance Best Practices for vSphere 9.1 says that from vSphere 7.0 Update 2 they give the best performance in nearly all cases; AMD's vSphere tuning guide for EPYC 9005 gives them for VMs of mixed or unknown sizes and for VMs above half the cores of a socket.
- NPS-1 keeps the socket one node with the bandwidth of all its channels, so a VM up to the cores of a socket fits one node and the NUMA scheduler balances VMs of any size.
- L3 locality needs no node per CCX: from vSphere 7.0 Update 2 the ESX CPU scheduler keeps the vCPUs of a VM within one CCX or CCD.
- CCX as NUMA Domain activated skews the scheduler's model of the memory architecture: Broadcom KB 432801 (ESX 8 and 9, all EPYC generations) says to deactivate it, because it can slow workloads such as VMmark and View Planner.
- NPS-4 may be worth testing only when all four apply (Performance Best Practices for vSphere 9.1):
  - very high memory bandwidth is required,
  - the lowest possible memory latency is required,
  - the workload is highly NUMA-optimized,
  - the VMs can be pinned or affinitized.
- AMD's EPYC 9005 guide also names NPS-4 with LLC as NUMA Node for a host whose VMs are all below a quarter of the cores of a socket. Broadcom KB 432801, the newer document, says to deactivate CCX as NUMA Domain, and the first larger VM on such a host spans nodes.
- AMD EPYC 9006 parts with two I/O dies (IODs) per socket, such as the 256-core EPYC 9996: NPS-1 interleaves memory over both IODs, so half the memory accesses of a vCPU cross the link between them; NPS-2 puts the node boundary on the IOD boundary (128 cores and 8 channels per node).
- No AMD or Broadcom document gives the ESX setting for EPYC 9006 yet; Performance Best Practices for vSphere 9.1 (revision 20260624) predates it. Keep NPS-1 on an EPYC 9006 cluster and test NPS-2 with its own workload before changing the BIOS.
- Dies and NUMA nodes by processor: [`vsphere/technology/cpu/concepts/cpu-topology`](../concepts/cpu-topology.md), section NUMA.

## Misconceptions
- "NUMA settings are always better tuned manually" → Performance Best Practices for vSphere 9.1 calls the ESX NUMA scheduling and memory placement intelligent and adaptive. Manual controls are for specific cases.
- "NPS-4 is the optimal setting for AMD EPYC 9005, because it matches the four quadrants of the socket" → EPYC 9005 has one central IOD; NPS-4 cuts each node to 3 of the 12 memory channels and a quarter of the cores, so a VM above a quarter of the socket spans nodes. Broadcom and AMD's vSphere tuning guide default a general-purpose cluster to NPS-1.
- "A monster VM runs better with NPS-4, because its memory is closer" → it spans several NPS-4 nodes; AMD's vSphere tuning guide names NPS-1 for VMs above half the cores of a socket.

## Metadata
```yaml
id: vsphere/technology/cpu/configuration/numa-settings
retriever_guide: what-to-set
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
- vsphere/technology/cpu/concepts/numa
- vsphere/technology/cpu/concepts/virtual-numa
- vsphere/object-types/esxi/configuration/bios-settings
source:
  document: Performance Best Practices for VMware vSphere 9.1 (revision 20260624); Tuning Guide for AMD EPYC 9005 Processors on vSphere (AMD PID 58474, v1.0, October 2024); Broadcom KB 432801, Guidance for AMD EPYC BIOS and NUMA Configuration on VMware ESXi
  path: 'Performance Best Practices: ESX CPU Considerations > Non-Uniform Memory Access (NUMA) (pp. 29-31; AMD EPYC Processor NUMA Settings, pp. 30-31); Hardware BIOS Settings > General BIOS Settings (p. 21); Guest Operating System CPU Considerations > Virtual NUMA (vNUMA) (p. 57). AMD 58474: 3.3.2.3 NUMA Configuration (pp. 6-7); Chapter 4 (p. 9)'
corrections: []
review_notes:
- 'Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-9-1-performance-best-practices'
- 'To check: the ''Using NUMA Systems with ESX'' section of the vSphere Resource Management guide, referenced by Performance Best Practices; not read.'
- 'To check: Section ''AMD EPYC'': a newer revision of AMD PID 58474 and an AMD vSphere tuning guide for EPYC 9006 (NPS setting under ESX, the two-IOD layout of the EPYC 9996), on the AMD Documentation Hub (https://docs.amd.com). On 2026-11-15 the amd.com URL of 58474 returned 404; v1.0 was read from a server vendor copy (https://www.xfusion.com/wp-content/uploads/2025/11/AMD-EPYC-9005-tg-vmware-vsphere.pdf).'
- 'Source URL, Broadcom KB 432801: https://knowledge.broadcom.com/external/article/432801/guidance-for-amd-epyc-bios-and-numa-conf.html'
status: draft
```
