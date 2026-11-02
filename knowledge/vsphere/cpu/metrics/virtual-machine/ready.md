---
id: vsphere/cpu/metrics/virtual-machine/ready
retriever_guide: metric-meaning
scope: vsphere
technology:
- cpu
pillar:
- performance
product:
- vsphere
object:
- VirtualMachine
metric_class: contention
internal_derive:
- vsphere/foundations/provider-consumer
- vsphere/foundations/resource-management
same_name: []
same_meaning: []
related:
- vsphere/cpu/metrics/virtual-machine/latency
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Other Nuances
corrections: []
review_notes: []
status: draft
---

# VM CPU Ready

## Meaning
- Ready applies to a consumer (the VM). A physical core or thread is always ready, so Ready does not apply to ESXi.

## Values above 100%
- VM CPU Ready can exceed 100%. Many VM-level values in esxtop exceed 100%.
- Cause: summation, not average.

## Effect of limits
- A CPU limit impacts CPU Ready.

## Traps
- "Host-level Ready is the host waiting for CPU" → Ready is a consumer metric. See `vsphere/foundations/provider-consumer`.
