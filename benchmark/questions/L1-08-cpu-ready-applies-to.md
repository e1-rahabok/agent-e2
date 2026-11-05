# Which object has CPU Ready

## Prompt
CPU Ready measures a consumer waiting to be scheduled. Which object does it apply to?

- A. A VM
- B. An ESXi host
- C. A physical core
- D. A cluster

## Likely wrong answer
B: reading a host-level Ready value as the host waiting.

## Expected key points
- Answer: A.
- Ready applies to a consumer: a VM (per vCPU).
- A physical core or thread is always ready, so Ready does not apply to ESXi; a host or cluster value is a sum of its VMs.

## Notes
- Previous id: question-0036 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0036"
title: "Which object has CPU Ready"
product: [vsphere]
technology: [system, cpu]
task: read-metric
level: 100
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/foundations/provider-consumer
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 100-200 allocation (benchmark/design.md, section 3.6)"
answer: [A]
trap: [B]
status: draft
```
