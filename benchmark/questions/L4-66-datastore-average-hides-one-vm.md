# A slow VM on a datastore that looks healthy

## Prompt
- The finance team says month-end reports on fin-rpt-03 took twice as long as last month.
- [The attached export](0184/ds-fin01-vms-disk-24-hours.csv) is a VCF Operations list view of the 24 VMs on VMFS datastore DS-FIN01, averaged over the last 24 hours: virtual disk read and write IOPS and latency, and snapshot space.
- The datastore's own counters for the same 24 hours: Datastore|Read IOPS 17,910 and Datastore|Read Latency 1.1 ms.
- The storage team points at the datastore: read latency 1.1 ms, so storage is fine.

Which statements are correct?

- A. The datastore read latency averages the reads of all 24 VMs, so it can stay near 1 ms while one VM reads slowly.
- B. The datastore reads at 1.1 ms, so fin-rpt-03's slowness must be inside its Guest OS.
- C. The other VMs read at about 1 ms, so the cause is more likely in fin-rpt-03's own disks or snapshot rather than in the array.
- D. At its low read IOPS, fin-rpt-03 cannot have a storage latency problem at all.
- E. Read latency and write latency of fin-rpt-03 are checked separately, per virtual disk.
- F. A snapshot on fin-rpt-03 is a first suspect: each read must check the snapshot chain.

## Likely wrong answer
B: the datastore average stands for every VM on it.

## Expected key points
- Answer: A, C, E, F.
- A: the datastore latency is an average over the VMs on the datastore, so one slow VM hides in it. fin-rpt-03 issues 41 of about 17,900 reads per second; the datastore reads 1.1 ms while the VM itself sees 35 ms. The option does not depend on how the average weights the VMs.
- C: 23 VMs on the same datastore read at 0.7-1.4 ms; the array serves them well.
- E: read latency 35.2 ms against write latency 2.1 ms: one side is affected, which the VM total would hide; look at that side, per disk.
- F: fin-rpt-03 is the only VM with a snapshot (312 GB). Reads on a VM with a redo-log snapshot must check every file of the chain.
- B is wrong: the datastore average hides the one VM that suffers. The VM's own virtual disk latency is 35 ms, below the Guest OS.
- D is wrong: queues and the snapshot chain add latency at any load; fin-rpt-03 issues only 41 read IOPS and still sees 35 ms.

## Notes
- Drafted by Claude 2026-11-12. Counts only after author approval.
- 2026-11-14: option A said the datastore value is weighted by commands, which the knowledge base states only for VM total latency (disk-latency), not for datastore latency; reworded to the stated fact (datastore latency is an average of the VMs on it; vm-performance). "VMFS" added to the stem: option F (snapshot chain reads) does not hold on vSAN ESA. Key unchanged.
- Review 2026-11-15: C, D, E and F no longer quote the export's values (41 IOPS, 312 GB, read against write), so the options do not read the CSV for the candidate. Key unchanged.
- Review 2026-11-15: unpaired from 0062, which tests high latency at low IOPS on one disk, not a datastore average hiding one VM (plan A6 dropped).

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
  - vsphere/object-types/vm/vm-performance
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
