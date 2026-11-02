---
id: vsphere/cpu/metrics/host/usage
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
- vsphere/foundations/provider-consumer
same_name:
- vsphere/cpu/metrics/virtual-machine/usage
same_meaning: []
related:
- vsphere/cpu/metrics/host/core-utilization
- vsphere/cpu/metrics/comparisons/consumption-metrics
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity
corrections:
- '2026-11-02: Hyper-Threading values (section: Hyper-Threading) from the author.'
- '2026-11-02: ESXi CPU Usage is artificially capped at 100%: accounting decision error, documented in an official VMware KB (section: Cap). The uploaded document describes it as normal behaviour.'
review_notes:
- KB article number for the 100% cap not yet provided.
status: draft
---

# ESXi CPU Usage

## Hyper-Threading
- When both threads of a core run, ESXi sees the core as fully busy.

| ESXi metric (core level) | Value |
|---|---|
| Usage (%) | 100% |
| Usage (MHz) | Reflects the Hyper-Threading benefit |
| Core Utilization | 100% |
| Thread Utilization | 100% |

## Cap
- ESXi CPU Usage is artificially capped at 100%. Usage (MHz) does not exceed total capacity.
- Cause: an accounting decision error in ESXi. Known issue, documented in an official VMware KB.

## Same metric, two names
- vCenter shows the same ESXi CPU utilization as Consumed (%) and as Usage (%).

## Traps
- "ESXi CPU Usage = 100% means maximum possible work" → the value is capped, not measured beyond 100%.
