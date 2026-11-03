# VM Virtual Disk Outstanding IO

## Meaning
- IOs issued but not yet completed. They wait in a queue: a bottleneck signal.
- Available at virtual disk level. Not at datastore level.

## Formula
```text
Average Latency = Average Outstanding IO / Average IOPS
```

## Use
- Read it together with latency. A long queue is acceptable while latency stays low.
- Less useful alone: its value rises with IOPS, and the goal is maximum IOPS at minimum latency.
- vSAN guidance on expected values: Broadcom KB 2150017.

## Traps
- "High Outstanding IO means a problem" → check latency.

## Metadata
```yaml
id: vsphere/storage/metrics/virtual-motherboard/outstanding-io
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
- vsphere/storage/metrics/virtual-motherboard/disk-latency
- vsphere/storage/metrics/virtual-motherboard/iops
source:
  document: PART 3 - Counters.docx
  path: Storage > VM > Performance Metrics > Contention Metrics > Virtual Disk
corrections: []
review_notes:
- 'KB from the book: https://kb.vmware.com/s/article/2150017 (not read).'
status: draft
```
