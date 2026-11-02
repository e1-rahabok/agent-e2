# ESXi CPU Demand

## Meaning
- A provider metric.
- Not the sum of VM worlds plus VMkernel worlds.
- An internal metric of the CPU scheduler: the ideal total demand had there been no contention at all.

## Traps
- "Demand comes from consumers, so ESXi Demand is the sum of VM Demand" → wrong.

## Metadata
```yaml
id: vsphere/cpu/metrics/host/demand
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
same_meaning: []
related:
- vsphere/cpu/metrics/comparisons/consumption-metrics
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Virtualization Impact
corrections:
- '2026-11-02: ESXi CPU Demand is a provider metric (section: Meaning). Not answered in the uploaded document.'
review_notes: []
status: draft
```
