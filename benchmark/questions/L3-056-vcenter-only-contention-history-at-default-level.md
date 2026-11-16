# vCenter only: which contention counters survive a day

## Prompt
- A site has vCenter 9.1 and no VCF Operations. The statistics level is at its default for every interval.
- On Sunday at 21:00 an owner reports that the 8-vCPU VM erp-batch-04 was slow earlier that day, between 03:20 and 03:40.
- You run the VM health check for that window from the vSphere Client performance charts. The check reads, in order, CPU Ready and Co-stop, memory Latency, disk latency, and dropped packets.

Which statements are correct?

- A. Co-stop, memory Latency and dropped packets are in the 1 Day chart as 5-minute averages, so the whole check can run.
- B. The Real-time chart still holds the window at 20-second resolution, so its peaks can be read there.
- C. CPU Ready of erp-batch-04 for Sunday 03:20 to 03:40 is in the 1 Day chart as 5-minute points.
- D. Maximum rollups are stored at every statistics level, so each 1 Day point can show a 5-minute maximum.
- E. No contention counter is kept at the default level, only consumption counters, so the check ends there.
- F. Highest Latency in the 1 Day chart is the last sample of each 5 minutes, not the worst sample.
- G. Balloon and swap-in rates are kept at level 1, so memory Latency can be rebuilt from them.
- H. The per-disk read and write latency of erp-batch-04 is in the 1 Day chart for the window.

## Answers
C, F

## Explanation
- A is wrong: at the default level 1 a VM keeps no Co-stop, no memory Latency and no dropped packets; they need a higher statistics level, set before the event.
- B is wrong: Real-time data (20-second samples) is kept for one hour only; at 21:00 the 03:20 window is long gone from it.
- C is correct: CPU Ready is one of the level 1 counters of a VM, and the 1 Day chart keeps 5-minute points for a day; the window ended about 17 hours before the check (and more than the 30-minute 1 Day delay), so the chart holds it.
- D is wrong: Minimum and Maximum rollups are stored only at statistics level 4; at level 1 the 1 Day point of Ready is a summation of its 15 samples and the latency point uses Latest.
- E is wrong: CPU Ready and Disk Highest Latency are contention counters kept at level 1.
- F is correct: Highest Latency (maxTotalLatency) has the Latest rollup: the 5-minute point is the last 20-second sample, not the worst, so it cannot be read as a peak.
- G is wrong: balloon and swap rates are reclamation counters, not the wait; memory Latency is a counter of its own and has no history at level 1.
- H is wrong: per-device storage latency has history only from level 3; at level 1 the VM keeps only Highest Latency across its disks.
- Misconception: A or D: the health-check counters are assumed to exist in the chart history, or a maximum is assumed to be kept by default.

## Notes
- Public source: VMware vSphere 9.1 Monitoring and Performance, Data Counters, Data Collection Intervals, Statistics Levels (Real-time 20 seconds; 1 Day 5 minutes; levels 1 to 4); counter list and levels from the vCenter 9.1.0 API export (build 25370922) in the knowledge catalog. Broadcom KB 444403: "vCenter only retains real-time 20-second granularity data for a limited time (typically 1 hour)."
- Why one answer: the retention (1 hour), the Latest rollup of maxTotalLatency and the level of the other counters are documented properties. Only C matches all of them.
- Debatable risk: moderate on one fact. Not re-verified here: the level of cpu.costop, mem.latency and net.droppedRx in the vSphere 9.1 chart tables; the knowledge file derives "not kept at level 1" from the 9.1 API export (level 1 list per object has none of them), and the vSphere 5-era documentation lists co-stop and the drop counters at level 2. The author should confirm against the 9.1 Data Counters tables before approving.
- Rests on: vendor documentation (retention, rollups, levels), and the health-check counter list of the VM check file.
- Background for a reviewer: this is why the health check is run in VCF Operations, which stores the 20-second peak of each 5-minute cycle; vCenter does not keep it in its history.
- Changed in the 2026-11-15 audit: old C (Ready and Highest Latency kept, Highest Latency is the last sample, the other three not stored: three facts in the only true option) split into C (Ready kept) and F (Latest rollup); its third part was dropped because A already tests it. D now states that maximum rollups exist at every level (false; the old D read a chart point as a peak, which 0047 and 0432 test). G (balloon and swap rates read as memory Latency) and H (per-disk latency) added. Key changed from C to C, F. Level 400 to 300: each option is one stored counter or one rollup type.
- Changed 2026-11-16: the report moved from Monday 10:00 to Sunday 21:00, so the window (03:20 to 03:40) is within the 1 Day archive of one day; at Monday 10:00 it was about 31 hours old and C was false.

## Metadata
```yaml
id: "0351"
title: "vCenter only: which contention counters survive a day"
product: [vsphere]
technology: [cpu, memory, storage, network, system]
task: troubleshoot
level: 300
answer_type: deterministic
input: [text]
object: [vm]
tool: [vcenter]
knowledge:
  - vsphere/object-types/vm/vm-health-check
  - vsphere/tools/vsphere-client/vcenter-statistics
  - vcf-operations/vcf-operations-role
knowledge_main: vsphere/tools/vsphere-client/vcenter-statistics
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
misconception: [A, D]
misconception_type: [rollup-and-interval, tool-confusion]
status: draft
```
