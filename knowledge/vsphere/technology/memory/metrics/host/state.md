# ESXi Memory State

## Meaning
- One of 5 states: High, Clear, Soft, Hard, Low. Each is a multiple of Free Memory Minimum.
- Soft: ballooning starts. Hard: compression and swapping start. Low: new VM memory allocations are blocked.
- Entering a state takes a lower free level than leaving it (hysteresis), so a short spike does not make the state flap.
- Aim for High, unless high utilization is the goal: in Clear, ESXi breaks large pages into 4 KB pages for page sharing.
- The free-memory level of each state: [`vsphere/technology/memory/concepts/host-memory-states`](../../concepts/host-memory-states.md), section States.
- Relevance for operations: alerting and capacity, as a leading warning: Soft and below mean ESXi reclaims memory from VMs. Not a measure of VM waits.

## Related counter
- Low Free Threshold (KB): the free-memory level below which ESXi reclaims from VMs.

## Misconceptions
- "State Soft means VMs are slow" → it means ballooning has started. Check contention.

## Metadata
```yaml
id: vsphere/technology/memory/metrics/host/state
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
metric_class: context
internal_derive:
- vsphere/technology/memory/concepts/host-memory-states
same_name: []
same_meaning: []
related:
- vsphere/technology/memory/metrics/comparisons/host-memory-metrics
- vsphere/technology/memory/metrics/host/ballooned
source:
  document: Knowledge base
  path: Memory > ESXi > Overview; Contention Metrics > Balloon
corrections: []
review_notes: []
status: draft
```
