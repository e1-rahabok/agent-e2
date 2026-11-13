# Disk latency peak 40 times the average

## Prompt
- db-14 is a database VM with 20 virtual disks.
- [The attached export](0089/db-14-disk-latency-1-day.csv) is one day of VCF Operations metrics for db-14, in 5-minute samples: read latency, write latency, and Peak Latency within collection cycle.
- At 02:15 the peak is 9,840 ms. The 5-minute write latency at 02:15 is 248 ms.
- The application owner asks whether the peak is real, and what it means for the database.

Is the peak real? How can it be 40 times the 5-minute value? What do you tell the owner, and what do you check?

## Likely wrong answer
"The peak cannot be 40 times the average: a 20-second value can be at most 15 times a 5-minute value, so the metric is wrong."

## Expected key points
- The peak is real. It is the highest of the 15 twenty-second points in the 5-minute cycle, taken across every virtual disk, read and write.
- It can exceed 15 times the 5-minute value: the 5-minute latency averages all the IO of all 20 disks over 300 seconds, while the peak is one 20-second point of one disk and one direction (20 disks × 2 × 15 = 600 values).
- It is a one-off: every other peak of the day is below 30 ms, and the 5-minute values stay low.
- In at least one 20-second point, IO to at least one disk waited close to 10 seconds. A 248 ms 5-minute write latency needs more than one such point or more than one disk. The database may have stalled or timed out: check the database and Guest OS logs at 02:15.
- Check every virtual disk at 02:15, write side, and what ran then (a backup or a scheduled job).

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Revised 2026-11-12 for question set 1.0: the screenshot and the 40-column table replaced by one small export; the vCommunity KPI file removed from `knowledge`. Counts only after author approval.

## Metadata
```yaml
id: "0089"
title: "Disk latency peak 40 times the average"
product: [vcf-operations, vsphere]
technology: [storage]
task: read-metric
level: 300
answer_type: judged
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
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
misconception_type: [rollup-and-interval]
status: draft
```
