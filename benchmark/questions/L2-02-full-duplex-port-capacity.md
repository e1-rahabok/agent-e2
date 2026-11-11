# Full-duplex port capacity

## Prompt
An ESXi host has one 25 Gb physical NIC port, full duplex.

What is its capacity?

- A. 25 Gb in total, shared by transmit and receive.
- B. 25 Gb transmit and 25 Gb receive, at the same time.
- C. 12.5 Gb each way.
- D. 50 Gb transmit, or 50 Gb receive.

## Likely wrong answer
A: treating the port speed as one pool for both directions.

## Expected key points
- Answer: B.
- Full duplex is 100% in each direction: a 25 Gb port handles 25 Gb transmit plus 25 Gb receive.
- So measure and size each direction separately.

## Notes
- Previous id: question-0040 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0040"
title: "Full-duplex port capacity"
product: [vsphere]
technology: [network]
task: decide-capacity
level: 200
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/technology/network/concepts/network-characteristics
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 100-200 allocation (benchmark/design.md, section 3.6)"
answer: [B]
misconception: [A]
status: draft
```
