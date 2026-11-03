# VM Disk Space | Virtual Machine Used (VCF Operations)

## Meaning
- Actual consumed size of all VM files + configured size of RDMs. All files in the VM folder(s).
- Always larger than Virtual Disk Used: includes snapshots, swap, logs and other files.
- Per-datastore variant: Disk Space | <Datastore Name> | Virtual Machine Used (GB). Only files on that datastore. Same value for a VM on one datastore.

## Formula
```text
Sum over layoutEx.file of (uniqueSize if not null else size) / (1024 × 1024 × 1024)
```

## Traps
- "VM Used = sum of virtual disks" → includes all files in the folder.

## Metadata
```yaml
id: vsphere/storage/metrics/virtual-motherboard/disk-space-used
retriever_guide: metric-meaning
scope: vsphere
technology:
- storage
pillar:
- capacity
product:
- vsphere
- vcf-operations
object:
- VirtualMachine
layer:
- virtual-motherboard
metric_class: consumption
internal_derive:
- vsphere/storage/concepts/vm-files
same_name: []
same_meaning: []
related:
- vsphere/storage/metrics/virtual-motherboard/virtual-disk-used
- vsphere/storage/metrics/virtual-motherboard/provisioned-space
- vsphere/storage/metrics/virtual-motherboard/snapshot-space
source:
  document: PART 3 - Counters.docx
  path: Storage > VM > Capacity Metrics > All VM Files
corrections: []
review_notes: []
status: draft
```
