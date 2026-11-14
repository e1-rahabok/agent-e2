# Datastore read IOPS above virtual disk read IOPS

## Prompt
- One VM has a single virtual disk on a VMFS datastore. It is the only VM with files on that datastore.
- In the vSphere Client, for the past week:
  - the VM's datastore read IOPS are consistently about 30% higher than its virtual disk read IOPS;
  - the datastore read throughput equals the virtual disk read throughput.

Which statements are correct?

- A. The most likely cause is a snapshot on this VM, kept through the past week.
- B. Another VM or a background job on the datastore adds the extra read IOPS.
- C. One of the two counters is wrong, since the same reads cannot give two IOPS values.
- D. The VM's virtual disk counters include snapshot IO, so the gap must come from outside the VM.
- E. The extra datastore reads carry data from older delta files, so they add to the VM's read throughput.
- F. If a snapshot caused it, write IOPS would show the same 30% gap, since writes walk the chain too.
- G. On a vSAN ESA datastore with a native snapshot, the VM would show this same read IOPS gap.
- H. Paging to the VM's swap file on the datastore explains the extra read IOPS.
- I. Check the VM for a snapshot; with none, the datastore and virtual disk read IOPS lines overlap.

## Likely wrong answer
- B: "Something else on that datastore is generating the extra IOs."
- C: "The counters don't agree, so one of them is broken."

## Expected key points
- Answer: A, I.
- A is true: with a redo-log snapshot, reads must check every file of the chain, so the datastore sees extra read IOs.
- B is false: the VM is the only one with files on the datastore, and the VM's datastore counters count only this VM's IO.
- C is false: the two counters sit at different levels; the datastore level includes snapshot IO, the virtual disk level does not.
- D is false: virtual disk counters exclude snapshot IO and space; the VM's datastore counters include them.
- E is false: the extra reads of the chain return no data, which is why read throughput stays equal while read IOPS rise.
- F is false: writes go to the newest delta file; the chain lookups hit reads.
- G is false: vSAN ESA native snapshots keep no delta chain (a B-tree maps each block), so this read signature does not apply.
- H is false: swap reads move data, so datastore read throughput would rise above the virtual disk throughput; it stays equal.
- I is true: confirm in Snapshot Manager or with Disk Space | Snapshot in VCF Operations; without a snapshot the two read IOPS lines overlap.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Revised 2026-11-12 for question set 1.0: the only VM on the datastore, so another VM cannot explain it. Counts only after author approval.
- The old key points on the mechanism (extra reads return no data; virtual disk counters exclude snapshot IO) are tested by the false options D and E, to keep the number of correct options low.
- Converted from judged to multiple choice (Q199 F, 2026-11-14).

## Metadata
```yaml
id: "0045"
title: "Datastore read IOPS above virtual disk read IOPS"
product: [vsphere]
technology: [storage]
task: troubleshoot
level: 200
answer_type: deterministic
answer: [A, I]
misconception: [B, C]
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
