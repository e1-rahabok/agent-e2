# Many-to-many object relationships

## Definition
- A VM with multiple virtual disks can span multiple datastores, and RDMs.
- A datastore typically hosts many VMs.
- An ESXi host can mount multiple LUNs.
- A LUN is typically presented to multiple ESXi hosts, and can be presented to multiple clusters.

## Consequence
- Totals across VM, datastore, ESXi, cluster and data center do not reconcile when viewed together.
- Each value is correct from its own vantage point.

## Misconceptions
- "VM totals ≠ datastore totals ≠ cluster totals, so a metric is wrong" → wrong. Different vantage points over many-to-many relationships.

## Metadata
```yaml
id: vsphere/architecture/object-relationships
retriever_guide: how-it-works
scope: vsphere
technology:
- storage
- cpu
- memory
pillar:
- capacity
product:
- vsphere
object:
- VirtualMachine
- Datastore
- HostSystem
- ClusterComputeResource
- Datacenter
internal_derive: []
related:
- vsphere/technology/storage/metrics/virtual-motherboard/virtual-disk
- vsphere/architecture/provider-consumer
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Architecture Complexity
corrections: []
review_notes: []
status: draft
```
