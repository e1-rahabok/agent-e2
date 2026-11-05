# Total disk latency vs read and write latency

## Prompt
A virtual disk shows Read latency, Write latency and a total latency.

How is the total latency related to the read and write latencies?

- A. It is the average of read latency and write latency.
- B. It is the average over all commands, so it is weighted by the number of reads and writes.
- C. It is read latency plus write latency.
- D. It is the higher of the two.

## Likely wrong answer
A: (read + write) / 2.

## Expected key points
- Answer: B.
- Total latency is the average over all commands. With 100 reads and 10 writes per second, it follows read latency.
- So check read and write separately: often only one of them has a problem.

## Notes
- Previous id: question-0044 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0044"
title: "Total disk latency vs read and write latency"
product: [vsphere]
technology: [storage]
task: read-metric
level: 200
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 100-200 allocation (benchmark/design.md, section 3.6)"
answer: [B]
trap: [A]
status: draft
```
