# CPU Ready in milliseconds on two charts

## Prompt
- A 4-vCPU VM.
- In the vSphere Client, the Real-time chart shows CPU Ready of 3,200 ms for one sample.
- The 1 Day chart shows CPU Ready of 12,000 ms for the 5-minute point that holds that sample.

Which statements are correct?

- A. In the Real-time sample, a vCPU was ready about 4% of the time on average.
- B. In the Real-time sample, each vCPU was ready 16% of the time: 3,200 of 20,000 ms.
- C. Over the 5-minute point, a vCPU was ready about 1% of the time on average.
- D. The 5-minute point is about 15% per vCPU: 12,000 of 20,000 ms, divided by the 4 vCPUs.
- E. The 5-minute point shows that no 20-second sample in those 5 minutes passed about 1% per vCPU.

## Likely wrong answer
B: the milliseconds of all 4 vCPUs read against one vCPU. Or E: the 5-minute value read as the worst moment.

## Expected key points
- Answer: A, C.
- Ready (ms) is a summation over the sample, added up over all vCPUs. 100% for one vCPU is the sample length.
- A: 3,200 / (20,000 × 4) = 4%.
- B is wrong: 3,200 ms is the sum over the 4 vCPUs. 16% is the VM-level sum (as the VMware conversion of 3,200 / 20,000 gives); per vCPU it is 4%. The VM has 80,000 vCPU-ms per 20-second sample.
- C: the 1 Day chart sums 15 Real-time samples over 300 seconds: 12,000 / (300,000 × 4) = 1%.
- D is wrong: a 5-minute point is not a 20-second sample.
- E is wrong: one sample in the window was at 4%. A 5-minute point averages the burst away.
- The Readiness (%) counter is already per vCPU and avoids the conversion.

## Metadata
```yaml
id: "0105"
title: "CPU Ready in milliseconds on two charts"
product: [vsphere]
technology: [cpu]
task: read-metric
level: 300
answer_type: deterministic
input: [text]
object: [vm]
tool: [vcenter]
knowledge:
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
  - vsphere/tools/vsphere-client/vcenter-statistics
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/ready
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12 for the CPU slots (project/plan.md, M2)"
answer: [A, C]
misconception: [B, E]
misconception_type: [unit-and-normalization, rollup-and-interval]
status: draft
```
