# Datastore space alert fired: what next

## Prompt
- A VMFS datastore, DS-PROD-07, has a capacity of 20,000 GB. The alert "Datastore consumption" (red, used space above 90%) fired this morning. Used: 18,200 GB, free: 1,800 GB.
- The datastore holds 61 VMs. The administrator has these facts:
  - Three thin-provisioned VMs have 4,500 GB of provisioned space that is not written yet. Their written data grows by about 15 GB per day, together.
  - One VM, on thick-provisioned disks, has a snapshot taken 5 weeks ago. The delta is 1,100 GB; since a database load started on the VM 4 days ago, it grows by about 160 GB per day. The change that the snapshot protected was validated last week.
  - 12 powered-off VMs of a disaster recovery test sit on the datastore. Each has 16 GB of configured memory and no memory reservation. They will all be powered on in 3 days.
  - Ordering and delivering more capacity for this datastore takes 10 days. Space can also be freed by deleting orphaned VMDKs (about 300 GB, confirmed) after the owner approves.
  - Latency on the datastore is normal, and the array is all-flash.
- The on-call engineer proposes to start the capacity request and wait, because 1,800 GB at 175 GB per day (160 for the snapshot, 15 for the thin disks) lasts 10.3 days, about as long as the 10-day delivery time.

Which statements are correct?

- A. The 10.3-day projection is longer than the 10-day delivery, so starting the request and waiting is safe.
- B. Powering on the 12 DR VMs creates about 192 GB of swap files, since they have no memory reservation.
- C. The DR VMs need no new space at power-on, because their files already sit on the datastore.
- D. Under the engineer's plan, with those swap files counted, the datastore fills in about 9 days, before the new capacity arrives.
- E. The 4,500 GB of unwritten thin space exceeds the 1,800 GB free, so the datastore can fill with no new VM and no warning in the trend.
- F. The snapshot should stay until the new capacity arrives, because it still protects the database.
- G. Removing the snapshot comes first: it returns about 1,100 GB at once and stops 160 of the 175 GB per day of growth.
- H. The thin disks count only through their 15 GB per day of growth; their provisioned size does not matter.
- I. Start the capacity request now, in parallel, because the 10-day delivery time does not shrink.
- J. At 91% used the all-flash datastore is already slower, so the alert is a performance warning.
- K. A full datastore stops any VM whose thin disk or snapshot must grow to write, whatever its load.

## Likely wrong answer
- A: "10.3 days is more than 10 days, so start the request and wait."
- C: "The DR VMs are already on the datastore, so powering them on takes no space."

## Expected key points
- Answer: B, D, E, G, I, K.
- A is false: the misconception; the projection is a trend alone. It ignores the swap files at power-on and the unwritten thin space, and that a snapshot is the cheapest space to give back.
- B is true: each VM creates a swap file of configured memory minus reservation at power-on: 12 x 16 GB = 192 GB, in 3 days.
- C is false: a powered-off VM holds no swap file; it is created at each power-on, so the DR test needs 192 GB of free space at that moment.
- D is true: after 3 days 1,800 - 3 x 175 = 1,275 GB, minus 192 GB = 1,083 GB, which lasts 1,083 / 175 = about 6.2 days: about 9.2 days in total, under the 10-day delivery time with no time left to install. The plan is not safe.
- E is true: provisioned minus used of the thin disks is space they can claim at any time; unwritten thin space larger than free space can fill the datastore with no trend in the history.
- F is false: the change the snapshot protected was validated last week; a snapshot kept beyond its change window is a space risk and a performance cost, and the delta grows with every write.
- G is true: snapshots before thin disks, because they grow fastest and are the easiest to remove; the base disks are thick, so the merge writes into space they already hold and the delta's 1,100 GB returns; growth falls from 175 to 15 GB per day. Then the orphaned VMDKs (300 GB, after approval).
- H is false: the 4,500 GB of unwritten thin space is a reservation in effect against the free space; the thin disks still need an overcommit decision after the snapshot is gone.
- I is true: the delivery time is fixed, so the request starts now while space is freed.
- J is false: space does not change speed on all-flash storage; it threatens availability. The latency is normal.
- K is true: space is availability: a VM whose thin disk or snapshot must grow cannot write when the datastore is full, whatever the load; hence the alert has no activity gate. A thick disk without a snapshot writes into space it already holds.

## Notes
- Converted from judged to multiple choice (Q199 F, 2026-11-14). Review 2026-11-14: the snapshot VM's disks are stated thick (so removing the snapshot returns the delta's space, option G), and the 160 GB per day started 4 days ago (5 weeks at that rate would make a delta far above 1,100 GB). Option K names the VMs that stop (thin disk or snapshot that must grow), as the knowledge file does.
- Public source: swap file size = configured memory minus memory reservation, created at power-on and deleted at power-off (vSphere Resource Management, "Swap File Location and VM swap files", Broadcom TechDocs, vSphere 9.0). A snapshot delta grows with every write to the disk under it, and a snapshot should not be kept longer than its change (vSphere Virtual Machine Administration, "Best practices for virtual machine snapshots", Broadcom TechDocs, vSphere 9.0; Broadcom KB 313399 "Best practices for using snapshots in the vSphere environment"). A thin disk can claim its provisioned space at any time (vSphere Storage, "About Virtual Disk Provisioning Policies", Broadcom TechDocs, vSphere 9.0).
- Knowledge file logic: vsphere/object-types/datastore/datastore-alerts, "Datastore consumption" (red only, space headroom flow); vsphere/technology/storage/datastore-space-headroom, checks 3 to 8 and "Order rationale": snapshots before thin disks, because they grow fastest and are the easiest to remove; reality overrides the projection.
- Why one answer: the swap files are a documented formula, the thin gap is arithmetic, and the snapshot is the largest part of the growth, so the 10.3-day trend drops under the delivery time once the swap files are counted. The key accepts any order that starts with the snapshot and the reclaim, as long as the reasons are given.
- Debatable risk: the order of the actions after the snapshot is a judgment; the key asks for the reasons, not for one fixed list. Time left: the engineer's 10.3 days against about 9.2 days (with the DR swap) are estimates; the judge should accept 9 to 10 days if the swap and the growth are used. The author's alert design (single symptom, red only) is not asked for; the prompt gives it.

## Metadata
```yaml
id: "0343"
title: "Datastore space alert fired: what next"
product: [vsphere, vcf-operations]
technology: [storage]
task: decide-capacity
level: 400
answer_type: deterministic
answer: [B, D, E, G, I, K]
misconception: [A, C]
input: [text]
object: [datastore, vm]
tool: [vcenter, vcf-operations]
knowledge:
  - vsphere/object-types/datastore/datastore-alerts
  - vsphere/technology/storage/datastore-space-headroom
knowledge_main: vsphere/technology/storage/datastore-space-headroom
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
misconception_type: [cumulative-vs-current]
pair: "0080"
status: draft
```
