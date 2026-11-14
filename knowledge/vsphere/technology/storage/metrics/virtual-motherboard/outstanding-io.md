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

## Misconceptions
- "High Outstanding IO means a problem" → check latency.

## Metadata
```yaml
id: vsphere/technology/storage/metrics/virtual-motherboard/outstanding-io
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
internal_derive:
- vsphere/technology/storage/concepts/esxi-storage-io-path
- vsphere/technology/storage/concepts/esxi-storage-latency-stack
same_name: []
same_meaning: []
related:
- vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
- vsphere/technology/storage/metrics/virtual-motherboard/iops
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: Storage > VM > Performance Metrics > Contention Metrics > Virtual Disk
corrections: []
review_notes:
- 'To check: KB cited by the source document, not read (https://kb.vmware.com/s/article/2150017).'
status: draft
```
