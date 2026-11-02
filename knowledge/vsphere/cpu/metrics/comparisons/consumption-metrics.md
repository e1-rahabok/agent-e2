# CPU consumption metrics: VM and ESXi

## The choices
- VM: 5 consumption metrics: Run, Used, Usage, Usage (MHz), Demand.
- ESXi: 7 consumption metrics: Core Utilization, Utilization, Used, Usage, Usage (MHz), Consumed, Demand.

## Source of each
- ESXi provides Run (ms), Used (ms), Demand (MHz).
- vCenter adds Usage (MHz) and Usage (%).

## Reservation
- CPU reservation is on demand. It is not included in Run, Used, Demand or Usage.

## Metadata
```yaml
id: vsphere/cpu/metrics/comparisons/consumption-metrics
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
- HostSystem
metric_class: consumption
internal_derive:
- vsphere/foundations/metric-sources
- foundations/metric-volume
same_name: []
same_meaning: []
related:
- vsphere/cpu/metrics/virtual-machine/run
- vsphere/cpu/metrics/virtual-machine/used
- vsphere/cpu/metrics/virtual-machine/usage
- vsphere/cpu/metrics/host/usage
- vsphere/cpu/metrics/host/demand
- vsphere/cpu/metrics/host/core-utilization
- vsphere/cpu/concepts/run-time-vs-run-quality
- vsphere/cpu/concepts/cpu-measurement-levels
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Other Nuances
corrections: []
review_notes: []
status: draft
```
