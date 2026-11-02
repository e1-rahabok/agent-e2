# VM Datastore (VM metrics at datastore level)

## Meaning
- The VM's IO at the datastore level. Covers VMFS and NFS, not RDM.
- Already aggregated at VM level: no per-virtual-disk breakdown.
- Includes snapshot IO: snapshots live at datastore level.

## Counters
- Latency: the only contention counter here. No outstanding IO.
- Highest Latency: useful for VMs on several datastores. Roll-up is Latest.
- VCF Operations read and write latency map to datastore.totalReadLatency.average and datastore.totalWriteLatency.average.
- IOPS map to datastore.numberReadAveraged.average and datastore.numberWriteAveraged.average.

## Behaviour
- Lower than disk and virtual-disk IOPS when most disks are RDM. Example: Oracle EBS VM with 26 virtual disks, mostly RDM.
- Higher read IOPS than virtual disk when a snapshot exists. See `vsphere/storage/concepts/snapshot-impact`.
- With all disks on one datastore backed by one LUN, virtual disk, disk and datastore metrics are nearly identical. Differences come from files outside virtual disks (snapshots, logs, swap).

## Traps
- "Datastore IOPS = VM total IOPS" → RDM IO is excluded.

## Metadata
```yaml
id: vsphere/storage/metrics/virtual-machine/datastore
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
metric_class: consumption
internal_derive: []
same_name: []
same_meaning: []
related:
- vsphere/storage/metrics/virtual-machine/disk
- vsphere/storage/metrics/virtual-machine/virtual-disk
- vsphere/storage/concepts/snapshot-impact
source:
  document: PART 3 - Counters.docx
  path: Storage > VM > Overview > Datastore; Mapping; Performance Metrics > Datastore
corrections: []
review_notes: []
status: draft
```
