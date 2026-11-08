# VM Disk Space | Snapshot (VCF Operations)

## Counters
| Counter | Meaning |
|---|---|
| Disk Space \| Snapshot \| Virtual Machine Used (GB) | Space of all files created by snapshots (VMDK and non-VMDK). Reclaimable by removing the snapshot. |
| Disk Space \| Snapshot \| Access Time (ms) | Timestamp when the snapshot was taken. Needs formatting. |

## Formula
```text
Sum of file sizes / (1024 × 1024 × 1024), for files whose layoutEx type is snapshotData, snapshotList or snapshotMemory
```

## Use
- Find VMs with large snapshots quickly.

## Traps
- "Snapshot size ≤ VMDK size" → a snapshot of a nearly empty thin disk can grow larger.

## Metadata
```yaml
id: vsphere/technology/storage/metrics/virtual-motherboard/disk-space-snapshot
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
- vsphere/technology/storage/concepts/snapshot-impact
- vsphere/technology/storage/metrics/virtual-motherboard/disk-space-used
source:
  document: PART 3 - Counters.docx
  path: Storage > VM > Capacity Metrics > All VM Files > Snapshot
corrections: []
review_notes:
- 'Moved 2026-11-06 from vsphere/technology/storage/metrics/virtual-motherboard/disk-space-snapshot (architecture review 2026-11-06, section 5).'
status: draft
```
