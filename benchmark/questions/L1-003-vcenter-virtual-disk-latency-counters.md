# Latency counters in a vCenter virtual disk chart

## Prompt
[The attached screenshot](0034/vcenter-vm-virtual-disk-chart.png) is a vCenter performance chart of one VM, metric group Virtual disk.

Which of the counters in the chart measure latency? Choose all that apply.

- A. Read latency
- B. Write latency
- C. Read rate
- D. Write rate


## Screenshot
![vCenter advanced performance chart of one VM, metric group Virtual disk, with four counters in the legend](0034/vcenter-vm-virtual-disk-chart.png)

## Answers
A, B

## Explanation
- A is correct: Read latency is in milliseconds, the time per read.
- B is correct: Write latency is in milliseconds, the time per write.
- C is wrong: Read rate is in kilobytes per second: read throughput, not latency.
- D is wrong: Write rate is in kilobytes per second: write throughput, not latency.
- Misconception: C or D: taking the rate (KBps) for latency.

## Notes
- 2026-11-14 (project/question-pairing-2026-11-14.md, section 3.B): in the screenshot, the VM name masked in the title and the legend (every VM name is masked); the stale `## Input to supply` removed.
- Synthetic, 2026-11-05, from the knowledge files listed in `knowledge`.
- Re-review 2026-11-16: who-said-it tags removed from `source_path` and Notes; the screenshot alt text no longer gives the units (the key); key points one per option. Key unchanged.

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
source_path: "Synthetic, 2026-11-05"
misconception: [C]
object: [vm]
tool: [vcenter]
knowledge_main: vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
misconception_type: []
status: reviewed
```
