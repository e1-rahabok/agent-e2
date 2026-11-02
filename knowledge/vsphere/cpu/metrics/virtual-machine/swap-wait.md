# VM CPU Swap Wait

## Meaning
- Time the vCPU waits for a memory page to come in from ESXi swap.
- Part of Wait. Contention for the guest: the guest experiences a freeze.

## Mechanism
- CPU is the fastest resource. It waits when data must come from memory, and the page is in ESXi swap.
- More RAM or faster RAM can lower Swap Wait, so Run goes up.
- Include Swap Wait in Guest OS CPU sizing: it is runtime the guest demanded.
- Superseded by the Memory Contention metric.
- VCF Operations counts Swap Wait as part of memory contention, not CPU Contention.

## vs Memory Latency
- Memory Latency is a superset: it covers swap-in and decompression. Swap Wait covers swap-in only.

## Traps
- "Swap Wait is a CPU problem" → its cause is memory. Check memory metrics.

## Metadata
```yaml
id: vsphere/cpu/metrics/virtual-machine/swap-wait
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
metric_class: contention
internal_derive:
- vsphere/cpu/metrics/virtual-machine/wait
same_name: []
same_meaning: []
related:
- vsphere/cpu/metrics/virtual-machine/wait
- vsphere/cpu/metrics/virtual-machine/other-wait
- vsphere/cpu/metrics/comparisons/vm-contention-metrics
- vsphere/memory/metrics/virtual-machine/latency
source:
  document: PART 3 - Counters.docx
  path: CPU > VM (pp. 78-118) > Wait Metrics
corrections: []
review_notes:
- 'Section ''vs Memory Latency'': from Memory > VM > Latency.'
status: draft
```
