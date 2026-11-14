# Protect a database from a noisy VM on a shared datastore

## Prompt
- A vSphere 9.1 cluster of 8 hosts shares VMFS datastore DS-SHR01 on an FC array.
- Every night from 01:00 to 03:00, reporting VM rpt-07 runs large sequential reads on DS-SHR01.
- In that window, database VM db-11, on another host and the same datastore, sees its read latency rise from 1 ms to 25 ms. Outside the window db-11 is fine.
- The team proposes to turn on Storage I/O Control on DS-SHR01 and give db-11 High disk shares, so that the database wins when the datastore is congested.

Will that work in vSphere 9.1? What do you advise instead?

## Likely wrong answer
"Yes. Enable Storage I/O Control and set db-11 to High shares: SIOC throttles rpt-07 when the datastore latency crosses its threshold."

## Expected key points
- Not as planned: Storage I/O Control is deprecated, and from VCF 9.0 its storage policies honour only limits; shares and reservations are ignored. High shares will not protect db-11.
- Put the control on the noisy VM: an IOPS limit on rpt-07's virtual disks (limits are still honoured), sized so its job still ends in the window. The limit is in IOPS, so with large blocks it also caps rpt-07's throughput.
- Or separate the two: move rpt-07 or db-11 to another datastore or LUN, or use the array's own QoS.
- Confirm where db-11 waits first: high DAVG with low KAVG on db-11's host shows the wait is in the array or fabric, shared with rpt-07's host; no setting on db-11's host alone fixes it.

## Notes
- Drafted by Claude 2026-11-12. Counts only after author approval.
- Vendor documents: Broadcom KB 385396, "Deprecation of default Storage Policy Components for SIOC Storage Policy" (https://knowledge.broadcom.com/external/article/385396): from VCF 9.0 the SIOC policy supports only limits and the backend ignores shares and reservations. Deprecation notice with vSphere 8.0 U3 (https://www.yellow-bricks.com/2024/11/25/storage-io-control-aka-sioc-deprecation-notice-with-8-0-u3).
- The key does not depend on whether SIOC can still be enabled on a datastore in 9.x (only a secondary source says it cannot). An answer that says so is a correct alternative, not a requirement.

## Metadata
```yaml
id: "0183"
title: "Protect a database from a noisy VM on a shared datastore"
product: [vsphere]
technology: [storage]
task: judge-setting
level: 400
answer_type: judged
input: [text]
object: [vm, datastore]
tool: [none]
knowledge:
  - vsphere/technology/storage/metrics/datastore/storage-io-control
  - vsphere/technology/storage/metrics/virtual-motherboard/iops
  - vsphere/technology/storage/concepts/esxi-storage-latency-stack
knowledge_main: vsphere/technology/storage/metrics/datastore/storage-io-control
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
misconception_type: []
status: draft
```
