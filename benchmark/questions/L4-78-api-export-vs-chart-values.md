# Report values from the vCenter API

## Prompt
- A team builds a weekly report with a script that reads the vCenter 9.1 performance API, 1 Day interval (5-minute points), for VM sql-02.
- The report prints raw values with no unit:
  - `mem.consumed.average` = 33,554,432
  - `net.usage.average` = 12,500
  - `disk.maxTotalLatency.latest` = 4, for the point stamped 10:05
- The vSphere Client chart of the same VM shows Consumed in MB.

Which statements are correct?

- A. sql-02's Consumed is about 32 GB.
- B. The API returns Consumed in MB, the unit the chart shows.
- C. Rewrite the script: a Consumed of 33,554,432 shows that it reads the wrong counter.
- D. A network usage of 12,500 is about 100 Mbps.
- E. The API reports network usage in kilobits per second.
- F. The vSphere Client Advanced chart of sql-02 shows network usage in a different unit from the API.
- G. The 4 ms is the value at the end of the 10:05 interval, so an earlier latency spike in that interval can be missing from it.
- H. The 4 ms is the average latency of all the VM's virtual disks over the 5 minutes.

## Likely wrong answer
B: reading the API value in the chart's unit, so Consumed reads about 32 TB and the script looks broken.

## Expected key points
- Answer: A, D, G.
- A is true: 33,554,432 KB = 32 GB.
- B is false: the API returns memory in KB; the chart converts to MB, so an API value read as MB is 1,024 times too large.
- C is false: the value is right in KB; the script reads the right counter in the API's unit.
- D is true: vCenter network usage is in kilobytes per second (KBps): 12,500 × 1,024 × 8 bits ≈ 102 Mbps.
- E is false: net.usage is kilobytes per second; read as kilobits it would be 8 times too low (12.5 Mbps).
- F is false: the Advanced chart and its CSV export plot the network counters as stored, in KBps, the same unit as the API; only memory and space are converted.
- G is true: rollup latest keeps one point in time, not the worst value of the interval; use the real-time interval or a peak metric for spikes.
- H is false: Highest latency is the highest value across the VM's disks, and with rollup latest it is one point in time, not an average over the 5 minutes.

## Notes
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): one fact per option (the old A and B split into a reading and a unit); wrong action C, unit error E and over-correction F added. Key changed from A, C, D to A, D, G (same facts, relettered). The author reviewed the earlier options; the rewrite follows the approved plan.
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
answer: [A, D, G]
misconception: [B]
misconception_type: [tool-confusion, unit-and-normalization]
status: draft   # options rewritten 2026-11-14: back to draft for the author's review
```
