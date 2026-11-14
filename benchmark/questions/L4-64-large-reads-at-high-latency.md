# Large reads at high latency on a shared datastore

## Prompt
- Datastore DS-PROD07 is a VMFS datastore on an all-flash FC array.
- Every night from 02:00 to 03:00, the backup proxy VM bkp-01 reads from it. In the same hour the database VM db-02 runs its night jobs on the same datastore.
- VCF Operations, 02:00-03:00, virtual disk counters:

| VM | Read IOPS | Read throughput | Read latency |
|---|---|---|---|
| bkp-01 | 400 | 200 MB/s | 7 ms |
| db-02 | 3,000 | 24 MB/s | 1.2 ms |

- On nights without a backup, db-02 reads at 1.1 ms in the same hour.
- The storage team sees 7 ms on an all-flash array and wants to escalate an array problem.

Which statements are correct?

- A. bkp-01 reads in blocks of about 512 KB (200 MB/s ÷ 400 IOPS); db-02 reads in blocks of about 8 KB.
- B. A 512 KB read takes longer to serve than an 8 KB read: 7 ms alone does not show a slow array.
- C. The array is overloaded: 7 ms on bkp-01 is almost 6 times the 1.2 ms of db-02 on the same datastore.
- D. Compare latency only at similar IO sizes: compare bkp-01 with its own past nights.
- E. db-02 is barely affected by the backup: its read latency is 1.2 ms against 1.1 ms on nights without it.
- F. A throughput limit in MB/s on bkp-01's virtual disks is the vSphere setting that caps the backup's load.

## Likely wrong answer
C: comparing the latency of large and small IOs as if they were the same work.

## Expected key points
- Answer: A, B, D, E.
- A: block size = throughput ÷ IOPS: 200 MB/s ÷ 400 = 0.5 MB; 24 MB/s ÷ 3,000 = 8 KB.
- B: the time to move and serve an IO grows with its size. High latency on large IOs is expected, not a fault.
- D: latency is a per-IO time, so a latency comparison is fair only at similar IO sizes.
- E: the VM that matters for performance, db-02, sees almost no change: no sign of contention on the array.
- C is wrong: it compares unlike IOs.
- F is wrong: vSphere offers an IOPS limit per virtual disk, not a throughput limit; with large blocks, an IOPS limit caps the throughput too.

## Notes
- Drafted by Claude 2026-11-12. Counts only after author approval.

## Metadata
```yaml
id: "0180"
title: "Large reads at high latency on a shared datastore"
product: [vsphere, vcf-operations]
technology: [storage]
task: troubleshoot
level: 400
answer_type: deterministic
input: [text]
object: [vm, datastore]
tool: [vcf-operations]
knowledge:
  - vsphere/technology/storage/concepts/storage-dimensions
  - vsphere/technology/storage/metrics/virtual-motherboard/iops
  - vsphere/technology/storage/metrics/datastore/storage-io-control
knowledge_main: vsphere/technology/storage/metrics/virtual-motherboard/iops
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
answer: [A, B, D, E]
misconception: [C]
misconception_type: [unit-and-normalization]
status: draft
```
