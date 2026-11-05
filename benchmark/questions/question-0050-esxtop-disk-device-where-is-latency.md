# Where the storage latency sits in esxtop

## Prompt
The attached screenshot is the esxtop disk device panel (u) of one ESXi host.

For the device with the highest GAVG, where does most of the latency come from?

- A. The device side: the fabric or the array (DAVG).
- B. The VMkernel queue (QAVG).
- C. The Guest OS.
- D. It cannot be told from esxtop.

## Input to supply
- Tool: esxtop on one ESXi 9.1 host, disk device panel (press u).
- Must show the columns DEVICE, DAVG/cmd, KAVG/cmd, GAVG/cmd, QAVG/cmd, and at least 3 devices.
- Condition for the key: the device with the highest GAVG has KAVG under 0.5 ms and DAVG at least 2 ms.
- Mask device names if they reveal the customer.
- Save as `benchmark/questions/question-0050/esxtop-disk-device-panel.png`.

## Likely wrong answer
B: blaming the ESXi queue when KAVG is small.

## Expected key points
- Answer: A.
- GAVG = KAVG + DAVG. Here KAVG is under 0.5 ms and DAVG makes up the rest: the latency is beyond the HBA.
- Next: check the fabric and the array (front-end ports, cache, back end). If the array reports low latency, check the fabric or the HBA configuration.
- C is wrong: esxtop has no Guest OS metrics; the guest queue is invisible to ESXi.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: question-0050
title: "Where the storage latency sits in esxtop"
product: [vsphere]
technology: [storage]
task: troubleshoot
level: 200
answer_type: deterministic
input: [screenshot]
knowledge:
  - vsphere/technology/storage/concepts/esxi-storage-latency-stack
  - vsphere/technology/storage/metrics/comparisons/esxtop-storage
  - vsphere/foundations/esxtop
attachments:
  - question-0050/esxtop-disk-device-panel.png
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 100-200 allocation (benchmark/design.md, section 3.6)"
answer: [A]
trap: [B]
status: awaiting-input
```
