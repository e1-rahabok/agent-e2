# Array IOPS twice the datastore IOPS at night

## Prompt
- Datastore DS-CRM02 is a VMFS datastore on one LUN (0x2A) of an FC array, mounted by 6 hosts.
- [The attached export](0188/ds-crm02-vs-lun-iops-1-day.csv) puts side by side, hour by hour for one day: the datastore IOPS summed over the 6 hosts (vCenter), the IOPS the array reports for LUN 0x2A, and the datastore read latency the VMs see.
- From 22:00 to 03:00, the CRM batch jobs on the VMs run slower than in the day.
- The vSphere team says the VMs do less IO at night, so the array cannot be busy. The storage team says vCenter under-reports.

Why does the array report about twice the IOPS vCenter shows at night, and what does it mean for the slow batch jobs?

## Likely wrong answer
"One of the two tools miscounts: the IOPS should match." Or: "The VMs must be doing more IO at night than vCenter shows."

## Expected key points
- Both are right from their own vantage point. vCenter counts only the IO the 6 hosts send. The array counts all IO on the LUN, including IO none of the 6 hosts sends: another initiator (for example a SAN-mode backup proxy) or array jobs (replication, array snapshots, rebuilds), where the array counts them.
- With one datastore on one LUN, array IOPS ÷ datastore IOPS should be about 1, as it is in the day. About 2 at night means the LUN serves as much other IO as the hosts send.
- The VMs' IO waits behind that other IO at the array: their read latency rises from about 1 ms to 7-9 ms while their own IO falls. The VMs are not the cause.
- Confirm on the hosts: device latency (DAVG) rises at night while kernel latency (KAVG) stays low, so the time is spent at the array or fabric, not in the hosts.
- No vSphere setting fixes it: ask the storage team which initiators and jobs hit the LUN at 22:00, and move or throttle them, or move the batch window. Track the ratio over time.

## Notes
- Drafted by Claude 2026-11-12: the backing device ratio. Counts only after author approval.

## Metadata
```yaml
id: "0188"
title: "Array IOPS twice the datastore IOPS at night"
product: [vsphere]
technology: [storage]
task: explain-mechanism
level: 400
answer_type: judged
input: [table]
object: [datastore, esxi]
tool: [vcenter]
knowledge:
  - vsphere/technology/storage/concepts/storage-layers
  - vsphere/technology/storage/troubleshooting/vm-storage-performance-checks
  - vsphere/technology/storage/concepts/esxi-storage-latency-stack
  - vsphere/architecture/provider-consumer
knowledge_main: vsphere/technology/storage/concepts/storage-layers
attachments:
  - 0188/ds-crm02-vs-lun-iops-1-day.csv
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
misconception_type: [provider-vs-consumer]
status: draft
```
