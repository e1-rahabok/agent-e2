# The real-time sample interval

## Prompt
How often does ESXi sample its performance counters for the real-time charts?

- A. Every 5 seconds
- B. Every 20 seconds
- C. Every 5 minutes
- D. Every 30 minutes

## Likely wrong answer
C: 5 minutes is the 1 Day interval, built from real-time samples.

## Expected key points
- Answer: B.
- ESXi samples every 20 seconds: the real-time data.
- vCenter rolls them up: 5 minutes (1 Day), 30 minutes (1 Week), 2 hours (1 Month), 1 day (1 Year). esxtop defaults to 5 seconds but is not the vCenter chart.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: question-0035
title: "The real-time sample interval"
product: [vsphere]
technology: [system]
task: read-metric
level: 100
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/foundations/vcenter-statistics
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 100-200 allocation (benchmark/design.md, section 3.6)"
answer: [B]
trap: [C]
status: draft
```
