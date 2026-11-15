# ESXi Memory Latency

## Meaning
- A normalized average of the Memory Latency of the running VMs.
- An average hides the VM that suffers. Use the maximum VM Memory Contention across the host's VMs instead.
- VM Memory Latency is the share of time a vCPU waits for a page fault: swap-in and decompression, not the balloon ([`vsphere/technology/memory/metrics/virtual-motherboard/latency`](../virtual-motherboard/latency.md)).
- Relevance for operations: none for alerting or troubleshooting, because an average across VMs hides the VM that waits. Read the maximum VM Memory Contention of the host's VMs.

## Misconceptions
- "Host memory latency is low, so no VM waits" → check the worst VM.

## Metadata
```yaml
id: vsphere/technology/memory/metrics/host/latency
retriever_guide: metric-meaning
scope: vsphere
technology:
- memory
pillar:
- performance
product:
- vsphere
object:
- HostSystem
metric_class: contention
internal_derive:
- vsphere/architecture/provider-consumer
- sp5-framework/observability/aggregation
same_name:
- vsphere/technology/memory/metrics/virtual-motherboard/latency
same_meaning: []
related:
- vsphere/technology/memory/metrics/comparisons/host-memory-metrics
- vsphere/technology/memory/metrics/virtual-motherboard/latency
source:
  document: Knowledge base
  path: Memory > ESXi > Overview; Contention Metrics
corrections: []
review_notes: []
status: draft
```
