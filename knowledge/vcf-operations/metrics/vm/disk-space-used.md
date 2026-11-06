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
id: vcf-operations/metrics/vm/disk-space-used
retriever_guide: metric-meaning
scope: vcf-operations
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
- vsphere/technology/storage/concepts/vm-files
same_name: []
same_meaning: []
related:
- vcf-operations/metrics/vm/disk-space-virtual-disk-used
- vcf-operations/metrics/vm/disk-space-provisioned
- vcf-operations/metrics/vm/disk-space-snapshot
source:
  document: PART 3 - Counters.docx
  path: Storage > VM > Capacity Metrics > All VM Files
corrections: []
review_notes:
- 'Moved 2026-11-06 from vcf-operations/metrics/vm/disk-space-used (architecture review 2026-11-06, section 5).'
status: draft
```
