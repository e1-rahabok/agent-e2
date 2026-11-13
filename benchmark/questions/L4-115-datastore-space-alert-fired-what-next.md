# Datastore space alert fired: what next

## Prompt
- A VMFS datastore, DS-PROD-07, has a capacity of 20,000 GB. The alert "Datastore consumption" (red, used space above 90%) fired this morning. Used: 18,200 GB, free: 1,800 GB.
- The datastore holds 61 VMs. The administrator has these facts:
  - Three thin-provisioned VMs have 4,500 GB of provisioned space that is not written yet. Their written data grows by about 15 GB per day, together.
  - One VM has a snapshot taken 5 weeks ago. The delta is 1,100 GB and grows by about 160 GB per day, because a database writes under it. The change that the snapshot protected was validated last week.
  - 12 powered-off VMs of a disaster recovery test sit on the datastore. Each has 16 GB of configured memory and no memory reservation. They will all be powered on in 3 days.
  - Ordering and delivering more capacity for this datastore takes 10 days. Space can also be freed by deleting orphaned VMDKs (about 300 GB, confirmed) after the owner approves.
  - Latency on the datastore is normal, and the array is all-flash.
- The on-call engineer proposes to start the capacity request and wait, because 1,800 GB at 175 GB per day (160 for the snapshot, 15 for the thin disks) lasts 10.3 days, about as long as the 10-day delivery time.

Is that plan safe? Give your own estimate of the time left, the order of what you would do, and why the datastore can fail before the projection says it will.

## Likely wrong answer
"Yes: 10.3 days is more than 10 days, so start the request and wait." This uses the trend alone, and ignores the thin disks, the swap files at power-on and the fact that a snapshot is the cheapest space to give back.

## Expected key points
- The plan is not safe. The projection is a trend, and several items can fill the datastore faster.
- Swap: each of the 12 VMs creates a swap file of configured memory minus reservation at power-on: 12 x 16 GB = 192 GB, in 3 days. After 3 days free space is 1,800 - 3 x 175 = 1,275 GB, minus 192 GB = 1,083 GB, which lasts 1,083 / 175 = about 6.2 days. The total is about 9.2 days, less than the 10-day delivery time, with no time left to install (the engineer's 10.3 days is a trend alone).
- Thin disks: 4,500 GB of unwritten thin space is more than the 1,800 GB free. The datastore can fill with no new VM and with no trend in the history, if the thin disks write.
- Order: first remove the snapshot (after the change is validated): it returns 1,100 GB at once and stops 160 GB per day of growth, which is most of the growth (175 GB per day falls to 15 GB per day). Then reclaim the orphaned VMDKs (300 GB, after approval). Start the capacity request now in parallel, because the delivery time is fixed.
- The alert is a single symptom (used space) with no activity gate: space is availability, so a full datastore stops the VMs that write, whatever the load. At 90% it is a prompt to run the headroom checks (free space now, snapshots, thin disks, swap, growth, reclaim), not proof of 10 days.
- After the snapshot is gone, the growth is 15 GB per day: free space (about 1,800 + 1,100 = 2,900 GB, minus 192 GB of swap) lasts months at 15 GB per day, but the thin disks still need an overcommit decision.

## Notes
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
answer_type: judged
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
status: draft
```
