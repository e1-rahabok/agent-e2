# Shared disk IOPS drop to zero on one cluster node

## Prompt
- Two Linux VMs, pg-ha-a and pg-ha-b, run an active/passive database cluster: one node at a time mounts the database file system.
- They share three VMDKs on datastore DS-PG07, set to multi-writer sharing. Each VM also has its own OS disk. Both VMs were powered on all week.
- VCF Operations, last 7 days, IOPS of the shared data disk scsi1:0 on each VM:
  - pg-ha-a: 3,000 to 5,000 until Wednesday 03:12, then 0 to the end of the chart.
  - pg-ha-b: no values until Wednesday 03:12, then 3,000 to 5,000.
- The OS disks of both VMs show a few IOPS all week.
- pg-ha-a, Disk Space: Not Shared 140 GB, Snapshot Space 25 GB (a snapshot of its OS disk, taken before a patch).
- The cost team flags pg-ha-a as idle since Wednesday. The monitoring team opens a ticket: data collection for pg-ha-b was broken before Wednesday.

Which statements are correct?

- A. The database moved from pg-ha-a to pg-ha-b in a failover at about 03:12 on Wednesday.
- B. pg-ha-a shows 0 on the shared disk after 03:12 because that is how a passive node reports.
- C. pg-ha-b's missing values before 03:12 show that data collection for it was broken until then.
- D. pg-ha-a has had no disk work since Wednesday, so it is a candidate to reclaim.
- E. pg-ha-a's Active Not Shared is 115 GB: the space only it owns, without the snapshot space.
- F. pg-ha-a's Not Shared includes the three shared disks, because each VM sees them as its own.
- G. A multi-writer disk's per-VM IOPS cannot be used at all; only datastore counters show its load.
- H. Adding the two VMs' IOPS on the shared disk counts its load twice, once for each VM.

## Likely wrong answer
"pg-ha-a has been idle since Wednesday, reclaim it" (D), or "no data before 03:12, so collection on pg-ha-b was broken" (C).

## Expected key points
- Answer: A, B, E.
- A is correct: in an active/passive pair the active node carries the shared disk's IO; the IO moves from pg-ha-a to pg-ha-b at 03:12.
- B is correct: after a failover the passive VM reports 0 for the shared disk (vCenter returns 0, not blank).
- C is wrong: the misconception. The VM that later became active reported blank while it was passive, before it took over; this is how the pair reports, not a collection fault.
- D is wrong: the wrong action. pg-ha-a is the passive node of a running cluster, and its OS disk is active all week.
- E is correct: Active Not Shared = Not Shared - Snapshot Space = 140 - 25 = 115 GB; snapshots count as non-active.
- F is wrong: Not Shared is the space of the VMDKs and RDMs owned only by this VM; the multi-writer disks are shared.
- G is wrong: the over-correction. The per-VM values are readable: the active node's IOPS on the shared disk are the disk's load, and the passive node's 0 adds nothing.
- H is wrong: at any time only the active node reports the IO; the other reports blank or 0, so the sum counts the load once.

## Notes
- The knowledge base holds the reporting pattern (passive 0 after a failover, blank before it took over) as an observation from VCF Operations charts. The stem states an active/passive cluster because the observation is of an active/passive pair; an active-active cluster on multi-writer disks is not covered by it.

## Metadata
```yaml
id: "0463"
title: "Shared disk IOPS drop to zero on one cluster node"
product: [vsphere, vcf-operations]
technology: [storage]
task: read-metric
level: 400
answer_type: deterministic
input: [text]
object: [vm, datastore]
tool: [vcf-operations]
knowledge:
  - vsphere/technology/storage/metrics/virtual-motherboard/virtual-disk
knowledge_main: vsphere/technology/storage/metrics/virtual-motherboard/virtual-disk
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-15, question bank audit gap: vsphere/technology/storage/metrics/virtual-motherboard/virtual-disk"
answer: [A, B, E]
misconception: [C, D]
misconception_type: []
status: draft
```
