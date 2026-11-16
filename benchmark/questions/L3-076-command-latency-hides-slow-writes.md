# Command latency looks fine while writes are slow

## Prompt
- A DBA says the writes of database VM db-ora-04 are slow. The VM is the only one on LUN naa.6000d31000a4b5000000000000000117, on host esx-db-02.
- The storage team's report watches Command latency of the LUN on each host and shows it as healthy.
- You export [the host's Disk chart of the LUN](0414/vcenter-host-disk-lun-realtime.csv) from the vSphere Client, Real-time, the last 30 minutes at 20-second samples.

Which statements are correct?

- A. Command latency weights each latency by its share of the commands, so with mostly reads it stays near Read latency.
- B. Command latency is (Read latency + Write latency) / 2.
- C. Write latency runs at about five times Read latency here, which Command latency does not show.
- D. Command latency tracks whichever side is slower.
- E. Command latency counts only the reads of the LUN.
- F. With Command latency healthy, the slow writes must come from inside the database, not from the LUN.
- G. Read and write latency are read separately: often only one of them has a problem.
- H. If the workload turned write-heavy, Command latency would move toward Write latency.
- I. In the export, Command latency sits closer to Write latency than to Read latency.

## Likely wrong answer
B: Command latency is (read + write) / 2. Or F: Command latency is healthy, so the LUN is not the cause.

## Expected key points
- Answer: A, C, G, H.
- A true: Command latency is the average over all commands, so each side counts by its number of commands. In the export `Average read requests per second` is 6 to 10 times `Average write requests per second` in every row, and `Command latency` stays at 1.2 to 1.8 times `Read latency` (4-5 ms against 3 ms).
- B false: with `Write latency` at 4 to 6 times `Read latency`, the plain mean of the two is 2.5 to 3.5 times Read latency, above the export's Command latency (1.8 times at most).
- C true: reading. `Write latency` is 4 to 6 times `Read latency` in every row (13-17 ms against 3 ms), while `Command latency` stays below half of Write latency.
- D false: Command latency sits below half of Write latency, the slower side.
- E false: the writes are in it, weighted by their share of the commands; that is why it sits above Read latency.
- F false: the combined value hides the slow side; the LUN's Write latency is 4 to 6 times its Read latency.
- G true: read and write latency have different patterns, and often only one has a problem.
- H true: a weighted average moves toward the side that carries most commands.
- I false: reading. In every row Command latency is 1-2 ms above Read latency and at least 8 ms below Write latency.

## Notes
- Paired with the theory question 0044 (theory and practical; design.md, section 3.9).
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item C19 (origin: synthetic). Counts only after author approval.
- Review 2026-11-15: the condition could not be met (with 6-10 reads per write and writes 4-6 times slower, Command latency is 1.27-1.71 times Read latency); it is now 1.2-1.8 times. Options reworded away from 0044; I (a false screen reading) added. Key unchanged: A, C, G, H.
- 2026-11-15: the screenshot replaced by a generated export (project/practical-questions-as-exports-2026-11-15.md); the generator meets the condition the capture could not (Command latency recomputed per row as the request-weighted mean).

## Metadata
```yaml
id: "0414"
title: "Command latency looks fine while writes are slow"
product: [vsphere]
technology: [storage]
task: troubleshoot
level: 300
answer_type: deterministic
input: [table]
object: [esxi]
tool: [vcenter]
knowledge:
  - vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
  - vsphere/technology/storage/metrics/host/disk
knowledge_main: vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
attachments:
  - 0414/vcenter-host-disk-lun-realtime.csv
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C19"
answer: [A, C, G, H]
misconception: [B, F]
misconception_type: [average-hides-worst, unit-and-normalization]
pair: "0044"
status: draft
```
