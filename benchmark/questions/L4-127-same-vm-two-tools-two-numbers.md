# The same VM in two tools, two numbers

## Prompt
- app-07, 8 vCPUs, yesterday between 14:00 and 14:30. The owner reported slowness around 14:15.
- vSphere Client, 1 Week chart, CPU Usage, the 30-minute point at 14:00: 58%.
- VCF Operations, CPU Usage (%) for the same VM, the six 5-minute points from 14:00 to 14:25: 40, 38, 42, 96, 92, 40.
- At the 14:15 cycle (the 96% point), VCF Operations shows CPU Contention (%) of 9.8%. The vSphere Client 1 Day chart for the same cycle shows CPU Ready of 2.9% per vCPU, and no counter called Contention.
- The 14:15 cycle in VCF Operations also shows these 5-minute values: Co-stop 6.4%, Overlap 0.2%, Other Wait 0.3%.
- The platform engineer says: "The two tools disagree, so one of them collects wrongly. Open a support case against VCF Operations."

Is one of the tools wrong? Explain both differences, say which number you would quote for the slowness, and say what you check next.

## Likely wrong answer
"The tools disagree on Usage and on Contention, so the VCF Operations data is wrong or delayed." Or "Contention is the vSphere Ready counter under another name, so 9.8% against 2.9% shows an error."

## Expected key points
- Neither tool is wrong. CPU Usage is a passed-through metric: VCF Operations takes the vSphere counter and its meaning is set by vSphere. The two numbers differ in interval and rollup: the vCenter 1 Week point is the average of six 5-minute points ((40 + 38 + 42 + 96 + 92 + 40) / 6 = 58%), which hides a plateau of about 95% for 10 minutes. Compare like with like; the 5-minute points are the sharper view.
- CPU Contention is computed by VCF Operations from vSphere counters; vSphere has no counter of that name (its nearest counter is Latency). The metric sums the time a vCPU does not get CPU: Overlap + Co-stop + Ready + Other Wait = 0.2 + 6.4 + 2.9 + 0.3 = 9.8%. It is not Ready under another name, so it cannot match the 2.9%.
- Most of the 9.8% is Co-stop (6.4%), not Ready: for an 8-vCPU VM the siblings are held back when one vCPU waits. The slowness at 14:15 is multi-vCPU scheduling loss, not a shortage of host CPU alone, and the Ready figure alone understates it.
- Quote Contention with its components (or Ready and Co-stop), read against Run: with Usage near 96% in those cycles, a loss of nearly 10% is material.
- Next: the CPU contention flow for the VM: Ready against Run at the 20-second peak, Co-stop and the vCPU count against the work (oversized wide VM), limits and shares, and the host load in the same cycles. The role split: vCenter is the administrative tool with a short, averaged history; analysis and history of contention are read in VCF Operations.

## Notes
- Public source: Broadcom KB 394770, How is CPU Contention (%) calculated (Aria/VCF Operations 8.x; no updated date shown): "Value is the sum of CPU overlap, ready, co-stop and other wait", from the 15 20-second points of each 5-minute cycle. vSphere 9.1 Monitoring and Performance: Data Collection Intervals (1 Week: 30-minute points; 6 points of 1 Day); Usage rollup is an average. The knowledge file states that Other Wait is added only when below 1% and that from VCF Operations 8.18 the formula includes limit time; the KB does not say so, and neither fact is used in the key (Other Wait is 0.3% and the VM has no limit in the scenario).
- Why one answer: both differences are arithmetic on the numbers given plus documented definitions.
- Debatable risk: low. I did not verify the knowledge file's July 2024 (8.18) change of the formula; the question does not rely on it.
- Rests on: the role file's principle that a passed-through metric means what its source means and only computed metrics have their own definition; the vendor sources above.

## Metadata
```yaml
id: "0357"
title: "The same VM in two tools, two numbers"
product: [vsphere, vcf-operations]
technology: [cpu, system]
task: explain-mechanism
level: 400
answer_type: judged
input: [text]
object: [vm]
tool: [vcenter, vcf-operations]
knowledge:
  - vcf-operations/vcf-operations-role
  - vsphere/technology/cpu/metrics/virtual-motherboard/contention
  - vsphere/technology/cpu/metrics/comparisons/vm-contention-metrics
  - vsphere/tools/vsphere-client/vcenter-statistics
  - vsphere/technology/cpu/metrics/virtual-motherboard/co-stop
knowledge_main: vcf-operations/vcf-operations-role
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
misconception_type: [tool-confusion, rollup-and-interval]
status: draft
```
