# ESXi CPU Used

## Meaning by source
- ESXi (esxtop) shows Used in %.
- vCenter shows Used in ms.
- The % form is affected by CPU frequency and can exceed 100%.

## Why
- ESXi is the metric source. vCenter converts or adds metrics, and formulas do not match in every case. See `vsphere/architecture/metric-sources`.

## Notes
- CPU Used is buggy. Do not build conclusions on it alone.

## Mechanism
- Calculated from Non-Halted Core Cycles (NHCC), a hardware counter. Higher clock speed, more cycles: Used rises with Turbo.
- Per thread: when both threads of a core run, Used charges 10,000 ms to each, not 20,000 ms. Normalized back at host level.
- A thread running alone can reach 20,000 ms.
- See `vsphere/technology/cpu/concepts/hyper-threading`.

## Traps
- "Used above 100% is a data error" → the % form includes frequency effects and can exceed 100%.

## Metadata
```yaml
id: vsphere/technology/cpu/metrics/host/used
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
- vsphere/architecture/metric-sources
same_name:
- vsphere/technology/cpu/metrics/virtual-motherboard/used
same_meaning: []
related:
- vsphere/technology/cpu/metrics/comparisons/consumption-metrics
- vsphere/technology/cpu/concepts/hyper-threading
- vsphere/technology/cpu/metrics/host/usage
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Architecture Complexity; CPU > ESXi > Used | Usage; Core vs Thread
corrections:
- '2026-11-02: Author states the CPU Used metric is buggy (section: Notes).'
review_notes:
- 'Section Mechanism: from CPU > ESXi.'
status: draft
```
