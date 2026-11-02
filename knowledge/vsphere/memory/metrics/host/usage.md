---
id: vsphere/memory/metrics/host/usage
retriever_guide: metric-meaning
scope: vsphere
technology:
- memory
pillar:
- capacity
product:
- vsphere
object:
- HostSystem
metric_class: consumption
internal_derive:
- foundations/resource-nature
same_name:
- vsphere/memory/metrics/virtual-machine/usage
- vsphere/memory/metrics/cluster/usage
same_meaning: []
related:
- vsphere/memory/metrics/host/consumed
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity
corrections: []
review_notes: []
status: draft
---

# ESXi Memory Usage

## Meaning
- Maps to Consumed: what the VMs have claimed. Related to capacity management.
- Memory is a cache, so values near 100% are expected.

## Traps
- "Host Usage at 95% means the host is short of memory" → Usage is Consumed, not Active. Check contention metrics.
