# Swap space for a mass power-on

## Prompt
- A disaster recovery test will power on 60 VMs at the recovery site. They are powered off now.
- All 60 VMs live on VMFS datastore DR-DS02, which has 2 TB of free space. Their swap files are kept in the VM folders (the default).
- Each VM has 64 GB of configured memory and a memory reservation of 16 GB.

Which statements are correct?

- A. Each VM creates a 48 GB swap file at power-on: 64 GB configured minus the 16 GB reservation.
- B. Each VM creates a 64 GB swap file: the swap file always matches the configured memory.
- C. The 60 swap files need about 2.8 TB; with 2 TB free, the last VMs fail to power on.
- D. A full 64 GB reservation per VM removes the swap space, at the cost of host memory.
- E. The swap files stay on the datastore while the VMs are powered off, so the test needs no new space.
- F. Swap space is needed only when the hosts run short of memory, so the free space can wait until then.

## Likely wrong answer
B: swap equals configured memory. Or E: powered-off VMs already hold their swap files.

## Expected key points
- Answer: A, C, D.
- A: the swap file (.vswp) is configured memory minus the memory reservation: 64 − 16 = 48 GB.
- C: 60 × 48 GB = 2,880 GB, more than the 2,048 GB free: a VM whose swap file cannot be created does not power on.
- D: with a full reservation, the swap file is 0 GB; the hosts must then reserve 64 GB for each VM, and admission control checks it.
- B is wrong: the reserved part never needs swap.
- E is wrong: a swap file is created at power-on and deleted at power-off.
- F is wrong: the file is created at power-on whatever the memory pressure.

## Notes
- Drafted by Claude 2026-11-12 for question set 1.0, Storage slot "swap file space on a mass power-on" (project/plan.md, M2). Counts only after author approval.

## Metadata
```yaml
id: "0181"
title: "Swap space for a mass power-on"
product: [vsphere]
technology: [storage, memory]
task: decide-capacity
level: 300
answer_type: deterministic
input: [text]
object: [datastore, vm]
tool: [none]
knowledge:
  - vsphere/technology/storage/concepts/vm-files
  - vsphere/technology/storage/datastore-space-headroom
knowledge_main: vsphere/technology/storage/concepts/vm-files
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12 for the Storage slots (benchmark/design.md, section 3)"
answer: [A, C, D]
misconception: [B, E]
misconception_type: []
status: draft
```
