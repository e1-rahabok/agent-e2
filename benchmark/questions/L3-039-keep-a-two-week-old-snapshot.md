# Keep a two-week-old snapshot?

## Prompt
- erp-db-01 has one 2 TB thin virtual disk. The base disk held about 1.1 TB when the snapshot was taken.
- A snapshot was taken two weeks ago, "to roll back if needed", before an upgrade that rewrote most of the database. The upgrade went well.
- VCF Operations: Disk Space | Snapshot | Virtual Machine Used for erp-db-01 is 1.4 TB, and it grows by about 10 GB a day.
- Its datastore, DS-ERP, is a VMFS datastore with 10 TB of capacity and 5 TB used. Other VMs on DS-ERP have thin disks too.
- The DBA asks to keep the snapshot one more month, just in case.

Which statements are correct?

- A. A snapshot only records changes, so it stays small and is a cheap safety net for one more month.
- B. Now that the upgrade is validated, remove the snapshot instead of keeping it another month.
- C. A snapshot is not a backup: its delta file is of no use without the base disk under it.
- D. While the snapshot exists, reads of the database disk must check the files of the snapshot chain, adding IO.
- E. The snapshot costs writes more than reads, because every write must walk the whole snapshot chain.
- F. Removing the snapshot merges its changes into the base disk and stuns the VM, so plan it off-peak.
- G. While the snapshot exists, only the datastore pays for it; the VM's CPU counters are unaffected.
- H. At about 10 GB a day, the growth of this snapshot alone fills DS-ERP within the month.
- I. Broadcom's best practice is not to keep a single snapshot for more than 72 hours.

## Answers
B, C, D, F, I

## Explanation
- A is wrong: the delta grows with every write to the disk under it; it is already 1.4 TB, more than the 1.1 TB the base disk held.
- B is correct: remove a snapshot once the change it protects is validated; a snapshot kept beyond its change window costs space and performance.
- C is correct: a snapshot is not a backup; it is a change log on top of the base disk, not a copy of it. Broadcom KB 318825 says not to use snapshots as backups.
- D is correct: with a redo-log snapshot on VMFS, reads must check the files of the chain, so the datastore sees extra read IO.
- E is wrong: writes go to the newest delta file; reads are the ones that check the chain.
- F is correct: consolidation copies the delta into the base disk, and snapshot consolidate is one of the causes of a checkpoint stun; a large delta on a busy VM lengthens the stun (Broadcom KB 323397), and the merge adds IO.
- G is wrong: snapshots are a cause of Co-stop and Other Wait on the VM, and its System time rises as the kernel traverses the snapshot chain.
- H is wrong: 30 days × 10 GB is about 300 GB against 5 TB free; the risk is the snapshot's age and IO cost, not this month's space.
- I is correct: Broadcom KB 318825, "Do not retain a single snapshot for more than 72 hours."
- Misconception: A: "The snapshot is just a small change log; keep it a month as a safety net, it does no harm."

## Notes
- 2026-11-16 (author, Q-E2-251): level 100 to 300, as the reviewers read it. A new Level 100 basics question for the guard is still to write.
- The datastore size and disk size are placed for distraction. The key point is that a snapshot should not be kept for days.
- Vendor sources: Broadcom KB 318825, Best practices for using VMware snapshots in the vSphere environment (was VMware KB 1025279), https://knowledge.broadcom.com/external/article/318825 (72 hours; not a backup); Broadcom KB 323397, Snapshot removal stops a virtual machine for long time, https://knowledge.broadcom.com/external/article/323397 (stun during consolidation).
- Option I rests on Broadcom KB 318825 only (the 72-hour rule): no knowledge file states it. URL above.
- Review 2026-11-14: the prompt names DS-ERP as VMFS, so option D (reads check the chain of a redo-log snapshot) is decidable; it would not hold on vSAN ESA. Option F no longer says when the stun happens: KB 323397 says the VM is stunned "for the duration of the consolidation" and also describes a helper snapshot that takes new writes while the delta merges, so the timing was not decidable; that the VM is stunned, longer with a large delta and heavy IO, is.
- Audit 2026-11-15: title fixed to two weeks (the prompt's age); the stem says the upgrade rewrote most of the database, so a 1.4 TB delta in two weeks is plausible; G (delete rolls back, decided only by KB 371714) replaced by the snapshot's CPU cost (snapshot-impact, CPU); key points C and F cite the knowledge base; level 100 -> 300: nothing here names a counter, it applies snapshot practice and a space check. Key unchanged.

## Metadata
```yaml
id: "0187"
title: "Keep a two-week-old snapshot?"
product: [vsphere, vcf-operations]
technology: [storage]
task: decide-capacity
level: 300                      # Q-E2-251, author 2026-11-16: relabelled as written (was 100)
answer_type: deterministic
misconception: [A]
input: [text]
object: [vm, datastore]
tool: [vcf-operations]
knowledge:
  - vsphere/technology/storage/datastore-space-headroom
  - vsphere/technology/storage/concepts/snapshot-impact
  - vsphere/technology/storage/metrics/virtual-motherboard/disk-space
  - vsphere/object-types/vm/vmotion
  - sp5-framework/capacity/reclamation
knowledge_main: vsphere/technology/storage/datastore-space-headroom
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-12"
misconception_type: [cumulative-vs-current]
status: draft                     # reviewed as a free-text question; converted to multiple choice 2026-11-14 (Q-E2-199): review again
```
