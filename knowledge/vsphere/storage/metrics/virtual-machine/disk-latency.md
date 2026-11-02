# VM Disk Latency

## Meaning
- Indicates a performance problem. A primary counter for how well the VM is served.
- Contrast: CPU Latency does not always indicate a performance problem. See `vsphere/cpu/metrics/virtual-machine/latency`.
- Threshold setting by layer: see `foundations/thresholds`.

## Metadata
```yaml
id: vsphere/storage/metrics/virtual-machine/disk-latency
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
metric_class: contention
internal_derive:
- vsphere/foundations/visibility-layers
same_name:
- vsphere/cpu/metrics/virtual-machine/latency
- vsphere/memory/metrics/virtual-machine/latency
same_meaning: []
related:
- vsphere/storage/metrics/virtual-machine/iops
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity
corrections: []
review_notes: []
status: draft
```
