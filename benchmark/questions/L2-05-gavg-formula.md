# How the esxtop storage latencies add up

## Prompt
- In esxtop, one device shows GAVG/cmd 3.1 ms, KAVG/cmd 2.1 ms, QAVG/cmd 1.6 ms and DAVG/cmd 1.0 ms.

How do the four counters relate?

- A. GAVG = KAVG + DAVG. QAVG is part of KAVG.
- B. GAVG = KAVG + QAVG + DAVG.
- C. GAVG = DAVG - KAVG.
- D. GAVG = QAVG + DAVG. KAVG is part of QAVG.

## Likely wrong answer
B: adding QAVG on top of KAVG, counting the queue time twice.

## Expected key points
- Answer: A.
- GAVG (total seen from the VM monitor) = KAVG (time in the VMkernel) + DAVG (device): 2.1 + 1.0 = 3.1 ms.
- QAVG is the queue part of the kernel time, so it is already inside KAVG.
- B is wrong: it counts the queue time twice (4.7 ms).
- C (-1.1 ms) and D (2.6 ms) do not match the values shown.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Revised 2026-11-12 for question set 1.0: values added so the relation can be checked. Counts only after author approval.

## Metadata
```yaml
id: "0043"
title: "How the esxtop storage latencies add up"
product: [vsphere]
technology: [storage]
task: explain-mechanism
level: 200
answer_type: deterministic
input: [text]
object: [esxi]
tool: [esxtop]
knowledge:
  - vsphere/technology/storage/concepts/esxi-storage-latency-stack
knowledge_main: vsphere/technology/storage/concepts/esxi-storage-latency-stack
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05"
answer: [A]
misconception: [B]
misconception_type: [unit-and-normalization]
status: draft
```
