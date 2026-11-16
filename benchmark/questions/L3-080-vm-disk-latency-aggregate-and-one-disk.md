# VM disk latency across many virtual disks

## Prompt
- A database VM has 12 virtual disks. VCF Operations shows, for this VM, a VM-level read latency built from all its virtual disks, the read latency of each virtual disk, and Peak Latency within collection cycle.

Which statements are correct?

- A. To find a slow disk behind a low VM-level value, read the latency of each virtual disk.
- B. A VM-level read latency of 2 ms bounds the read latency of the 12 disks near 2 ms.
- C. A VM-level metric cannot show one slow virtual disk; that takes the per-disk view.
- D. Peak Latency within collection cycle is not capped at 15 times the VM-level read latency.
- E. Peak Latency within collection cycle names which of the 12 virtual disks set the peak.
- F. Close the slowness ticket once the VM-level read latency is back to a low value.
- G. The peak metric keeps last week's 20-second peaks after vCenter drops its samples.
- H. The vSphere Client offers the same VM-level aggregate of virtual disk read latency.

## Likely wrong answer
B: the VM's latency is low, so every disk is fine. Or C, the overshoot: no VM-level metric can show a slow disk.

## Expected key points
- Answer: A, D, G.
- A is correct: a VM aggregate blends the disks and hides the one slow disk; the check is per virtual disk, read and write.
- B is wrong: the misconception. The aggregate does not bound each disk.
- C is wrong: the over-correction. Peak Latency within collection cycle takes the peak across all virtual disks, read and write, so a slow disk raises it.
- D is correct: for one series a 20-second peak is at most 15 times its 5-minute average, but this peak is taken across all 24 series (12 disks, read and write), while the VM-level value blends the disks; one slow disk can set a peak far above 15 times the average.
- E is wrong: it is one metric for the VM; it stores the peak value, not which disk produced it. The per-disk view finds the disk.
- F is wrong: the wrong action. A low aggregate does not clear any single disk.
- G is correct: VCF Operations computes the peak at collection time from the 15 samples of 20 seconds that vCenter holds for about an hour, and stores it as a metric of its own, so it stays after the samples are gone.
- H is wrong: the vSphere Client has no VM-level aggregate for virtual disks; its objects are the individual scsiM:N disks. Its VM Disk and Datastore charts do have a VM-level Highest latency, but that is the device and datastore layer, not virtual disk latency, and it is the latest value of the period (rollup Latest), not an aggregate of the disks. VCF Operations has the aggregate of all instances.

## Notes
- Theory half of pair D4 with 0423 (practical; design.md, section 3.9). Different VM and numbers from 0423.
- No option computes the aggregate: the knowledge base does not say whether it weights the disks by their IO.
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item D4 (origin: synthetic). Counts only after author approval.
- Review 2026-11-15: 12 virtual disks, so the situation differs from 0423 (8 or more). Key unchanged.
- Audit 2026-11-15 (redundancy): D (the peak is taken across all disks, read and write; kept by 0089 and 0356) replaced by the peak above 15 times the average across instances (also 0089 A, two questions); G (read and write checked apart; kept by 0081 and 0405) replaced by the peak kept after vCenter drops its 20-second samples (also 0356 E, two questions). E, F and H lengthened (truth unchanged); H key point explains the Highest latency of the other layers. Key unchanged: A, D, G.
- Re-review 2026-11-16: the hedges sat only in the correct options (A "can hide", D "can exceed") and the absolutes only in the wrong ones (B "every", C "No ... only"), and A was the near-negation of B. A now states the per-disk check (vm-storage-performance-checks, step 1), D says the peak is not capped at 15 times; B and C lose their absolutes (truth unchanged). Key unchanged: A, D, G.

## Metadata
```yaml
id: "0422"
title: "VM disk latency across many virtual disks"
product: [vsphere, vcf-operations]
technology: [storage]
task: read-metric
level: 300
answer_type: deterministic
input: [text]
object: [vm]
tool: [vcf-operations, vcenter]
knowledge:
  - vsphere/technology/storage/troubleshooting/vm-storage-performance-checks
  - vcf-operations/features/peak-20-second-metrics
  - vsphere/technology/storage/metrics/virtual-motherboard/virtual-disk
  - vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
  - vsphere/technology/storage/metrics/virtual-motherboard/disk
knowledge_main: vsphere/technology/storage/troubleshooting/vm-storage-performance-checks
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D4"
answer: [A, D, G]
misconception: [B]
misconception_type: [average-hides-worst]
pair: "0423"
status: draft
```
