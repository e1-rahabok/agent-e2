# ESXi Memory Latency

## Meaning
- A normalized average of the Memory Latency of the running VMs.
- An average hides the VM that suffers. Use the maximum VM Memory Contention across the host's VMs instead.

## Traps
- "Host memory latency is low, so no VM waits" → check the worst VM.

## Metadata
```yaml
id: vsphere/memory/metrics/host/latency
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
internal_derive: []
same_name:
- vsphere/memory/metrics/virtual-machine/latency
same_meaning: []
related:
- vsphere/memory/metrics/virtual-machine/latency
source:
  document: PART 3 - Counters.docx
  path: Memory > ESXi > Overview; Contention Metrics
corrections: []
review_notes: []
status: draft
```
