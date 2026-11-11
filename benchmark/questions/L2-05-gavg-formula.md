# How the esxtop storage latencies add up

## Prompt
In esxtop, the disk panels show GAVG, KAVG, QAVG and DAVG.

How do they relate?

- A. GAVG = KAVG + DAVG. QAVG is part of KAVG.
- B. GAVG = KAVG + QAVG + DAVG.
- C. GAVG = DAVG - KAVG.
- D. GAVG = QAVG + DAVG. KAVG is part of QAVG.

## Likely wrong answer
B: adding QAVG on top of KAVG, counting the queue time twice.

## Expected key points
- Answer: A.
- GAVG (total seen from the VMM) = KAVG (time in the VMkernel) + DAVG (device).
- QAVG is the queue part of the kernel time, so it is already inside KAVG. QAVG can even exceed KAVG, because QAVG covers kernel IO too.

## Notes
- Previous id: question-0043 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
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
knowledge:
  - vsphere/technology/storage/concepts/esxi-storage-latency-stack
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 100-200 allocation (benchmark/design.md, section 3.6)"
answer: [A]
misconception: [B]
status: draft
```
