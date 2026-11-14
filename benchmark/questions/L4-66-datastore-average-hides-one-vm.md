# A slow VM on a datastore that looks healthy

## Prompt
- The finance team says month-end reports on fin-rpt-03 took twice as long as last month.
- [The attached export](0184/ds-fin01-vms-disk-24-hours.csv) is a VCF Operations list view of the 24 VMs on datastore DS-FIN01, averaged over the last 24 hours: virtual disk read and write IOPS and latency, and snapshot space.
- The datastore's own counters for the same 24 hours: Datastore|Read IOPS 17,910 and Datastore|Read Latency 1.1 ms.
- The storage team points at the datastore: read latency 1.1 ms, so storage is fine.

Which statements are correct?

- A. The datastore value is weighted by commands, so a VM with few IOs barely moves it.
- B. The datastore reads at 1.1 ms, so fin-rpt-03's slowness must be inside its Guest OS.
- C. The other VMs read at about 1 ms, so the cause is more likely in fin-rpt-03 itself.
- D. At only 41 read IOPS, fin-rpt-03 cannot have a storage latency problem at all.
- E. Work on fin-rpt-03's reads, per virtual disk: its reads are slow, its writes are not.
- F. Its 312 GB snapshot is a first suspect: each read must check the snapshot chain.

## Likely wrong answer
B: the datastore average stands for every VM on it.

## Expected key points
- Answer: A, C, E, F.
- A: the datastore read latency is an average over all read commands. fin-rpt-03 issues 41 of about 17,900 reads per second, so its 35 ms adds almost nothing. An unweighted mean of the VMs would be about 2.5 ms; the VM itself sees 35 ms.
- C: 23 VMs on the same datastore read at 0.7-1.4 ms; the array serves them well.
- E: read latency 35.2 ms against write latency 2.1 ms: one side is affected; look at that side, per disk.
- F: fin-rpt-03 is the only VM with a snapshot. Reads on a VM with a snapshot must check every file of the chain.
- B is wrong: the datastore average hides the one VM that suffers. The VM's own virtual disk latency is 35 ms, below the Guest OS.
- D is wrong: queues and the snapshot chain add latency at any load.

## Notes
- Drafted by Claude 2026-11-12. Counts only after author approval.

## Metadata
```yaml
id: "0184"
title: "A slow VM on a datastore that looks healthy"
product: [vsphere, vcf-operations]
technology: [storage]
task: troubleshoot
level: 400
answer_type: deterministic
input: [table]
object: [vm, datastore]
tool: [vcf-operations]
knowledge:
  - vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
  - vsphere/technology/storage/troubleshooting/vm-storage-performance-checks
  - vsphere/technology/storage/concepts/snapshot-impact
  - vsphere/technology/storage/concepts/guest-os-vs-vm-storage
knowledge_main: vsphere/technology/storage/troubleshooting/vm-storage-performance-checks
attachments:
  - 0184/ds-fin01-vms-disk-24-hours.csv
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
answer: [A, C, E, F]
misconception: [B, D]
misconception_type: [average-hides-worst]
status: draft
```
