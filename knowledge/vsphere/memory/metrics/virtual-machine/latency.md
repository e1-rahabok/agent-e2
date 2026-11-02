# VM Memory Latency

## Meaning
- Indicates a performance problem. A primary counter for how well the VM is served.
- Contrast: CPU Latency does not always indicate a performance problem. See `vsphere/cpu/metrics/virtual-machine/latency`.

## Unit
- Percentage of memory space that takes longer than expected to read. Not latency in nanoseconds.
- The only ESXi counter for memory speed.
- Disk is the opposite: disk latency is time, not share of space.

## Traps
- "Memory Latency 5% means 5 ns" → it is the share of memory space reading slower than expected.

## Metadata
```yaml
id: vsphere/memory/metrics/virtual-machine/latency
retriever_guide: metric-meaning
scope: vsphere
technology:
- memory
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
- vsphere/storage/metrics/virtual-machine/disk-latency
same_meaning: []
related:
- vsphere/memory/concepts/memory-as-storage
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity; Memory > Architecture
corrections: []
review_notes:
- 'Section ''Unit'': from Memory > Architecture.'
status: draft
```
