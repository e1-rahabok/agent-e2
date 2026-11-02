---
id: vsphere/cpu/metrics/host/core-utilization
retriever_guide: metric-meaning
scope: vsphere
technology:
- cpu
pillar:
- performance
- capacity
product:
- vsphere
object:
- HostSystem
metric_class: consumption
internal_derive:
- vsphere/cpu/concepts/hyper-threading
same_name: []
same_meaning: []
related:
- vsphere/cpu/metrics/host/usage
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Other Nuances
corrections: []
review_notes: []
status: draft
---

# ESXi CPU Core Utilization

## Meaning
- Reports 100% when one thread of the core runs.
- Also reports 100% when both threads run.
- To tell the two cases apart, check Thread Utilization.

## Traps
- "Core Utilization 100% means both threads are busy" → it is 100% with one busy thread too.
