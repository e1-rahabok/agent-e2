# VM Disk Space | Provisioned Space for VM (VCF Operations)

## Meaning
- Like Virtual Machine Used ([`vsphere/technology/storage/metrics/virtual-motherboard/disk-space-used`](disk-space-used.md)), but thin disks count at configured size, not actual use.
- Higher than Used when thin disks are not full.
- Relevance for operations: capacity risk, not capacity use: summed per datastore it is the space the VMs claim once every thin disk fills. Provisioned ÷ capacity is the datastore's overcommit ratio, and provisioned − used the unwritten thin space ([`vsphere/technology/storage/datastore-space-headroom`](../../datastore-space-headroom.md), step 5).

## Use
- At datastore level: total space if every VM grows to full size. For overcommitted datastores.
- Not a usage metric: it mixes allocation (thin disks at configured size) and utilization (every other file at its actual size).

## Misconceptions
- "Provisioned = used" → thin disks count at full size.
- "Provisioned Space above the datastore capacity means the datastore is full" → the part above used is unwritten thin space. Compare provisioned − used with the datastore's free space ([`vsphere/technology/storage/datastore-space-headroom`](../../datastore-space-headroom.md)).

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
review_notes: []
status: draft
```
