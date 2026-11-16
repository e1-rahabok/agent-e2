# A slow VM on a datastore that looks healthy

## Prompt
- The finance team says month-end reports on fin-rpt-03 took twice as long as last month.
- [The attached export](0184/ds-fin01-vms-disk-24-hours.csv) is a VCF Operations list view of the 24 VMs on VMFS datastore DS-FIN01, averaged over the last 24 hours: virtual disk read and write IOPS and latency, and snapshot space.
- The datastore's own counters for the same 24 hours: Datastore|Read IOPS 17,910 and Datastore|Read Latency 1.1 ms.
- The storage team points at the datastore: read latency 1.1 ms, so storage is fine.

Which statements are correct?

- A. The datastore read latency averages the 24 VMs, so one VM's slow reads hide in it.
- B. The datastore reads at 1.1 ms, so fin-rpt-03's slowness must be inside its Guest OS.
- C. The other 23 VMs read at about 1 ms from this datastore: the array serves them.
- D. At its low read IOPS, fin-rpt-03 cannot have a storage latency problem of any kind.
- E. Ranking the 24 VMs by read latency, rather than averaging them, finds fin-rpt-03.
- F. A snapshot on fin-rpt-03 is the first thing to check, before the host or the array.

## Likely wrong answer
B: the datastore average stands for every VM on it.

## Expected key points
- Answer: A, C, E, F.
- A is correct: the datastore latency is an average over the VMs on the datastore, so one slow VM hides in it. fin-rpt-03 issues 41 of about 17,900 reads per second; the datastore reads 1.1 ms while the VM itself sees 35 ms. The option does not depend on how the average weights the VMs.
- B is wrong: the misconception. The datastore average hides the one VM that suffers. The VM's own virtual disk latency is 35 ms, below the Guest OS.
- C is correct: 23 VMs on the same datastore read at 0.7-1.4 ms; the array serves them well, so the cause sits with the one slow VM.
- D is wrong: the misconception. Queues and the snapshot chain add latency at any load; fin-rpt-03 issues only 41 read IOPS and still sees 35 ms.
- E is correct: the worst member gives the depth of a problem, which an average blends away; sorted by read latency, fin-rpt-03 (35.2 ms) stands at the top.
- F is correct: latency on one VM only, with a snapshot (fin-rpt-03 is the only VM with one, 312 GB): the snapshot first. Latency on many VMs of a datastore would point to the host or the array.

## Notes
- Synthetic, 2026-11-12. Counts only after author approval.
- 2026-11-14: option A said the datastore value is weighted by commands, which the knowledge base states only for VM total latency (disk-latency), not for datastore latency; reworded to the stated fact (datastore latency is an average of the VMs on it; vm-performance). "VMFS" added to the stem: option F (snapshot chain reads) does not hold on vSAN ESA. Key unchanged.
- Review 2026-11-15: C, D, E and F no longer quote the export's values (41 IOPS, 312 GB, read against write), so the options do not read the CSV for the candidate. Key unchanged.
- Review 2026-11-15: unpaired from 0062, which tests high latency at low IOPS on one disk, not a datastore average hiding one VM (plan A6 dropped).
- Audit 2026-11-15: A and C reworded without hedges, D without "at all" (truth unchanged); E (read and write checked apart; kept by 0081 and 0405) replaced by ranking the VMs rather than averaging them (aggregation, added to `knowledge`); F (reads check the redo-log chain; kept by 0187 and 0045) reworded to the check order: one slow VM with a snapshot, the snapshot first. Key unchanged: A, C, E, F.

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
  - sp5-framework/observability/aggregation
knowledge_main: vsphere/technology/storage/troubleshooting/vm-storage-performance-checks
attachments:
  - 0184/ds-fin01-vms-disk-24-hours.csv
origin: synthetic
source_path: "Synthetic, 2026-11-12"
answer: [A, C, E, F]
misconception: [B, D]
misconception_type: [average-hides-worst]
status: draft
```
