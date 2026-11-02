# VM Disk IOPS

## Under-reporting
- IO queued inside the Guest OS has not reached the hypervisor. VM-level IOPS does not include it. See `vsphere/foundations/visibility-layers`, area A.

## Limits
- A disk IOPS limit exists.
- A disk throughput limit does not exist. Throughput depends on block size, which varies, so a throughput limit is not practical.

## Metadata
```yaml
id: vsphere/storage/metrics/virtual-machine/iops
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
internal_derive:
- vsphere/foundations/visibility-layers
- foundations/resource-nature
same_name: []
same_meaning: []
related:
- vsphere/storage/metrics/virtual-machine/disk-latency
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Architecture Complexity
corrections: []
review_notes: []
status: draft
```
