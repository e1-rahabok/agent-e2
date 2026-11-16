# Which reclamation runs in the Guest OS

## Prompt
- An ESXi host under memory pressure reclaims memory from its VMs.

Which of these reclamation techniques run as a driver inside the Guest OS?

- A. Ballooning
- B. Swapping to the VM swap file
- C. Memory compression
- D. Transparent page sharing

## Likely wrong answer
C: assuming compression happens inside the guest.

## Expected key points
- Answer: A.
- A is correct: the balloon is a kernel driver inside the Guest OS (shipped with VMware Tools on Windows; the upstream `vmw_balloon` module on Linux, not part of open-vm-tools). The VMkernel sets its target; the Guest OS picks the pages, free first, then cache, modified and in use.
- B is wrong: host swapping to the VM swap file is done by the VMkernel, transparent to the Guest OS; it is not the guest page file.
- C is wrong: ESXi compresses 4 KB pages in the VMkernel, without the Guest OS knowing.
- D is wrong: page sharing is done by the VMkernel, transparent to the Guest OS.

## Metadata
```yaml
id: "0038"
title: "Which reclamation runs in the Guest OS"
product: [vsphere, windows, linux]
technology: [memory]
task: explain-mechanism
level: 100
answer_type: deterministic
input: [text]
object: [vm, guest-os]
tool: [none]
knowledge:
  - vsphere/technology/memory/concepts/ballooning
  - vsphere/technology/memory/concepts/memory-layers
knowledge_main: vsphere/technology/memory/concepts/ballooning
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-05"
answer: [A]
misconception: [C]
misconception_type: [layer-confusion]
status: draft
```
