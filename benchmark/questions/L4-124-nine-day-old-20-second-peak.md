# A 20-second peak from nine days ago

## Prompt
- The backup window of vm-sql-03 ran nine days ago between 02:00 and 02:30. The DBA asks how high the disk latency of the VM got in any 20-second period of that window. The VM has 12 virtual disks.
- vCenter 9.1 keeps its default collection intervals and statistics level. VCF Operations 9.1 has collected from that vCenter every 5 minutes since before the window, with a time series retention of 6 months and the default policy.
- In the 5-minute data of VCF Operations, the disk latency of the VM at 02:15 is 9 ms. The metric "Peak Latency within collection cycle" for the same 5-minute cycle is 2,640 ms.
- You have both tools open.

Which statements are correct?

- A. The vCenter Real-time chart, set to that night, shows the window in 20-second points.
- B. Each 5-minute cycle, VCF Operations reads the fifteen 20-second values of the cycle from vCenter.
- C. The 30-minute point of the vCenter 1 Week chart holds the highest of the 5-minute values it covers.
- D. The peak metric holds the highest 20-second value of the cycle, taken across all 12 virtual disks.
- E. The peak metric is kept for the same retention period as the other VCF Operations metrics of the VM.
- F. A peak almost 300 times the 5-minute value shows that the peak metric is faulty.
- G. The peak metric names the virtual disk and the 20-second period that held the highest value.
- H. With the peak metric in place, the 5-minute latency average has no further use.
- I. The DBA must rerun the backup with esxtop running, because no tool kept 20-second data from that night.

## Likely wrong answer
F: a 20-second peak can be at most 15 times its 5-minute value, so the peak metric must be wrong. Or I: the 20-second data is assumed to be lost everywhere after an hour.

## Expected key points
- Answer: B, D, E.
- A is false: vCenter keeps the 20-second samples for one hour only.
- B is true: VCF Operations collects every 5 minutes but takes the 15 samples of 20 seconds per cycle; a peak metric stores the highest of them next to the average.
- C is false: vCenter's history is a chain of averages: 15 samples into a 5-minute point, 6 of those into the 30-minute point of the 1 Week chart. A 20-second burst is diluted 90 times there.
- D is true: the peak is taken across instances: all virtual disks, read and write, and all 15 periods of the cycle.
- E is true: the peak is a metric of its own, stored like any other, so it stays for the retention period.
- F is false: the misconception. The average runs over the 15 periods and over the disks; the peak is the single highest of all those values, so the gap can be far larger than 15 times.
- G is false: one value per cycle for the VM; it does not say which disk or which of the 15 periods.
- H is false: the over-correction. The peak is a new metric, not a replacement: the 5-minute average stays for trends and capacity, and a large gap between peak and average marks a one-off burst rather than a sustained level.
- I is false: the wrong action. The peak metric already answers the DBA's question for that night.

## Notes
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): 9 single-fact options instead of 5 compound ones; the misconception (F), its over-correction (H) and the wrong action (I) added. Numbers changed (12 disks, 9 ms, 2,640 ms) so that the practical half 0089 is not given away. Key changed from D to B, D, E.
- Paired with the table question 0089 (the same peak metric in an export).
- Public source: Broadcom KB 444403, Understanding "Peak" or "Worst" Performance Metrics in VMware VCF / Aria Operations (VCF Operations 9.x, Aria Operations 8.x): the collector reads 15 samples of 20 seconds per 5-minute cycle; peak metrics show the highest; "vCenter only retains real-time 20-second granularity data for a limited time (typically 1 hour)"; "Virtual Disk | Peak Latency within collection cycle" is listed. vSphere 9.1 Monitoring and Performance: Data Collection Intervals (Real-time 20 s, 1 Day 5 min, 1 Week 30 min).
- Debatable risk: low. The statement that the average runs over disks as well as samples is the knowledge file's description of the metric (the same reading as the table question 0089); the Broadcom KB does not spell it out, so the author should confirm. The time series retention of 6 months is given in the prompt, so no default is claimed.
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
answer: [B, D, E]
misconception: [F, I]
misconception_type: [rollup-and-interval, tool-confusion, average-hides-worst]
pair: "0089"
status: draft
```
