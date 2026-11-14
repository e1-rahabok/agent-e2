# Is the datastore full: provisioned vs used space

## Prompt
- [The attached table](0046/datastore-ds01-vm-disk-space.csv) is a VCF Operations export of every VM on datastore DS01: one row per VM, with a summary row.
- DS01 has a capacity of 10 TB.

Is DS01 already out of space, so that no new VM can be placed on it? Choose all the correct statements.

- A. Yes: the provisioned space of the VMs adds up to more than the 10 TB capacity.
- B. No: the space the VMs use adds up to less than the 10 TB capacity.
- C. Thin disks count at full size in provisioned space: DS01 fills if they grow.
- D. Provisioned space is the capacity metric to compare with the 10 TB of DS01.

## Likely wrong answer
A: reading provisioned space as used space.

## Expected key points
- Answer: B, C.
- B: Virtual Machine Used adds up to about 6.2 TB (6,177 GB), under the 10 TB capacity.
- C: Provisioned Space counts thin disks at their full configured size (14,100 GB, about 14 TB). All 29 VMs are thin: the datastore is overcommitted, a risk if the disks grow.
- A is wrong: provisioned space is not space in use.
- D is wrong: provisioned space measures what the disks may claim, the input of an overcommit ratio, not the space in use. Whether DS01 is full is read from used space against capacity.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
- CSV supplied by the author 2026-11-05 (VM names masked): Provisioned 14,100 GB, Virtual Machine Used 6,177.23 GB, snapshots 128.99 GB. 2026-11-12 (author, Q183): every disk thin (4 rows were marked thick with used below provisioned, which a thick disk cannot show); header typo and empty last column fixed.

## Metadata
```yaml
id: "0046"
title: "Is the datastore full: provisioned vs used space"
product: [vsphere, vcf-operations]
technology: [storage]
task: decide-capacity
level: 200
answer_type: deterministic
input: [table]
object: [datastore, vm]
tool: [vcf-operations]
knowledge:
  - vsphere/technology/storage/metrics/virtual-motherboard/disk-space-provisioned
  - vsphere/technology/storage/metrics/virtual-motherboard/disk-space-used
knowledge_main: vsphere/technology/storage/metrics/virtual-motherboard/disk-space-provisioned
attachments:
  - 0046/datastore-ds01-vm-disk-space.csv
origin: synthetic
source_path: "Drafted by Claude 2026-11-05"
answer: [B, C]
misconception: [A]
misconception_type: []
status: draft
```
