# Which datastores run out of space first

## Prompt
The attached table is an export of 200 datastores: capacity, used space, provisioned space, snapshot space, thin-provisioned share, and the number of VMs.

- The storage team asks which datastores will run out of space first, and how much they can overcommit.

Which datastores are most at risk, and why? How do you set the overcommit ratio?

## Input to supply
- Source: VCF Operations 9.1 or vSphere Client export, 200 VMFS and vSAN datastores, one row per datastore.
- Columns: datastore name, type (VMFS, NFS, vSAN), capacity (GB), used (GB), provisioned (GB), snapshot space (GB), thin-provisioned disks (%), VMs, vSAN storage policy FTT (for vSAN only).
- Condition for the key: at least 3 datastores with used below 70% but provisioned above 150% of capacity and mostly thin disks; at least 2 datastores where snapshot space is above 20% of used; at least 1 vSAN datastore with FTT 1 (RAID 1).
- Record in the Notes the names of the datastores that meet each condition.
- Save as `benchmark/questions/80/datastore-space-200-datastores.xlsx`.

## Likely wrong answer
"The datastores with the highest used % are the only ones at risk."

## Expected key points
- Provisioned above capacity with thin disks is the risk: thin disks can grow to their provisioned size, so used % alone under-states it. The datastores named in the Notes for the first condition.
- Snapshots can exceed the size of their VMDK, especially for thin disks snapshotted early; large snapshot space is reclaimable and a risk at the same time. The datastores named for the second condition.
- Overcommit ratio: count only virtual disks; exclude snapshots and swap files.
- On vSAN, exclude the FTT protection and lower the ratio to match: with FTT doubling space, halve the ratio.
- Datastore metrics include snapshot space; virtual disk metrics exclude it.

## Notes
- Previous id: question-0080 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0080"
title: "Which datastores run out of space first"
product: [vsphere, vcf-operations]
technology: [storage]
task: decide-capacity
level: 400
answer_type: judged
input: [table]
knowledge:
  - vsphere/technology/storage/metrics/virtual-motherboard/provisioned-space
  - vsphere/technology/storage/concepts/snapshot-impact
  - operations-management/capacity/capacity-model
attachments:
  - 0080/datastore-space-200-datastores.xlsx
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
status: awaiting-input
```
