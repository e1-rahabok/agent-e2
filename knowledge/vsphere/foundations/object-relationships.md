---
id: vsphere/foundations/object-relationships
type: concept
scope: vsphere
resources: [storage, cpu, memory]
objects: [vm, datastore, esxi, cluster, datacenter]
related: [vsphere/storage/distinctions, vsphere/foundations/provider-consumer]
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Architecture Complexity
corrections: []
review_notes: []
status: draft
---

# Many-to-many object relationships

## Definition
- A VM with multiple virtual disks can span multiple datastores, and RDMs.
- A datastore typically hosts many VMs.
- An ESXi host can mount multiple LUNs.
- A LUN is typically presented to multiple ESXi hosts, and can be presented to multiple clusters.

## Consequence
- Totals across VM, datastore, ESXi, cluster and data center do not reconcile when viewed together.
- Each value is correct from its own vantage point.

## Trap
- "VM totals ≠ datastore totals ≠ cluster totals, so a metric is wrong" → wrong. Different vantage points over many-to-many relationships.
