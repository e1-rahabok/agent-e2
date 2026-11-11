# ESXi CPU Reserved Capacity

## Meaning
- The only CPU reservation metric for ESXi. Unit: MHz.
- Memory has 3 reservation counters. CPU has 1.
- The reservable total is capped at base (nominal) clock speed × cores, not Turbo: ESXi guarantees only the frequency it can always deliver.

## Why only one
- CPU reservation is transient. When a VM is not running, its reserved CPU can be used by other VMs.
- Memory reservation is sticky: memory is a form of storage.

## Includes / excludes
- excludes: hypervisor (kernel) reservation.

## Misconceptions
- "Reserved CPU is unavailable to other VMs" → unused reserved CPU is used by other VMs.
- "A CPU reservation speeds up the VM" → it only matters under contention. With enough CPU for every VM it changes nothing.
- "The host can reserve up to its Turbo capacity" → reservation is capped at base clock speed × cores.

## Metadata
```yaml
id: vsphere/technology/cpu/metrics/host/reserved-capacity
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
- vsphere/technology/cpu/metrics/host/demand
- vsphere/architecture/resource-controls
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: CPU > ESXi > Consumption Metrics > Reservation
corrections:
- 'Sections Meaning, Misconceptions: CPU reservation capped at base clock speed × cores, and applies only under contention (quiz CPU Q8 key options A and B).'
review_notes: []
status: draft
```
