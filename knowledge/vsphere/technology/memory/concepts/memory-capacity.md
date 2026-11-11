# Memory capacity

## Nature
- Only space, no speed by default. Speed enters with memory tiering.
- Guest OS and VM are separate realms; neither is a perfect input.

| Metric | Allocation model | Demand model |
|---|---|---|
| Total capacity | Physical memory | Same |
| Hypervisor overhead | GB assigned manually | Already in ESXi counters |
| Consumption | Sum of running VM configured RAM | ESXi Consumed |
| Performance | Not applicable | ESXi Swapped + Zipped + Guest OS Ballooned |

## Demand
- TPS lowers actual use. Balloon means host pressure or a VM limit. Compressed pages stay in DIMM, smaller. Swapped and compressed share the same input. Host cache and memory tiering add layers; tiering adds performance risk. VM overhead is negligible and excluded.
- Do not mix Guest OS and VM metrics.
```text
ESXi Demand = Kernel Consumed + Sum (running VM Demand)
VM Demand   = Min (Limit, Consumed + Ballooned + Zipped + Swapped)
```
- Consumed is mostly inactive pages; adding ballooned, zipped and swapped makes it more conservative.
- Guest OS metrics are more accurate and smaller, but unaware of ESXi memory management.

## VCF Operations metrics (ESXi)
| Metric | Meaning |
|---|---|
| Memory \| Total Capacity (KB) | Capacity seen by the kernel: physical size. |
| Memory \| Utilization (KB) | Sum of running VM demand + ESXi kernel reservation. VM demand = max(VM reservation, Guest OS needed memory + page-in in the cycle); page-in = rate × block size; falls back to Consumed without guest data; includes VM overhead. |
| Memory \| Workload (%) | Utilization / Total Capacity. Likely usable. |
| Memory \| Memory Allocated on all Powered On Consumers | Sum of running VM configured memory. Allocation model. |

## VCF Operations metrics (cluster)
| Metric | Meaning |
|---|---|
| Cluster Configuration \| vSphere HA \| HA Memory Failover (%) | HA failover for memory. |
| Memory \| Demand \| Usable Capacity after HA and Buffer (GB) | Total minus HA and buffer. |
| Memory \| ESX System Usage (GB) | Kernel reservation. |
| Memory \| Utilization (KB) | Sum of hosts. |
| Memory \| Demand \| Workload (%) | Utilization / usable. |
| Memory \| Memory Allocated on all Powered On Consumers | Sum of hosts. |
| Memory \| Workload (%) | Possibly a normalized average of hosts. |

## Storage: used can exceed allocated
- vSAN protects in software. A 10 GB thick disk (vSAN policy) consumes 20 GB at the VMFS layer.

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
- sp5-framework/capacity/capacity-model
- vsphere/technology/memory/metrics/host/utilization
- vsphere/technology/memory/metrics/virtual-motherboard/utilization
source:
  document: PART 3 - Counters.docx
  path: Provider Objects > Capacity > Memory; Storage; Implementation
corrections: []
review_notes:
- 'Section ''VCF Operations metrics (ESXi)'': VM demand here is max(reservation, Guest OS needed + page-in); the VM Utilization formula in vsphere/technology/memory/metrics/virtual-motherboard/utilization adds unusable memory. Both from the book.'
status: draft
```
