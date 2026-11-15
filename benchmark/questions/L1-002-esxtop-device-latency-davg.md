# The esxtop counter for device latency

## Prompt
- In esxtop, the disk adapter and disk device panels show four latency counters per command.

Which counter measures the time from the ESXi host bus adapter to the storage array and back?

- A. GAVG
- B. KAVG
- C. QAVG
- D. DAVG

## Likely wrong answer
A: GAVG is the total latency the VM sees, not the device part.

## Expected key points
- Answer: D.
- DAVG (device average): from the ESXi HBA to the array and back.
- A is wrong: GAVG is the total seen from the VM monitor: kernel plus device.
- B is wrong: KAVG is the time spent in the VMkernel.
- C is wrong: QAVG is the time in kernel queues, part of KAVG.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Revised 2026-11-12 for question set 1.0. Counts only after author approval.

## Metadata
```yaml
id: "0032"
title: "The esxtop counter for device latency"
product: [vsphere]
technology: [storage]
task: read-metric
level: 100
answer_type: deterministic
input: [text]
object: [esxi]
tool: [esxtop]
knowledge:
  - vsphere/technology/storage/concepts/esxi-storage-latency-stack
  - vsphere/tools/esxtop/storage
knowledge_main: vsphere/technology/storage/concepts/esxi-storage-latency-stack
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05"
answer: [D]
misconception: [A]
misconception_type: []
status: draft
```
