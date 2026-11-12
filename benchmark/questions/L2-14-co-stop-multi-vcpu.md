# What Co-stop measures

## Prompt
Which statements about VM CPU Co-stop are correct? Choose all that apply.

- A. It is time a vCPU is held back because a sibling vCPU of the same VM has fallen too far behind.
- B. It applies only to VMs with more than one vCPU.
- C. It is time the vCPU waits for disk IO.
- D. While a vCPU is in Co-stop, its physical thread can run another VM.

## Likely wrong answer
C: confusing Co-stop with Wait.

## Expected key points
- Answer: A, B, D.
- Co-stop: the kernel holds a vCPU because another vCPU of the same VM is far behind; it needs siblings, so a 1-vCPU VM has none.
- The physical thread is free during Co-stop, Ready or Wait: another VM can run on it.
- C is Wait (IO or idle), not Co-stop.

## Notes
- Previous id: question-0053 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
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
source_path: "Drafted by Claude 2026-11-05 for the Level 100-200 allocation (benchmark/design.md, section 3.6)"
answer: [A, B, D]
misconception: [C]
misconception_type: []
status: draft
```
