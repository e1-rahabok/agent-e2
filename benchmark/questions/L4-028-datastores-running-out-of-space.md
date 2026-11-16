# Which datastores run out of space first

## Prompt
- [The attached export](0080/datastore-space-30-datastores.csv) lists the 30 datastores of one site: type, capacity, used space, the provisioned size of the virtual disks (before the vSAN storage policy), snapshot space, the share of thin virtual disks, the number of VMs, and the vSAN storage policy.
- The storage team asks which datastores will run out of space first, and how far they can overcommit thin disks.

Which statements about the datastores most at risk and the overcommit ratio are correct?

- A. Used % alone understates the risk: thin disks can grow to their provisioned size.
- B. DS-ARCH-01 is the only datastore at risk: it is 95% full, and the others are below 80%.
- C. Rank datastores by unwritten thin space (provisioned - used) against free space (capacity - used).
- D. DS-APP-04, DS-APP-09 and DS-WEB-02 rank highest: their unwritten thin space is two to three times their free space.
- E. DS-DB-03 and DS-DEV-11 hold snapshots of over a quarter of their used space, close to their free space.
- F. DS-ARCH-01 cannot fill by itself: its disks are all thick and it holds no snapshot.
- G. The used space of VSAN-PROD-A counts each virtual disk once; its RAID-1 copy is kept outside it.
- H. The thin disks of VSAN-PROD-A can still claim more space than the datastore has free today.
- I. Keep a vSAN datastore below about 80% used, to leave room to rebuild after a host failure.
- J. The overcommit ratio of a datastore is the provisioned size of its virtual disks divided by its used space.
- K. Snapshot space and VM swap files belong in the provisioned figure when computing the overcommit ratio.
- L. With RAID-1 on vSAN, the overcommit ratio that fits is about half the VMFS one, as each disk is kept twice.
- M. The ratio that fits depends on how fast the thin disks fill against the lead time to expand or reclaim.
- N. Powering off the VMs on DS-APP-04 frees the space that their thin disks can still claim later.

## Answers
A, C, D, E, F, H, I, L, M

## Explanation
- A is correct: thin disks can claim their unwritten space at any time; a datastore at 60% used with thin disks provisioned well above capacity can fill before a nearly full datastore of thick disks.
- B is wrong: DS-ARCH-01 cannot grow by itself, and three thin datastores below 70% used can fill with no new VM added.
- C is correct: compare what can still grow with free space, not used %.
- D is correct: used below 70%, provisioned 160% to 175% of capacity with mostly thin disks. DS-APP-04: (14,336 - 5,160) / (8,192 - 5,160) is about 3.0; DS-APP-09 about 2.4; DS-WEB-02 about 2.8.
- E is correct: 1,720 of 6,390 GB with 1,802 GB free, and 980 of 3,050 GB with 1,046 GB free. A delta grows with every write; remove the snapshots once the change is validated.
- F is correct: 95% used, but all thick and no snapshot. Watch it for new snapshots and swap files; it is not the first to run out.
- G is wrong: vSAN used space holds the copies of the storage policy; FTT=1 with RAID-1 doubles both provisioned and used space (47,900 GB used holds about 23,950 GB of data).
- H is correct: on vSAN the provisioned size is multiplied by the copies: 32,000 GB × 2 = 64,000 GB can be claimed against 47,900 GB used, about 16,100 GB more, against 13,540 GB free. Compared with capacity as on VMFS (32,000 against 61,440 GB) it looks safe.
- I is correct: VSAN-PROD-A is at 78%; above 80% vSAN rebalances, and it needs room to rebuild after a host failure or maintenance.
- J is wrong: the ratio is provisioned divided by capacity, counting virtual disks only; used space is what the thin disks have written so far.
- K is wrong: the ratio counts virtual disks only, not snapshots or swap.
- L is correct: multiply the provisioned size by the copies before comparing it with capacity: 32,000 GB claims 64,000 GB, about 104% of VSAN-PROD-A.
- M is correct: there is no ratio that fits every datastore.
- N is wrong: powering off a VM frees only its swap file; its disks stay until the VM is deleted.
- Misconception: B: "DS-ARCH-01 is the only datastore at risk: it is 95% full. The others are below 80%." - G: "vSAN used space is the VM data; the mirror copy is kept elsewhere." - N: "Power off the VMs to free their space."

## Notes
- Synthetic, 2026-11-05, from the knowledge files listed in `knowledge`. Revised 2026-11-12 for question set 1.0: 200 datastores reduced to 30 so the export is read in the prompt; vSAN provisioned shown before the policy, so the three thin VMFS and NFS datastores stay the most overcommitted. Counts only after author approval.
- Review 2026-11-14: options G and J turned into near-miss false options that test the same facts (vSAN used space holds the policy copies; the ratio divides by capacity), so fewer options are true.
- Review 2026-11-15: VSAN-PROD-A provisioned raised from 26,000 to 32,000 GB in the CSV, so H becomes true and the VMFS-style reading (provisioned against capacity) misleads; key points H and L recomputed; misconception types filled. Key changed from A, C, D, E, F, I, L, M to A, C, D, E, F, H, I, L, M.
- Audit 2026-11-15: G and N listed as misconceptions too (both are misconception lines of datastore-space-headroom). Key unchanged.

## Metadata
```yaml
id: "0080"
title: "Which datastores run out of space first"
product: [vsphere, vcf-operations]
technology: [storage]
task: decide-capacity
level: 400
answer_type: deterministic
misconception: [B, G, N]
input: [table]
object: [datastore]
tool: [vcf-operations]
knowledge:
  - vsphere/technology/storage/datastore-space-headroom
  - vsphere/technology/storage/metrics/virtual-motherboard/disk-space
  - vsphere/technology/storage/concepts/snapshot-impact
  - sp5-framework/capacity/overcommit
knowledge_main: vsphere/technology/storage/datastore-space-headroom
attachments:
  - 0080/datastore-space-30-datastores.csv
origin: synthetic
source_path: "Synthetic, 2026-11-05"
misconception_type: [provider-vs-consumer, unit-and-normalization]
pair: "0343"
status: draft
```
