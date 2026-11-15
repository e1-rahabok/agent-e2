# ESXi CPU Reserved Capacity

## Meaning
- The only CPU reservation metric for ESXi. Unit: MHz.
- Memory has 3 reservation counters. CPU has 1.
- The reservable total is capped at base (nominal) clock speed × cores, not Turbo: ESXi guarantees only the frequency it can always deliver.
- Relevance for operations: capacity: how much of the host's base-clock capacity the VMs have reserved. Not performance: a CPU reservation acts only under contention.

## One reservation counter
- CPU reservation is transient. When a VM is not running, its reserved CPU can be used by other VMs.
- Memory reservation is sticky: memory is a form of storage.

## Includes / excludes
- Includes: the CPU reservations of the VMs. vSphere Web Services API 9.1 defines `cpu.reservedCapacity` as total CPU capacity reserved by virtual machines.
- Excludes: the hypervisor (kernel) reservation, the System Resource Reservation that ESXi CPU Demand in VCF Operations adds ([`vsphere/technology/cpu/metrics/host/demand`](demand.md), section vCenter vs VCF Operations).

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
internal_derive:
- vsphere/architecture/resource-controls
- vsphere/technology/cpu/concepts/cpu-frequency
same_name: []
same_meaning: []
related:
- vsphere/technology/cpu/metrics/host/demand
- vsphere/architecture/resource-controls
source:
  document: Knowledge base; vSphere Web Services API 9.1 reference, CPU Counters
  path: CPU > ESXi > Consumption Metrics > Reservation; https://developer.broadcom.com/xapis/vsphere-web-services-api/9.1/cpu_counters.html, reservedCapacity
corrections: []
review_notes: []
status: draft
```
