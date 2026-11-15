# Many-to-many object relationships

## Definition
- A VM runs on one ESXi host at a time, but its files can sit on several datastores: each virtual disk can be on a different datastore, and an RDM points to a LUN outside any datastore.
- A datastore typically holds the files of many VMs.
- An ESXi host can mount multiple LUNs and datastores.
- A LUN or datastore is typically presented to multiple ESXi hosts in the same cluster. It can also be presented to hosts of other clusters, and even to hosts managed by different vCenter Servers.
- On the network side, a host connects to several distributed switches and a switch spans many hosts; a VM can connect to several port groups.
- The relations and their cardinality per object type: `catalog/objects.yaml`.

## Consequence
- Totals across VM, datastore, ESXi, cluster and data center do not reconcile when viewed together, because the same disk or packet is counted from each object's own vantage point.
- Each value is correct from its own vantage point.
- Datastore Virtual Disk counts only the VMDKs on that datastore; VM Virtual Disk adds the RDMs and the disks on other datastores ([`vsphere/technology/storage/metrics/datastore/virtual-disk`](../technology/storage/metrics/datastore/virtual-disk.md), [`vsphere/technology/storage/metrics/virtual-motherboard/virtual-disk`](../technology/storage/metrics/virtual-motherboard/virtual-disk.md)).
- A host's datastore counters show this host's share of a shared datastore; the datastore object spans all its hosts ([`vsphere/technology/storage/metrics/host/datastore`](../technology/storage/metrics/host/datastore.md)).
- Storage capacity cannot be summed per cluster when datastores are shared across clusters ([`vsphere/technology/storage/concepts/storage-layers`](../technology/storage/concepts/storage-layers.md)).

## Misconceptions
- "VM totals ≠ datastore totals ≠ cluster totals, so a metric is wrong" → wrong. Different vantage points over many-to-many relationships: each object counts its own share.

## Metadata
```yaml
id: vsphere/architecture/object-relationships
retriever_guide: how-it-works
scope: vsphere
technology:
- storage
- cpu
- memory
- network
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
internal_derive:
- vsphere/technology/storage/metrics/datastore/virtual-disk
- vsphere/technology/storage/metrics/virtual-motherboard/virtual-disk
- vsphere/technology/storage/metrics/host/datastore
- vsphere/technology/storage/concepts/storage-layers
related:
- vsphere/architecture/provider-consumer
source:
  document: Knowledge base
  path: The World of Metrics > Metrics Nuances > Complexity > Architecture Complexity
corrections: []
review_notes: []
status: draft
```
