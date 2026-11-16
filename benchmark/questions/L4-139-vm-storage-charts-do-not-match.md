# A VM's storage charts do not match

## Prompt
- An administrator troubleshooting a slow application on VM rpt-app-11 compares its storage counters with those of its host esx-c4-05. The numbers differ, and he suspects the vCenter statistics are broken.
- Hard disk 1 (scsi0:0) is on the VMFS datastore ds-vmfs-21, backed by one LUN (naa.600a0b80003c5d2e00001f4a6b7c8d90) with no extents. Other running VMs on esx-c4-05 also use that LUN.
- Hard disk 2 (scsi0:1) is on the NFS datastore nfs-arch-02. The VM has no snapshot.
- He exported four Real-time charts to CSV, the same 10 minutes: [the VM's Virtual disk chart](0427/vcenter-vm-virtual-disk-realtime.csv), [the VM's Datastore chart](0427/vcenter-vm-datastore-realtime.csv), [the VM's Disk chart](0427/vcenter-vm-disk-realtime.csv) and [the host's Disk chart of the LUN](0427/vcenter-host-disk-lun-realtime.csv).

- The chart legends (not in the exports) give the units: rates in KBps, latencies in ms.

Which statements are correct?

- A. The NFS disk's IO is missing from the VM's Disk export, because that view covers block devices (VMFS and RDM) only.
- B. The VM's Disk IOPS match its Hard disk 1 IOPS within 10%.
- C. The host's Disk export of the LUN counts the IO of every VM on this host that uses the LUN.
- D. The VM's Disk export is the whole LUN's IO, so it should match the host's Disk export of the LUN.
- E. The three VM exports measure different IO and never agree.
- F. Raise a support case: the vCenter statistics are inconsistent.
- G. The VM's Datastore export shows the NFS disk's IO.
- H. The VM's Disk export has a column for each virtual disk of the VM.

## Likely wrong answer
D: the VM's Disk export is the LUN, so it should match the host's. Or E and F: the exports never agree, so the statistics are broken.

## Expected key points
- Answer: A, B, C, G.
- A true: the VM Disk level covers VMFS and RDM devices, not NFS: an NFS datastore has no SCSI device. The VM's Disk export has only columns `... for Fibre Channel Disk (naa.600a0b80003c5d2e00001f4a6b7c8d90)`, while scsi0:1 does 250 IOPS or more in the Virtual disk export.
- B true: reading. In every row, `Average read requests per second` plus `Average write requests per second` for the LUN in the VM's Disk export is within 10% of the same sum for scsi0:0 in the Virtual disk export: the VM Disk value is this VM's IO on the LUN, and only Hard disk 1 sits on it.
- C true: the host's device counters cover all the IO this host sends to the LUN, for all its VMs; there is no breakdown per VM at the device.
- D false: the misconception. The VM Disk value is this VM's IO only; the host's Disk export of the LUN shows at least 1.5 times the VM's Disk IOPS in every row: the other VMs of the host on the same LUN.
- E false: the over-correction. Hard disk 1 (scsi0:0), the VM's Disk export and the ds-vmfs-21 columns of the Datastore export agree within 10% in every row: one LUN, no extents, no snapshot.
- F false: the wrong action. Each export is right from its level.
- G true: the VM datastore level covers VMFS and NFS: the nfs-arch-02 columns of the Datastore export are within 10% of scsi0:1.
- H false: reading. The Disk export has columns for the LUN, a device, only; it is not split per virtual disk, and the NFS disk has no column there.

## Notes
- Practical half of pair D7 with 0426 (theory; design.md, section 3.9).
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item D7 (origin: synthetic). Counts only after author approval.
- Review 2026-11-15: B is a screen reading now (it was the negation of D); H a false screen reading. Key unchanged: A, B, C, G.
- 2026-11-15: screenshots replaced by generated exports (project/practical-questions-as-exports-2026-11-15.md); H now reads the export's columns.

## Metadata
```yaml
id: "0427"
title: "A VM's storage charts do not match"
product: [vsphere]
technology: [storage]
task: read-metric
level: 400
answer_type: deterministic
input: [table]
object: [vm, datastore, esxi]
tool: [vcenter]
knowledge:
  - vsphere/technology/storage/metrics/virtual-motherboard/disk
  - vsphere/technology/storage/metrics/virtual-motherboard/virtual-disk
  - vsphere/technology/storage/metrics/virtual-motherboard/datastore
  - vsphere/technology/storage/concepts/storage-layers
  - vsphere/technology/storage/metrics/host/disk
knowledge_main: vsphere/technology/storage/metrics/virtual-motherboard/disk
attachments:
  - 0427/vcenter-vm-virtual-disk-realtime.csv
  - 0427/vcenter-vm-datastore-realtime.csv
  - 0427/vcenter-vm-disk-realtime.csv
  - 0427/vcenter-host-disk-lun-realtime.csv
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D7"
answer: [A, B, C, G]
misconception: [D]
misconception_type: [same-name-other-object, provider-vs-consumer]
pair: "0426"
status: draft
```
