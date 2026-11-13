# A 20-second peak from nine days ago

## Prompt
- The backup window of vm-sql-03 ran nine days ago between 02:00 and 02:30. The DBA asks how high the disk latency of the VM got in any 20-second period of that window. The VM has 20 virtual disks.
- vCenter 9.1 keeps its default collection intervals and statistics level. VCF Operations 9.1 has collected from that vCenter every 5 minutes since before the window, with a time series retention of 6 months and the default policy.
- In the 5-minute data of VCF Operations, the disk latency of the VM at 02:15 is 12 ms. The metric "Peak Latency within collection cycle" for the same 5-minute cycle is 1,900 ms.
- You have both tools open.

Which statement is correct?

- A. Select the date in the vCenter Real-time chart: it holds 20-second points and shows the window.
- B. The vCenter 1 Week chart shows the answer: its 30-minute point averages the 5-minute values, so the peak is the highest of them.
- C. The 12 ms value is the answer: VCF Operations stores the 5-minute average only, so the 1,900 ms cannot come from the window.
- D. VCF Operations answers: the peak metric keeps the highest 20-second value of each cycle, though not which disk, nor which of the 15 periods.
- E. Neither tool answers: the 20-second samples are gone everywhere after one hour, so the DBA must reproduce the backup.

## Likely wrong answer
B or E: the chart history is read as a store of peaks, or the 20-second data is assumed to be lost everywhere.

## Expected key points
- Answer: D.
- vCenter keeps the 20-second samples for one hour only (A is wrong). Its history is a chain of averages: 15 samples into a 5-minute point, 6 of those into the 30-minute point of the 1 Week chart. A 20-second burst is diluted 90 times there and cannot be recovered (B is wrong).
- VCF Operations computes the peak while it collects: each 5-minute cycle it reads the 15 samples of 20 seconds from vCenter, and a peak metric stores the highest of them next to the average. The metric is stored like any other, so it stays for the retention period (C and E are wrong).
- The 12 ms and the 1,900 ms are both right and do not contradict each other. The average is taken over the 15 samples and the virtual disks; the peak is the single highest value of all of them, so the gap can be far larger than 15 times. One burst on one disk moves the peak and hardly moves the average.
- Limits of the answer: the metric is one value per cycle for the VM (taken across the virtual disks), so it does not say which disk or which of the 15 periods; the peaks of other metrics can come from different periods. A per-disk 5-minute view and the storage flow come next.

## Notes
- Public source: Broadcom KB 444403, Understanding "Peak" or "Worst" Performance Metrics in VMware VCF / Aria Operations (VCF Operations 9.x, Aria Operations 8.x): the collector reads 15 samples of 20 seconds per 5-minute cycle; peak metrics show the highest; "vCenter only retains real-time 20-second granularity data for a limited time (typically 1 hour)"; "Virtual Disk | Peak Latency within collection cycle" is listed. vSphere 9.1 Monitoring and Performance: Data Collection Intervals (Real-time 20 s, 1 Day 5 min, 1 Week 30 min).
- Why one answer: A fails on retention, B on the rollup chain, C and E on the stored peak metric; D is the documented behaviour.
- Debatable risk: low. The statement that the average runs over disks as well as samples is the knowledge file's description of the metric (same reading as the existing question on a 9,840 ms peak against a 248 ms average); the Broadcom KB does not spell it out, so the author should confirm. The time series retention of 6 months is given in the prompt, so no default is claimed.
- Rests on: the vendor sources above and the role split in the VCF Operations role file (vCenter: short, averaged history; VCF Operations: capacity and troubleshooting history).

## Metadata
```yaml
id: "0356"
title: "A 20-second peak from nine days ago"
product: [vsphere, vcf-operations]
technology: [storage, system]
task: read-metric
level: 400
answer_type: deterministic
input: [text]
object: [vm]
tool: [vcenter, vcf-operations]
knowledge:
  - vcf-operations/vcf-operations-role
  - vcf-operations/features/peak-20-second-metrics
  - vsphere/tools/vsphere-client/vcenter-statistics
  - vsphere/object-types/vm/vm-health-check
knowledge_main: vcf-operations/vcf-operations-role
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
answer: [D]
misconception: [B, E]
misconception_type: [rollup-and-interval, tool-confusion]
status: draft
```
