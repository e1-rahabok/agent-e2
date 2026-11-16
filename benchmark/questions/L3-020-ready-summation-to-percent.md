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
- E. Ready (ms) on the 1 Day chart cannot be compared with the Real-time value: the two use different units.
- F. A Ready of 4% per vCPU in one sample calls for two more vCPUs to spread the wait.

## Likely wrong answer
B: the milliseconds of all 4 vCPUs read against one vCPU.

## Expected key points
- Answer: A, C.
- A is correct: Ready (ms) is a summation over the sample, added up over all vCPUs; 100% for one vCPU is the sample length. 3,200 / (20,000 × 4) = 4%.
- B is wrong: 3,200 ms is the sum over the 4 vCPUs. 16% is the VM-level sum (as the VMware conversion of 3,200 / 20,000 gives); per vCPU it is 4%. The VM has 80,000 vCPU-ms per 20-second sample.
- C is correct: the 1 Day chart sums 15 Real-time samples over 300 seconds: 12,000 / (300,000 × 4) = 1%.
- D is wrong: a 5-minute point on the vCenter 1 Day chart sums its 15 samples, so its base is 300,000 ms per vCPU, not 20,000. (20,000 ms per vCPU is the base of a VCF Operations 5-minute value, an average of the 15 samples.)
- E is wrong: both are milliseconds summed over the interval; divided by the interval length (20,000 or 300,000 ms per vCPU) they compare directly.
- F is wrong: more vCPUs make co-scheduling harder and can raise Ready; a single 4% sample is no reason to resize.
- The Readiness (%) counter is already per vCPU and avoids the conversion.

## Notes
- Options F (the over-correction) and G (the wrong action) added 2026-11-14 (design.md 3.9; project/question-pairing-2026-11-14.md). Key unchanged, A, C.
- B kept: the audit listed it as a copy of option E of 0231. 0231 E tests that statistics level 1 keeps only the VM total, so one vCPU's wait cannot be told apart; B here tests the ms-to-% conversion over the vCPU count, the core of this question.
- Paired with 0369 (theory and practical, design.md 3.9).
- 2026-11-15 audit: old E ("the 5-minute point shows that no 20-second sample passed about 1%", a rollup misconception) dropped: a rolled-up point diluting a burst is the most repeated fact in the bank (home: 0047/0432). Letters: old F -> E, old G -> F.

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
source_path: "Synthetic, 2026-11-12"
answer: [A, C]
misconception: [B]
misconception_type: [unit-and-normalization, rollup-and-interval]
pair: "0369"
status: draft
```
