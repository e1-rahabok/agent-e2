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
- vsphere/cpu/concepts/cpu-measurement-levels
same_name: []
same_meaning: []
related:
- vsphere/cpu/metrics/host/usage
- vsphere/cpu/concepts/cpu-frequency
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Other Nuances; CPU > Architecture (pp. 52-78) > ESXi ≠ VM + Kernel; Impacts on ESXi
corrections: []
review_notes:
- Sections Why: from CPU > Architecture in the pre-correction book file (uploaded 2026-11-02). Re-check when the corrected file is uploaded.
status: draft
---

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

## Traps
- "Core Utilization 100% means both threads are busy" → it is 100% with one busy thread too.
