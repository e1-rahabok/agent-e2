# VM Disk Space (VCF Operations)

## Metric group
- VCF Operations computes four disk space metrics per VM from the file layout vCenter reports for the VM (`layoutEx`), in GB: Virtual Machine Used, Virtual Disk Used, Provisioned Space for VM, and Snapshot.
- The four differ in which files they count and whether a thin disk counts at its written or its configured size. The file types behind them: [`vsphere/technology/storage/concepts/vm-files`](../../concepts/vm-files.md).
- Order of size on a VM with thin disks: Virtual Disk Used is the smallest, Virtual Machine Used adds every other file, Provisioned Space for VM counts the thin disks at full size.

## Virtual Machine Used
- VM Disk Space | Virtual Machine Used: the actual consumed size of all VM files plus the configured size of RDMs. All files in the VM folder(s).
- Always larger than Virtual Disk Used: it includes snapshots, swap, logs and other files.
- Per-datastore variant: Disk Space | <Datastore Name> | Virtual Machine Used (GB). Only the VM's files on that datastore; the same value for a VM on one datastore.
- Relevance for operations: capacity: the space the VM takes on its datastores today, every file included. A value far above Virtual Disk Used points to snapshots, swap files or files left in the VM folder ([`vsphere/technology/storage/concepts/vm-files`](../../concepts/vm-files.md), section File categories).

```text
Virtual Machine Used = Sum over layoutEx.file of (uniqueSize if not null else size) / (1024 × 1024 × 1024)
```

## Virtual Disk Used
- VM Disk Space | Virtual Disk Used: the actual consumed size of the VMDK files. It excludes the other files, such as snapshots.
- RDM: counted at configured size (like a thick disk), unless the array thin-provisions the LUN.
- Not aware of vSAN overhead.
- Virtual Disk | Configured Size is the guest view. It excludes vSAN: it is taken from the consumer layer.
- Relevance for operations: capacity and reclamation: on a thin disk, Virtual Disk Used above the Guest OS used space is unmapped blocks to reclaim with unmap (trim) ([`sp5-framework/capacity/reclamation`](../../../../../sp5-framework/capacity/reclamation.md), section TRIM and unmap).

## Provisioned Space for VM
- VM Disk Space | Provisioned Space for VM: like Virtual Machine Used, but thin disks count at their configured size, not their actual use.
- Higher than Virtual Machine Used when thin disks are not full.
- At datastore level, the sum is the total space if every VM grows to full size: the reading for overcommitted datastores.
- Not a usage metric: it mixes allocation (thin disks at configured size) and utilization (every other file at its actual size).
- Relevance for operations: capacity risk, not capacity use: summed per datastore it is the space the VMs take once every thin disk fills. Provisioned ÷ capacity is the datastore's overcommit ratio, and provisioned − used the unwritten thin space ([`vsphere/technology/storage/datastore-space-headroom`](../../datastore-space-headroom.md), step 5).

## Snapshot
| Counter | Meaning |
|---|---|
| Disk Space \| Snapshot \| Virtual Machine Used (GB) | Space of all files created by snapshots (VMDK and non-VMDK). Reclaimable by removing the snapshot. |
| Disk Space \| Snapshot \| Access Time (ms) | Timestamp when the snapshot was taken. Needs formatting. |

- Use: find VMs with large snapshots quickly.
- Relevance for operations: capacity and reclamation: finds the VMs whose snapshots hold space that removing the snapshot frees ([`vsphere/technology/storage/datastore-space-headroom`](../../datastore-space-headroom.md), step 4). A snapshot also costs read IO and CPU ([`vsphere/technology/storage/concepts/snapshot-impact`](../../concepts/snapshot-impact.md)).

```text
Snapshot Virtual Machine Used = Sum of file sizes / (1024 × 1024 × 1024), for files whose layoutEx type is snapshotData, snapshotList or snapshotMemory
```

## Misconceptions
- "VM Used = sum of virtual disks" → Virtual Machine Used includes every file in the VM folder: snapshots, swap, logs.
- "Virtual Disk Used includes snapshots" → it excludes them; Snapshot | Virtual Machine Used holds them.
- "Provisioned = used" → Provisioned Space for VM counts thin disks at full size.
- "Provisioned Space above the datastore capacity means the datastore is full" → the part above used is unwritten thin space. Compare provisioned − used with the datastore's free space ([`vsphere/technology/storage/datastore-space-headroom`](../../datastore-space-headroom.md)).
- "Snapshot size ≤ VMDK size" → a snapshot of a nearly empty thin disk can grow larger.

## Metadata
```yaml
id: vsphere/technology/storage/metrics/virtual-motherboard/disk-space
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
- vsphere/technology/storage/metrics/virtual-motherboard/virtual-disk
- vsphere/technology/storage/datastore-space-headroom
source:
  document: Knowledge base
  path: Storage > VM > Capacity Metrics > All VM Files; All VM Files > Snapshot; Single VMDK
corrections: []
review_notes: []
status: draft
```
