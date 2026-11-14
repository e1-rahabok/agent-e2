# One slow disk behind a low VM disk latency

## Prompt
- The application team says a nightly report that reads from one of the VM's disks ran much slower yesterday.
- The VMware team looked at the VM's disk latency in VCF Operations, found it low all day, and wants to close the ticket.
- See [the VM-level disk latency and IOPS](0423/vcf-operations-vm-disk-aggregate-24h.png), [the read latency and IOPS of each virtual disk](0423/vcf-operations-vm-virtual-disks-24h.png) and [the VM's Peak Latency within collection cycle](0423/vcf-operations-vm-peak-latency-24h.png).

Which statements are correct?

- A. One virtual disk ran at 15 ms or more for about an hour while the VM-level latency stayed low.
- B. The VM-level latency stayed low, so every virtual disk was served well.
- C. Peak Latency within collection cycle rose in the same hour, because it takes the worst 20 seconds across all the virtual disks.
- D. No VM-level metric could have shown this disk's latency.
- E. Close the ticket: the VM-level latency stayed within target all day.
- F. The slow disk's latency can be set aside because it did few IOs.
- G. The next checks follow the slow disk: its read and write latency, errors, outstanding IO and the datastore behind it.
- H. The slow disk carried most of the VM's IO in that hour.

## Input to supply
- Product and version: VCF Operations 9.1, vSphere 9.1.
- Object: one VM with 6 or more virtual disks.
- How to produce it: keep 5 or more disks busy all day at low latency (1 ms or less, a few thousand IOPS in total), and for about one hour run a small read load (100-300 IOPS) on one disk that sits on a slow datastore (for example an NFS export on a small server, or a busy array), so that its read latency is 15 ms or more.
- Screen 1, VCF Operations > the VM > Metrics: the virtual disk aggregate of all instances, Read Latency (ms) and Read IOPS, last 24 hours. Save as `0423/vcf-operations-vm-disk-aggregate-24h.png`.
- Screen 2, the same VM, Read Latency (ms) and Read IOPS of each virtual disk instance (scsiM:N), last 24 hours, on one chart or as a list with the values for the slow hour. Save as `0423/vcf-operations-vm-virtual-disks-24h.png`.
- Screen 3, the same VM, Peak Latency within collection cycle (ms), last 24 hours. Save as `0423/vcf-operations-vm-peak-latency-24h.png`.
- Condition the key depends on: the aggregate read latency at 3 ms or less all day; one virtual disk at 15 ms or more for about an hour; that disk's IOPS under 10% of the VM's IOPS in that hour; Peak Latency within collection cycle at 15 ms or more in the same hour and below 10 ms the rest of the day.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
B or E: the VM's disk latency is low all day, so storage is fine and the ticket can be closed. Or D, the overshoot: no VM-level metric could show it.

## Expected key points
- Answer: A, C, G.
- A true: screen 2 shows one disk at 15 ms or more for about an hour; screen 1 shows the aggregate at 3 ms or less.
- B false: the misconception. A VM aggregate hides the one slow disk; read each virtual disk.
- C true: the peak metric takes the highest 20-second value across all virtual disks, read and write; screen 3 rises in the slow hour.
- D false: the over-correction. Peak Latency within collection cycle showed it.
- E false: the wrong action. The report reads from the slow disk.
- F false: latency with low IOPS points to a queue in one of the layers; the report waited on every one of those IOs.
- G true: the flow goes per virtual disk, read and write, then errors, then IOPS and outstanding IO, then the backing device and the configuration.
- H false: the slow disk did under 10% of the VM's IOPS in that hour.

## Notes
- Practical half of pair D4 with 0422 (theory; design.md, section 3.9).
- No option computes the aggregate: the knowledge base does not say whether it weights the disks by their IO. The condition fixes the values the key reads.
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item D4 (origin: synthetic). Counts only after author approval.

## Metadata
```yaml
id: "0423"
title: "One slow disk behind a low VM disk latency"
product: [vsphere, vcf-operations]
technology: [storage]
task: troubleshoot
level: 400
answer_type: deterministic
input: [screenshot]
object: [vm]
tool: [vcf-operations]
knowledge:
  - vsphere/technology/storage/troubleshooting/vm-storage-performance-checks
  - vcf-operations/features/peak-20-second-metrics
  - vsphere/technology/storage/metrics/virtual-motherboard/virtual-disk
knowledge_main: vsphere/technology/storage/troubleshooting/vm-storage-performance-checks
attachments:
  - 0423/vcf-operations-vm-disk-aggregate-24h.png
  - 0423/vcf-operations-vm-virtual-disks-24h.png
  - 0423/vcf-operations-vm-peak-latency-24h.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D4"
answer: [A, C, G]
misconception: [B, E]
misconception_type: [average-hides-worst]
pair: "0422"
status: awaiting-input
```
