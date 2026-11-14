# Command latency looks fine while writes are slow

## Prompt
- A DBA says the database's writes are slow. The storage team's report watches Command latency of the LUN on each host and shows it as healthy.
- See [the vSphere Client disk chart of the LUN](0414/vcenter-host-disk-latency-real-time.png).

Which statements are correct?

- A. Command latency is the average over all commands, so with many more reads than writes it follows read latency.
- B. Command latency is the mean of read latency and write latency, each counted once.
- C. Write latency runs at about five times read latency here, which Command latency does not show.
- D. Command latency is the higher of read latency and write latency.
- E. Command latency leaves the writes out.
- F. Command latency is healthy, so the DBA's ticket can be closed.
- G. Read and write latency are read separately: often only one of them has a problem.
- H. If the workload turned write-heavy, Command latency would move toward write latency.

## Input to supply
- Product and version: vSphere 9.1 (vSphere Client 9.1).
- Object: one ESXi host and one LUN (device naa.*) that a test VM uses alone.
- How to produce it: in the VM, a mixed random workload with about 8 reads for each write (for example fio `--rw=randrw --rwmixread=89 --bs=8k --iodepth=16`) on a LUN whose writes are slower than its reads (parity RAID, or an array without write cache). Any source works if the condition holds.
- Screen, vSphere Client > the host > Monitor > Performance > Advanced > Disk, Chart Options: Real-time, the last hour, object the one device only, counters Read latency, Write latency, Command latency, Average read requests per second and Average write requests per second, with the legend table (Latest, Maximum, Average). Save as `0414/vcenter-host-disk-latency-real-time.png`.
- Condition the key depends on, over the hour: reads per second 6 to 10 times writes per second; write latency 4 to 6 times read latency; Command latency within 25% of read latency.
- Masking: mask every VM, host, datastore and cluster name, and the device identifier.

## Likely wrong answer
B: Command latency is (read + write) / 2. Or F: Command latency is fine, so storage is fine.

## Expected key points
- Answer: A, C, G, H.
- A true: Command latency is weighted by the number of commands: with about 8 reads per write it stays close to read latency.
- B false: with writes at about five times read latency, the plain mean of the two would be about three times read latency, far above the chart's Command latency.
- C true: the chart shows write latency at 4 to 6 times read latency, while Command latency stays within 25% of read latency.
- D false: Command latency sits near read latency, far below write latency.
- E false: the writes are in it, weighted by their share of the commands.
- F false: the combined value hides the slow side; the DBA's writes are slow.
- G true: read and write latency have different patterns, and often only one has a problem.
- H true: a weighted average moves toward the side that carries most commands.

## Notes
- Paired with the theory question 0044 (theory and practical; design.md, section 3.9).
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item C19 (origin: synthetic). Counts only after author approval.

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
