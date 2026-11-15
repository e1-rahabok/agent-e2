# Datastore Virtual Disk

## Meaning
- The virtual disk files a datastore holds: the VMDKs on it. A datastore counts the files on it and leaves out the VMDKs of the same VMs on other datastores ([`vsphere/technology/storage/concepts/storage-layers`](../../concepts/storage-layers.md), section Datastore layer).
- Excludes RDM. The RDM data sits on an external LUN, not on the datastore; the datastore holds only the RDM pointer file.
- The same label on the VM includes RDM: [`vsphere/technology/storage/metrics/virtual-motherboard/virtual-disk`](../virtual-motherboard/virtual-disk.md). The two vantage points differ by the RDMs and by the VMs whose disks span datastores.
- Relevance for operations: capacity and performance of the datastore, for the VMDK files it holds. Not a VM total: a VM with RDMs or with disks on other datastores shows more at VM level.

## Misconceptions
- "Datastore Virtual Disk equals the sum of its VMs' Virtual Disk" → the VM value includes RDMs and the VM's disks on other datastores; the datastore value counts only the VMDKs on that datastore. Compare per VM and datastore pair.

## Metadata
```yaml
id: vsphere/technology/storage/metrics/datastore/virtual-disk
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
- Datastore
metric_class: consumption
internal_derive:
- vsphere/architecture/object-relationships
same_name:
- vsphere/technology/storage/metrics/virtual-motherboard/virtual-disk
same_meaning: []
related: []
source:
  document: Knowledge base
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity
corrections: []
review_notes: []
status: draft
```
