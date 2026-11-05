# Network units in the vSphere Client and esxtop

## Prompt
Which units do the two tools use for VM network throughput?

- A. Both show kilobytes per second.
- B. The vSphere Client shows kilobytes per second; esxtop shows megabits per second.
- C. The vSphere Client shows megabits per second; esxtop shows kilobytes per second.
- D. Both show megabits per second.

## Likely wrong answer
A: assuming both tools use the same unit, then comparing the numbers directly.

## Expected key points
- Answer: B.
- The vSphere Client (vCenter) shows network counters in kilobytes per second.
- esxtop shows them in megabits per second: convert bits to bytes and mega to kilo before comparing.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: question-0029
title: "Network units in the vSphere Client and esxtop"
product: [vsphere]
technology: [network]
task: read-metric
level: 100
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/technology/network/metrics/comparisons/esxtop-vs-vsphere-client-units
  - vsphere/technology/network/metrics/virtual-motherboard/throughput
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 100-200 allocation (benchmark/design.md, section 3.6)"
answer: [B]
trap: [A]
status: draft
```
