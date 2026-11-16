# Command latency looks fine while writes are slow

## Prompt
- A DBA says the writes of database VM db-ora-04 are slow. The VM is the only one on LUN naa.6000d31000a4b5000000000000000117, on host esx-db-02.
- The storage team's report watches Command latency of the LUN on each host and shows it as healthy.
- You export [the host's Disk chart of the LUN](0414/vcenter-host-disk-lun-realtime.csv) from the vSphere Client, Real-time, the last 30 minutes at 20-second samples.

Which statements are correct?

- A. Weighted by command count, Command latency stays near Read latency when most commands are reads.
- B. Command latency is the plain mean: (Read latency + Write latency) / 2.
- C. Write latency runs at about five times Read latency here, which Command latency does not show.
- D. Command latency tracks whichever side is slower, reads or writes.
- E. Command latency counts only the reads of the LUN and leaves the writes out.
- F. With Command latency healthy, the slow writes must come from inside the database, not from the LUN.
- G. If the workload turned write-heavy, Command latency would move toward Write latency.
- H. In the export, most of Command latency is time in the host's kernel rather than at the device.

## Answers
A, C, G

## Explanation
- A is correct: Command latency is the average over all commands, so each side counts by its number of commands. In the export `Average read requests per second` is 6 to 10 times `Average write requests per second` in every row, and `Command latency` stays at 1.2 to 1.8 times `Read latency` (4-5 ms against 3 ms).
- B is wrong: the misconception. With `Write latency` at 4 to 6 times `Read latency`, the plain mean of the two is 2.5 to 3.5 times Read latency, above the export's Command latency (1.8 times at most).
- C is correct: reading. `Write latency` is 4 to 6 times `Read latency` in every row (13-17 ms against 3 ms), while `Command latency` stays below half of Write latency.
- D is wrong: Command latency sits below half of Write latency, the slower side.
- E is wrong: the writes are in it, weighted by their share of the commands; that is why it sits above Read latency.
- F is wrong: the misconception. The combined value hides the slow side; the LUN's Write latency is 4 to 6 times its Read latency.
- G is correct: a weighted average moves toward the side that carries most commands.
- H is wrong: reading. Command latency is Physical device command latency plus Kernel command latency, and Kernel command latency is 0 in at least 90% of the rows: the time is at the device, with the slow side being the writes.
- Misconception: B: Command latency is (read + write) / 2. Or F: Command latency is healthy, so the LUN is not the cause.

## Notes
- Paired with the theory question 0044 (theory and practical; design.md, section 3.9).
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item C19 (origin: synthetic). Counts only after author approval.
- Review 2026-11-15: the condition could not be met (with 6-10 reads per write and writes 4-6 times slower, Command latency is 1.27-1.71 times Read latency); it is now 1.2-1.8 times. Options reworded away from 0044; I (a false screen reading) added. Key unchanged: A, C, G, H.
- 2026-11-15: the screenshot replaced by a generated export (project/practical-questions-as-exports-2026-11-15.md); the generator meets the condition the capture could not (Command latency recomputed per row as the request-weighted mean).
- Audit 2026-11-15 (redundancy): old G (read and write latency read separately; kept by the pair 0081/0405) dropped; old H and I are now G and H (letter map: A-F unchanged, G dropped, H to G, I to H; the generator case still labels the H condition "I"). A, B, D and E reworded for length (truth unchanged). Key changed from A, C, G, H to A, C, G (same options).
- Re-review 2026-11-16: H (Command latency closer to Write than to Read) was the reverse of A on this data; it now reads the kernel and device split of Command latency (still false). Case labels follow. Key unchanged: A, C, G.

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
misconception: [B, F]
misconception_type: [average-hides-worst, unit-and-normalization]
pair: "0044"
status: draft
```
