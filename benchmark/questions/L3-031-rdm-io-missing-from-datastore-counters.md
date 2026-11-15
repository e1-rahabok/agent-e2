# VM IOPS lower at the datastore than at the virtual disk

## Prompt
- ora-01 is an Oracle VM with 7 virtual disks: one VMDK for the OS on VMFS datastore DS-ORA01, and six RDMs for the data.
- vSphere Client, last hour, for ora-01:
  - Virtual disk read IOPS, summed over the 7 disks: 4,000.
  - Disk (device level) read IOPS: 4,000.
  - Datastore read IOPS: 50.
- A colleague says almost 4,000 IOPS are lost between the virtual disk and the datastore, so the counters are broken.

Which statements are correct?

- A. The VM's datastore counters count only IO to files on DS-ORA01, so the six RDMs are not in them.
- B. The gap is a fault: IO cannot be lower at the datastore than at the virtual disk.
- C. The virtual disk counters include the RDMs, since an RDM appears to the VM as a virtual disk.
- D. The device-level Disk counters cover the RDM LUNs as well as the VMFS LUN.
- E. The datastore's used space includes the data on the RDMs, since their mapping files live there.
- F. The 50 datastore read IOPS include reads by other VMs on DS-ORA01.
- G. Device-level Disk read IOPS match virtual disk read IOPS for any VM, whatever backs its disks.
- H. With only 50 datastore read IOPS, the database storage has plenty of headroom, so its LUNs need no check.

## Likely wrong answer
B: reading the gap as lost IO.

## Expected key points
- Answer: A, C, D.
- A is true: an RDM is a pointer file on the datastore; its data lives on a separate LUN. The VM's datastore counters see only the VMDK's 50 read IOPS.
- B is false: each counter is right for its own layer.
- C is true: the virtual disk counters cover VMDKs and RDMs alike.
- D is true: the device-level counters cover every LUN the VM uses, VMFS and RDM, so they also show 4,000.
- E is false: the RDM data is not on the datastore; only the small mapping file is.
- F is false: the VM's datastore counters hold this VM's IO only.
- G is false: the Disk level covers VMFS and RDM, not NFS; a VM with disks on NFS shows virtual disk IO that the Disk level does not.
- H is false: the RDM LUNs carry the 4,000 read IOPS; the datastore counters see only the OS disk.

## Notes
- Drafted by Claude 2026-11-12, replacing a question on "write latency below read latency": that topic depends on the array's cache design, so its key would not be decidable from public mechanisms. Counts only after author approval.
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): the compatibility-mode option (old F) dropped, as the knowledge base does not name the mode; F (other VMs), over-correction G and wrong action H added. Key unchanged: A, C, D.

## Metadata
```yaml
id: "0185"
title: "VM IOPS lower at the datastore than at the virtual disk"
product: [vsphere]
technology: [storage]
task: read-metric
level: 300
answer_type: deterministic
input: [text]
object: [vm, datastore]
tool: [vcenter]
knowledge:
  - vsphere/technology/storage/metrics/virtual-motherboard/datastore
  - vsphere/technology/storage/metrics/virtual-motherboard/virtual-disk
  - vsphere/technology/storage/metrics/virtual-motherboard/disk
  - vsphere/technology/storage/concepts/vm-files
knowledge_main: vsphere/technology/storage/metrics/virtual-motherboard/datastore
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
answer: [A, C, D]
misconception: [B]
misconception_type: [same-name-other-object]
status: draft
```
