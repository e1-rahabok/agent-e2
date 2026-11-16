# VM storage charts: virtual disk, datastore and disk

## Prompt
- In the vSphere Client, a VM's Advanced performance charts offer Virtual disk, Datastore and Disk.
- The VM has two VMDKs on one VMFS datastore, backed by one LUN that other VMs share, and one RDM.

Which statements are correct?

- A. The Virtual disk chart shows each disk as its own object (scsiM:N), the RDM included.
- B. The Datastore chart leaves out the RDM's IO.
- C. The Datastore chart sums both VMDKs into one datastore instance, with no per-disk line.
- D. The Disk chart shows the total IO of the whole LUN, from every VM on it.
- E. The Disk chart includes the RDM's IO.
- F. Even with all disks on one VMFS datastore on one LUN and no snapshot, the three charts show clearly different IOPS.
- G. A gap between the Datastore and Virtual disk charts shows a statistics collection fault.
- H. The Disk chart breaks the VM's device IO down per scsiM:N disk.

## Likely wrong answer
D: the Disk chart is the whole LUN. Or F, the overshoot: the three charts differ even in the simplest layout.

## Expected key points
- Answer: A, B, C, E.
- A is correct: virtual disk covers VMDKs on VMFS and NFS and RDMs; the vSphere Client objects are the individual disks.
- B is correct: VM datastore metrics cover VMFS and NFS, not RDM: the RDM's data is on an external LUN.
- C is correct: the VM's datastore metrics are already aggregated at VM level, one instance per datastore; they have no per-virtual-disk breakdown.
- D is wrong: the misconception. The VM Disk chart is this VM's IO at the device level, not the IO other VMs send to the shared LUN.
- E is correct: the VM Disk level covers VMFS and RDM devices (not NFS).
- F is wrong: the over-correction. With all disks on one datastore backed by one LUN, virtual disk, disk and datastore metrics are nearly identical; differences come from files outside the virtual disks (snapshots, logs, swap) and from RDMs.
- G is wrong: the wrong conclusion. RDM IO and IO to files outside the virtual disks (snapshots, logs, swap) explain a gap; each chart is right from its level.
- H is wrong: the Disk level is per device; it is not split per virtual disk.

## Notes
- Theory half of pair D7 with 0427 (practical; design.md, section 3.9). Different disk layout from 0427 (RDM here, NFS there).
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item D7 (origin: synthetic). Counts only after author approval.
- Review 2026-11-15: F and H reworded away from 0427. Key unchanged: A, B, C, E.
- Audit 2026-11-15: C (snapshot IO in the datastore chart, tested by 0045 and 0090) replaced by the datastore chart's one instance per datastore. Key unchanged: A, B, C, E.

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
