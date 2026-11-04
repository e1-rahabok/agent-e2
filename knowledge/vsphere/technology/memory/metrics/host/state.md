# ESXi Memory State

## Meaning
- One of 5 states: High, Clear, Soft, Hard, Low. Each is a multiple of Free Memory Minimum.
- Soft: ballooning starts. Hard: compression and swapping start. Low: execution is blocked.
- Keep hosts in High or Clear.
- See `vsphere/technology/memory/concepts/host-memory-states`.

## Related counter
- Low Free Threshold (KB): the free-memory level below which ESXi reclaims from VMs.

## Traps
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
- vsphere/technology/memory/metrics/host/ballooned
source:
  document: PART 3 - Counters.docx
  path: Memory > ESXi > Overview; Contention Metrics > Balloon
corrections: []
review_notes: []
status: draft
```
