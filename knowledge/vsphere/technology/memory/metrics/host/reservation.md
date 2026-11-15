# ESXi Memory Reservation counters

## Counters
| Counter | Unit in vCenter | Meaning |
|---|---|---|
| Total reservation | MB | The host's reservable capacity: Reservation consumed plus Reservation available. A near-constant of the host, not the memory reserved by VMs. |
| Reservation consumed | MB | Reserved memory in use by the running VMs. Rises and falls with a VM's reservation. |
| Reservation available | KB | Total reservation minus Reservation consumed. Available for new reservations. |

## Counter scope
- Total reservation does not follow VM activity: on a 9.1 lab host it stayed at about 362,000 MB (354 GiB) while Reservation consumed rose from 373 MB to 9,385 MB. Read as the memory reserved by VMs, it would be far too high.
- Total reservation equals Reservation consumed plus Reservation available on every sample of that host, to within 1 MB.
- Reservation consumed counts VMs only. It excludes the kernel reservation (System Resource Reservation, [overhead](../../../../architecture/overhead.md), section Memory metrics) and kernel use: on the lab host it read 373 MB, below both the 4.2 GB kernel reservation and VMkernel consumed (704 MB).
- Reservation consumed follows a VM's reservation. Test on the lab host (20-second real-time samples): raising one VM's reservation by 8 GB raised Reservation consumed by 8,192 MB and lowered Reservation available by the same amount, to within 4 MB.
- The counters of the same chart that did not move in that test: Consumed, Granted, VMkernel consumed and Overhead consumed ([ESXi memory metrics compared](../comparisons/host-memory-metrics.md), section VM reservation across counters).
- The vCenter chart mixes units: MB for Total reservation and Reservation consumed, KB for Reservation available, Consumed, Granted and VMkernel consumed. Convert before comparing: 373 MB against a VMkernel consumed of 720,980 KB (704 MB).

## Three reservation counters
- A provider must account for reservations: they cannot be overcommitted.
- Memory reservation is sticky. CPU has only 1 reservation counter: CPU reservation is transient.
- A memory reservation is held only after it is used. Until a VM has touched its full reservation, the VMkernel can give the unused part of the reservation to other VMs. Once touched, the pages stay with the VM even when it goes idle: that is the sticky part.
- Admission control is a separate check: it counts the full reservation whether used or not. A VM powers on only if the unreserved memory covers its reservation, so an untouched reservation still blocks new reservations, not other VMs' use of the pages.

## Misconceptions
- "Reserved = used" → check Reservation consumed.
- "Total reservation is the memory reserved by powered-on VMs" → it is the host's reservable capacity (Reservation consumed plus Reservation available). Reservation consumed is the VM part.
- "Reservation consumed includes the kernel reservation" → it counts VMs only. The kernel reservation is System Resource Reservation.
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
  document: Knowledge base
  path: Memory > ESXi > Overview; Consumption Metrics > Reservation
corrections: []
review_notes:
- 'Section ''Counter scope'': the lab test cannot tell whether Reservation consumed counts the reservation as set or only the touched pages of it (the VM may already have touched 8 GB); to separate them, raise the reservation of a VM that has touched less than the new value. API 9.1 (https://developer.broadcom.com/xapis/vsphere-web-services-api/9.1/memory_counters.html) defines reservedCapacity as the reservation used by powered-on VMs and vSphere services and totalCapacity as that reservation used and available; the match of these to the UI labels Reservation consumed and Total reservation is by unit and definition.'
- 'Section ''Three reservation counters'': check the 9.1 wording that the VMkernel can allocate the unused portion of a reservation to other VMs until the VM consumes it (stated in vSphere 8.0 Resource Management; no 9.1 page found yet). https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-1/vsphere-resource-management.html'
status: draft
```
