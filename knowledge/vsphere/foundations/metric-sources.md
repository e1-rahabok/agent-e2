# Metric sources: ESXi vs vCenter

## Definition
- ESXi is the source of metrics.
- vCenter adds its own metrics on top.
- ESXi and vCenter formulas do not match 100% in all scenarios. Example: Used vs Usage.

## VM CPU metrics by source
| Source | VM CPU metrics |
|---|---|
| ESXi | Run (ms), Used (ms), Demand (MHz) |
| vCenter (added) | Usage (MHz), Usage (%) |

## Used: ESXi vs vCenter
- ESXi shows Used in %. vCenter shows Used in ms.
- ESXi Used (%) is affected by CPU frequency and can exceed 100%.

## Consequence
- When two tools disagree on a value, first check which source and which formula each tool uses.
- A metric file must state its data source (ESXi, vCenter, VCF Operations, Guest OS).

## Metadata
```yaml
id: vsphere/foundations/metric-sources
retriever_guide: how-it-works
scope: vsphere
technology:
- cpu
pillar:
- performance
product:
- vsphere
object:
- VirtualMachine
- HostSystem
internal_derive: []
related:
- vsphere/cpu/metrics/comparisons/consumption-metrics
- vsphere/foundations/provider-consumer
- vsphere/foundations/vcenter-statistics
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Architecture Complexity
corrections: []
review_notes: []
status: draft
```
