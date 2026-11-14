# VM CPU Swap Wait

## Meaning
- Time the vCPU waits for a memory page to come in from ESXi swap.
- Part of Wait. Contention for the guest: the guest experiences a freeze.

## Mechanism
- CPU is the fastest resource. It waits when data must come from memory, and the page is in ESXi swap.
- More host memory for the VM (less overcommit, a reservation) or a faster swap location lowers Swap Wait, so Run goes up.
- Include Swap Wait in Guest OS CPU sizing: it is runtime the guest demanded.
- Superseded by the Memory Contention metric.
- VCF Operations counts Swap Wait as part of memory contention, not CPU Contention.

## vs Memory Latency
- Memory Latency is a superset: it covers swap-in and decompression. Swap Wait covers swap-in only.

## Misconceptions
- "Swap Wait is a CPU problem" → its cause is memory. Check memory metrics.

## Metadata
```yaml
id: vsphere/technology/cpu/metrics/virtual-motherboard/swap-wait
retriever_guide: metric-meaning
scope: vsphere
technology:
- cpu
- memory
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
- vsphere/technology/cpu/metrics/virtual-motherboard/wait
same_name: []
same_meaning: []
related:
- vsphere/technology/cpu/metrics/virtual-motherboard/wait
- vsphere/technology/cpu/metrics/virtual-motherboard/other-wait
- vsphere/technology/cpu/metrics/comparisons/vm-contention-metrics
- vsphere/technology/memory/metrics/virtual-motherboard/latency
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: CPU > VM > Wait Metrics
corrections: []
review_notes:
- 'Section ''vs Memory Latency'': from Memory > VM > Latency.'
status: draft
```
