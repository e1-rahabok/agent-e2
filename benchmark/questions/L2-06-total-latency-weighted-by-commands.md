# Command latency vs read and write latency

## Prompt
- The vSphere Client Disk chart of host esx-05, for LUN naa.624a9370c3, shows in one 20-second sample:
  - 100 reads per second at a Read latency of 2 ms;
  - 10 writes per second at a Write latency of 20 ms;
  - a Command latency of about 3.6 ms.

Which statements about the Command latency are correct?

- A. Command latency is the mean of the read latency and the write latency, each counted once.
- B. Command latency is the average over all commands in the sample, reads and writes alike.
- C. Command latency is the sum of the read latency and the write latency.
- D. Command latency is the higher of the read latency and the write latency.
- E. Command latency equals the read latency whenever reads outnumber writes.
- F. If the writes slowed to 40 ms with the same IO counts, Command latency would rise to about 5.5 ms.
- G. With Command latency at 3.6 ms, close the ticket: the LUN serves all its IO well.

## Likely wrong answer
A: (read + write) / 2, which would be 11 ms.

## Expected key points
- Answer: B, F.
- A is false: it would give 11 ms, not the 3.6 ms shown.
- B is true: (100 × 2 + 10 × 20) / 110 ≈ 3.6 ms. With ten reads per write it follows read latency.
- C is false: it would give 22 ms.
- D is false: it would give 20 ms.
- E is false: Command latency follows the read latency when reads dominate, but the slower writes still pull it up: 3.6 ms against 2 ms.
- F is true: (100 × 2 + 10 × 40) / 110 = 600 / 110 ≈ 5.5 ms.
- G is false: the writes take 20 ms, and the combined value hides them; check read and write latency separately, as often only one has a problem.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Revised 2026-11-12 for question set 1.0: values added; moved to the host Disk chart (disk.totalLatency), since the vSphere Client has no total latency counter for a virtual disk. Counts only after author approval.
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): plural stem; over-correction E, a computed option F and wrong action G added. Key changed from B to B, F.

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
answer: [B, F]
misconception: [A, G]
misconception_type: [unit-and-normalization]
pair: "0414"
status: draft
```
