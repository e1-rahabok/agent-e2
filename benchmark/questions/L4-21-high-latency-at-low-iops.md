# High disk latency at low IOPS

## Prompt
- sql-07 is a VM with three virtual disks on one VMFS datastore of an FC array.
- VCF Operations, last hour:

| Virtual disk | Use | Read IOPS | Read latency | Write IOPS | Write latency |
|---|---|---|---|---|---|
| scsi0:0 | OS | 4 | 1.1 ms | 6 | 0.9 ms |
| scsi0:1 | Data | 30 | 24 ms | 5 | 1.3 ms |
| scsi0:2 | Log | 1 | 0.8 ms | 4 | 1.0 ms |

- The storage team says the array is idle and reports 0.6 ms for the LUN, so storage cannot be the cause.

How can latency be high at so few IOPS? Give the checks, in order, that find where it comes from.

## Likely wrong answer
"At 30 IOPS the disk is not busy, so the latency cannot be a storage problem."

## Expected key points
- Latency at low IOPS is possible: every layer below the VM has its own queue (virtual disk, kernel, adapter, fabric, array), and errors add delay at any load.
- The problem is one disk and one side: reads on scsi0:1. The VM total hides it; work on that disk's reads.
- The array sees 0.6 ms while the VM sees 24 ms: the time is added between the VM and the array: in the host, the HBA or the fabric.
- Check errors: aborted commands and bus resets should be 0; dropped frames on FC.
- Check outstanding IO with latency, and whether the VM has a snapshot (reads must check the snapshot chain).
- On the host, split GAVG into KAVG and DAVG for that LUN: KAVG well above zero (the vSphere documentation targets 0-1 ms) points to kernel queues; DAVG high while the array reports 0.6 ms points to the fabric or HBA.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Revised 2026-11-12 for question set 1.0: per-disk values and the array's own reading added. Counts only after author approval.

## Metadata
```yaml
id: "0062"
title: "High disk latency at low IOPS"
product: [vsphere, vcf-operations]
technology: [storage]
task: troubleshoot
level: 400
answer_type: judged
input: [text]
object: [vm, esxi]
tool: [vcf-operations, esxtop]
knowledge:
  - vsphere/technology/storage/troubleshooting/vm-storage-performance-checks
  - vsphere/technology/storage/troubleshooting/host-storage-latency
  - vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
  - vsphere/technology/storage/concepts/esxi-storage-latency-stack
knowledge_main: vsphere/technology/storage/troubleshooting/vm-storage-performance-checks
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
misconception_type: [consumption-as-contention, average-hides-worst]
status: draft
```
