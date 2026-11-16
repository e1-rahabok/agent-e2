# Command latency vs read and write latency

## Prompt
- The vSphere Client Disk chart of host esx-05, for LUN naa.624a9370c3, shows in one 20-second sample:
  - 120 reads per second at a Read latency of 2 ms;
  - 15 writes per second at a Write latency of 20 ms;
  - a Command latency of about 4.0 ms.

Which statements about the Command latency are correct?

- A. Command latency gives the read side and the write side equal weight.
- B. Command latency is the mean over all commands in the sample, reads and writes alike.
- C. In Command latency, one 64 KB write carries the weight of sixteen 4 KB reads.
- D. Command latency is the median latency of the commands in the sample.
- E. Command latency equals the read latency whenever reads outnumber the writes in the sample.
- F. With writes at 40 ms and the same IO counts, Command latency would be about 6.2 ms.
- G. The LUN needs no follow-up, as its Command latency of 4.0 ms is low.

## Likely wrong answer
A: (read + write) / 2, which would be 11 ms.

## Expected key points
- Answer: B, F.
- A is wrong: equal weight would give (2 + 20) / 2 = 11 ms, not the 4.0 ms shown.
- B is correct: (120 × 2 + 15 × 20) / 135 = 540 / 135 = 4.0 ms. With eight reads per write it follows read latency.
- C is wrong: each command counts once, whatever its size; the layers below the Guest OS count commands, not bytes, so a 64 KB write weighs the same as a 4 KB read.
- D is wrong: Command latency is a mean over the commands, weighted by their count; with 120 reads at 2 ms the median would be 2 ms.
- E is wrong: Command latency follows the read latency when reads dominate, but the slower writes still pull it up: 4.0 ms against 2 ms.
- F is correct: (120 × 2 + 15 × 40) / 135 = 840 / 135 ≈ 6.2 ms.
- G is wrong: the writes take 20 ms, and the combined value hides them; read and write latency are checked separately, as often only one has a problem.

## Notes
- Synthetic, 2026-11-05. Revised 2026-11-12 for question set 1.0: values added; moved to the host Disk chart (disk.totalLatency), since the vSphere Client has no total latency counter for a virtual disk. Counts only after author approval.
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): plural stem; over-correction E, a computed option F and wrong action G added. Key changed from B to B, F.
- Review 2026-11-15: new sample values (120 reads at 2 ms, 15 writes at 20 ms; the old 100 and 10 were the knowledge example); A, D and G reworded so they share no wording with the practical half 0414; esxtop storage added to `knowledge` (the /cmd counters are weighted by reads and writes). Key unchanged: B, F.
- Audit 2026-11-15: C (the sum of read and write latency, a throwaway against the 4.0 ms shown) replaced by a weighting by IO size, which the command count rejects; B, E and F reworded for length (truth unchanged); esxi-storage-io-path added to `knowledge`. Key unchanged: B, F.

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
  - vsphere/tools/esxtop/storage
  - vsphere/technology/storage/concepts/esxi-storage-io-path
knowledge_main: vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-05"
answer: [B, F]
misconception: [A, G]
misconception_type: [unit-and-normalization]
pair: "0414"
status: draft
```
