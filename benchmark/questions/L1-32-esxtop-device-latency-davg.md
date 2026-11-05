# The esxtop counter for device latency

## Prompt
In esxtop, which counter measures the latency from the ESXi host bus adapter to the storage array and back?

- A. GAVG
- B. KAVG
- C. QAVG
- D. DAVG

## Likely wrong answer
A: GAVG is the total latency the VM sees, not the device part.

## Expected key points
- Answer: D.
- DAVG (Device Average): from the ESXi HBA to the array and back.
- GAVG is the total seen by the VM; KAVG the time in the VMkernel; QAVG the time in kernel queues, part of KAVG.

## Notes
- Previous id: question-0032 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "32"
title: "The esxtop counter for device latency"
product: [vsphere]
technology: [storage]
task: read-metric
level: 100
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/technology/storage/concepts/esxi-storage-latency-stack
  - vsphere/technology/storage/metrics/comparisons/esxtop-storage
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 100-200 allocation (benchmark/design.md, section 3.6)"
answer: [D]
trap: [A]
status: draft
```
