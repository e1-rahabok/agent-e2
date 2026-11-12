# The VM network contention metric

## Prompt
Which VM network counter shows that the VM did not get the network service it asked for (contention)?

- A. Packets dropped
- B. Usage
- C. Packets received
- D. Broadcast packets received

## Likely wrong answer
B: reading high Usage as a network performance problem.

## Expected key points
- Answer: A.
- Packets dropped is the only VM network contention metric.
- Usage, packets received and broadcast packets are consumption: they count work done, not work refused.

## Notes
- Previous id: question-0030 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0030"
title: "The VM network contention metric"
product: [vsphere]
technology: [network]
task: read-metric
level: 100
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/technology/network/metrics/virtual-motherboard/packets-dropped
  - vsphere/technology/network/metrics/vm-network-metrics
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 100-200 allocation (benchmark/design.md, section 3.6)"
answer: [A]
misconception: [B]
status: draft
```
