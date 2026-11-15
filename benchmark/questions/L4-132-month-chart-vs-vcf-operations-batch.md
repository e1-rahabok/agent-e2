# A batch burst on the month chart and in VCF Operations

## Prompt
- A 16-vCPU reporting VM ran a batch for about 20 minutes last Tuesday night.
- The application owner compares [the vSphere Client Last month chart](0370/vcenter-vm-cpu-usage-last-month.png), where the marked 2-hour point covers the batch, with [the VCF Operations chart](0370/vcf-operations-vm-cpu-2-hours.png) of the same VM for the same 2 hours.
- She says: "VCF Operations exaggerates the batch. vCenter shows a far lower number."

Which statements are correct?

- A. The marked 2-hour point averages the VM's Usage over its 2 hours, so the 20-minute batch is about a sixth of what it averages.
- B. The marked 2-hour point is higher than every 5-minute Usage value VCF Operations shows for those 2 hours.
- C. VCF Operations overstates the batch: its 5-minute values should equal the vCenter point.
- D. Each tool computes Usage its own way, so the two screens can never be set side by side.
- E. The Contention line is a VCF Operations calculation; the vSphere Client has no such counter to chart for the VM.
- F. On the VCF Operations chart, Contention during the batch equals Ready.
- G. Co-stop accounts for most of the distance between Contention and Ready during the batch.
- H. Contention rose during the batch, so the cluster needs another host.
- I. For a 20-minute batch, the 5-minute values describe the load better than the 2-hour point.

## Input to supply
- Product and version: vSphere 9.1 (vSphere Client) and VCF Operations 9.1, the same VM.
- Object: one VM with 16 vCPUs, no CPU limit, sized to fit one NUMA node of its host.
- Screen 1, vSphere Client > the VM > Monitor > Performance > Advanced > CPU, Chart Options: Last month, counter Usage (%). Hover over (or mark) the 2-hour point that covers the batch so its value shows. Save as `0370/vcenter-vm-cpu-usage-last-month.png`.
- Screen 2, VCF Operations > the VM > Metrics: CPU|Usage (%), CPU|Contention (%), CPU|Ready (%), CPU|Co-stop (%) on one chart, zoomed to the same 2 hours (24 five-minute points), values of the batch points visible on hover or in the data grid. Save as `0370/vcf-operations-vm-cpu-2-hours.png`.
- How to produce it in a lab: run a 16-thread CPU burner in the VM for about 20 minutes (four whole VCF Operations cycles) on a host made busy with burners in other VMs so the VM also shows Co-stop; keep the VM at light load for the rest of the 2-hour window. Capture once the Last month rollup holds the point (up to about 3 hours later).
- Condition the key depends on: in VCF Operations, four consecutive Usage points at 80-100% and the other twenty at 20-40%; the vSphere Last month point within 5 points of the mean of the 24 and below the lowest batch point; during the batch, Contention at least 2 points above Ready, with Co-stop making up most of that gap; no CPU limit on the VM.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
C: the two tools should show the same number, so VCF Operations is wrong. Or F: Contention is just Ready under another name.

## Expected key points
- Answer: A, E, G, I.
- A true: the Last month interval keeps 2-hour points averaged from four 1 Week points; the 20 minutes of batch weigh a sixth.
- B false: reading and arithmetic. An average cannot exceed the values it averages; the marked point sits below every batch point.
- C false: the misconception. Usage is a vSphere counter that VCF Operations passes through; the screens differ in interval and rollup, not in collection.
- D false: over-correction. Usage has one meaning in both tools; the averaging window is what differs.
- E true: Contention is a VCF Operations metric; the nearest vSphere counter is Latency, with another formula.
- F false: reading. Contention runs at least 2 points above Ready during the batch: it adds Co-stop, Overlap and small Other Wait to Ready.
- G true: reading. Contention = Overlap + Co-stop + Ready + Other Wait (below 1%); Co-stop fills most of the gap here.
- H false: wrong action. Contention mixes causes; here most of the rise is Co-stop, which comes from the VM's own vCPUs drifting apart. Check the other VMs' Ready, limits, shares and the VM's width before adding a host.
- I true: the 5-minute points show the batch plateau that the 2-hour average flattens.

## Reasoning path
1. The 2-hour point averages 24 five-minute values: the batch is a sixth of it.
2. Subtract Ready from Contention during the batch and compare the rest with Co-stop.
3. No collection fault: interval, rollup and formula explain both gaps.

## Notes
- Paired with the theory question 0357 (theory and practical; design.md, section 3.9).
- Contention formula: Broadcom KB 394770 (sum of overlap, ready, co-stop and other wait). Last month interval: vSphere Monitoring and Performance, Data Collection Intervals (2-hour points from four 1 Week points).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item C5). Counts only after author approval.
- Review 2026-11-15: new situation (16-vCPU batch VM, Last month 2-hour point, the application owner) and new wording, away from 0357; screen readings added (B, F false; G true). Key letters A, E, G, I, on the new options.

## Metadata
```yaml
id: "0370"
title: "A batch burst on the month chart and in VCF Operations"
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
  - 0370/vcenter-vm-cpu-usage-last-month.png
  - 0370/vcf-operations-vm-cpu-2-hours.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C5"
answer: [A, E, G, I]
misconception: [C, F]
misconception_type: [tool-confusion, rollup-and-interval]
pair: "0357"
status: awaiting-input
```
