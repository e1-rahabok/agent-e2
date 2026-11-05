# Datastore read IOPS above virtual disk read IOPS

## Prompt
- One VM has a single virtual disk on a VMFS datastore.
- For this VM, the datastore read IOPS are consistently higher than its virtual disk read IOPS.
- The datastore read throughput equals the virtual disk read throughput.

What is the most likely cause, and how do you confirm it?

## Likely wrong answer
"Another VM on the same datastore adds the extra IOPS."

## Expected key points
- The VM most likely has a snapshot.
- Reads must check every file in the snapshot chain: the datastore sees extra read IOs that return no data, so read IOPS rise while throughput stays equal.
- Virtual disk metrics exclude snapshot IO; datastore metrics include it.
- Confirm: check the VM for snapshots (Disk Space | Snapshot in VCF Operations, or the snapshot manager).

## Notes
- Previous id: question-0045 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "45"
title: "Datastore read IOPS above virtual disk read IOPS"
product: [vsphere]
technology: [storage]
task: troubleshoot
level: 200
answer_type: judged
input: [text]
knowledge:
  - vsphere/technology/storage/concepts/snapshot-impact
  - vsphere/technology/storage/metrics/virtual-motherboard/datastore
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 100-200 allocation (benchmark/design.md, section 3.6)"
status: draft
```
