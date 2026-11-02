# ESXi CPU Reserved Capacity

## Meaning
- The only CPU reservation metric for ESXi. Unit: MHz.
- Memory has 3 reservation counters. CPU has 1.

## Why only one
- CPU reservation is transient. When a VM is not running, its reserved CPU can be used by other VMs.
- Memory reservation is sticky: memory is a form of storage.

## Includes / excludes
- excludes: hypervisor (kernel) reservation.

## Traps
- "Reserved CPU is unavailable to other VMs" → unused reserved CPU is used by other VMs.

## Metadata
```yaml
id: vsphere/cpu/metrics/host/reserved-capacity
retriever_guide: metric-meaning
scope: vsphere
technology:
- cpu
pillar:
- capacity
product:
- vsphere
object:
- HostSystem
metric_class: context
internal_derive: []
same_name: []
same_meaning: []
related:
- vsphere/cpu/metrics/host/demand
- vsphere/foundations/resource-management
source:
  document: PART 3 - Counters.docx
  path: CPU > ESXi > Consumption Metrics > Reservation
corrections: []
review_notes: []
status: draft
```
