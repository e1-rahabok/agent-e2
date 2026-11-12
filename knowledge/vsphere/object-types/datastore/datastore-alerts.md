# Datastore alerts

## Coverage and receivers
- A datastore is a storage provider: its alerts go to the infrastructure team, above all the storage team.
- Alerted: datastore consumption (space). Not alerted: datastore latency.
- Every value is in the alert rows of [`catalog/thresholds-alerts.yaml`](../../../catalog/thresholds-alerts.yaml), shown with this file.
- Storage consumption has two sides: capacity (disk space) and performance (IOPS and throughput). Performance consumption is hard to alert on: storage has no clear 100%, so the ceiling is hard to define.

## Datastore consumption
- Detects: the datastore is running out of space. Red only.
- Space headroom and what fills a datastore: [`vsphere/technology/storage/datastore-space-headroom`](../../technology/storage/datastore-space-headroom.md).
- The datastore cluster built from this alert: [`vsphere/object-types/datastore-cluster/datastore-cluster-alerts`](../datastore-cluster/datastore-cluster-alerts.md).

## Datastore latency: not implemented
- VMs and datastores are many-to-many: a VM can span datastores and a datastore serves many VMs, so a VM-level condition cannot be set for a datastore.
- Guide if you build one, all of:
  - more than 25% of the VM population has latency above 10 ms;
  - the highest VM latency is above 40 ms;
  - overall datastore latency is above 5 ms.
- VM disk latency is alerted on the VM: [`vsphere/object-types/vm/vm-alerts`](../vm/vm-alerts.md).

## Misconceptions
- "Datastore latency alerts are easy from VM latency" → VMs and datastores are many-to-many.

## Metadata
```yaml
id: vsphere/object-types/datastore/datastore-alerts
retriever_guide: what-to-set
scope: vsphere
technology:
- storage
pillar:
- capacity
- performance
product:
- vsphere
- vcf-operations
object:
- Datastore
internal_derive:
- sp5-framework/outputs/alert-design
- vsphere/technology/storage/datastore-space-headroom
related:
- vsphere/object-types/vm/vm-alerts
- vsphere/object-types/datastore-cluster/datastore-cluster-alerts
- vsphere/technology/storage/troubleshooting/host-storage-latency
- vsphere/technology/storage/metrics/host/datastore
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: 'Proactive Operations > Alert > Storage Alerts (Contention Alerts: Infrastructure Contention; Consumption Alerts); Alerts Planning > Design (alert count table)'
corrections: []
review_notes:
- 'Section ''Datastore latency: not implemented'': the source says Infrastructure Contention is not yet implemented; its alert count table shows Datastore disk contention 0. Parked after 1.0 (Q142).'
- 'Section ''Datastore latency: not implemented'': the guide values stay in this file because no alert in the set holds them; a catalog row exists only for an alert in the set.'
status: draft
```
