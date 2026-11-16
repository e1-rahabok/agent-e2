# Disk latency peak far above the average

## Prompt
- mx-02 is a mail server VM with 6 virtual disks.
- [The attached export](0089/mx-02-disk-latency-1-day.csv) is one day of VCF Operations metrics for mx-02, in 5-minute samples: read latency, write latency, and Peak Latency within collection cycle.
- The mail team saw one tall spike of the peak line in the afternoon. They ask whether it is real, and what it means for the mail service.

Which statements are correct?

- A. The spike cannot be real: a 20-second value can be at most 15 times the 5-minute value it belongs to.
- B. The peak is the highest of the 15 twenty-second values in the 5-minute collection cycle.
- C. The peak is taken across all 6 virtual disks, reads and writes together, as one value.
- D. In the spike's cycle the read latency rose far above its usual level while the write latency stayed in its usual range.
- E. VCF Operations keeps all 15 twenty-second values of each cycle, so you can see when within the spike's cycle the burst came.
- F. The peak metric tells you which of the 6 virtual disks had the stall in that cycle.
- G. It is a one-off: every other peak that day stays below about 20 ms, and every other 5-minute value below about 4 ms.
- H. In at least one 20-second point, IO to at least one disk took about 4 seconds on average.
- I. An IO wait that long can stall or time out the mail service, so check the application and Guest OS logs of that cycle.
- J. Check each virtual disk's latency in that cycle, and what ran then, such as a backup or a scheduled job.
- K. The 5-minute latency of that cycle is what the mail service felt, so one cycle like this is harmless.
- L. In that cycle the 5-minute read latency is far above the write latency, so only one of the six disks can have been involved.

## Answers
B, C, D, G, H, I, J

## Explanation
- A is wrong: the gap can exceed 15 times, because the peak is one point of one disk and one direction, and the average is not. Here 4,180 ms against 71 ms is about 59 times.
- B is correct: a Peak ... within collection cycle metric is the highest of the 15 twenty-second averages in the 5-minute cycle.
- C is correct: the peak is taken across instances, all virtual disks, read and write.
- D is correct: at 14:35 the read latency is 71.0 ms against about 1 to 2 ms in the cycles around it, while the write latency is 2.6 ms, inside its usual range for the day.
- E is wrong: only the peak of the 15 points is stored; there is no pattern within the 300 seconds.
- F is wrong: the peak is one metric across all instances; it does not name the disk.
- G is correct: in the export every other peak is below 19 ms, and every other read and write value is below 3.4 ms; only the 14:35 cycle stands out (read latency 71 ms, peak 4,180 ms).
- H is correct: a 20-second point is an average, so the IO in it averaged about 4.2 seconds.
- I is correct: a 5-minute average hides 20-second peaks; a wait of several seconds is enough for an application to stall or time out.
- J is correct: the peak does not name the disk or direction; per disk, the read value is the one that moved at 14:35.
- K is wrong: the 5-minute read latency of 71 ms averages the cycle; the 20-second peak inside it was about 4.2 seconds.
- L is wrong: the 5-minute read latency is a VM-level value and the peak does not name the disk, so the export cannot tell how many of the six disks were slow; read and write latency often move apart, so a high read value says nothing about the disk count.
- Misconception: A: "A 20-second peak can only be 15 times the 5-minute average, so about 60 times means the metric is wrong."

## Notes
- Synthetic, 2026-11-05, from the knowledge files listed in `knowledge` (origin: synthetic). Revised 2026-11-12 for question set 1.0: the screenshot and the 40-column table replaced by one small export; the vCommunity KPI file removed from `knowledge`. Counts only after author approval.
- Dropped from the key: "a 5-minute latency in the tens or hundreds of ms needs more than one such point or more than one disk". How many points or disks it takes depends on how the 5-minute value weights IO across disks and points, which the knowledge base does not settle.
- Changed in the 2026-11-15 audit: level 300 to 400 (A needs the across-instance mechanism); D replaced by a reading of the export (the old D, a 5-minute point dilutes a burst, is held by 0047 and 0432); L added (a read-heavy cycle read as one disk).
- Review 2026-11-15: G no longer claims every 5-minute value is low (14:35 reads 71 ms); D states the averaging positively instead of negating A; E, I, J and K no longer name the time or the value, so the options do not read the CSV for the candidate. Key unchanged.
- 2026-11-14: the CSV was a near-copy of the knowledge example (a VM with 20 virtual disks, about 10,000 ms against about 250 ms); regenerated with a seeded script for a new scenario (a mail server VM with 6 virtual disks, a read burst at 14:35: 4,180 ms peak against 71 ms read latency). The stem no longer states the values: the export supplies them. Practical half of 0356 (project/question-pairing-2026-11-14.md, A12). Key unchanged: B, C, D, G, H, I, J.

## Metadata
```yaml
id: "0089"
title: "Disk latency peak far above the average"
product: [vcf-operations, vsphere]
technology: [storage]
task: read-metric
level: 400
answer_type: deterministic
misconception: [A]
input: [table]
object: [vm]
tool: [vcf-operations]
knowledge:
  - vcf-operations/features/peak-20-second-metrics
  - vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
  - vsphere/technology/storage/concepts/guest-os-vs-vm-storage
knowledge_main: vcf-operations/features/peak-20-second-metrics
attachments:
  - 0089/mx-02-disk-latency-1-day.csv
origin: synthetic
source_path: "Synthetic, 2026-11-05"
misconception_type: [rollup-and-interval]
pair: "0356"
status: draft
```
