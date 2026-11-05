# Is the datastore full: provisioned vs used space

## Prompt
- The attached table is a VCF Operations export of every VM on datastore DS01: one row per VM.
- DS01 has a capacity of 10 TB.

Is DS01 out of space? Choose all the correct statements.

- A. Yes: the VMs' provisioned space adds up to more than 10 TB.
- B. No: the space the VMs use adds up to less than 10 TB.
- C. Provisioned space counts thin disks at their configured size, so DS01 is overcommitted: it fills if the thin disks grow.
- D. Provisioned space is the right capacity metric for a datastore.

## Input to supply
- Tool: VCF Operations 9.1, a list view or report of the VMs on one datastore, exported to CSV or Excel.
- Rows: 150-250 VMs on one datastore named DS01 (rename it if needed; mask the VM names).
- Columns: VM name; Datastore; Disk Space | Provisioned Space for VM (GB); Disk Space | Virtual Machine Used (GB); Disk Space | Snapshot | Virtual Machine Used (GB); Thin provisioned (yes or no).
- Condition for the key: the sum of Virtual Machine Used is about 6 TB; the sum of Provisioned Space is about 14 TB; most disks are thin.
- Save as `benchmark/questions/question-0046/datastore-ds01-vm-disk-space.csv` (or .xlsx: tell Claude to change the name).

## Likely wrong answer
A: reading provisioned space as used space.

## Expected key points
- Answer: B, C.
- Virtual Machine Used adds up to about 6 TB: under the 10 TB capacity.
- Provisioned Space counts thin disks at their full configured size (about 14 TB): the datastore is overcommitted, a risk if the disks grow.
- D is wrong: provisioned space mixes allocation and utilization; it is not a capacity metric.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: question-0046
title: "Is the datastore full: provisioned vs used space"
product: [vsphere, vcf-operations]
technology: [storage]
task: decide-capacity
level: 200
answer_type: deterministic
input: [table]
knowledge:
  - vsphere/technology/storage/metrics/virtual-motherboard/provisioned-space
  - vsphere/technology/storage/metrics/virtual-motherboard/disk-space-used
attachments:
  - question-0046/datastore-ds01-vm-disk-space.csv
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 100-200 allocation (benchmark/design.md, section 3.6)"
answer: [B, C]
trap: [A]
status: awaiting-input
```
