# VM Memory Ballooned

## Meaning
- Past tense. A non-zero value does not mean ballooning is happening now.
- Ballooning may have happened days ago. The page stays ballooned while idle, because the Guest OS has not asked for it.
- Some ballooning is normal. See `vsphere/memory/diagnosis/overcommit-indicators`.

## Mechanism
- Proactive: starts before ESXi fails to meet demand.
- Reduces guest cache.
- Ballooned pages exist only in the VM view. They map to no ESXi page.
- Not unmet demand. Demand is unmet only when Contention occurs.

## Traps
- "Ballooned > 0, so the host is under memory pressure now" → not necessarily.
- "Ballooning means VMs are contending for RAM" → check Contention.

## Metadata
```yaml
id: vsphere/memory/metrics/virtual-machine/ballooned
retriever_guide: metric-meaning
scope: vsphere
technology:
- memory
pillar:
- performance
- capacity
product:
- vsphere
object:
- VirtualMachine
metric_class: contention
internal_derive:
- vsphere/memory/concepts/overcommit-techniques
same_name: []
same_meaning: []
related:
- vsphere/memory/diagnosis/overcommit-indicators
- vsphere/memory/concepts/memory-layers
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Other Nuances; Memory > Architecture > Virtual Memory; Relationship
corrections: []
review_notes:
- metric_class set to contention. Author to confirm.
- 'Section ''Mechanism'': from Memory > Architecture.'
status: draft
```
