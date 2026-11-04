# VM Disk Space | Virtual Disk Used (VCF Operations)

## Meaning
- Actual consumed size of the VMDK files. Excludes other files, such as snapshots.
- RDM: counted at configured size (like a thick disk), unless the array thin-provisions the LUN.
- Not aware of vSAN overhead.

## Related
- Virtual Disk | Configured Size: the guest view. Excludes vSAN: taken from the consumer layer.

## Use
- Higher than Guest OS used on thin disks: run unmap (trim) to reclaim unmapped blocks.

## Traps
- "Virtual Disk Used includes snapshots" → it excludes them.

## Metadata
```yaml
id: vsphere/technology/storage/metrics/virtual-motherboard/virtual-disk-used
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
- vsphere/technology/storage/metrics/virtual-motherboard/virtual-disk
source:
  document: PART 3 - Counters.docx
  path: Storage > VM > Capacity Metrics > Single VMDK
corrections: []
review_notes: []
status: draft
```
