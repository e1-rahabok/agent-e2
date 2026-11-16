# One slow disk behind a low VM disk latency

## Prompt
- The application team says the nightly report on VM rpt-db-12, which starts at 02:00 and reads from one of the VM's eight virtual disks, ran much slower yesterday.
- The VMware team looked at the VM's disk latency in VCF Operations, found it low all day, and wants to close the ticket.
- From VCF Operations, for yesterday 01:00 to 04:00: [the VM-level read latency](0423/vcf-operations-vm-disk-read-latency.csv) and [the VM's Peak Latency within collection cycle](0423/vcf-operations-vm-peak-latency.csv), each a chart export at 5-minute points, and [a list view of the VM for 02:00 to 03:00](0423/vcf-operations-vm-virtual-disks-0200-0300.csv) with the read latency (average, Min, Max) and read IOPS of the aggregate and of each virtual disk.

Which statements are correct?

- A. One disk read at 15 ms or more for an hour while VM-level latency stayed low.
- B. The VM-level latency stayed low, so every one of its virtual disks was served well.
- C. Peak Latency within collection cycle is 15 ms or more at every point from 02:05 to 03:00.
- D. No VM-level metric in VCF Operations could have shown the latency of this one disk.
- E. Close the ticket: the VM-level latency stayed within its target for the whole day.
- F. A disk that serves only a few IOs per second can be left out of the latency check.
- G. Next, check that disk: read and write latency, errors, outstanding IO, datastore.
- H. The slow disk carried most of the VM's read IOPS during the hour of the report.

## Likely wrong answer
B or E: the VM's disk latency is low all day, so storage is fine and the ticket can be closed. Or D, the overshoot: no VM-level metric could show it.

## Expected key points
- Answer: A, C, G.
- A is correct: reading. In the list view, `Virtual Disk:scsi1:2|Read Latency (ms) (Min)` is 15 ms or more for 02:00 to 03:00, while `Virtual Disk:Aggregate of all instances|Read Latency (ms) (Max)` is 3 ms or less; the VM-level read latency export stays at 3 ms or less at every point from 01:00 to 04:00.
- B is wrong: the misconception. A VM aggregate hides the one slow disk; read each virtual disk.
- C is correct: reading. The Peak Latency export is 15 ms or more at every point from 02:05 to 03:00 and below 10 ms at every other point: the peak takes the highest 20-second value across all virtual disks, read and write, so the slow disk sets it.
- D is wrong: the over-correction. Peak Latency within collection cycle showed it.
- E is wrong: the wrong action. The report reads from the slow disk.
- F is wrong: queues add latency at any load; the report waited on every one of that disk's IOs.
- G is correct: the flow goes per virtual disk, read and write, then errors, then IOPS and outstanding IO, then the backing device and the configuration.
- H is wrong: reading. `Virtual Disk:scsi1:2|Read IOPS` is under 10% of `Virtual Disk:Aggregate of all instances|Read IOPS` for 02:00 to 03:00, and under 10% of the sum of the eight disks' Read IOPS.

## Notes
- Practical half of pair D4 with 0422 (theory; design.md, section 3.9).
- No option computes the aggregate: the knowledge base does not say whether it weights the disks by their IO. The condition fixes the values the key reads.
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item D4 (origin: synthetic). Counts only after author approval.
- Review 2026-11-15: F one fact; 8 or more disks, so that the aggregate can stay at 3 ms or less whatever its weighting (one disk at 15 ms among eight averages to 2.75 ms even unweighted). Key unchanged: A, C, G.
- 2026-11-15: screenshots replaced by generated exports (project/practical-questions-as-exports-2026-11-15.md), cut to 01:00-04:00. The slow disk stays at 15-17 ms and the other seven at 1 ms or less, so the aggregate stays at 3 ms or less whether VCF Operations weights it by IO or not.
- Audit 2026-11-15 (redundancy): C no longer states that the peak is taken across all disks (kept by the pair 0089/0356); it is a reading of the Peak Latency export. Options A, B, D-H reworded for length only (truth unchanged). Key unchanged: A, C, G.
- Re-review 2026-11-16: C said "in the report's hour", which a reader could take to include the 02:00 point (3.75 ms, the cycle before the report); it now names the points 02:05 to 03:00. Key unchanged: A, C, G.

## Metadata
```yaml
id: "0423"
title: "One slow disk behind a low VM disk latency"
product: [vsphere, vcf-operations]
technology: [storage]
task: troubleshoot
level: 400
answer_type: deterministic
input: [table]
object: [vm]
tool: [vcf-operations]
knowledge:
  - vsphere/technology/storage/troubleshooting/vm-storage-performance-checks
  - vcf-operations/features/peak-20-second-metrics
  - vsphere/technology/storage/metrics/virtual-motherboard/virtual-disk
knowledge_main: vsphere/technology/storage/troubleshooting/vm-storage-performance-checks
attachments:
  - 0423/vcf-operations-vm-disk-read-latency.csv
  - 0423/vcf-operations-vm-peak-latency.csv
  - 0423/vcf-operations-vm-virtual-disks-0200-0300.csv
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D4"
answer: [A, C, G]
misconception: [B, E]
misconception_type: [average-hides-worst]
pair: "0422"
status: draft
```
