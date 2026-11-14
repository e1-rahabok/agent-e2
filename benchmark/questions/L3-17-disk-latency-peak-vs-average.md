# Disk latency peak 40 times the average

## Prompt
- db-14 is a database VM with 20 virtual disks.
- [The attached export](0089/db-14-disk-latency-1-day.csv) is one day of VCF Operations metrics for db-14, in 5-minute samples: read latency, write latency, and Peak Latency within collection cycle.
- At 02:15 the peak is 9,840 ms. The 5-minute write latency at 02:15 is 248 ms.
- The application owner asks whether the peak is real, and what it means for the database.

Which statements are correct?

- A. The peak cannot be real: a 20-second value can be at most 15 times the 5-minute value it belongs to.
- B. The peak is the highest of the 15 twenty-second values in the 5-minute collection cycle.
- C. The peak is taken across all 20 virtual disks, reads and writes together.
- D. The 5-minute value averages IO across the disks and the cycle, so one 20-second point of one disk can exceed it far more than 15 times.
- E. VCF Operations keeps all 15 twenty-second values of each cycle, so you can see when within 02:15 the burst came.
- F. The peak metric tells you which of the 20 virtual disks had the stall.
- G. It is a one-off: every other peak that day stays below about 22 ms, and the 5-minute values stay low.
- H. In at least one 20-second point, IO to at least one disk took close to 10 seconds on average.
- I. An IO wait that long can stall or time out the database, so check the database and Guest OS logs at 02:15.
- J. Check each virtual disk's write latency at 02:15, and what ran then, such as a backup or a scheduled job.
- K. The 5-minute write latency of 248 ms is what the database felt, so one cycle like this is harmless.

## Likely wrong answer
- A: "A 20-second peak can only be 15 times the 5-minute average, so 40 times means the metric is wrong."

## Expected key points
- Answer: B, C, D, G, H, I, J.
- A is false: the gap can exceed 15 times, because the peak is one point of one disk and one direction, and the average is not.
- B is true: a Peak ... within collection cycle metric is the highest of the 15 twenty-second averages in the 5-minute cycle.
- C is true: the peak is taken across instances, all virtual disks, read and write.
- D is true: 20 disks × 2 directions × 15 points = 600 values; the peak is the highest of them, while the 5-minute value averages all the IO.
- E is false: only the peak of the 15 points is stored; there is no pattern within the 300 seconds.
- F is false: the peak is one metric across all instances; it does not name the disk.
- G is true: in the export every other peak is below 22 ms, and read and write latency stay below about 4 ms outside 02:15.
- H is true: a 20-second point is an average, so the IO in it averaged about 9.8 seconds.
- I is true: a 5-minute average hides 20-second peaks; a wait of several seconds is enough for a database to stall or time out.
- J is true: the peak does not name the disk or direction, and the write value is the one that moved at 02:15.
- K is false: a value below a threshold on a 5-minute average says nothing about the 20-second peaks inside it.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Revised 2026-11-12 for question set 1.0: the screenshot and the 40-column table replaced by one small export; the vCommunity KPI file removed from `knowledge`. Counts only after author approval.
- Dropped from the key: "a 248 ms 5-minute write latency needs more than one such point or more than one disk". How many points or disks it takes depends on how the 5-minute value weights IO across disks and points, which the knowledge base does not settle.
- Converted from judged to multiple choice (Q199 F, 2026-11-14).

## Metadata
```yaml
id: "0089"
title: "Disk latency peak 40 times the average"
product: [vcf-operations, vsphere]
technology: [storage]
task: read-metric
level: 300
answer_type: deterministic
answer: [B, C, D, G, H, I, J]
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
  - 0089/db-14-disk-latency-1-day.csv
origin: synthetic
source_path: "Drafted by Claude 2026-11-05"
misconception_type: [rollup-and-interval]
status: draft
```
