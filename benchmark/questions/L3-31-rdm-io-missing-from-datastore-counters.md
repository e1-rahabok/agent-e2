# VM IOPS lower at the datastore than at the virtual disk

## Prompt
- ora-01 is an Oracle VM with 7 virtual disks: one VMDK for the OS on VMFS datastore DS-ORA01, and six RDMs for the data.
- vSphere Client, last hour, for ora-01:
  - Virtual disk read IOPS, summed over the 7 disks: 4,000.
  - Disk (device level) read IOPS: 4,000.
  - Datastore read IOPS: 50.
- A colleague says almost 4,000 IOPS are lost between the virtual disk and the datastore, so the counters are broken.

Which statements are correct?

- A. The VM's datastore counters exclude RDM IO: the RDM data sits on its own LUNs, not on the datastore.
- B. The gap is a fault: IO cannot be lower at the datastore than at the virtual disk.
- C. The virtual disk counters include the RDMs: an RDM appears to the VM as a virtual disk.
- D. The device-level Disk counters include the RDM LUNs, so they match the virtual disk total here.
- E. The datastore's used space includes the data on the RDMs, since their mapping files live there.
- F. The datastore counters would include the RDMs if the RDMs were in virtual compatibility mode.

## Likely wrong answer
B: reading the gap as lost IO.

## Expected key points
- Answer: A, C, D.
- A: an RDM is a pointer file on the datastore; its data lives on a separate LUN. The VM's datastore counters see only the VMDK's 50 read IOPS.
- C: the virtual disk counters cover VMDKs and RDMs alike.
- D: the device-level counters cover every LUN the VM uses, VMFS and RDM, so they also show 4,000.
- B is wrong: each counter is right for its own layer.
- E is wrong: the RDM data is not on the datastore; only the small mapping file is.
- F is wrong: the compatibility mode changes how SCSI commands are virtualized, not where the data lives.

## Notes
- Drafted by Claude 2026-11-12 for question set 1.0, Storage slot (Level 300 read-metric), replacing "write latency below read latency": that slot depends on the array's cache design, so its key would not be decidable from public mechanisms. Counts only after author approval.

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
source_path: "Drafted by Claude 2026-11-12 for the Storage slots (benchmark/design.md, section 3)"
answer: [A, C, D]
misconception: [B]
misconception_type: [same-name-other-object]
status: draft
```
