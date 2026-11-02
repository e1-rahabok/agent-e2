---
id: vsphere/cpu/metrics/virtual-machine/run
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
- VirtualMachine
metric_class: consumption
internal_derive:
- vsphere/foundations/provider-consumer
same_name: []
same_meaning:
- vsphere/cpu/metrics/host/utilization
related:
- vsphere/cpu/metrics/comparisons/consumption-metrics
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity
corrections: []
review_notes: []
status: draft
---

# VM CPU Run

## Meaning
- Static-frequency CPU utilization, from the VM vantage point.
- The ESXi equivalent is called Utilization. See `vsphere/cpu/metrics/host/utilization`.
- Source: ESXi provides Run in ms.

## Reservation
- CPU reservation is on demand. It is not included in Run.
