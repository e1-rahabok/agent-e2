# Keep a six-week-old snapshot?

## Prompt
- erp-db-01 has one 2 TB thin virtual disk. The base disk held about 1.1 TB when the snapshot was taken.
- A snapshot was taken six weeks ago before an upgrade, "to roll back if needed". The upgrade went well.
- VCF Operations: Disk Space | Snapshot | Virtual Machine Used for erp-db-01 is 1.4 TB, and it grows by about 30 GB a day.
- Its datastore, DS-ERP, has 10 TB of capacity and 9.5 TB used. Other VMs on DS-ERP have thin disks too.
- The DBA asks to keep the snapshot one more month, just in case.

Is it safe to keep it? What do you advise?

## Likely wrong answer
"A snapshot is small and only records changes: keep it as a safety net for another month."

## Expected key points
- No: remove it now, once the change is validated. A snapshot is not a backup: it depends on the base disk it sits on.
- The delta grows with every write to the disk under it. The 1.4 TB delta is already larger than the 1.1 TB base, and it can grow to the full 2 TB of the disk.
- Space: 0.5 TB free at about 30 GB a day is about 17 days, less than the month asked for, and every other thin disk on DS-ERP competes for the same space. When the datastore is full, VMs that need a new block cannot write: an outage for all of them.
- Performance: reads must check the snapshot chain, adding IO and latency to the database while the snapshot exists.
- Remove it off-peak: consolidation reads and writes the delta and stuns the VM briefly at the end.

## Notes
- Drafted by Claude 2026-11-12 for question set 1.0, Storage slot "a long-lived snapshot" (project/plan.md, M2). Counts only after author approval.
- Vendor document: Broadcom KB 318825 (was VMware KB 1025279), "Best practices for using VMware snapshots in the vSphere environment" (https://knowledge.broadcom.com/external/article/318825): do not keep a single snapshot more than 72 hours; snapshots are change logs on the base disk, not a backup. Nice to know in an answer, not a key point.

## Metadata
```yaml
id: "0187"
title: "Keep a six-week-old snapshot?"
product: [vsphere, vcf-operations]
technology: [storage]
task: decide-capacity
level: 300
answer_type: judged
input: [text]
object: [vm, datastore]
tool: [vcf-operations]
knowledge:
  - vsphere/technology/storage/datastore-space-headroom
  - vsphere/technology/storage/concepts/snapshot-impact
  - vsphere/technology/storage/metrics/virtual-motherboard/disk-space-snapshot
knowledge_main: vsphere/technology/storage/datastore-space-headroom
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12 for the Storage slots (benchmark/design.md, section 3)"
misconception_type: [cumulative-vs-current]
status: draft
```
