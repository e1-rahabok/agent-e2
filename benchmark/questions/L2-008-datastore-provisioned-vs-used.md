# Is the datastore full: provisioned vs used space

## Prompt
- [The attached table](0046/datastore-ds01-vm-disk-space.csv) is a VCF Operations export of every VM on datastore DS01: one row per VM, with a summary row.
- DS01 has a capacity of 10 TB; VCF Operations shows its Used Space at 6.3 TB.

Is DS01 already out of space, so that no new VM can be placed on it? Choose all the correct statements.

- A. DS01 is full: the provisioned space of its VMs exceeds its 10 TB.
- B. The files of DS01's VMs take about 6 TB of its 10 TB.
- C. Thin disks count at full size in provisioned space: DS01 fills if they grow.
- D. DS01's free space is its 10 TB minus the provisioned space of its VMs.

## Likely wrong answer
A: reading provisioned space as used space.

## Expected key points
- Answer: B, C.
- A is wrong: provisioned space is not space in use; the part above used is unwritten thin space, an overcommit risk, not fullness.
- B is correct: Virtual Machine Used adds up to 6,177 GB, about 6 TB (VCF Operations GB are 1024³ bytes), under the 10 TB capacity; the datastore's own Used Space of 6.3 TB, which includes every file on it, agrees.
- C is correct: Provisioned Space counts thin disks at their full configured size (14,100 GB, about 13.8 TB). All 29 VMs are thin: the datastore is overcommitted, a risk if the disks grow.
- D is wrong: free space is capacity minus used space (here about 3.7 TB). Provisioned minus used is the unwritten thin space that can still claim part of it.

## Notes
- Synthetic, 2026-11-05. Counts only after author approval.
- CSV supplied by the author 2026-11-05 (VM names masked): Provisioned 14,100 GB, Virtual Machine Used 6,177.23 GB, snapshots 128.99 GB. 2026-11-12 (author, Q183): every disk thin (4 rows were marked thick with used below provisioned, which a thick disk cannot show); header typo and empty last column fixed.
- Audit 2026-11-15: datastore Used Space (6.3 TB) added to the stem, so B is read from the datastore and not only from the VM rows; A and B no longer open with "Yes:" and "No:"; D reworded to the free-space formula (it was ambiguous: provisioned against capacity is the overcommit ratio); `datastore-space-headroom` added to `knowledge`. Key unchanged: B, C.
- Open (knowledge base): Provisioned Space for VM counts non-disk files at actual size, but the CSV rows show round disk sizes (row 009: 1,000 GB with an 88.92 GB snapshot). Check against a VCF Operations 9.1 export.

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
  - vsphere/technology/storage/metrics/virtual-motherboard/disk-space
  - vsphere/technology/storage/datastore-space-headroom
knowledge_main: vsphere/technology/storage/metrics/virtual-motherboard/disk-space
attachments:
  - 0046/datastore-ds01-vm-disk-space.csv
origin: synthetic
source_path: "Synthetic, 2026-11-05"
answer: [B, C]
misconception: [A]
misconception_type: []
status: draft
```
