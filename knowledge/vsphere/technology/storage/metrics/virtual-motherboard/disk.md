# VM Disk (device level)

## Meaning
- The VM's IO at the device (LUN or RDM) level. The book would name it Physical Disk or Device: "disk" sounds like a superset of virtual disk.
- Covers VMFS and RDM, not NFS.
- The value is this VM's IO only, not the whole device or datastore that other VMs share. It is not split per virtual disk: different layers.
- With a 1:1 datastore-to-LUN mapping and no extents, values match the datastore level.

## Counters
- Highest Latency: peak among disks. Roll-up is Latest: the single value at the end of the collection period.
- Error counters: Bus Resets and Commands Aborted. The book has always seen 0.
- IOPS: two forms, the total commands in the period and the per-second average. Basically the same.
- Throughput: read and write.
- No block size counter. The maximum block size in the period would help.

## Traps
- "Highest Latency is an average" → it is the latest value.

## Metadata
```yaml
id: vsphere/technology/storage/metrics/virtual-motherboard/disk
retriever_guide: metric-meaning
scope: vsphere
technology:
- storage
pillar:
- performance
product:
- vsphere
object:
- VirtualMachine
layer:
- virtual-motherboard
metric_class: contention
internal_derive: []
same_name: []
same_meaning: []
related:
- vsphere/technology/storage/metrics/virtual-motherboard/virtual-disk
- vsphere/technology/storage/metrics/virtual-motherboard/datastore
- vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
- vsphere/technology/storage/troubleshooting/vm-storage-performance-checks
source:
  document: PART 3 - Counters.docx
  path: Storage > VM > Overview > Disk; Performance Metrics > Disk
corrections: []
review_notes: []
status: draft
```
