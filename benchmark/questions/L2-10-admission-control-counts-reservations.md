# Insufficient Resources on a quiet host

## Prompt
- An ESXi host runs at 10% CPU usage.
- Powering on a VM with a CPU reservation fails with Insufficient Resources.

Which statements are correct? Choose all that apply.

- A. Admission control counts reservations, not usage.
- B. Per-VM overhead memory counts as reserved, on top of the memory reservation.
- C. The power-on fails only when actual CPU usage is high.
- D. A VM with no reservation also fails CPU admission control on this host.

## Likely wrong answer
C: expecting admission control to look at usage.

## Expected key points
- Answer: A, B.
- Admission control compares the VM reservation with the unreserved capacity of the host, resource pool or cluster. A host at 10% usage can be fully reserved.
- Per-VM overhead memory counts as reserved.
- D is wrong: a VM with no reservation passes CPU and memory admission control (its overhead memory is still checked).

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0048"
title: "Insufficient Resources on a quiet host"
product: [vsphere]
technology: [system, cpu, memory]
task: judge-setting
level: 200
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
  - vsphere/architecture/resource-controls
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 100-200 allocation (benchmark/design.md, section 3.6)"
answer: [A, B]
misconception: [C]
object: [esxi, vm]
tool: [none]
knowledge_main: vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
misconception_type: [consumption-as-contention]
status: draft
```
