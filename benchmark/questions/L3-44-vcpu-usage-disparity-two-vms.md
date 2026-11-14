# vCPU Usage Disparity on two large VMs

## Prompt
- VCF Operations, last 7 days. Both VMs run on hosts with a 2.6 GHz base clock.
  - vm-x, 16 vCPUs: CPU Usage (%) 6-8%; CPU vCPU Usage Disparity (%) 104-117%.
  - vm-y, 16 vCPUs: CPU Usage (%) 4-5%; CPU vCPU Usage Disparity (%) 2-4%.
- Both owners refuse to give back vCPUs.

Which statements about vCPU Usage Disparity and these two VMs are correct?

- A. The disparity is the gap between the busiest and the least busy vCPU of the VM.
- B. The disparity is the average usage of the VM's vCPUs.
- C. For vm-x, a value above 100% means its busiest vCPU ran above the 2.6 GHz base clock, which Turbo Boost allows.
- D. For vm-x, a value above 100% is a collection error, since one vCPU cannot use more than its clock.
- E. With vm-x at 6-8% CPU Usage, none of its vCPUs can be saturated.
- F. vm-y uses its vCPUs evenly and lightly: its application does not keep even one vCPU busy.
- G. Any disparity between a VM's vCPUs is a fault: a healthy guest uses its vCPUs evenly.
- H. Add vCPUs to vm-x, so that the work of its busiest vCPU spreads over more of them.
- I. VCF Operations cannot see inside the guest, so the disparity does not show why one vCPU is busier.
- J. vCPUs taking turns at being the busiest point to processes moving between vCPUs.
- K. On a 16-vCPU VM the minimum among the vCPUs tells little: some vCPU almost always sits near 0%.

## Likely wrong answer
D: a disparity above 100% is impossible, so the data is wrong. Or E: the VM averages 6-8%, so no vCPU can be busy.

## Expected key points
- Answer: A, C, F, I, J, K.
- A true: VCF Operations builds the metric from per-vCPU usage: the peak among vCPUs minus the minimum.
- B false: an average across 16 vCPUs would hide the busy one; the metric exists to show it.
- C true: per-vCPU usage is measured against the base clock, and Turbo can push one vCPU above 100%. The minimum is near 0%, so the gap passes 100%.
- D false: the misconception. Turbo makes usage above 100% of base normal.
- E false: the misconception from the average. A gap above 100% means at least one vCPU is fully busy; 16 vCPUs average it down to single digits.
- F true: all vCPUs balanced and low: the application cannot consume even one vCPU (16 x 4-5% is under one vCPU in total), which questions the vendor's request.
- G false: over-correction. Disparity is an observation, not a diagnosis; vCPUs are not meant to be balanced, which is why the metric is named disparity, not imbalance.
- H false: wrong action. The work runs on few vCPUs; more vCPUs add idle vCPUs, not speed.
- I true: only the guest can show why (its CPU count, its threads, affinity).
- J true: the jumping-process pattern: frequent start and stop, or a process moving between vCPUs, each move costing a context switch and cache warm-up.
- K true: on a large VM the minimum is almost always near 0%; the peak and the gap carry the information.

## Notes
- Paired with the practical question 0101 (theory and practical; design.md, section 3.9). Situation numbers differ from 0101 and from the knowledge example on purpose.
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item B14). Counts only after author approval.

## Metadata
```yaml
id: "0366"
title: "vCPU Usage Disparity on two large VMs"
product: [vsphere, vcf-operations]
technology: [cpu]
task: read-metric
level: 300
answer_type: deterministic
input: [text]
object: [vm]
tool: [vcf-operations]
knowledge:
  - vsphere/technology/cpu/metrics/virtual-motherboard/usage-disparity
  - vsphere/technology/cpu/concepts/cpu-frequency
  - vsphere/technology/cpu/decision-tree/oversized-vm-downsizing
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/usage-disparity
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item B14"
answer: [A, C, F, I, J, K]
misconception: [D, E]
misconception_type: [average-hides-worst, frequency-and-hyper-threading]
pair: "0101"
status: draft
```
