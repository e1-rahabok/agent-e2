---
id: vsphere/cpu/architecture/numa
type: concept
scope: vsphere
resources: [cpu, memory]
objects: [esxi, vm, cluster]
related:
  - vsphere/cpu/architecture/virtual-numa
  - vsphere/cpu/architecture/hyper-threading
  - vsphere/cpu/architecture/idle-and-unused-vcpus
source:
  document: Performance Best Practices for VMware vSphere 9.0 (revision 20250731)
  path: ESX CPU Considerations > Non-Uniform Memory Access (NUMA) (pp. 27-28); Hardware BIOS Settings > General BIOS Settings (p. 21)
corrections: []
review_notes:
  - "Superseded: vSphere 9.1 (revision 20260624) exists. This file was written from the 9.0 document (revision 20250731). Re-check against 9.1 before review."
  - "Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-90-performance-best-practices"
  - "Source refers to the 'Using NUMA Systems with ESX' section of the vSphere Resource Management guide. Not read."
status: draft
---

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
- Wide VM latency increase can be reduced with vNUMA. See `vsphere/cpu/architecture/virtual-numa`.

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
- vCPU counts above the physical core count use hyper-threads. See `vsphere/cpu/architecture/hyper-threading`.

## Virtual topology (ESXi 8.0 and later)
- ESXi 8.0 enhanced virtual topology:
  - selects optimal coresPerSocket values for VMs,
  - selects optimal virtual L3 sizes,
  - exposes NUMA for virtual devices, and vNUMA topology, when CPU hot plug is enabled.

## Snoop modes
- Five snoop modes exist. Not all modes are available on all processors:
  - Early Snoop (ES),
  - Home Snoop (HS),
  - Home snoop with Directory and Opportunistic Snoop Broadcast (HS with DIS + OSB),
  - Cluster-on-Die (COD),
  - Sub-NUMA Cluster (SNC).
- COD partitions a processor at boot into one or more NUMA nodes.
- SNC is similar to COD. It differs in how it uses the last-level cache.
- The best mode depends on the workload and the hardware.
- Follow the server manufacturer's guidance.

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
- "A VM with more vCPUs than cores per node is as fast as one that fits" → wide VMs can access remote memory and have higher average memory latency.
- "NUMA settings are always better tuned manually" → the source says the default ESX NUMA scheduling is intelligent and adaptive. Manual controls are for specific cases.
