# vCenter only: which contention counters survive a day

## Prompt
- A site has vCenter 9.1 and no VCF Operations. The statistics level is at its default for every interval.
- On Monday at 10:00 an owner reports that the 8-vCPU VM erp-batch-04 was slow on Sunday between 03:20 and 03:40.
- You run the VM health check for that window from the vSphere Client performance charts. The check reads, in order, CPU Ready and Co-stop, memory Latency, disk latency, and dropped packets.

Which statements are correct?

- A. Co-stop, memory Latency and dropped packets are all in the 1 Day chart as 5-minute averages, so the whole check can run.
- B. The Real-time chart still holds the window at 20-second resolution, so the peaks are readable there for any day of the past week.
- C. CPU Ready and Highest Latency are in the 1 Day chart, but Highest Latency is the last sample of each 5 minutes, and the other three counters are not stored.
- D. The 1 Day chart shows the 5-minute maximum of each counter, so the worst 20-second value of the window can be read from it.
- E. No contention counter is kept at the default level, only consumption counters, so the check ends at the consumption step.

## Likely wrong answer
A or D: the health-check counters are assumed to exist in the chart history, or the chart point is assumed to be a peak.

## Expected key points
- Answer: C.
- Real-time data (20-second samples) is kept for one hour only, so B is wrong. History is the rolled-up 1 Day, 1 Week, 1 Month and 1 Year intervals.
- At the default level 1 a VM keeps CPU Ready (a summation of the 15 samples, so a 20-second burst is diluted 15 times) and Disk Highest Latency, plus balloon and the swap rates. It keeps no Co-stop, no memory Latency, no per-disk latency and no dropped packets: they need a higher statistics level, set before the event, which also raises the vCenter database and vpxd load.
- Highest Latency has the Latest rollup: the 5-minute point is the value of the last 20-second sample, not the worst, so it cannot be read as a peak (D is wrong; Minimum and Maximum rollups exist only at level 4).
- A is wrong for the reason above. E is wrong: Ready and Highest Latency are contention counters kept at level 1.
- This is why the health check is run in VCF Operations: it collects every 5 minutes from the 15 samples and stores the peak of them, a metric vCenter does not keep in its history.

## Notes
- Public source: VMware vSphere 9.1 Monitoring and Performance, Data Counters, Data Collection Intervals, Statistics Levels (Real-time 20 seconds; 1 Day 5 minutes; levels 1 to 4); counter list and levels from the vCenter 9.1.0 API export (build 25370922) in the knowledge catalog. Broadcom KB 444403: "vCenter only retains real-time 20-second granularity data for a limited time (typically 1 hour)."
- Why one answer: the retention (1 hour), the Latest rollup of maxTotalLatency and the level of the other counters are documented properties. Only C matches all of them.
- Debatable risk: moderate on one fact. I did not re-verify the level of cpu.costop, mem.latency and net.droppedRx in the vSphere 9.1 chart tables myself: the knowledge file derives "not kept at level 1" from the 9.1 API export (level 1 list per object has none of them), and the vSphere 5-era documentation lists co-stop and the drop counters at level 2. The author should confirm against the 9.1 Data Counters tables before approving.
- Rests on: vendor documentation (retention, rollups, levels), and the health-check counter list of the VM check file.
- Stem made plural (2026-11-14): the singular form told the candidate that one option is correct (Q199: the count is never disclosed). Was: "Which statement is correct?"

## Metadata
```yaml
id: "0351"
title: "vCenter only: which contention counters survive a day"
product: [vsphere]
technology: [cpu, memory, storage, network, system]
task: troubleshoot
level: 400
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
answer: [C]
misconception: [A, D]
misconception_type: [rollup-and-interval, tool-confusion]
status: draft
```
