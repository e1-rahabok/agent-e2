# Command latency vs read and write latency

## Prompt
- The vSphere Client Disk chart of host esx-05, for LUN naa.624a9370c3, shows in one 20-second sample:
  - 100 reads per second at a Read latency of 2 ms;
  - 10 writes per second at a Write latency of 20 ms;
  - a Command latency of about 3.6 ms.

How is the Command latency related to the read and write latencies?

- A. It is the mean of the read latency and the write latency, so each counts once.
- B. It is the mean over all commands, so each read and each write counts once.
- C. It is the read latency plus the write latency, as both run in the sample.
- D. It is the higher of the read and write latencies in the sample.

## Likely wrong answer
A: (read + write) / 2, which would be 11 ms.

## Expected key points
- Answer: B.
- Command latency is the average over all commands: (100 × 2 + 10 × 20) / 110 ≈ 3.6 ms. With ten reads per write it follows read latency.
- A is wrong: it would give 11 ms. C (22 ms) and D (20 ms) do not match either.
- So check read and write latency separately: often only one of them has a problem, and the combined value hides it.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Revised 2026-11-12 for question set 1.0: values added; moved to the host Disk chart (disk.totalLatency), since the vSphere Client has no total latency counter for a virtual disk. Counts only after author approval.

## Metadata
```yaml
id: "0044"
title: "Command latency vs read and write latency"
product: [vsphere]
technology: [storage]
task: read-metric
level: 200
answer_type: deterministic
input: [text]
object: [esxi]
tool: [vcenter]
knowledge:
  - vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
  - vsphere/technology/storage/metrics/host/disk
  - vsphere/technology/storage/concepts/esxi-storage-latency-stack
knowledge_main: vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05"
answer: [B]
misconception: [A]
misconception_type: [unit-and-normalization]
status: draft
```
