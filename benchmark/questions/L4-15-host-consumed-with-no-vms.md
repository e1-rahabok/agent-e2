# Host Consumed with no VMs

## Prompt
- An ESXi 9.1 host in a vSAN cluster is evacuated for maintenance: 0 VMs run on it.
- Its Memory Consumed drops from 400 GB to 32 GB, not to 0.
- Its kernel memory reservation stays at about 57 GB, before and after.

Which statements are correct?

- A. Consumed includes the kernel's actual memory use, including vSAN, so it does not fall to 0.
- B. Consumed shows the kernel reservation, so with no VMs it should read the 57 GB the kernel holds.
- C. Kernel reservation and kernel use are different: the reservation can be higher than what the kernel uses.
- D. 32 GB with no VMs proves a memory leak in the kernel, since an idle host should consume almost nothing.
- E. With the VMs gone, Consumed should equal the sum of the VM overhead that was reserved before the evacuation.

## Likely wrong answer
B: expecting Consumed to equal the kernel reservation.

## Expected key points
- Answer: A, C.
- Host Consumed counts pages in physical DIMM: VMs, VM overhead and all kernel processes, including vSAN. With 0 VMs it is the kernel and vSAN.
- Consumed is actual use, not reservation: the 57 GB reservation stays while the use is 32 GB.
- D is wrong: vSAN and kernel modules keep memory with no VMs.
- E is wrong: VM overhead leaves with the VMs; what stays is the kernel's own use.

## Notes
- Revised 2026-11-12 (question set 1.0): option E added; tags added.
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0056"
title: "Host Consumed with no VMs"
product: [vsphere, vsan]
technology: [memory, system]
task: explain-mechanism
level: 400
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/technology/memory/metrics/host/consumed
  - vsphere/architecture/overhead
object: [esxi]
tool: [vcenter]
knowledge_main: vsphere/technology/memory/metrics/host/consumed
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
answer: [A, C]
misconception: [B]
misconception_type: [provider-vs-consumer]
status: draft
```
