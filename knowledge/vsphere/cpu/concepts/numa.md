---
id: vsphere/cpu/concepts/numa
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
- vsphere/cpu/concepts/virtual-numa
- vsphere/cpu/concepts/hyper-threading
- vsphere/cpu/concepts/idle-and-unused-vcpus
- vsphere/cpu/concepts/cpu-topology
source:
  document: Performance Best Practices for VMware vSphere 9.1 (revision 20260624)
  path: ESX CPU Considerations > Non-Uniform Memory Access (NUMA) (pp. 29-30); Hardware BIOS Settings > General BIOS Settings (p. 21)
corrections: []
review_notes:
- Checked against 9.1 (revision 20260624). Snoop mode list removed in 9.1 (p. 30). Hardware locality and Intel Granite Rapids guidance added (p. 30).
- 'Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-9-1-performance-best-practices'
- Source refers to the 'Using NUMA Systems with ESX' section of the vSphere Resource Management guide. Not read.
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
- Wide VM latency increase can be reduced with vNUMA. See `vsphere/cpu/concepts/virtual-numa`.

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
- NUMA controls, sizing, snoop modes and processor-specific settings: see `vsphere/cpu/configuration/numa-settings`.

## Traps
- "A VM with more vCPUs than cores per node is as fast as one that fits" → wide VMs can access remote memory and have higher average memory latency.
