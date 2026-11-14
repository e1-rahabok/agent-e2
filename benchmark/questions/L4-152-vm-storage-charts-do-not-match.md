# A VM's storage charts do not match

## Prompt
- An administrator troubleshooting a slow application compares the VM's Virtual disk, Datastore and Disk charts with the host's chart of the LUN behind the VM's VMFS datastore.
- The numbers differ, and he suspects the vCenter statistics are broken.
- See [the VM's Virtual disk chart](0427/vcenter-vm-virtual-disk-real-time.png), [the VM's Datastore chart](0427/vcenter-vm-datastore-real-time.png), [the VM's Disk chart](0427/vcenter-vm-disk-real-time.png) and [the host's Disk chart of the LUN](0427/vcenter-host-disk-lun-real-time.png), same minutes.

Which statements are correct?

- A. The NFS disk's IO is missing from the VM's Disk chart, because that chart covers block devices (VMFS and RDM) only.
- B. The VM's Disk chart counts only this VM's IO on the LUN.
- C. The host's chart of the LUN counts the IO of every VM on this host that uses the LUN.
- D. The VM's Disk chart is the whole LUN's IO, so it should match the host's chart of the LUN.
- E. The three VM charts measure different IO and never agree.
- F. Raise a support case: the vCenter statistics are inconsistent.
- G. The VM's Datastore chart shows the NFS disk's IO.
- H. The VM's Disk chart splits the LUN's IO per virtual disk.

## Input to supply
- Product and version: vSphere 9.1 (vSphere Client 9.1).
- Object: one VM with Hard disk 1 on a VMFS datastore backed by one LUN (no extents) that other running VMs on the same host also use, and Hard disk 2 on an NFS datastore; no snapshot on the VM.
- How to produce it: in the VM, a steady load on both disks (for example fio at about 500 IOPS on Hard disk 1 and 300 IOPS on Hard disk 2); keep other VMs on the same host and the same LUN busy, so that the host's IO to the LUN is at least 1.5 times this VM's IO.
- Screen 1, vSphere Client > the VM > Monitor > Performance > Advanced > Virtual disk, Real-time, both disk instances, counters Average read requests per second and Average write requests per second. Save as `0427/vcenter-vm-virtual-disk-real-time.png`.
- Screen 2, the same VM, Advanced > Datastore, Real-time, both datastores, the same two counters. Save as `0427/vcenter-vm-datastore-real-time.png`.
- Screen 3, the same VM, Advanced > Disk, Real-time, the LUN, the same two counters. Save as `0427/vcenter-vm-disk-real-time.png`.
- Screen 4, vSphere Client > the VM's host > Monitor > Performance > Advanced > Disk, Real-time, the same LUN only, the same two counters. Save as `0427/vcenter-host-disk-lun-real-time.png`.
- Capture all four within the same minutes, each with its legend table.
- Condition the key depends on: the NFS disk's IO shows in screens 1 and 2 and is absent from screen 3; the VM's Disk IOPS (screen 3) within 10% of Hard disk 1's IOPS (screen 1); the VM's VMFS datastore IOPS (screen 2) within 10% of Hard disk 1's IOPS; the host's IOPS for the LUN (screen 4) at least 1.5 times the VM's Disk IOPS.
- Masking: mask every VM, host, datastore and cluster name, and the device identifier.

## Likely wrong answer
D: the VM's Disk chart is the LUN, so it should match the host's chart. Or E and F: the charts never agree, so the statistics are broken.

## Expected key points
- Answer: A, B, C, G.
- A true: the VM Disk level covers VMFS and RDM devices, not NFS: an NFS datastore has no SCSI device.
- B true: the VM Disk value is this VM's IO only, not the whole device that other VMs share.
- C true: the host's device counters cover all the IO this host sends to the LUN, for all its VMs; there is no breakdown per VM at the device.
- D false: the misconception. Screen 4 shows at least 1.5 times screen 3: the other VMs of the host on the same LUN.
- E false: the over-correction. Hard disk 1, the VM's Disk chart and its VMFS datastore line agree within 10%: one LUN, no extents, no snapshot.
- F false: the wrong action. Each chart is right from its level.
- G true: the VM datastore level covers VMFS and NFS.
- H false: the Disk level is not split per virtual disk.

## Notes
- Practical half of pair D7 with 0426 (theory; design.md, section 3.9).
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item D7 (origin: synthetic). Counts only after author approval.

## Metadata
```yaml
id: "0427"
title: "A VM's storage charts do not match"
product: [vsphere]
technology: [storage]
task: read-metric
level: 400
answer_type: deterministic
input: [screenshot]
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
  - 0427/vcenter-vm-virtual-disk-real-time.png
  - 0427/vcenter-vm-datastore-real-time.png
  - 0427/vcenter-vm-disk-real-time.png
  - 0427/vcenter-host-disk-lun-real-time.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D7"
answer: [A, B, C, G]
misconception: [D]
misconception_type: [same-name-other-object, provider-vs-consumer]
pair: "0426"
status: awaiting-input
```
