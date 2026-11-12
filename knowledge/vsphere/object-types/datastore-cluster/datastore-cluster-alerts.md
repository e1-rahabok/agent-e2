# Datastore cluster alerts

## Coverage and receivers
- A datastore cluster is a storage provider: its alerts would go to the infrastructure team, above all the storage team.
- No alert in the set. Its member datastores have their own alerts ([`vsphere/object-types/datastore/datastore-alerts`](../datastore/datastore-alerts.md)).

## Not alerted
- Consumption: not implemented. It should fire when a member datastore meets the datastore consumption condition, because the cluster average hides a full member. Remediation: run Storage DRS.
- Latency: not implemented. VMs and datastores are many-to-many, and a VM's disks can sit on several members.

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
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: 'Proactive Operations > Alert > Storage Alerts (Consumption Alerts); Alerts Planning > Design (alert count table)'
corrections: []
review_notes:
- 'Section ''Not alerted'': the source''s alert count table shows Datastore Cluster disk contention 2, while Storage Alerts > Infrastructure Contention says not yet implemented. Parked after 1.0 (Q142).'
- 'To check: Section ''Coverage and receivers'': the datastore cluster object type is StoragePod; not in the source.'
status: draft
```
