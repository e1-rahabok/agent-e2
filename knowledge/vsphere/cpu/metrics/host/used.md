---
id: vsphere/cpu/metrics/host/used
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
- vsphere/foundations/metric-sources
same_name:
- vsphere/cpu/metrics/virtual-machine/used
same_meaning: []
related:
- vsphere/cpu/metrics/comparisons/consumption-metrics
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Architecture Complexity
corrections:
- '2026-11-02: Author states the CPU Used metric is buggy (section: Notes).'
review_notes: []
status: draft
---

# ESXi CPU Used

## Meaning by source
- ESXi (esxtop) shows Used in %.
- vCenter shows Used in ms.
- The % form is affected by CPU frequency and can exceed 100%.

## Why
- ESXi is the metric source. vCenter converts or adds metrics, and formulas do not match in every case. See `vsphere/foundations/metric-sources`.

## Notes
- The author states CPU Used is buggy. Do not build conclusions on it alone.

## Traps
- "Used above 100% is a data error" → the % form includes frequency effects and can exceed 100%.
