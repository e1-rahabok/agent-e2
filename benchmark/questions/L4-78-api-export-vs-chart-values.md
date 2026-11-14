# Report values from the vCenter API

## Prompt
- A team builds a weekly report with a script that reads the vCenter 9.1 performance API, 1 Day interval (5-minute points), for VM sql-02.
- The report prints raw values with no unit:
  - `mem.consumed.average` = 33,554,432
  - `net.usage.average` = 12,500
  - `disk.maxTotalLatency.latest` = 4, for the point stamped 10:05
- The vSphere Client chart of the same VM shows Consumed in MB.

Which statements are correct?

- A. Consumed is about 32 GB: the API reports memory in KB, while the chart converts to MB.
- B. Read in MB, as on the chart, Consumed is about 32 TB, so the script or the API is broken.
- C. Network usage is in KBps: 12,500 KBps is about 100 Mbps.
- D. `maxTotalLatency` with rollup latest is the last value in the 5-minute point, so a latency spike earlier in that interval can be missing from the 4 ms.
- E. The 4 ms is the average latency of all the VM's virtual disks over the 5 minutes.

## Likely wrong answer
B: reading the API value in the chart's unit.

## Expected key points
- Answer: A, C, D.
- A: 33,554,432 KB = 32 GB. The API returns memory in KB; the chart converts to MB, so an API value read as MB is 1,024 times too large.
- B is wrong for the same reason.
- C: vCenter network usage is in kilobytes per second (KBps): 12,500 × 1,024 × 8 bits ≈ 102 Mbps.
- D: rollup latest keeps one point in time, not the worst value of the interval; use the real-time interval or a peak metric for spikes.
- E is wrong: Highest latency is the highest value across the VM's disks, and with rollup latest it is one point in time, not an average over the 5 minutes.

## Notes
- Units and rollups: vSphere 9.1 API reference, PerformanceManager counters (mem.consumed in KB; net.usage in KBps; disk.maxTotalLatency rollup latest).

## Metadata
```yaml
id: "0237"
title: "Report values from the vCenter API"
product: [vsphere]
technology: [system, memory, network, storage]
task: read-metric
level: 400
answer_type: deterministic
input: [text]
object: [vm]
tool: [vcenter]
knowledge:
  - vsphere/tools/vsphere-client/vcenter-statistics
  - vsphere/tools/esxtop/units-vs-vsphere-client
  - vsphere/technology/storage/metrics/virtual-motherboard/disk
knowledge_main: vsphere/tools/vsphere-client/vcenter-statistics
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
answer: [A, C, D]
misconception: [B]
misconception_type: [tool-confusion, unit-and-normalization]
status: reviewed
```
