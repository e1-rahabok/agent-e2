# High disk latency at low IOPS

## Prompt
- A VM with three virtual disks shows a total disk latency of 25 ms at only 50 IOPS.
- The storage team says the array is idle, so storage cannot be the cause.

How do you find where the latency comes from? Give the checks in order.

## Likely wrong answer
"Low IOPS, so latency cannot be a storage problem."

## Expected key points
- Latency at low IOPS is possible: every layer has its own queue (application, Guest OS, VM driver, kernel, array).
- Check packet loss (IP storage), dropped frames (FC) and aborted SCSI commands; Bus Resets and Commands Aborted should be 0.
- Check latency together with outstanding IO; check read and write latency separately: often only one side is affected.
- Check per virtual disk, not only the VM total.
- On the host, split GAVG into KAVG and DAVG: KAVG above 0.5 ms points to kernel queues; DAVG high points to the fabric or array.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: question-0062
title: "High disk latency at low IOPS"
product: [vsphere]
technology: [storage]
task: troubleshoot
level: 400
answer_type: judged
input: [text]
knowledge:
  - vsphere/technology/storage/diagnosis/vm-storage-performance-checks
  - vsphere/technology/storage/diagnosis/host-storage-latency
  - vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
status: draft
```
