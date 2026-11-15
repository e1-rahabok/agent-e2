# Datastore read IOPS above virtual disk read IOPS

## Prompt
- One VM has a single virtual disk on a VMFS datastore. It is the only VM with files on that datastore.
- In the vSphere Client, for the past week:
  - the VM's datastore read IOPS are consistently about 30% higher than its virtual disk read IOPS;
  - the datastore read throughput equals the virtual disk read throughput.

Which statements are correct?

- A. A snapshot on this VM, kept through the week, explains the gap.
- B. One of the two counters is faulty: the same reads cannot give two IOPS values.
- C. The VM's virtual disk read IOPS include the reads to its snapshot files.
- D. The extra datastore reads are lookups through the snapshot chain that return no data.
- E. A snapshot raises the VM's datastore write IOPS by the same share as its read IOPS.
- F. A native snapshot on a vSAN ESA datastore would show the same read IOPS gap.
- G. Reads from the VM's swap file explain the extra datastore read IOPS.
- H. A datastore read IOPS below the virtual disk read IOPS would also point to a snapshot.
- I. Move the VM to a faster datastore to remove the extra read IOPS.

## Likely wrong answer
- B: "The counters don't agree, so one of them is broken."

## Expected key points
- Answer: A, D.
- A is true: with a redo-log snapshot (VMFS delta disk), reads must check the files of the chain, so the datastore sees extra read IOs. Confirm in Snapshot Manager or with Disk Space | Snapshot in VCF Operations; without a snapshot the two read IOPS lines overlap.
- B is false: the two counters sit at different levels; the datastore level includes snapshot IO, the virtual disk level does not.
- C is false: virtual disk counters exclude snapshot IO and space; the VM's datastore counters include them.
- D is true: the chain lookups return no data, which is why read throughput stays equal while read IOPS rise.
- E is false: writes go to the newest delta file; the chain lookups hit reads, so writes are less affected.
- F is false: vSAN ESA native snapshots keep no delta chain (a B-tree maps each block), so this read signature does not apply.
- G is false: swap reads move data, so datastore read throughput would rise above the virtual disk throughput; it stays equal.
- H is false: a datastore value below the virtual disk value comes from RDM disks, which the virtual disk counters include and the datastore counters do not.
- I is false: the extra reads come from the snapshot chain, not from a slow datastore; removing the snapshot once the change is validated removes them.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Revised 2026-11-12 for question set 1.0: the only VM on the datastore, so another VM cannot explain it. Counts only after author approval.
- Converted from judged to multiple choice (Q199 F, 2026-11-14).
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): one fact per option; the mechanism (old E, false) stated positively as D; over-correction H and wrong action I added; old B (another VM) dropped, as the stem rules it out. Key changed from A, I to A, D.

## Metadata
```yaml
id: "0045"
title: "Datastore read IOPS above virtual disk read IOPS"
product: [vsphere]
technology: [storage]
task: troubleshoot
level: 200
answer_type: deterministic
answer: [A, D]
misconception: [B]
input: [text]
object: [vm, datastore]
tool: [vcenter]
knowledge:
  - vsphere/technology/storage/concepts/snapshot-impact
  - vsphere/technology/storage/metrics/virtual-motherboard/datastore
  - vsphere/technology/storage/metrics/virtual-motherboard/virtual-disk
knowledge_main: vsphere/technology/storage/concepts/snapshot-impact
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05"
misconception_type: [same-name-other-object]
status: draft
```
