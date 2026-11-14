# The same VM in two tools, two numbers

## Prompt
- app-07, 8 vCPUs, yesterday between 14:00 and 14:30. The owner reported slowness around 14:15.
- vSphere Client, 1 Week chart, CPU Usage, the 30-minute point at 14:00: 58%.
- VCF Operations, CPU Usage (%) for the same VM, the six 5-minute points from 14:00 to 14:25: 40, 38, 42, 96, 92, 40.
- At the 14:15 cycle (the 96% point), VCF Operations shows CPU Contention (%) of 9.8%. The vSphere Client 1 Day chart for the same cycle shows CPU Ready of 2.9% per vCPU, and no counter called Contention.
- The 14:15 cycle in VCF Operations also shows these 5-minute values: Co-stop 6.4%, Overlap 0.2%, Other Wait 0.3%.
- The platform engineer says: "The two tools disagree, so one of them collects wrongly. Open a support case against VCF Operations."

Which statements about the two pairs of numbers and the next step are correct?

- A. Neither tool collects wrongly: the two CPU Usage numbers differ in interval and rollup.
- B. The tools disagree on CPU Usage, so VCF Operations collects wrongly or late.
- C. The 58% point is the mean of the six 5-minute values, which hides about ten minutes near 95%.
- D. The 1 Week chart keeps the highest value of each 30-minute window, so 58% was the peak at 14:00.
- E. vSphere has no counter named Contention; VCF Operations computes it from vSphere counters.
- F. CPU Contention is the vSphere Ready counter under another name, so 9.8% against 2.9% points to a collection error.
- G. The 9.8% is Overlap plus Co-stop plus Ready plus Other Wait for the 14:15 cycle.
- H. CPU Contention in VCF Operations 9.1 is the vSphere CPU Latency counter, passed through.
- I. Most of the 9.8% at 14:15 is Co-stop, not Ready.
- J. The co-stopped vCPUs of app-07 were held back because no physical thread was free for them.
- K. Ready of 2.9% per vCPU is the full CPU wait of app-07 in the 14:15 cycle.
- L. For the 14:15 slowness, the 5-minute VCF Operations values are sharper evidence than the 1 Week point.
- M. Co-stop tends to rise with the vCPU count, so a next check is whether the work of app-07 needs eight vCPUs.
- N. History and analysis of contention are read in VCF Operations; vCenter keeps a short, averaged history.

## Likely wrong answer
- B: "The tools disagree on Usage, so the VCF Operations data is wrong or delayed."
- F: "Contention is the vSphere Ready counter under another name, so 9.8% against 2.9% shows an error."

## Expected key points
- Answer: A, C, E, G, I, L, M, N.
- A true: CPU Usage is a passed-through metric: VCF Operations takes the vSphere counter, and its meaning is set by vSphere. Compare like with like.
- B false: the difference is the interval (30 minutes against 5 minutes) and the rollup (average), not collection.
- C true: (40 + 38 + 42 + 96 + 92 + 40) / 6 = 58%. The 1 Week point is built from six 1 Day points.
- D false: the 1 Week chart shows 30-minute averages; peaks are rolled away.
- E true: CPU Contention is computed by VCF Operations; vSphere has no counter of that name (its nearest counter is Latency).
- F false: Contention sums the time a vCPU does not get CPU, so it cannot match Ready alone.
- G true: 0.2 + 6.4 + 2.9 + 0.3 = 9.8% (Other Wait is added while below 1%).
- H false: Contention has its own formula (Broadcom KB 394770: the sum of overlap, ready, co-stop and other wait). Latency also reflects Hyper-Threading and frequency, which Contention does not.
- I true: Co-stop is 6.4 of the 9.8 points. For an 8-vCPU VM the siblings are held back when one vCPU waits: multi-vCPU scheduling loss, not a shortage of host CPU alone.
- J false: co-stopped vCPUs are held back to stay in step with a sibling, even when physical threads are free for them.
- K false: Co-stop (6.4%), Overlap and Other Wait add to the wait; Ready alone understates it. Quote Contention with its parts, or Ready and Co-stop, read against Run.
- L true: the 5-minute points show the 96% and 92% plateau that the 30-minute average hides.
- M true: Co-stop tends to be higher on VMs with more vCPUs. Next in the contention flow: Ready against Run at the 20-second peak, Co-stop and the vCPU count against the work, limits and shares, and the host load in the same cycles.
- N true: vCenter is the administrative tool, with a short history that rolls peaks away; capacity and performance analysis are done in VCF Operations.

## Notes
- Public source: Broadcom KB 394770, How is CPU Contention (%) calculated (Aria/VCF Operations 8.x; no updated date shown): "Value is the sum of CPU overlap, ready, co-stop and other wait", from the 15 20-second points of each 5-minute cycle. vSphere 9.1 Monitoring and Performance: Data Collection Intervals (1 Week: 30-minute points; 6 points of 1 Day); Usage rollup is an average. The knowledge file states that Other Wait is added only when below 1% and that from VCF Operations 8.18 the formula includes limit time; the KB does not say so, and neither fact is used in the key (Other Wait is 0.3% and the VM has no limit in the scenario).
- Why one answer: both differences are arithmetic on the numbers given plus documented definitions.
- Debatable risk: low. I did not verify the knowledge file's July 2024 (8.18) change of the formula; the question does not rely on it.
- Rests on: the role file's principle that a passed-through metric means what its source means and only computed metrics have their own definition; the vendor sources above.
- Converted from judged to multiple choice (Q199 F, 2026-11-14). Option H rests on Broadcom KB 394770 (the formula) and the knowledge file's comparison of Contention and Latency, not on the 8.18 date.

## Metadata
```yaml
id: "0357"
title: "The same VM in two tools, two numbers"
product: [vsphere, vcf-operations]
technology: [cpu, system]
task: explain-mechanism
level: 400
answer_type: deterministic
answer: [A,C,E,G,I,L,M,N]
misconception: [B,F]
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
