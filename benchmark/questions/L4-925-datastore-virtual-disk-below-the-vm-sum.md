# Datastore virtual disk space below the sum of its VMs

## Prompt
- Capacity review of VMFS datastore DS-ERP01 in VCF Operations. No VM has a snapshot.
- DS-ERP01, Disk Space | Virtual Disk Used: 1,200 GB.
- Three VMs have files on DS-ERP01. Their VM Disk Space | Virtual Disk Used: erp-app-01 800 GB, erp-db-01 2,064 GB, erp-rpt-01 260 GB.
- Their disks, from the VM settings and the datastore browser:

| VM | Disk | Where | Used (GB) |
|---|---|---|---|
| erp-app-01 | Hard disk 1, thin VMDK | DS-ERP01 | 120 |
| erp-app-01 | Hard disk 2, thin VMDK | DS-ERP01 | 680 |
| erp-db-01 | Hard disk 1, thin VMDK | DS-ERP01 | 140 |
| erp-db-01 | Hard disk 2, thin VMDK | DS-ERP02 | 900 |
| erp-db-01 | Hard disk 3, RDM in physical compatibility mode, 1,024 GB thick LUN; mapping file in the VM folder on DS-ERP01 | own LUN | - |
| erp-rpt-01 | Hard disk 1, thin VMDK | DS-ERP01 | 260 |

- A capacity analyst adds up the three VMs to 3,124 GB and reports that DS-ERP01's own figure misses 1,924 GB.

Which statements are correct?

- A. DS-ERP01's Virtual Disk Used counts only the VMDK files on it: 120 + 680 + 140 + 260 = 1,200 GB.
- B. The VM values should add up to the datastore's value, so the 1,924 GB gap is a collection error to raise with support.
- C. erp-db-01's 2,064 GB includes the RDM, whose data sits on its own LUN, not on DS-ERP01.
- D. Sizing DS-ERP01 needs room for the 3,124 GB of disks the three VMs report.
- E. The RDM takes its 1,024 GB on DS-ERP01, because its mapping file sits in the VM folder there.
- F. The VM and datastore values come from different objects, so neither can serve the datastore's capacity review.
- G. The space each VM takes on DS-ERP01, every file included, is its per-datastore Virtual Machine Used for DS-ERP01.
- H. DS-ERP01's Virtual Disk Used also includes the swap files and logs of the three VMs on DS-ERP01.
- I. Moving erp-db-01's Hard disk 2 to DS-ERP01, still thin, raises DS-ERP01's value by 900 GB and leaves erp-db-01's unchanged.

## Likely wrong answer
"The VMs on the datastore add up to 3,124 GB, so the datastore figure is wrong" (B), and the plan built on it, "size DS-ERP01 for 3,124 GB" (D).

## Expected key points
- Answer: A, C, G, I.
- A is correct: the datastore counts the VMDKs it holds and leaves out the VMs' disks on other datastores and their RDMs.
- B is wrong: the misconception. The VM value includes RDMs and the disks on other datastores. The gap is erp-db-01's Hard disk 2 on DS-ERP02 (900 GB) and its RDM (1,024 GB): 900 + 1,024 = 1,924 GB.
- C is correct: the VM's virtual disk value includes RDMs; the RDM's data is on an external LUN, and the datastore holds only the pointer file. 140 + 900 + 1,024 = 2,064 GB.
- D is wrong: the wrong action. 1,924 GB of the VM total sits on DS-ERP02 or on the RDM's LUN; DS-ERP01 holds 1,200 GB of virtual disks.
- E is wrong: the mapping file is only a pointer to the external LUN; the RDM's data is not on the datastore.
- F is wrong: the over-correction. Each value is right from its own vantage point; compare them per VM and datastore pair.
- G is correct: Disk Space | <Datastore Name> | Virtual Machine Used counts only the VM's files on that datastore, swap, logs and other files included.
- H is wrong: Virtual Disk Used counts the virtual disk files only; swap files, logs and other files are counted in Virtual Machine Used.
- I is correct: the disk moves into the datastore's vantage point, while it stays one of erp-db-01's virtual disks wherever it sits.

## Notes
- The RDM's LUN is stated thick on purpose: the knowledge base differs on how an RDM on a thin-provisioned array LUN is counted in VM Virtual Disk Used (disk-space: configured size unless the array thin-provisions the LUN; vm-files: always configured size). With a thick LUN both give 1,024 GB.
- The datastore label follows the knowledge base (datastore/virtual-disk: the same label as on the VM).

## Metadata
```yaml
id: "0461"
title: "Datastore virtual disk space below the sum of its VMs"
product: [vsphere, vcf-operations]
technology: [storage]
task: decide-capacity
level: 400
answer_type: deterministic
input: [text]
object: [datastore, vm]
tool: [vcf-operations]
knowledge:
  - vsphere/technology/storage/metrics/datastore/virtual-disk
  - vsphere/technology/storage/metrics/virtual-motherboard/virtual-disk
  - vsphere/technology/storage/metrics/virtual-motherboard/disk-space
  - vsphere/architecture/object-relationships
knowledge_main: vsphere/technology/storage/metrics/datastore/virtual-disk
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-15, question bank audit gap: vsphere/technology/storage/metrics/datastore/virtual-disk"
answer: [A, C, G, I]
misconception: [B, D]
misconception_type: [same-name-other-object]
status: draft
```
