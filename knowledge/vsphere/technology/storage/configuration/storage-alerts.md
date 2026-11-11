# Storage alerts

## What to set
- Design storage alerts as a set: every object, and for each object both contention and consumption.
- Read latency and write latency get separate alerts: their causes usually differ, so their remediation differs.
- Each alert below fires only when all its conditions hold.

## VM disk latency
- Red, read, all of:
  - VM Disk Read Latency (average) above 80 ms;
  - VM Peak Disk Latency (read or write) above 320 ms;
  - VM CPU Usage above 1 GHz;
  - VM Disk Read IOPS above 100.
- Red, write: the same with VM Disk Write Latency above 80 ms and VM Disk Write IOPS above 100.
- Orange, read, all of:
  - VM Disk Read Latency (average) above 40 ms;
  - VM Peak Disk Latency (read or write) above 160 ms;
  - VM CPU Usage above 1 GHz;
  - VM Disk Read IOPS above 100.
- Orange, write: the same with VM Disk Write Latency above 40 ms and VM Disk Write IOPS above 100.
- Wait 10 minutes. Vendor best practice and field reality differ, so the wait is longer and the thresholds higher. A lower number is right in theory, but there are hardly any complaints at these levels, and investment is hard to justify without complaints.
- The 20-second peak covers read and write together. This is a known limit.
- CPU Usage and IOPS cut alerts during low activity, where business impact is likely negligible.
- These are the standard production values. Class-of-service examples (30, 60, 120 ms): `sp5-framework/alerts/alert-design`.
- Metrics: `vsphere/technology/storage/metrics/virtual-motherboard/disk-latency`, `vsphere/technology/storage/metrics/virtual-motherboard/iops`, `vcf-operations/features/peak-20-second-metrics`.

## Datastore latency
- Not implemented. VMs and datastores are many-to-many: a VM can span datastores and a datastore serves many VMs, so a VM-level condition cannot be set for a datastore.
- Guide if you build one, all of:
  - more than 25% of the VM population has latency above 10 ms;
  - the highest VM latency is above 40 ms;
  - overall datastore latency is above 5 ms.

## Storage consumption
- Storage consumption has two sides: capacity (disk space) and performance (IOPS and throughput).
- Performance consumption is hard to alert on: storage has no clear 100%, so the ceiling is hard to define.
- Datastore, red: used space above 90%.
- Datastore cluster: not implemented. It should fire when a member datastore is above 90% used; remediation is to run Storage DRS.

## Misconceptions
- "One latency alert for read and write" → causes differ; separate them.
- "VM disk latency above 20 ms is red" → this set uses 80 ms average and 320 ms peak for standard production; lower values in theory draw no complaints in practice.
- "Alert on latency at any load" → require at least 1 GHz CPU and 100 IOPS; low activity has negligible impact.
- "The peak latency in the alert is read latency" → the 20-second peak covers read and write together.
- "Datastore latency alerts are easy from VM latency" → VM and datastore are many-to-many.
- "Alert when the datastore cluster is 90% full" → one member datastore can be full while the cluster average is not.

## Metadata
```yaml
id: vsphere/technology/storage/configuration/storage-alerts
retriever_guide: what-to-set
scope: vsphere
technology:
- storage
pillar:
- performance
- capacity
product:
- vsphere
- vcf-operations
object:
- VirtualMachine
- Datastore
- StoragePod
internal_derive:
- sp5-framework/alerts/alert-design
- vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
- vsphere/technology/storage/metrics/virtual-motherboard/iops
- vcf-operations/features/peak-20-second-metrics
related:
- vsphere/technology/storage/troubleshooting/vm-storage-performance-checks
- vsphere/technology/storage/metrics/host/datastore
source:
  document: PART 2 - Consumption for Agent E2.docx
  path: 'Proactive Operations > Alert > Storage Alerts (Contention Alerts: VM Contention, Infrastructure Contention; Consumption Alerts) (pp. 24-26)'
corrections: []
review_notes:
- 'Section ''VM disk latency'': the 80 ms red is read as standard production; the class-of-service example in the same chapter gives standard production 60 ms for 10 minutes. Q146.'
- 'To check: Section ''Storage consumption'': the datastore cluster object type is StoragePod; not in the source. Storage DRS as the remediation for a full member datastore is from the source.'
- 'Section ''Datastore latency'': the source says Infrastructure Contention, not yet implemented; the alert count table shows Datastore Cluster contention 2. Q142.'
status: draft
```
