# One slow disk behind a low VM disk latency

## Prompt
- The application team says the nightly report on VM rpt-db-12, which starts at 02:00 and reads from one of the VM's eight virtual disks, ran much slower yesterday.
- The VMware team looked at the VM's disk latency in VCF Operations, found it low all day, and wants to close the ticket.
- From VCF Operations, for yesterday 01:00 to 04:00: [the VM-level read latency](0423/vcf-operations-vm-disk-read-latency.csv) and [the VM's Peak Latency within collection cycle](0423/vcf-operations-vm-peak-latency.csv), each a chart export at 5-minute points, and [a list view of the VM for 02:00 to 03:00](0423/vcf-operations-vm-virtual-disks-0200-0300.csv) with the read latency (average, Min, Max) and read IOPS of the aggregate and of each virtual disk.

Which statements are correct?

- A. One virtual disk ran at 15 ms or more for about an hour while the VM-level latency stayed low.
- B. The VM-level latency stayed low, so every virtual disk was served well.
- C. Peak Latency within collection cycle rose in the same hour, because it takes the worst 20 seconds across all the virtual disks.
- D. No VM-level metric could have shown this disk's latency.
- E. Close the ticket: the VM-level latency stayed within target all day.
- F. A disk with few IOs can be left out of the latency check.
- G. The next checks follow the slow disk: its read and write latency, errors, outstanding IO and the datastore behind it.
- H. The slow disk carried most of the VM's IO in that hour.

## Likely wrong answer
B or E: the VM's disk latency is low all day, so storage is fine and the ticket can be closed. Or D, the overshoot: no VM-level metric could show it.

## Expected key points
- Answer: A, C, G.
- A true: reading. In the list view, `Virtual Disk:scsi1:2|Read Latency (ms) (Min)` is 15 ms or more for 02:00 to 03:00, while `Virtual Disk:Aggregate of all instances|Read Latency (ms) (Max)` is 3 ms or less; the VM-level read latency export stays at 3 ms or less at every point from 01:00 to 04:00.
- B false: the misconception. A VM aggregate hides the one slow disk; read each virtual disk.
- C true: the peak metric takes the highest 20-second value across all virtual disks, read and write; the Peak Latency export is 15 ms or more at every point from 02:05 to 03:00 and below 10 ms at every other point.
- D false: the over-correction. Peak Latency within collection cycle showed it.
- E false: the wrong action. The report reads from the slow disk.
- F false: queues add latency at any load; the report waited on every one of that disk's IOs.
- G true: the flow goes per virtual disk, read and write, then errors, then IOPS and outstanding IO, then the backing device and the configuration.
- H false: reading. `Virtual Disk:scsi1:2|Read IOPS` is under 10% of `Virtual Disk:Aggregate of all instances|Read IOPS` for 02:00 to 03:00, and under 10% of the sum of the eight disks' Read IOPS.

## Notes
- Practical half of pair D4 with 0422 (theory; design.md, section 3.9).
- No option computes the aggregate: the knowledge base does not say whether it weights the disks by their IO. The condition fixes the values the key reads.
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item D4 (origin: synthetic). Counts only after author approval.
- Review 2026-11-15: F one fact; 8 or more disks, so that the aggregate can stay at 3 ms or less whatever its weighting (one disk at 15 ms among eight averages to 2.75 ms even unweighted). Key unchanged: A, C, G.
- 2026-11-15: screenshots replaced by generated exports (project/practical-questions-as-exports-2026-11-15.md), cut to 01:00-04:00. The slow disk stays at 15-17 ms and the other seven at 1 ms or less, so the aggregate stays at 3 ms or less whether VCF Operations weights it by IO or not.

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
