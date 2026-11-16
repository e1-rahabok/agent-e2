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
- B. If DS-PROD-07 sits on a thin LUN, the free space of the array pool behind it must be checked too.
- C. The DR VMs need no new space at power-on, because their files already sit on the datastore.
- D. Counting the DR VMs' swap files, the engineer's plan fills the datastore in about 9 days, before delivery.
- E. The 4,500 GB of unwritten thin space, above the 1,800 GB free, can fill the datastore with no new VM added.
- F. The snapshot should stay until the new capacity arrives, because it still protects the database.
- G. Removing the snapshot comes first: it returns about 1,100 GB at once and stops 160 of the 175 GB per day of growth.
- H. The thin disks count only through their 15 GB per day of growth; their provisioned size does not matter.
- I. Start the capacity request now, in parallel, because the 10-day delivery time does not shrink.
- J. At 91% used the all-flash datastore is already slower, so the alert is a performance warning.
- K. A full datastore stops any VM whose thin disk or snapshot must grow to write, whatever its load.

## Answers
B, D, E, G, I, K

## Explanation
- A is wrong: the misconception; the projection is a trend alone. It ignores the swap files at power-on and the unwritten thin space, and that a snapshot is the cheapest space to give back.
- B is correct: on an array with thin LUNs the datastore can show room the array no longer has; when the thin LUN has no physical space left, the host pauses the VMs. Read the array's free space as well as the datastore's.
- C is wrong: a powered-off VM holds no swap file; each VM creates one of configured memory minus reservation at power-on, so the DR test needs 12 x 16 GB = 192 GB of free space at that moment.
- D is correct: the DR VMs' swap files take 12 x 16 GB = 192 GB at power-on. After 3 days 1,800 - 3 x 175 = 1,275 GB, minus 192 GB = 1,083 GB, which lasts 1,083 / 175 = about 6.2 days: about 9.2 days in total, under the 10-day delivery time with no time left to install. The plan is not safe.
- E is correct: provisioned minus used of the thin disks is space they can claim at any time; unwritten thin space larger than free space can fill the datastore with no trend in the history.
- F is wrong: the change the snapshot protected was validated last week; a snapshot kept beyond its change window is a space risk and a performance cost, and the delta grows with every write.
- G is correct: snapshots before thin disks, because they grow fastest and are the easiest to remove; the base disks are thick, so the merge writes into space they already hold and the delta's 1,100 GB returns; growth falls from 175 to 15 GB per day. Then the orphaned VMDKs (300 GB, after approval).
- H is wrong: the 4,500 GB of unwritten thin space is a reservation in effect against the free space; the thin disks still need an overcommit decision after the snapshot is gone.
- I is correct: the delivery time is fixed, so the request starts now while space is freed.
- J is wrong: space does not change speed on all-flash storage; it threatens availability. The latency is normal.
- K is correct: space is availability: a VM whose thin disk or snapshot must grow cannot write when the datastore is full, whatever the load; hence the alert has no activity gate. A thick disk without a snapshot writes into space it already holds.
- Misconception: A: "10.3 days is more than 10 days, so start the request and wait." - C: "The DR VMs are already on the datastore, so powering them on takes no space."

## Notes
- Review 2026-11-14: the snapshot VM's disks are stated thick (so removing the snapshot returns the delta's space, option G), and the 160 GB per day started 4 days ago (5 weeks at that rate would make a delta far above 1,100 GB). Option K names the VMs that stop (thin disk or snapshot that must grow), as the knowledge file does.
- Knowledge file logic: vsphere/object-types/datastore/datastore-alerts, "Datastore consumption" (red only, space headroom flow); vsphere/technology/storage/datastore-space-headroom, checks 1 to 8 and "Order rationale": thin LUNs on the array (step 1), snapshots before thin disks, because they grow fastest and are the easiest to remove; reality overrides the projection. Every fact the key uses is in these files and in vsphere/technology/storage/concepts/vm-files (swap file size, created at power-on); the snapshot practice is also in Broadcom KB 318825, https://knowledge.broadcom.com/external/article/318825.
- Why one answer: the swap files are a documented formula, the thin gap is arithmetic, and the snapshot is the largest part of the growth, so the 10.3-day trend drops under the delivery time once the swap files are counted. The 9.2 days of D and the 10.3 days of the engineer are estimates; D says "about 9 days", before the 10-day delivery.
- Audit 2026-11-15: B (the swap file size, tested by 0181 and 0296) replaced by the thin-LUN check of datastore-space-headroom step 1, which no other question tests; D and E shortened (length cue), D no longer leans on B. Judge-era notes removed. Key unchanged.

## Metadata
```yaml
id: "0343"
title: "Datastore space alert fired: what next"
product: [vsphere, vcf-operations]
technology: [storage]
task: decide-capacity
level: 400
answer_type: deterministic
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
