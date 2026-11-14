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
- A memory reservation is held only after it is used. Until a VM has touched its full reservation, the VMkernel can give the unused part of the reservation to other VMs. Once touched, the pages stay with the VM even when it goes idle: that is the sticky part.
- Admission control is a separate check: it counts the full reservation whether used or not. A VM powers on only if the unreserved memory covers its reservation, so an untouched reservation still blocks new reservations, not other VMs' use of the pages.

## Misconceptions
- "Reserved = used" → check Reservation consumed.
- "A reservation takes its memory away from other VMs from power-on" → untouched reserved pages can serve other VMs; only admission control counts the full amount at power-on.

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
internal_derive:
- vsphere/architecture/resource-controls
- vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
same_name: []
same_meaning: []
related:
- vsphere/technology/memory/metrics/comparisons/host-memory-metrics
- vsphere/technology/cpu/metrics/host/reserved-capacity
- vsphere/technology/memory/metrics/host/consumed
- vsphere/architecture/resource-controls
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: Memory > ESXi > Overview; Consumption Metrics > Reservation
corrections: []
review_notes:
- 'Section ''Three reservation counters'': check the 9.1 wording that the VMkernel can allocate the unused portion of a reservation to other VMs until the VM consumes it (stated in vSphere 8.0 Resource Management; no 9.1 page found yet). https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-1/vsphere-resource-management.html'
status: draft
```
