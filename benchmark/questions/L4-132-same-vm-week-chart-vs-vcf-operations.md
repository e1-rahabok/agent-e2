# One VM, the vSphere week chart and VCF Operations

## Prompt
- The owner of an 8-vCPU VM reported about ten minutes of slowness yesterday afternoon.
- [The vSphere Client chart](0370/vcenter-vm-cpu-usage-last-week.png) shows the VM's CPU Usage (%) on the Last week view; the marked point covers the 30 minutes around the slowness.
- [The VCF Operations chart](0370/vcf-operations-vm-cpu-30-minutes.png) shows the same VM in the same 30 minutes.
- A platform engineer says: "The two tools do not agree. Open a support case against VCF Operations."

Which statements are correct?

- A. The marked Last week point is about the mean of the six 5-minute VCF Operations Usage values.
- B. VCF Operations collects CPU Usage wrongly or late, since its values do not match the vSphere chart.
- C. The Last week chart keeps the highest value of each 30-minute window.
- D. CPU Usage has its own formula in each tool, so the two numbers are not comparable.
- E. CPU Contention (%) is computed by VCF Operations; vSphere has no counter of that name.
- F. CPU Contention (%) is the vSphere Ready counter shown under another name.
- G. At the busiest point, most of the gap between Contention and Ready is the VM's Co-stop.
- H. Contention at the busiest point shows the cluster is short of CPU: add a host.
- I. For the ten minutes of slowness, the 5-minute VCF Operations values are sharper evidence than the 30-minute point.
- J. At the busiest point, Ready alone is the whole time the VM's vCPUs could not run.

## Input to supply
- Product and version: vSphere 9.1 (vSphere Client) and VCF Operations 9.1, the same VM.
- Object: one VM with 8 vCPUs or more, no CPU limit.
- Screen 1, vSphere Client > the VM > Monitor > Performance > Advanced > CPU, Chart Options: Last week, counter Usage (%). Hover over (or mark) the 30-minute point that covers the burst so its value shows. Save as `0370/vcenter-vm-cpu-usage-last-week.png`.
- Screen 2, VCF Operations > the VM > Metrics: CPU|Usage (%), CPU|Contention (%), CPU|Ready (%), CPU|Co-stop (%) on one chart, zoomed to the same 30 minutes (six 5-minute points), values visible on hover or in the data grid. Save as `0370/vcf-operations-vm-cpu-30-minutes.png`.
- How to produce it in a lab: run a multi-thread CPU burner in the VM for about 10 minutes, aligned to two whole VCF Operations cycles, on a host made busy with burners in other VMs so the VM also shows Co-stop. Capture the next day, once the Last week rollup has the point.
- Condition the key depends on: in VCF Operations, two consecutive Usage points at 80-100% and the other four at 25-50%; the vSphere Last week point within 3 points of the mean of the six; at the busiest point, Contention at least 2 points above Ready, with Co-stop making up most of that gap; no CPU limit on the VM.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
B: the tools disagree on Usage, so VCF Operations is wrong. Or F: Contention is Ready under another name, so Contention above Ready is an error.

## Expected key points
- Answer: A, E, G, I.
- A true: the Last week interval stores 30-minute points built from six 5-minute points, averaged. The burst is averaged with four quiet points.
- B false: the misconception. CPU Usage is a vSphere counter that VCF Operations passes through; the gap is the interval and the rollup.
- C false: the rollup is an average; peaks are rolled away.
- D false: over-correction. Usage has one meaning in both tools; only the interval differs.
- E true: Contention is a VCF Operations metric; vSphere's nearest counter is Latency.
- F false: the misconception. Contention adds Co-stop, Overlap and small Other Wait to Ready, so it reads above Ready.
- G true: Contention = Overlap + Co-stop + Ready + Other Wait (below 1%); on this capture Co-stop fills most of the gap.
- H false: wrong action. Contention mixes causes; much of it here is Co-stop, which comes from the VM's own vCPUs drifting apart. Check Ready across the host's VMs, limits, shares and the VM's size before adding capacity.
- I true: the 5-minute values show the plateau that the 30-minute average hides.
- J false: Co-stop, Overlap and Other Wait also stop the vCPUs; Ready alone understates the wait.

## Reasoning path
1. Average the six VCF Operations Usage points and compare with the Last week point.
2. Subtract Ready from Contention at the busiest point and compare the rest with Co-stop.
3. No collection fault: interval, rollup and formula explain both gaps.

## Notes
- Paired with the theory question 0357 (theory and practical; design.md, section 3.9).
- Contention formula: Broadcom KB 394770 (sum of overlap, ready, co-stop and other wait). Last week interval: vSphere Monitoring and Performance, Data Collection Intervals (30-minute points from six 1 Day points).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item C5). Counts only after author approval.

## Metadata
```yaml
id: "0370"
title: "One VM, the vSphere week chart and VCF Operations"
product: [vsphere, vcf-operations]
technology: [cpu, system]
task: troubleshoot
level: 400
answer_type: deterministic
input: [screenshot]
object: [vm]
tool: [vcenter, vcf-operations]
knowledge:
  - vcf-operations/vcf-operations-role
  - vsphere/technology/cpu/metrics/virtual-motherboard/contention
  - vsphere/technology/cpu/metrics/comparisons/vm-contention-metrics
  - vsphere/tools/vsphere-client/vcenter-statistics
  - vsphere/technology/cpu/metrics/virtual-motherboard/co-stop
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/contention
attachments:
  - 0370/vcenter-vm-cpu-usage-last-week.png
  - 0370/vcf-operations-vm-cpu-30-minutes.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C5"
answer: [A, E, G, I]
misconception: [B, F]
misconception_type: [tool-confusion, rollup-and-interval]
pair: "0357"
status: awaiting-input
```
