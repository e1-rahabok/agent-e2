# Where the balloon runs

## Prompt
- An ESXi host under memory pressure reclaims memory from its VMs.

Which of these reclamation techniques runs as a driver inside the Guest OS?

- A. Ballooning
- B. Swapping to the VM swap file
- C. Memory compression
- D. Transparent page sharing

## Likely wrong answer
C: assuming compression happens inside the guest.

## Expected key points
- Answer: A.
- The balloon is a driver inside the Guest OS, installed with VMware Tools. The VMkernel tells it to inflate or deflate; the Guest OS chooses which pages to give it.
- Swapping, compression and page sharing are done by the VMkernel, without the Guest OS knowing.

## Notes
- Revised 2026-11-12 (question set 1.0): "four techniques" removed; ESXi has five (sharing, ballooning, compression, swap to host cache, host swapping).

## Metadata
```yaml
id: "0038"
title: "Where the balloon runs"
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
source_path: "Drafted by Claude 2026-11-05 for the Level 100-200 allocation (benchmark/design.md, section 3.6)"
answer: [A]
misconception: [C]
misconception_type: [layer-confusion]
status: draft
```
