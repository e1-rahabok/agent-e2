# ESXi Memory Reservation counters

## Counters
| Counter | Meaning |
|---|---|
| Total reservation (Reserved Capacity) | Memory reserved by powered-on VMs. Excludes powered-off VMs and the kernel reservation. Reserved is not necessarily used. |
| Reservation consumed | Actual consumption of reserved memory. Consistently below Reserved Capacity: over-reservation. |
| Reservation available | Memory not reserved. Available for new reservations. |

## Three reservation counters
- A provider must account for reservations: they cannot be overcommitted.
- Memory reservation is sticky. CPU has only 1 reservation counter: CPU reservation is transient.

## Misconceptions
- "Reserved = used" → check Reservation consumed.

## Metadata
```yaml
id: vsphere/technology/memory/metrics/host/reservation
retriever_guide: metric-meaning
scope: vsphere
technology:
- memory
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
- vsphere/technology/cpu/metrics/host/reserved-capacity
- vsphere/technology/memory/metrics/host/consumed
- vsphere/architecture/resource-controls
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: Memory > ESXi > Overview; Consumption Metrics > Reservation
corrections: []
review_notes: []
status: draft
```
