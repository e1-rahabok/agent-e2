# Latency counters in a vCenter virtual disk chart

## Prompt
[The attached screenshot](0034/vcenter-vm-virtual-disk-chart.png) is a vCenter performance chart of one VM, metric group Virtual disk.

Which of the counters in the chart measure latency? Choose all that apply.

- A. Read latency
- B. Write latency
- C. Read rate
- D. Write rate


## Screenshot
![vCenter advanced chart of one VM, Virtual disk: read and write latency (ms), read and write rate (KBps)](0034/vcenter-vm-virtual-disk-chart.png)

## Input to supply
- Tool: vCenter (vSphere Client 9.1).
- Where: one VM > Monitor > Performance > Advanced > Chart Options > Virtual disk.
- Counters to tick: Read latency, Write latency, Read rate, Write rate. Real-time interval.
- Must show: the legend at the bottom with the 4 counter names and their units (ms, KBps).
- Mask the VM name and the host name.
- Save as `benchmark/questions/34/vcenter-vm-virtual-disk-chart.png`.

## Likely wrong answer
C or D: taking the rate (KBps) for latency.

## Expected key points
- Answer: A, B.
- Read latency and Write latency are in milliseconds: the time per IO.
- Read rate and Write rate are in kilobytes per second: throughput, not latency.

## Notes
- Previous id: question-0034 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). 

## Metadata
```yaml
id: "0034"
title: "Latency counters in a vCenter virtual disk chart"
product: [vsphere]
technology: [storage]
task: read-metric
level: 100
answer_type: deterministic
input: [screenshot]
knowledge:
  - vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
  - vsphere/technology/storage/concepts/storage-layers
attachments:
  - 0034/vcenter-vm-virtual-disk-chart.png
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 100-200 allocation (benchmark/design.md, section 3.6)"
answer: [A, B]
misconception: [C]
status: approved
```
