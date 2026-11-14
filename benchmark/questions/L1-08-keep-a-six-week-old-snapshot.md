# Keep a six-week-old snapshot?

## Prompt
- erp-db-01 has one 2 TB thin virtual disk. The base disk held about 1.1 TB when the snapshot was taken.
- A snapshot was taken two weeks ago before an upgrade, "to roll back if needed". The upgrade went well.
- VCF Operations: Disk Space | Snapshot | Virtual Machine Used for erp-db-01 is 1.4 TB, and it grows by about 10 GB a day.
- Its datastore, DS-ERP, has 10 TB of capacity and 5 TB used. Other VMs on DS-ERP have thin disks too.
- The DBA asks to keep the snapshot one more month, just in case.

Is it safe to keep it? What do you advise?

## Likely wrong answer
"A snapshot is small and only records changes: keep it as a safety net for another month."

## Expected key points
- No: remove it now, once the change is validated. A snapshot is not a backup: it depends on the base disk it sits on.
- Performance: reads must check the snapshot chain, adding IO and latency to the database while the snapshot exists.
- Remove it off-peak: consolidation reads and writes the delta and stuns the VM briefly at the end.
- Broadcom KB 318825 (was VMware KB 1025279), "Best practices for using VMware snapshots in the vSphere environment" (https://knowledge.broadcom.com/external/article/318825): do not keep a single snapshot more than 72 hours; snapshots are change logs on the base disk, not a backup.

## Notes
- The datastore size and disk size are placed for distraction. The key point is snapshot should not be kept for days.

## Metadata
```yaml
id: "0187"
title: "Keep a six-week-old snapshot?"
product: [vsphere, vcf-operations]
technology: [storage]
task: decide-capacity
level: 100
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
source_path: "Drafted by Claude 2026-11-12"
misconception_type: [cumulative-vs-current]
status: reviewed
```
