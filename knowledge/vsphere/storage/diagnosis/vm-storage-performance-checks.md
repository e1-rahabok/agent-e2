# VM storage performance: what to check

## Checks, in order
1. Packet loss for IP storage, dropped frames for FC, aborted SCSI commands for block storage. Signs of contention on a shared datastore.
2. Bus Resets and Commands Aborted: both should be 0 all the time. Track them at higher-level objects with a super metric (max or sum). Expect a flat line.
3. Latency and outstanding IO.
4. Read latency and write latency separately.
5. Per virtual disk, not only the VM aggregate.
6. Backing device ratio: LUN IOPS / datastore IOPS. Above 1: array-side IO (replication, snapshots).

## How to read the result
- Latency with low IOPS: queues in one of the layers.
- Only read or only write affected: common. Look at that side only.

## Traps
- "Low IOPS, so latency cannot be a storage problem" → queues add latency at any load.

## Metadata
```yaml
id: vsphere/storage/diagnosis/vm-storage-performance-checks
retriever_guide: what-to-check
scope: vsphere
technology:
- storage
pillar:
- performance
product:
- vsphere
- vcf-operations
object:
- VirtualMachine
- Datastore
internal_derive:
- vsphere/storage/metrics/virtual-machine/disk-latency
- vsphere/storage/concepts/storage-layers
related:
- vsphere/storage/metrics/virtual-machine/iops
source:
  document: PART 3 - Counters.docx
  path: Storage > Architecture > VM Layer > Performance; Backing Device
corrections: []
review_notes: []
status: draft
```
