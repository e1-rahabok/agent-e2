# VM storage charts: virtual disk, datastore and disk

## Prompt
- In the vSphere Client, a VM's Advanced performance charts offer Virtual disk, Datastore and Disk.
- The VM has two VMDKs on one VMFS datastore, backed by one LUN that other VMs share, and one RDM.

Which statements are correct?

- A. The Virtual disk chart shows each disk as its own object (scsiM:N), the RDM included.
- B. The Datastore chart leaves out the RDM's IO.
- C. The Datastore chart includes snapshot IO, which the Virtual disk chart leaves out.
- D. The Disk chart shows the total IO of the whole LUN, from every VM on it.
- E. The Disk chart includes the RDM's IO.
- F. The three charts measure different IO and never agree.
- G. A gap between the Datastore and Virtual disk charts shows a statistics collection fault.
- H. The Disk chart splits the VM's IO per virtual disk.

## Likely wrong answer
D: the Disk chart is the whole LUN. Or F, the overshoot: the three charts never agree.

## Expected key points
- Answer: A, B, C, E.
- A true: virtual disk covers VMDKs on VMFS and NFS and RDMs; the vSphere Client objects are the individual disks.
- B true: VM datastore metrics cover VMFS and NFS, not RDM: the RDM's data is on an external LUN.
- C true: snapshots live at datastore level; virtual disk metrics exclude snapshot data.
- D false: the misconception. The VM Disk chart is this VM's IO at the device level, not the IO other VMs send to the shared LUN.
- E true: the VM Disk level covers VMFS and RDM devices (not NFS).
- F false: the over-correction. With all disks on one datastore backed by one LUN, virtual disk, disk and datastore metrics are nearly identical; the differences come from files outside the virtual disks and from RDMs.
- G false: the wrong conclusion. RDM IO and snapshot IO explain the gap; each chart is right from its level.
- H false: the Disk level is not split per virtual disk.

## Notes
- Theory half of pair D7 with 0427 (practical; design.md, section 3.9). Different disk layout from 0427 (RDM here, NFS there).
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item D7 (origin: synthetic). Counts only after author approval.

## Metadata
```yaml
id: "0426"
title: "VM storage charts: virtual disk, datastore and disk"
product: [vsphere]
technology: [storage]
task: read-metric
level: 300
answer_type: deterministic
input: [text]
object: [vm, datastore]
tool: [vcenter]
knowledge:
  - vsphere/technology/storage/metrics/virtual-motherboard/disk
  - vsphere/technology/storage/metrics/virtual-motherboard/virtual-disk
  - vsphere/technology/storage/metrics/virtual-motherboard/datastore
  - vsphere/technology/storage/concepts/storage-layers
knowledge_main: vsphere/technology/storage/metrics/virtual-motherboard/disk
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D7"
answer: [A, B, C, E]
misconception: [D]
misconception_type: [same-name-other-object]
pair: "0427"
status: draft
```
