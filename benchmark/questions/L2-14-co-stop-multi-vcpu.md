# What Co-stop measures

## Prompt
Which statements about VM CPU Co-stop are correct? Choose all that apply.

- A. It is time a vCPU is held back because a sibling vCPU of the same VM has fallen too far behind.
- B. It applies only to VMs with more than one vCPU.
- C. It comes from the host being short of physical CPU, the same cause as Ready.
- D. While a vCPU is in Co-stop, its physical thread can run another VM.
- E. Co-stop and Ready move independently of each other.
- F. High Co-stop on a VM calls for more vCPUs.
- G. It is time the vCPU waits for disk IO.

## Likely wrong answer
C: Co-stop read as a host shortage, like Ready. Or G: Co-stop confused with Wait.

## Expected key points
- Answer: A, B, D.
- A is true: the kernel holds a vCPU that is too far ahead of a sibling that cannot be served, to keep the vCPUs in step.
- B is true: Co-stop needs siblings; on a 1-vCPU VM it is always 0.
- C is false: Ready comes from ESXi having no thread; Co-stop comes from the VM's own vCPUs drifting apart. The co-stopped vCPUs stop even when threads are free.
- D is true: during Co-stop, Ready or Wait the physical thread is free, so another VM can run on it.
- E is false: Ready on one vCPU causes Co-stop on its siblings, so the two often move together.
- F is false: Co-stop rises with the vCPU count; the remedy is a smaller VM.
- G is false: waiting for IO is part of Wait, not Co-stop.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
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
source_path: "Drafted by Claude 2026-11-05"
answer: [A, B, D]
misconception: [C, G]
misconception_type: []
pair: "0375"
status: draft
```
