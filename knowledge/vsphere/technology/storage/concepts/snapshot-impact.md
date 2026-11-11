# Snapshot impact on metrics

## IO
- Reads must check all snapshot files. Datastore-level read IOPS rise; write is less affected (writes go to the newest file).
- The extra reads return no data: datastore throughput stays equal to virtual-disk throughput while datastore read IOPS is consistently higher.
- Test: with no snapshot, datastore and virtual-disk read IOPS overlap 100%. With a snapshot, datastore read IOPS is consistently higher.
- The .vmsd metadata file is updated on every snapshot create and delete.
![Datastore read IOPS rises when a snapshot exists](../images/datastore-read-iops-rise-with-vm-snapshot.png)

## Space
- A snapshot can exceed the size of its VMDK, especially for thin disks snapshotted early while nearly empty.
- Disk Space | Snapshot | Virtual Machine Used shows reclaimable space.

## CPU
- Snapshots are a cause of Co-stop (KB 2000058) and of Other Wait.
- System time rises: the kernel traverses the snapshot chain.

## Metric scope
- Virtual disk metrics exclude snapshot IO and space.
- Datastore metrics include them.

## Misconceptions
- "Datastore IOPS above virtual disk IOPS means another VM" → check for snapshots on this VM.

## Metadata
```yaml
id: vsphere/technology/storage/concepts/snapshot-impact
retriever_guide: how-it-works
scope: vsphere
technology:
- storage
pillar:
- performance
- capacity
product:
- vsphere
object:
- VirtualMachine
- Datastore
internal_derive: []
related:
- vsphere/technology/storage/concepts/vm-files
- vsphere/technology/storage/metrics/virtual-motherboard/datastore
- vsphere/technology/cpu/metrics/virtual-motherboard/co-stop
- vsphere/technology/cpu/metrics/virtual-motherboard/other-wait
- vsphere/technology/cpu/metrics/virtual-motherboard/system
images:
  - path: ../images/datastore-read-iops-rise-with-vm-snapshot.png
    product: [vsphere]
    object: [Datastore, VirtualMachine]
    metric: ['Datastore Read IOPS']
    topic: 'VM snapshot'
    image_type: timeline
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: Storage > VM > Performance Metrics > Consumption metrics > Datastore
corrections: []
review_notes:
- 'To check: best-practice blog cited by the book, not read (https://blogs.vmware.com/performance/2021/06/performance-best-practices-for-vmware-snapshots.html). Snapshot file docs linked by the book are vSphere 7.0.'
status: draft
```
