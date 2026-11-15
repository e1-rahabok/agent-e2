# Datastore cluster alerts

## Coverage and receivers
- A datastore cluster is a storage provider: its alerts would go to the infrastructure team, above all the storage team.
- No alert in the set. Its member datastores have their own alerts ([`vsphere/object-types/datastore/datastore-alerts`](../datastore/datastore-alerts.md)).

## Not alerted
- Consumption: not implemented. It should fire when a member datastore meets the datastore consumption condition, because the cluster average hides a full member. Remediation: run Storage DRS ([`vsphere/object-types/datastore-cluster/storage-drs`](storage-drs.md)).
- Latency: not implemented. VMs and datastores are many-to-many, and a VM's disks can sit on several members ([`vsphere/architecture/object-relationships`](../../architecture/object-relationships.md)). VM disk latency is alerted on the VM ([`vsphere/object-types/vm/vm-alerts`](../vm/vm-alerts.md)).

## Misconceptions
- "Alert when the datastore cluster is 90% full" → one member datastore can be full while the cluster average is not.

## Metadata
```yaml
id: vsphere/object-types/datastore-cluster/datastore-cluster-alerts
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
- StoragePod
internal_derive:
- sp5-framework/outputs/alert-design
- vsphere/object-types/datastore/datastore-alerts
related:
- vsphere/technology/storage/datastore-space-headroom
- vsphere/architecture/object-relationships
- vsphere/object-types/vm/vm-alerts
- vsphere/object-types/datastore-cluster/storage-drs
source:
  document: Knowledge base
  path: 'Proactive Operations > Alert > Storage Alerts (Consumption Alerts); Alerts Planning > Design (alert count table)'
corrections: []
review_notes:
- 'To check after 1.0: Section ''Not alerted'': a count of the recommended alert set lists 2 datastore cluster disk contention alerts, while the storage alert design says datastore cluster latency is not implemented; settle with the review of the VCF Operations alert set (plan, After 1.0, VCF Operations alert mastery).'
status: draft
```
