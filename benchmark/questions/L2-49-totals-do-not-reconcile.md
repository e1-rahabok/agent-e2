# Why VM, datastore and cluster totals differ

## Prompt
- You add up the disk IOPS of all VMs in a cluster.
- The total differs from the sum of the datastore IOPS, and from the sum of the host IOPS.

Why? Choose all that apply.

- A. A VM with several virtual disks can span several datastores.
- B. A LUN is typically presented to several hosts, and can be presented to several clusters.
- C. One of the metrics must be wrong.
- D. Each value is correct from its own vantage point.

## Likely wrong answer
C: concluding that a metric is broken.

## Expected key points
- Answer: A, B, D.
- The relationships are many-to-many: a VM spans datastores, a datastore hosts many VMs, a LUN is mounted by many hosts and clusters.
- So totals across VM, datastore, host and cluster do not reconcile, and each value is still correct from its vantage point.
- Snapshots add datastore IO that virtual disk metrics exclude, another reason for a gap.

## Notes
- Previous id: question-0049 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "49"
title: "Why VM, datastore and cluster totals differ"
product: [vsphere]
technology: [system, storage]
task: explain-mechanism
level: 200
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/foundations/object-relationships
  - vsphere/technology/storage/concepts/snapshot-impact
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 100-200 allocation (benchmark/design.md, section 3.6)"
answer: [A, B, D]
trap: [C]
status: draft
```
