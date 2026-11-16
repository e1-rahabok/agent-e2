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
- B. Large IOs raise latency by themselves, so bkp-01's 7 ms alone does not show a slow array.
- C. The array is overloaded: 7 ms on bkp-01 is almost 6 times the 1.2 ms of db-02 on the same datastore.
- D. bkp-01's low IOPS at high throughput means large blocks: check them against the block size its backup job is set to use.
- E. db-02 is barely affected by the backup: 1.2 ms read latency against 1.1 ms on nights without it.
- F. With Storage I/O Control on, DS-PROD07's Normalized Latency would read about 7 ms for this hour.

## Likely wrong answer
C: comparing the latency of large and small IOs as if they were the same work.

## Expected key points
- Answer: A, B, D, E.
- A is correct: block size = throughput ÷ IOPS: 200 MB/s ÷ 400 = 0.5 MB; 24 MB/s ÷ 3,000 = 8 KB.
- B is correct: Storage I/O Control's Normalized Latency discounts the high latency that large IOs cause, so large-block workloads do not make a datastore look slower than it is. High latency on 512 KB reads is expected, not a fault; judge it against bkp-01's own past nights, not against db-02's 8 KB reads.
- C is wrong: the misconception. It compares unlike IOs.
- D is correct: low IOPS with high throughput means large blocks (200 MB/s ÷ 400 = 512 KB); compare that with the block size planned for the backup, which tells whether the 7 ms comes from the job's own design.
- E is correct: the VM that matters for performance, db-02, sees almost no change: no sign of contention on the array.
- F is wrong: Normalized Latency is device latency weighted by IO count over all hosts and VMs, and adjusted for IO size. Even unadjusted, 400 reads at 7 ms against 3,000 at 1.2 ms give about 1.9 ms ((400 × 7 + 3,000 × 1.2) ÷ 3,400); the size adjustment lowers it further, and it leaves out kernel queuing.

## Notes
- Synthetic, 2026-11-12. Counts only after author approval.
- Audit 2026-11-15: F (no throughput limit in vSphere, a third copy after 0424 F and 0183 F) replaced by Storage I/O Control Normalized Latency (IO-count weighted, size-adjusted); E shortened (truth unchanged). Key unchanged: A, B, D, E.
- Re-review 2026-11-16: B and D rested on an inference (latency grows with IO size; compare only at similar sizes). B now paraphrases storage-io-control ("Normalized Latency discounts high latency caused by large IOs"); D replaced by the block-size check of iops ("Low IOPS with high throughput: large blocks. Compare with the planned block size."). Key unchanged: A, B, D, E.
- Open (knowledge base): no knowledge file states as a mechanism line that per-IO latency grows with IO size; B and C rest on the size adjustment of Normalized Latency in storage-io-control.

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
source_path: "Synthetic, 2026-11-12"
answer: [A, B, D, E]
misconception: [C]
misconception_type: [unit-and-normalization]
status: draft
```
