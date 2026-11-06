# VM Disk Space | Provisioned Space for VM (VCF Operations)

## Meaning
- Like Virtual Machine Used, but thin disks count at configured size, not actual use.
- Higher than Used when thin disks are not full.

## Use
- At datastore level: total space if every VM grows to full size. For overcommitted datastores.
- Not a capacity metric: it mixes allocation and utilization.

## Known issue
- Can report a much higher value: Broadcom KB 83990. Fixed in ESXi 7.0 U2c (7.0.2 P03), PR 2725886.

## Traps
- "Provisioned = used" → thin disks count at full size.

## Metadata
```yaml
id: vcf-operations/metrics/vm/disk-space-provisioned
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
- vcf-operations/metrics/vm/disk-space-used
source:
  document: PART 3 - Counters.docx
  path: Storage > VM > Capacity Metrics > All VM Files
corrections: []
review_notes:
- 'KB from the book: https://kb.vmware.com/s/article/83990 (not read).'
- 'Moved 2026-11-06 from vcf-operations/metrics/vm/disk-space-provisioned (architecture review 2026-11-06, section 5).'
status: draft
```
