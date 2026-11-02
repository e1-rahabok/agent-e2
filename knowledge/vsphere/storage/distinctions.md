---
id: vsphere/storage/distinctions
type: distinction
scope: vsphere
resources: [storage]
objects: [vm, datastore, esxi]
related:
  - foundations/naming-patterns
  - foundations/resource-nature
  - foundations/terminology
  - vsphere/foundations/object-relationships
  - vsphere/foundations/visibility-layers
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity
corrections: []
review_notes: []
status: draft
---

# Storage distinctions

## Virtual Disk: VM vs Datastore
- pattern: same-name-same-purpose-different-formula
- VM: Virtual Disk includes RDM.
- Datastore: Virtual Disk excludes RDM.
- why: different vantage points. An RDM belongs to the VM but its data is on an external LUN, not on the datastore.
- src: Naming Complexity

## "Virtual disk" includes RDM
- pattern: confusing-name
- The term virtual disk covers both VMDK and RDM.
- why: an RDM appears as a virtual disk when browsing the datastore directory, although the RDM file is only a pointer to an external LUN.
- src: Naming Complexity

## Disk Latency
- Disk Latency indicates a performance problem. It is a primary counter for how well the VM is served.
- Contrast: CPU Latency does not always indicate a performance problem. See `vsphere/cpu/distinctions`.
- src: Naming Complexity

## Limits: IOPS vs throughput
- A disk IOPS limit exists.
- A disk throughput limit does not exist.
- why: throughput depends on block size, which varies. A throughput limit is not practical to implement.
- src: Architecture Complexity

## Disk reservation
- Reservation does not apply to disk. Utilization and allocation do.
- See `vsphere/foundations/resource-management`.

## Throughput unit
- Disk throughput is in bytes/second (node view), unlike network throughput (wire view).
- See `foundations/resource-nature`.

## VM IOPS can under-report
- IO queued inside the Guest OS has not reached the hypervisor. VM-level IOPS does not include it.
- See `vsphere/foundations/visibility-layers` (area A).

## Totals do not reconcile across objects
- VM, datastore, ESXi and cluster disk totals differ because of many-to-many relationships.
- See `vsphere/foundations/object-relationships`.
