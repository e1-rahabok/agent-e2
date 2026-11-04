# Storage: speed and space

## Two dimensions
| Dimension | Consumption counters | Notes |
|---|---|---|
| Speed | IOPS, throughput | Throughput = IOPS × block size. |
| Space | Disk space (bytes) | Capacity. |

- Both dimensions have consumption metrics, but they are unrelated.

## Speed: contention at 3 stages of IO
| Stage | Contention signal |
|---|---|
| Pre-processing | Each layer has its own queue: outstanding IO. |
| Processing | Aborted SCSI commands, dropped frames, packet loss. |
| Post-processing | Latency. |

- Performance is measured as contention and utilization.

## Space
- On SSD-based storage, space used does not change speed. 1% full is not faster than 99% full: no platter, no defragmentation effect.
- Space affects availability: at 100% full, storage stops processing IO and applications crash.
- Reality overwrites projection. In compute, capacity remaining is projected from the past. In storage, 0 bytes left overrides any projection.
- Focus on reclamation: the reclaimable amount tends to be large.

## Traps
- "A 95% full datastore is slow" → space does not affect speed on SSD. It threatens availability.
- "IOPS and space are the same capacity" → separate dimensions.

## Metadata
```yaml
id: vsphere/storage/concepts/storage-dimensions
retriever_guide: how-it-works
scope: vsphere
technology:
- storage
pillar:
- performance
- capacity
- availability
product:
- vsphere
object:
- VirtualMachine
- HostSystem
- Datastore
internal_derive: []
related:
- vsphere/storage/concepts/storage-layers
- vsphere/storage/metrics/virtual-motherboard/disk-latency
- vsphere/storage/metrics/virtual-motherboard/iops
source:
  document: PART 3 - Counters.docx
  path: Storage > Architecture > Architecture intro
corrections: []
review_notes: []
status: draft
```
