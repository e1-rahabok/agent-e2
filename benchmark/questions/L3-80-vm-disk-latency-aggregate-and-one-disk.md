# VM disk latency across many virtual disks

## Prompt
- A database VM has 8 virtual disks. VCF Operations shows, for this VM, a VM-level read latency built from all its virtual disks, the read latency of each virtual disk, and Peak Latency within collection cycle.

Which statements are correct?

- A. The VM-level latency combines all the virtual disks, so one slow disk can hide in it.
- B. A VM-level read latency of 2 ms shows that every virtual disk is served within about 2 ms.
- C. No VM-level metric can reveal one slow virtual disk: only the per-disk view can.
- D. Peak Latency within collection cycle takes the highest 20-second value across all the virtual disks, reads and writes.
- E. Peak Latency within collection cycle names the virtual disk that was slow.
- F. Close the slowness ticket when the VM-level latency is low.
- G. Read and write latency are checked separately for each virtual disk, because often only one side is slow.
- H. The vSphere Client offers the same VM-level aggregate of virtual disk latency.

## Likely wrong answer
B: the VM's latency is low, so every disk is fine. Or C, the overshoot: no VM-level metric can show a slow disk.

## Expected key points
- Answer: A, D, G.
- A true: a VM aggregate hides the one slow disk; the check is per virtual disk.
- B false: the misconception. The aggregate does not bound each disk.
- C false: the over-correction. Peak Latency within collection cycle takes the peak across all virtual disks, read and write, so a slow disk raises it.
- D true: the peak metric is the highest of the 15 values of 20 seconds, across instances: all virtual disks, read and write.
- E false: it is one metric for the VM; it stores the peak value, not which disk produced it. The per-disk view finds the disk.
- F false: the wrong action. A low aggregate does not clear any single disk.
- G true: read and write latency have different patterns and causes; only read or only write affected is common.
- H false: the vSphere Client has no VM-level aggregate for virtual disks; its objects are the individual scsiM:N disks. VCF Operations has the aggregate of all instances.

## Notes
- Theory half of pair D4 with 0423 (practical; design.md, section 3.9). Different VM and numbers from 0423.
- No option computes the aggregate: the knowledge base does not say whether it weights the disks by their IO.
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item D4 (origin: synthetic). Counts only after author approval.

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
