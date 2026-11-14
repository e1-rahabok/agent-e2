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

Which statements about this latency and the checks that find where it comes from are correct?

- A. Latency can be high at low IOPS, because each layer below the VM has its own queue.
- B. At 30 IOPS the data disk is not busy, so its latency cannot be a storage problem.
- C. The problem sits in one disk and one direction: the reads of scsi0:1.
- D. The total latency of scsi0:1 is the average of its read and write latency, about 12.7 ms.
- E. The array reports 0.6 ms while the VM sees 24 ms, so the extra time is added between the VM and the array.
- F. Aborted commands, bus resets and dropped FC frames add delay at any load, so check that they are 0.
- G. Because the writes of scsi0:1 are fast, the 24 ms of reads must be spent inside the Guest OS.
- H. A redo-log snapshot on sql-07 would slow its reads more than its writes, so check whether it has one.
- I. On the host, split GAVG into KAVG and DAVG for the LUN behind the datastore.
- J. KAVG high with DAVG low points to the array, since the array returns the data.
- K. DAVG high while the array reports 0.6 ms points to the fabric or the HBA configuration.
- L. To locate the problem per adapter and path, read the highest latency of the hour, not a percentile.

## Likely wrong answer
- B: "At 30 IOPS the disk is not busy, so the latency cannot be a storage problem."

## Expected key points
- Answer: A, C, E, F, H, I, K.
- A true: every layer below the VM has its own queue (virtual disk, kernel, adapter, fabric, array). Check outstanding I/O with the latency.
- B false: queues and errors add latency at any load.
- C true: work on that disk's reads; the VM total hides it, and read and write often have different causes.
- D false: total latency is weighted by command count: (30 x 24 + 5 x 1.3) / 35 is about 20.8 ms, close to the read latency.
- E true: the time is added in the host, the HBA or the fabric.
- F true: aborted commands and bus resets should be 0 all the time; dropped frames on FC are a sign of contention with an availability impact.
- G false: the VM's virtual disk latency starts below the Guest OS; only one side being slow is common and points to that side's cause, not to the guest.
- H true: with a redo-log snapshot on VMFS, reads must check the files of the chain; writes go to the newest file and are less affected.
- I true: the split tells kernel latency (the host) from device latency (the HBA, fabric or array).
- J false: KAVG high with DAVG low is queuing inside ESXi: queue depths or a saturated adapter.
- K true: DAVG runs from the HBA to the array and back; with the array at 0.6 ms, the difference is in the fabric or the HBA configuration.
- L false: one outlier dominates the maximum; use the 95th or 99th percentile per adapter and path.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Revised 2026-11-12 for question set 1.0: per-disk values and the array's own reading added. Counts only after author approval.
- Converted from judged to multiple choice (Q199 F, 2026-11-14). Knowledge added: snapshot-impact (reads check the snapshot chain). The old key's KAVG level (0-1 ms in the vSphere documentation) is left out of the options; the knowledge files give 0.5 ms.

## Metadata
```yaml
id: "0062"
title: "High disk latency at low IOPS"
product: [vsphere, vcf-operations]
technology: [storage]
task: troubleshoot
level: 400
answer_type: deterministic
answer: [A,C,E,F,H,I,K]
misconception: [B]
input: [text]
object: [vm, esxi]
tool: [vcf-operations, esxtop]
knowledge:
  - vsphere/technology/storage/troubleshooting/vm-storage-performance-checks
  - vsphere/technology/storage/troubleshooting/host-storage-latency
  - vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
  - vsphere/technology/storage/concepts/esxi-storage-latency-stack
  - vsphere/technology/storage/concepts/snapshot-impact
knowledge_main: vsphere/technology/storage/troubleshooting/vm-storage-performance-checks
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05"
misconception_type: [consumption-as-contention, average-hides-worst]
pair: "0184"
status: draft
```
