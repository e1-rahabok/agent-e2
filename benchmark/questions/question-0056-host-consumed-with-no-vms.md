# Host Consumed with no VMs

## Prompt
- An ESXi host in a vSAN cluster is evacuated for maintenance: 0 VMs run on it.
- Its Memory Consumed drops from 400 GB to 32 GB, not to 0.
- Its kernel memory reservation (Memory \ ESX System Usage) stays at about 57 GB.

Which statements are correct? Choose all that apply.

- A. Consumed includes the kernel's actual memory use, including vSAN, so it does not fall to 0.
- B. Consumed shows the kernel reservation, so it should read 57 GB.
- C. Kernel reservation and kernel use are different: the reservation can be higher than what the kernel uses.
- D. 32 GB with no VMs proves a memory leak.

## Likely wrong answer
B: expecting Consumed to equal the kernel reservation.

## Expected key points
- Answer: A, C.
- Host Consumed counts pages in physical DIMM: VMs, VM overhead and all kernel processes, including vSAN. With 0 VMs it is the kernel and vSAN.
- Consumed is actual use, not reservation: the 57 GB reservation stays while the use is 32 GB.
- D is wrong: vSAN and kernel modules keep memory with no VMs.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: question-0056
title: "Host Consumed with no VMs"
product: [vsphere, vsan]
technology: [memory, system]
task: explain-mechanism
level: 400
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/technology/memory/metrics/host/consumed
  - vsphere/foundations/overhead
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
answer: [A, C]
trap: [B]
status: draft
```
