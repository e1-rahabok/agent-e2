# Datastore read IOPS above virtual disk read IOPS

## Prompt
- One VM has a single virtual disk on a VMFS datastore. It is the only VM with files on that datastore.
- In the vSphere Client, for the past week:
  - the VM's datastore read IOPS are consistently about 30% higher than its virtual disk read IOPS;
  - the datastore read throughput equals the virtual disk read throughput.

What is the most likely cause, and how do you confirm it?

## Likely wrong answer
"Another VM or a background job on the datastore adds the extra IOPS." Or: "One of the two counters is wrong."

## Expected key points
- The VM most likely has a snapshot.
- Reads must check every file in the snapshot chain: the datastore sees extra read IOs that return no data, so read IOPS rise while throughput stays equal.
- Virtual disk counters exclude snapshot IO; the VM's datastore counters include it.
- Confirm: look for a snapshot on the VM (Snapshot Manager, or Disk Space | Snapshot in VCF Operations). Without a snapshot the two read IOPS lines overlap.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Revised 2026-11-12 for question set 1.0: the only VM on the datastore, so another VM cannot explain it. Counts only after author approval.

## Metadata
```yaml
id: "0045"
title: "Datastore read IOPS above virtual disk read IOPS"
product: [vsphere]
technology: [storage]
task: troubleshoot
level: 200
answer_type: judged
input: [text]
object: [vm, datastore]
tool: [vcenter]
knowledge:
  - vsphere/technology/storage/concepts/snapshot-impact
  - vsphere/technology/storage/metrics/virtual-motherboard/datastore
knowledge_main: vsphere/technology/storage/concepts/snapshot-impact
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05"
misconception_type: [same-name-other-object]
status: draft
```
