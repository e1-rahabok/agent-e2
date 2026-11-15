# VM Disk Space | Virtual Disk Used (VCF Operations)

## Meaning
- Actual consumed size of the VMDK files. Excludes other files, such as snapshots.
- RDM: counted at configured size (like a thick disk), unless the array thin-provisions the LUN.
- Not aware of vSAN overhead.
- Relevance for operations: capacity and reclamation: on a thin disk, Virtual Disk Used above the Guest OS used space is unmapped blocks to reclaim ([`sp5-framework/capacity/reclamation`](../../../../../sp5-framework/capacity/reclamation.md), section TRIM and unmap).

## Related
- Virtual Disk | Configured Size: the guest view. Excludes vSAN: taken from the consumer layer.

## Use
- Higher than Guest OS used on thin disks: run unmap (trim) to reclaim unmapped blocks.

## Misconceptions
- "Virtual Disk Used includes snapshots" → it excludes them.

## Metadata
```yaml
id: vsphere/technology/storage/metrics/virtual-motherboard/disk-space-virtual-disk-used
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
  document: Knowledge base
  path: Storage > VM > Capacity Metrics > Single VMDK
corrections: []
review_notes: []
status: draft
```
