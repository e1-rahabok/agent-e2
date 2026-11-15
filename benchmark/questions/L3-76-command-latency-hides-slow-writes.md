# Command latency looks fine while writes are slow

## Prompt
- A DBA says the database's writes are slow. The storage team's report watches Command latency of the LUN on each host and shows it as healthy.
- See [the vSphere Client disk chart of the LUN](0414/vcenter-host-disk-latency-real-time.png).

Which statements are correct?

- A. Command latency weights each latency by its share of the commands, so with mostly reads it stays near Read latency.
- B. Command latency is (Read latency + Write latency) / 2.
- C. Write latency runs at about five times Read latency here, which Command latency does not show.
- D. Command latency tracks whichever side is slower.
- E. Command latency counts only the reads of the LUN.
- F. With Command latency healthy, the slow writes must come from inside the database, not from the LUN.
- G. Read and write latency are read separately: often only one of them has a problem.
- H. If the workload turned write-heavy, Command latency would move toward Write latency.
- I. On the chart, Command latency sits closer to Write latency than to Read latency.

## Input to supply
- Product and version: vSphere 9.1 (vSphere Client 9.1).
- Object: one ESXi host and one LUN (device naa.*) that a test VM uses alone.
- How to produce it: in the VM, a mixed random workload with about 8 reads for each write (for example fio `--rw=randrw --rwmixread=89 --bs=8k --iodepth=16`) on a LUN whose writes are slower than its reads (parity RAID, or an array without write cache). Any source works if the condition holds.
- Screen, vSphere Client > the host > Monitor > Performance > Advanced > Disk, Chart Options: Real-time, the last hour, object the one device only, counters Read latency, Write latency, Command latency, Average read requests per second and Average write requests per second, with the legend table (Latest, Maximum, Average). Save as `0414/vcenter-host-disk-latency-real-time.png`.
- Condition the key depends on, over the hour (legend averages): reads per second 6 to 10 times writes per second; Write latency 4 to 6 times Read latency; Command latency 1.2 to 1.8 times Read latency and below half of Write latency.
- Masking: mask every VM, host, datastore and cluster name, and the device identifier.

## Likely wrong answer
B: Command latency is (read + write) / 2. Or F: Command latency is healthy, so the LUN is not the cause.

## Expected key points
- Answer: A, C, G, H.
- A true: Command latency is the average over all commands, so each side counts by its number of commands; with 6 to 10 reads per write it stays at 1.2 to 1.8 times Read latency.
- B false: with writes at 4 to 6 times Read latency, the plain mean of the two is 2.5 to 3.5 times Read latency, above the chart's Command latency (1.8 times at most).
- C true: the chart shows Write latency at 4 to 6 times Read latency, while Command latency stays below half of Write latency.
- D false: Command latency sits below half of Write latency, the slower side.
- E false: the writes are in it, weighted by their share of the commands; that is why it sits above Read latency.
- F false: the combined value hides the slow side; Write latency of the LUN is 4 to 6 times its Read latency.
- G true: read and write latency have different patterns, and often only one has a problem.
- H true: a weighted average moves toward the side that carries most commands.
- I false: the screen reading. Command latency is at most 0.8 times Read latency above Read latency, and at least 2.2 times Read latency below Write latency.

## Notes
- Paired with the theory question 0044 (theory and practical; design.md, section 3.9).
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item C19 (origin: synthetic). Counts only after author approval.
- Review 2026-11-15: the condition could not be met (with 6-10 reads per write and writes 4-6 times slower, Command latency is 1.27-1.71 times Read latency); it is now 1.2-1.8 times. Options reworded away from 0044; I (a false screen reading) added. Key unchanged: A, C, G, H.

## Metadata
```yaml
id: "0414"
title: "Command latency looks fine while writes are slow"
product: [vsphere]
technology: [storage]
task: troubleshoot
level: 300
answer_type: deterministic
input: [screenshot]
object: [esxi]
tool: [vcenter]
knowledge:
  - vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
  - vsphere/technology/storage/metrics/host/disk
knowledge_main: vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
attachments:
  - 0414/vcenter-host-disk-latency-real-time.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C19"
answer: [A, C, G, H]
misconception: [B, F]
misconception_type: [average-hides-worst, unit-and-normalization]
pair: "0044"
status: awaiting-input
```
