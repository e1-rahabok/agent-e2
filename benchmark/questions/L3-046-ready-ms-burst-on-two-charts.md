# A Ready burst on the Real-time and Last day charts

## Prompt
- The owner of an 8-vCPU VM reports a short freeze about 45 minutes ago.
- You open the VM's CPU Ready (ms) in the vSphere Client: [the Real-time chart](0369/vcenter-vm-ready-real-time.png) and [the Last day chart](0369/vcenter-vm-ready-last-day.png). The marked 5-minute point on the Last day chart covers the minutes of the freeze.

Which statements are correct?

- A. Divided by 8 x 20,000 ms, the highest Real-time sample comes to about 2-3% per vCPU.
- B. The Real-time peak puts each vCPU in Ready about a fifth of that sample.
- C. A point on the Last day chart adds up the 15 Real-time samples of its 5 minutes.
- D. Divided by 8 x 300,000 ms, the marked Last day point is below 0.5% per vCPU.
- E. The freeze the owner reported cannot be CPU Ready: the 5-minute point is far below 1% per vCPU.
- F. Several Real-time samples in the same 5 minutes pass 3,000 ms.
- G. The marked Last day point reads higher in ms than the Real-time peak because it adds up 15 samples, not because the wait grew.
- H. Raise the vCenter statistics level to 4 so that the Last day chart keeps the burst at full height.
- I. Judge Ready from the Last day chart only: single 20-second samples are too noisy to mean anything.

## Input to supply
- Product and version: vSphere 9.1 (vSphere Client), statistics level 1 (default) for the 5-minute interval.
- Object: one VM with 8 vCPUs.
- Screen 1, vSphere Client > the VM > Monitor > Performance > Advanced > CPU, Chart Options: Real-time, the last hour, object the VM (not the vCPU instances), counter Ready (ms) only, with the legend table (Latest, Maximum, Average). Save as `0369/vcenter-vm-ready-real-time.png`.
- Screen 2, the same chart with Chart Options: Last day, counter Ready (ms). Hover over the 5-minute point that holds the burst so its tooltip shows the value, or mark it. Save as `0369/vcenter-vm-ready-last-day.png`.
- When: capture both 35-55 minutes after the burst: the Last day point can take up to 30 minutes to appear, and the Real-time chart keeps only the last hour.
- How to produce it in a lab: keep the VM busy on several vCPUs; for about 20 seconds start CPU burners in other VMs on the same host so that one Real-time sample of the VM jumps, then stop them.
- Condition the key depends on: one Real-time sample between 3,500 and 4,500 ms; every other sample in the same 5 minutes below 400 ms; the Last day point holding the burst above the Real-time peak and below 10,000 ms.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
B: 4,000 of 20,000 ms puts the VM in Ready a fifth of the time. Or E: the 5-minute point is low, so Ready cannot explain the freeze.

## Expected key points
- Answer: A, C, D, G.
- A true: Ready (ms) is summed over the 8 vCPUs; one 20-second sample holds 8 x 20,000 = 160,000 ms. 3,500-4,500 ms is about 2.2-2.8% per vCPU.
- B false: the misconception. 20,000 ms is the base of one vCPU; the VM value is the sum of eight.
- C true: Ready is a summation counter; the rollup sums the 15 samples (300,000 ms per vCPU).
- D true: a point below 10,000 ms against 8 x 300,000 = 2,400,000 ms is at most about 0.4%.
- E false: one 20-second sample in that window was at about 2.5% per vCPU, a burst the 5-minute point dilutes about 15 times. Ready lasts seconds; the freeze fits the burst.
- F false: reading. One sample stands out; the others in those 5 minutes stay below 400 ms.
- G true: a sum of 15 samples exceeds its largest sample, while its per-vCPU percentage is far lower.
- H false: wrong action. Ready is stored as a summation; a higher level adds minimum and maximum rollups of aggregated values, not the raw 20-second samples, so the 5-minute point stays diluted.
- I false: over-correction. Ready is read at the 20-second sample: a wait that lasts seconds shows there and is averaged away in 5-minute points.

## Reasoning path
1. Divide the Real-time peak by 20,000 ms x 8 vCPUs.
2. Divide the Last day point by 300,000 ms x 8 vCPUs.
3. Compare: the burst is diluted in the 5-minute point.

## Notes
- Paired with the theory question 0105 (theory and practical; design.md, section 3.9).
- vCenter rollups of summation counters are sums (knowledge base, vCenter statistics and aggregation; Broadcom KB 306576 (legacy 2002181), Converting between CPU summation and CPU % ready values: Past Day 300 seconds, ready % = summation / (interval in seconds x 1000) x 100, per vCPU after dividing by the vCPU count, https://knowledge.broadcom.com/external/article?legacyId=2002181). Not affected by Q224 (settled 2026-11-15: a VCF Operations 5-minute ms value averages the 15 samples, base 20,000 ms per vCPU): this question reads vCenter only. The vCenter rollup lengths moved from aggregation to collection-interval (section Base of a millisecond value) the same day.
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item C2). Counts only after author approval.
- Review 2026-11-15: options reworded away from 0105 (B, E, F, H, I); a false screen reading (F) added; the freeze is 45 minutes old, so both charts hold it. Key unchanged: A, C, D, G.

## Metadata
```yaml
id: "0369"
title: "A Ready burst on the Real-time and Last day charts"
product: [vsphere]
technology: [cpu]
task: read-metric
level: 300
answer_type: deterministic
input: [screenshot]
object: [vm]
tool: [vcenter]
knowledge:
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
  - vsphere/tools/vsphere-client/vcenter-statistics
  - sp5-framework/observability/aggregation
  - sp5-framework/observability/collection-interval
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/ready
attachments:
  - 0369/vcenter-vm-ready-real-time.png
  - 0369/vcenter-vm-ready-last-day.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C2"
answer: [A, C, D, G]
misconception: [B, E]
misconception_type: [unit-and-normalization, rollup-and-interval]
pair: "0105"
status: awaiting-input
```
