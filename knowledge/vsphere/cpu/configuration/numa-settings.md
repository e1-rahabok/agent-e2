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
- Example from the source (p. 55): six cores per NUMA node means a VM of six vCPUs or fewer fits one node.
- vCPU counts above the physical core count use hyper-threads. See `vsphere/cpu/concepts/hyper-threading`.

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

## Intel Granite Rapids (9.1 p. 30)
- Size VMs to align with NUMA node and SNC domain boundaries.
- Design workloads to maximize NUMA locality. Consider vCPU placement, memory allocation, and NUMA node and SNC domain boundaries.
- Reduce unnecessary VM movement to stabilize NUMA locality: set the NUMA migration threshold to 50 or greater, `numa.migThreshold = XX`.
- The source names these workloads as especially relevant: in-memory databases, HPC, low-latency and real-time services, and high I/O applications.

## AMD EPYC
- NUMA Nodes per Socket (NPS). Not all EPYC processors offer all values:
  - NPS-1: each CPU is one NUMA node,
  - NPS-2: each CPU is two NUMA nodes,
  - NPS-4: each CPU is four NUMA nodes.
- CCX as NUMA Domain:
  - activated: each Core Cache Complex (CCX) is a NUMA domain,
  - deactivated: CPUs are presented as set by NPS.
- The CCX setting does not change the memory channel interleave policy. NPS controls that.
- From vSphere 7.0 Update 2, the defaults are NPS-1 with CCX as NUMA Domain deactivated. The source says these give the best performance in nearly all cases.
- NPS-4 may be worth testing only when all four apply:
  - very high memory bandwidth is required,
  - the lowest possible memory latency is required,
  - the workload is highly NUMA-optimized,
  - the VMs can be pinned or affinitized.

## Traps
- "NUMA settings are always better tuned manually" → the source says the default ESX NUMA scheduling is intelligent and adaptive. Manual controls are for specific cases.

## Metadata
```yaml
id: vsphere/cpu/configuration/numa-settings
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
- vsphere/cpu/concepts/numa
- vsphere/cpu/concepts/virtual-numa
- vsphere/system/configuration/bios-settings
source:
  document: Performance Best Practices for VMware vSphere 9.1 (revision 20260624)
  path: ESX CPU Considerations > Non-Uniform Memory Access (NUMA) (pp. 29-30); Hardware BIOS Settings > General BIOS Settings (p. 21)
corrections: []
review_notes:
- Checked against 9.1 (revision 20260624). Snoop mode list removed in 9.1 (p. 30). Hardware locality and Intel Granite Rapids guidance added (p. 30).
- 'Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-9-1-performance-best-practices'
- Source refers to the 'Using NUMA Systems with ESX' section of the vSphere Resource Management guide. Not read.
status: draft
```
