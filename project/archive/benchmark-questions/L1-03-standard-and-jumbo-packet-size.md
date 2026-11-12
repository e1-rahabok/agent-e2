# Standard and jumbo packet size

## Prompt
What is the standard Ethernet packet size, and the jumbo frame size?

- A. 1,500 bytes and 9,000 bytes
- B. 1,000 bytes and 4,000 bytes
- C. 1,500 bytes and 1,600 bytes
- D. 9,000 bytes and 1,500 bytes

## Likely wrong answer
C: taking the typical NSX size (1,600 bytes) for the jumbo frame size.

## Expected key points
- Answer: A.
- Standard: 1,500 bytes. Jumbo frames: 9,000 bytes.
- NSX overlay typically uses 1,600 bytes: larger than standard, far below jumbo.

## Notes
- Retired 2026-11-12 (question set 1.0): trivia (packet sizes), not operations knowledge.
- Previous id: question-0031 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0031"
title: "Standard and jumbo packet size"
product: [vsphere, nsx]
technology: [network]
task: read-metric
level: 100
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/technology/network/metrics/virtual-motherboard/throughput
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 100-200 allocation (benchmark/design.md, section 3.6)"
answer: [A]
misconception: [C]
status: retired
```
