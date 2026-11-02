---
id: vsphere/cpu/metrics/host/utilization
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
- vsphere/foundations/provider-consumer
same_name: []
same_meaning:
- vsphere/cpu/metrics/virtual-machine/run
related: []
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity
corrections: []
review_notes: []
status: draft
---

# ESXi CPU Utilization

## Meaning
- Static-frequency CPU utilization, from the host vantage point.
- The VM equivalent is called Run. See `vsphere/cpu/metrics/virtual-machine/run`.

## Why the names differ
- Different vantage points: provider (ESXi) and consumer (VM).
