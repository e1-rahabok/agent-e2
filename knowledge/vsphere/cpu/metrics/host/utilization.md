# ESXi CPU Utilization

## Meaning
- Static-frequency CPU utilization, from the host vantage point.
- The VM equivalent is called Run. See `vsphere/cpu/metrics/virtual-machine/run`.

## Why the names differ
- Different vantage points: provider (ESXi) and consumer (VM).

## Mechanism
- Utilization is measured per thread. Each thread has its own 100%.
- ESXi Utilization (%) = average of thread utilization.
- It is a static counter: it ignores frequency. So it suits capacity management.
- Ready and Wait do not apply at this level. A thread runs or is idle.
- See `vsphere/cpu/concepts/cpu-measurement-levels`.

## Thread Utilization
- Read Utilization (%) as Thread Utilization (%).
- Binary per moment per thread. Averaged over the sample: 50% = running half the time.
- Ignores frequency and Hyper-Threading. Relevant only with Hyper-Threading on.
- Disregards that Hyper-Threading does not deliver 2x. Example: both threads of every core busy = 100%; one thread per core = 50%.
- Usually lower than Core Utilization. Without Hyper-Threading, equal to it.
- See `vsphere/cpu/concepts/esxi-thread-core-accounting`.

## Traps
- "ESXi Utilization = sum of VM Run + kernel" → different vantage points. See `vsphere/cpu/concepts/cpu-measurement-levels`.
- "Thread Utilization 50%, so half the host is free" → every core can already be busy. Check Core Utilization.

## Metadata
```yaml
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
- vsphere/cpu/concepts/cpu-measurement-levels
same_name: []
same_meaning:
- vsphere/cpu/metrics/virtual-machine/run
related:
- vsphere/cpu/metrics/host/core-utilization
- vsphere/cpu/concepts/esxi-thread-core-accounting
- vsphere/cpu/metrics/host/imbalance
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity; CPU > Architecture (pp. 52-78) > ESXi ≠ VM + Kernel; CPU > ESXi > Thread Utilization
corrections: []
review_notes:
- Sections Mechanism and Traps: from CPU > Architecture.
- 'Section Thread Utilization: from CPU > ESXi.'
status: draft
```
