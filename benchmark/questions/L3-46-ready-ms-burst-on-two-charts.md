# A Ready burst on the Real-time and Last day charts

## Prompt
- The owner of an 8-vCPU VM reports a short freeze about 20 minutes ago.
- You open the VM's CPU Ready (ms) in the vSphere Client: [the Real-time chart](0369/vcenter-vm-ready-real-time.png) and [the Last day chart](0369/vcenter-vm-ready-last-day.png). The marked 5-minute point on the Last day chart covers the minutes of the burst.

Which statements are correct?

- A. The highest Real-time sample is about 2-3% Ready per vCPU: its value against 160,000 ms.
- B. The highest Real-time sample is about 20% Ready: its value against 20,000 ms.
- C. A point on the Last day chart is the sum of the 15 Real-time samples in its 5 minutes.
- D. The marked Last day point is below 0.5% Ready per vCPU: its value against 2,400,000 ms.
- E. The marked Last day point shows that no 20-second sample in those 5 minutes passed 0.5% per vCPU.
- F. The Last day chart cannot be read as a percentage: a 5-minute Ready value has no fixed base.
- G. The marked Last day point reads higher in ms than the Real-time peak because it adds up 15 samples, not because the wait grew.
- H. Add 2 vCPUs to the VM to absorb bursts like this one.

## Input to supply
- Product and version: vSphere 9.1 (vSphere Client), statistics level 1 (default) for the 5-minute interval.
- Object: one VM with 8 vCPUs.
- Screen 1, vSphere Client > the VM > Monitor > Performance > Advanced > CPU, Chart Options: Real-time, the last hour, object the VM (not the vCPU instances), counter Ready (ms) only, with the legend table (Latest, Maximum, Average). Save as `0369/vcenter-vm-ready-real-time.png`.
- Screen 2, the same chart with Chart Options: Last day, counter Ready (ms). Hover over the 5-minute point that holds the burst so its tooltip shows the value, or mark it. Capture within the hour after the burst, while the Real-time chart still holds it. Save as `0369/vcenter-vm-ready-last-day.png`.
- How to produce it in a lab: keep the VM busy on several vCPUs; for about 20 seconds start CPU burners in other VMs on the same host (or briefly lower the host's free threads) so that one Real-time sample of the VM jumps, then stop them.
- Condition the key depends on: one Real-time sample between 3,500 and 4,500 ms; every other sample in the same 5 minutes below 400 ms; the Last day point holding the burst above the Real-time peak and below 10,000 ms.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
B: 4,000 of 20,000 ms is 20% Ready. Or E: the 5-minute point is low, so there was no burst.

## Expected key points
- Answer: A, C, D, G.
- A true: Ready (ms) is summed over the 8 vCPUs; one 20-second sample holds 8 x 20,000 = 160,000 ms. 3,500-4,500 ms is about 2.2-2.8% per vCPU.
- B false: the misconception. 20,000 ms is the base of one vCPU; the VM value is the sum of eight.
- C true: Ready is a summation counter; the rollup sums the 15 samples (300,000 ms per vCPU).
- D true: a point below 10,000 ms against 8 x 300,000 = 2,400,000 ms is at most about 0.4%.
- E false: one sample in that window was at about 2.5% per vCPU; the 5-minute point dilutes it about 15 times.
- F false: over-correction. The base is fixed: 300,000 ms per vCPU for a 5-minute point.
- G true: a sum of 15 samples exceeds its largest sample; the per-vCPU percentage of the point is far lower.
- H false: wrong action. More vCPUs make a VM harder to schedule and tend to raise Ready; one short burst is no sizing evidence.

## Reasoning path
1. Divide the Real-time peak by 20,000 ms x 8 vCPUs.
2. Divide the Last day point by 300,000 ms x 8 vCPUs.
3. Compare: the burst is diluted in the 5-minute point.

## Notes
- Paired with the theory question 0105 (theory and practical; design.md, section 3.9).
- vCenter rollups of summation counters are sums (knowledge base, vCenter statistics and aggregation; Broadcom KB 306576 (legacy 2002181), Converting between CPU summation and CPU % ready values: Past Day 300 seconds, ready % = summation / (interval in seconds x 1000) x 100, per vCPU after dividing by the vCPU count, https://knowledge.broadcom.com/external/article?legacyId=2002181). Not affected by the open question on VCF Operations 5-minute ms values (the 0104 base): this question reads vCenter only.
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item C2). Counts only after author approval.

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
