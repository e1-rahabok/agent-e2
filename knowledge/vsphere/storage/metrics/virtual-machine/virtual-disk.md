---
id: vsphere/storage/metrics/virtual-machine/virtual-disk
retriever_guide: metric-meaning
scope: vsphere
technology:
- storage
pillar:
- capacity
- performance
product:
- vsphere
object:
- VirtualMachine
metric_class: consumption
internal_derive:
- vsphere/foundations/object-relationships
same_name:
- vsphere/storage/metrics/datastore/virtual-disk
same_meaning: []
related: []
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity
corrections: []
review_notes: []
status: draft
---

# VM Virtual Disk

## Meaning
- Includes RDM.
- The term virtual disk covers both VMDK and RDM, because an RDM appears as a virtual disk when browsing the datastore directory. The RDM file is only a pointer to an external LUN.

## Why it differs from Datastore Virtual Disk
- Different vantage points. The RDM belongs to the VM, but its data is on an external LUN, not on the datastore.

## Traps
- "VM disk totals should match datastore totals" → RDM and many-to-many relationships break that. See `vsphere/foundations/object-relationships`.
