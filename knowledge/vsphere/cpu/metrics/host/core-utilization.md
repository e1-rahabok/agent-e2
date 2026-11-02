# ESXi CPU Core Utilization

## Meaning
- Reports 100% when one thread of the core runs.
- Also reports 100% when both threads run.
- To tell the two cases apart, check Thread Utilization.

## Why
- The core does the work, not the thread. A core running one thread is fully busy.
- Thread Utilization reports 200% for a core when both threads are busy (esxtop). Core Utilization stays at 100%.
- Core Utilization is a capacity metric: it ignores frequency.
- With All-Core Turbo at 20%, Usage (%) = 120% when Core Utilization = 100% (book table). See `vsphere/cpu/concepts/cpu-frequency`.

## Rollup
- ESXi Core Utilization = average of core values.
- vSphere Client lists threads (PCPUs) only when Hyper-Threading is on. Each thread shows the core value, duplicated.
- Usually higher than Thread Utilization. Without Hyper-Threading, equal to it.
- Core Utilization below 2 × Thread Utilization: some cores run 2 threads while others are idle.
- ESXi Usage (%) is based on Core Utilization, not Thread Utilization.

## Traps
- "Core Utilization 100% means both threads are busy" → it is 100% with one busy thread too.

## Metadata
```yaml
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
- vsphere/cpu/concepts/cpu-measurement-levels
same_name: []
same_meaning: []
related:
- vsphere/cpu/metrics/host/usage
- vsphere/cpu/concepts/cpu-frequency
- vsphere/cpu/concepts/esxi-thread-core-accounting
- vsphere/cpu/metrics/host/imbalance
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Other Nuances; CPU > Architecture (pp. 52-78) > ESXi ≠ VM + Kernel; Impacts on ESXi; CPU > ESXi > Thread Utilization
corrections: []
review_notes:
- Sections Why: from CPU > Architecture.
- 'Section Rollup: from CPU > ESXi.'
status: draft
```
