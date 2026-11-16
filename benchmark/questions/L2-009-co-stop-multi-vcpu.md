# What Co-stop measures

## Prompt
Which statements about VM CPU Co-stop are correct?

- A. It is time a vCPU is paused for running too far ahead of a sibling vCPU.
- B. It applies only to VMs with more than one vCPU.
- C. It comes from the host being short of physical CPU, the same cause as Ready.
- D. While a vCPU is in Co-stop, its physical thread can run another VM.
- E. Co-stop and Ready move independently of each other.
- F. High Co-stop on a VM calls for giving it more vCPUs.
- G. It is the time a vCPU waits for its disk IO to complete.

## Answers
A, B, D

## Explanation
- A is correct: the kernel pauses a vCPU that is too far ahead of a sibling that cannot be served, to keep the vCPUs in step.
- B is correct: Co-stop needs siblings; on a 1-vCPU VM it is always 0.
- C is wrong: Co-stop is the VM's own vCPUs drifting apart. It rises with the vCPU count and the NUMA span, and a sibling's Ready often starts it; the co-stopped vCPUs stop even when threads are free.
- D is correct: during Co-stop, Ready or Wait the physical thread is free, so another VM can run on it.
- E is wrong: Ready on one vCPU causes Co-stop on its siblings, so the two often move together.
- F is wrong: Co-stop rises with the vCPU count and the NUMA span; the remedy is a smaller VM.
- G is wrong: waiting for IO is part of Wait, not Co-stop.
- Misconception: C: Co-stop read as a host shortage, like Ready. Or G: Co-stop confused with Wait.

## Notes
- Synthetic, 2026-11-05, from the knowledge files listed in `knowledge`. Counts only after author approval.
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): C (the Level 300 misconception), E (its over-correction) and F (the wrong action) added; the old C is now G. Key unchanged, A, B, D.

## Metadata
```yaml
id: "0053"
title: "What Co-stop measures"
product: [vsphere]
technology: [cpu]
task: explain-mechanism
level: 200
answer_type: deterministic
input: [text]
object: [vm]
tool: [vcenter]
knowledge:
  - vsphere/technology/cpu/concepts/vcpu-states
  - vsphere/technology/cpu/metrics/virtual-motherboard/co-stop
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/co-stop
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-05"
misconception: [C, G]
misconception_type: []
pair: "0375"
status: draft
```
