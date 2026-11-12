# Datastore and datastore cluster alerts

## Coverage and receivers
- A datastore is a storage provider: its alerts go to the infrastructure team, above all the storage team.
- Alerted: datastore consumption (space). Not alerted: datastore latency, and both alerts on the datastore cluster.
- Every value is in the alert rows of [`catalog/thresholds-alerts.yaml`](../../../../catalog/thresholds-alerts.yaml), shown with this file.
- Storage consumption has two sides: capacity (disk space) and performance (IOPS and throughput). Performance consumption is hard to alert on: storage has no clear 100%, so the ceiling is hard to define.

## Datastore consumption
- Detects: the datastore is running out of space. Red only.
- Space headroom and what fills a datastore: [`vsphere/technology/storage/decision-tree/datastore-space-headroom`](../../../technology/storage/decision-tree/datastore-space-headroom.md).

## Datastore latency: not implemented
- VMs and datastores are many-to-many: a VM can span datastores and a datastore serves many VMs, so a VM-level condition cannot be set for a datastore.
- Guide if you build one, all of:
  - more than 25% of the VM population has latency above 10 ms;
  - the highest VM latency is above 40 ms;
  - overall datastore latency is above 5 ms.
- VM disk latency is alerted on the VM: [`vsphere/object-types/vm/alerts/vm-alerts`](../../vm/alerts/vm-alerts.md).

## Datastore cluster: not implemented
- Consumption: it should fire when a member datastore meets the datastore consumption condition. The cluster average hides a full member. Remediation: run Storage DRS.
- Latency: the same many-to-many limit as a datastore.

## Misconceptions
- "Datastore latency alerts are easy from VM latency" → VMs and datastores are many-to-many.
- "Alert when the datastore cluster is 90% full" → one member datastore can be full while the cluster average is not.

## Metadata
```yaml
id: vsphere/object-types/datastore/alerts/datastore-alerts
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
- StoragePod
internal_derive:
- sp5-framework/outputs/alert-design
- vsphere/technology/storage/decision-tree/datastore-space-headroom
related:
- vsphere/object-types/vm/alerts/vm-alerts
- vsphere/technology/storage/troubleshooting/host-storage-latency
- vsphere/technology/storage/metrics/host/datastore
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: 'Proactive Operations > Alert > Storage Alerts (Contention Alerts: Infrastructure Contention; Consumption Alerts)'
corrections: []
review_notes:
- 'To check: Section ''Datastore cluster: not implemented'': the datastore cluster object type is StoragePod; not in the source. Storage DRS as the remediation for a full member datastore is from the source.'
- 'Section ''Datastore latency: not implemented'' and ''Datastore cluster: not implemented'': the source says Infrastructure Contention is not yet implemented; its alert count table shows Datastore disk contention 0 and Datastore Cluster disk contention 2. Parked after 1.0 (Q142).'
- 'Section ''Datastore latency: not implemented'': the guide values stay in this file because no alert holds them; a catalog row exists only for an alert in the set.'
status: draft
```
