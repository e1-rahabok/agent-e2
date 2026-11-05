# How much a rollup dilutes a 20-second peak

## Prompt
- A VM has one 20-second burst of CPU Ready.
- You look at it in the vCenter 1 Day chart.

By how much is the burst diluted in that chart?

- A. 5 times
- B. 15 times
- C. 288 times
- D. 4,320 times

## Likely wrong answer
C: 288 is the number of points per day, not the dilution of one point.

## Expected key points
- Answer: B.
- One 1 Day point (5 minutes) is built from 15 real-time samples (20 seconds), so a single burst is diluted 15 times.
- In the 1 Year interval the same burst is diluted 4,320 times. Use real-time or esxtop to see bursts.

## Notes
- Previous id: question-0047 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "47"
title: "How much a rollup dilutes a 20-second peak"
product: [vsphere]
technology: [system]
task: read-metric
level: 200
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
