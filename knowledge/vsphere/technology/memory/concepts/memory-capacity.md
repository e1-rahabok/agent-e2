# Memory capacity

## Nature
- Only space, no speed by default. Speed enters with memory tiering.
- Guest OS and VM are separate realms; neither is a perfect input.

| Metric | Allocation model | Demand model |
|---|---|---|
| Total capacity | Physical memory | Same |
| Hypervisor overhead | GB assigned manually | Kernel reservation, inside ESXi Memory Utilization |
| Consumption | Sum of running VM configured RAM | ESXi Memory Utilization |
| Performance | Not applicable | ESXi Swapped + Zipped + Guest OS Ballooned |

## Demand
- Three formulas share the word Demand for host memory. Each has one home; this file points to them.
- Capacity model of the method: Demand = Max (Utilization, Reservation), per VM, summed at the host, with the kernel counted by its reservation. Home: [`sp5-framework/capacity/demand`](../../../../sp5-framework/capacity/demand.md), section Demand.
- VCF Operations formula of the host: ESXi Memory Utilization = Machine Demand + ESX System Usage (the kernel reservation). Home: [`vsphere/technology/memory/metrics/host/utilization`](../metrics/host/utilization.md), section Formula. It applies the capacity model of the method, and the VCF Operations capacity pages show it as memory Demand.
- VCF Operations formula of the VM, the input of the host formula: VM Memory Utilization, from Guest OS Needed Memory, falling back to Consumed without guest data. Home: [`vsphere/technology/memory/metrics/virtual-motherboard/utilization`](../metrics/virtual-motherboard/utilization.md).
- The capacity counter of a host: ESXi Memory Utilization; ESXi Memory Consumed only on a host that runs with no ballooning by design. Home: [`vsphere/technology/memory/metrics/host/utilization`](../metrics/host/utilization.md), section Reason.
- Consumed plus ballooned, compressed and swapped pages is the VM's footprint on ESXi, not its demand. Home: [`sp5-framework/capacity/vm-footprint-sizing`](../../../../sp5-framework/capacity/vm-footprint-sizing.md), section Memory. Consumed is mostly inactive pages, so a demand built on it overstates the need.
- Do not mix Guest OS and VM metrics in one sum: the Guest OS counts its cache and free pages, ESXi counts the pages the VM touched.
- Guest OS metrics are more accurate and smaller than VM metrics, but unaware of ESXi memory management.

## Reclamation effects on the counters
- TPS lowers Consumed: a shared page is backed once for all the VMs that share it.
- Ballooned above 0 means host pressure or a limit on the VM or on a pool above it ([`vsphere/technology/memory/concepts/ballooning`](ballooning.md), section Trigger and requirement).
- Compressed pages stay in DIMM, at a smaller size.
- Swapped and Compressed share one input, the Swap Target: ESXi compresses a page it would otherwise swap.
- Host cache and memory tiering add layers below DRAM; memory tiering adds a performance risk ([`vsphere/technology/memory/concepts/memory-tiering`](memory-tiering.md)).
- VM overhead is small against the VM's memory; ESXi Memory Utilization includes it.

## VCF Operations metrics (ESXi)
| Metric | Meaning |
|---|---|
| Memory \| Total Capacity (KB) | Capacity seen by the kernel: physical size. |
| Memory \| Utilization (KB) | Host memory demand: formula in host/utilization. |
| Memory \| Workload (%) | Utilization over capacity. Not in the 9.1 Host System list. |
| Memory \| Memory Allocated on all Powered On Consumers | Sum of running VM configured memory. Allocation model. |

## VCF Operations metrics (cluster)
| Metric | Meaning |
|---|---|
| Cluster Configuration \| vSphere HA \| HA Memory Failover (%) | HA failover for memory. |
| Memory \| Demand \| Usable Capacity after HA and Buffer (GB) | Total minus HA and buffer. |
| Memory \| ESX System Usage (GB) | Kernel reservation (VCF Operations metric). |
| Memory \| Utilization (KB) | Sum of hosts. |
| Memory \| Demand \| Workload (%) | Utilization / usable. |
| Memory \| Memory Allocated on all Powered On Consumers | Sum of hosts. |
| Memory \| Workload (%) | Demand over usable capacity; demand includes limit and contention. |

- Cluster Memory \| Workload (%) is described in VCF Operations 9.1 (Cluster Compute Resource metrics); the description gives no formula for the limit and contention it includes.
- Usable capacity in the VCF Operations capacity engine is Total Capacity minus HA minus buffer (Capacity Analytics Generated Metrics); the method's usable capacity: [`sp5-framework/capacity/supply`](../../../../sp5-framework/capacity/supply.md).

## Storage: used above allocated
- vSAN protects in software. A 10 GB thick disk with a RAID-1, FTT=1 policy consumes 20 GB of vSAN capacity.

## Misconceptions
- "Allocated is the ceiling of used" → vSAN protection and other files exceed it.

## Metadata
```yaml
id: vsphere/technology/memory/concepts/memory-capacity
retriever_guide: how-it-works
scope: vsphere
technology:
- memory
- storage
pillar:
- capacity
product:
- vsphere
- vcf-operations
- vsan
object:
- HostSystem
- ClusterComputeResource
internal_derive:
- vsphere/technology/memory/concepts/memory-layers
related:
- sp5-framework/capacity/supply
- sp5-framework/capacity/demand
- sp5-framework/capacity/vm-footprint-sizing
- vsphere/technology/memory/metrics/host/utilization
- vsphere/technology/memory/metrics/virtual-motherboard/utilization
source:
  document: Knowledge base; VCF Operations 9.1 documentation (TechDocs, last updated 2026-11-12), Host System Metrics, Cluster Compute Resource Metrics, Capacity Analytics Generated Metrics
  path: Provider Objects > Capacity > Memory; Storage; Implementation
corrections: []
review_notes:
- 'To check: Section ''VCF Operations metrics (ESXi)'': host Memory|Workload (%) is not in the VCF Operations 9.1 Host System metric list (TechDocs, updated 2026-11-12); check in a 9.1 instance whether the host shows it and whether it divides by Total Capacity or by Usable Memory (`mem|host_usable`), https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/infrastructure-operations/metric-property-and-alert-definitions/metrics-definitions-in-vrealize-operations-manager/metrics-for-vcenter-server-components/host-system-metrics.html.'
status: draft
```
