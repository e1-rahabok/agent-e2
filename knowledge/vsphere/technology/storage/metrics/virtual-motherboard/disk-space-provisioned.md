# VM Disk Space | Provisioned Space for VM (VCF Operations)

## Meaning
- Like Virtual Machine Used, but thin disks count at configured size, not actual use.
- Higher than Used when thin disks are not full.

## Use
- At datastore level: total space if every VM grows to full size. For overcommitted datastores.
- Not a capacity metric: it mixes allocation and utilization.

## Known issue
- Can report a much higher value: Broadcom KB 83990. Fixed in ESXi 7.0 U2c (7.0.2 P03), PR 2725886.

## Misconceptions
- "Provisioned = used" → thin disks count at full size.

## Metadata
```yaml
id: vsphere/technology/storage/metrics/virtual-motherboard/disk-space-provisioned
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
- vsphere/technology/storage/concepts/vm-files
same_name: []
same_meaning: []
related:
- vsphere/technology/storage/metrics/virtual-motherboard/disk-space-used
source:
  document: Knowledge base
  path: Storage > VM > Capacity Metrics > All VM Files
corrections: []
review_notes:
- 'To check: KB not read (https://kb.vmware.com/s/article/83990).'
status: draft
```
