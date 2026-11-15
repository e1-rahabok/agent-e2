# VM Virtual Disk Outstanding IO

## Meaning
- IOs issued but not yet completed. They wait in a queue: a bottleneck signal.
- Available at virtual disk level. Not at datastore level.
- Little's Law ties it to the other two counters: outstanding IO = IOPS × latency, the same identity esxtop shows for each layer ([`vsphere/technology/storage/concepts/esxi-storage-io-path`](../../concepts/esxi-storage-io-path.md), section esxtop figures for a device).
- Relevance for operations: performance troubleshooting only, read with latency and IOPS. It rises with IOPS, so alone it is no alert.

## Formula
```text
Average Latency = Average Outstanding IO / Average IOPS
```

## Use
- Read it together with latency. A long queue is acceptable while latency stays low.
- Less useful alone: its value rises with IOPS, and the goal is maximum IOPS at minimum latency.
- Broadcom KB 326828 (legacy 2150017) gives outstanding IO per host for vSAN benchmarks, by test goal (maximum IOPS or throughput against minimum latency). It is guidance for a benchmark, not a reading of production VMs.

## Misconceptions
- "High Outstanding IO means a problem" → check latency.
- "Low Outstanding IO, so storage latency is fine" → outstanding IO is IOPS × latency; at low IOPS a long latency still gives a small count. Read the latency.

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
  document: Knowledge base
  path: Storage > VM > Performance Metrics > Contention Metrics > Virtual Disk
corrections: []
review_notes: []
status: draft
```
