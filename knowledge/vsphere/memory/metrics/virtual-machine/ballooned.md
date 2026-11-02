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

## Behaviour
- Ballooned pages are removed from Granted: not functionally used.
- Guest OS memory counters still include them. Exclude them when working out Guest OS utilization.
- A flat Ballooned value for weeks: the guest never requested those pages again.
- Example: 8 GB CentOS VM running MySQL with a 2 GB limit was heavily ballooned. The book notes a default maximum of around 63%.
- See `vsphere/memory/concepts/ballooning`.

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
- vsphere/memory/concepts/ballooning
- vsphere/memory/metrics/virtual-machine/balloon-target
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Other Nuances; Memory > Architecture > Virtual Memory; Relationship; Memory > VM > Contention Metrics > Balloon; Consumption Metrics > Ballooned
corrections: []
review_notes:
- metric_class set to contention. Author to confirm.
- 'Section ''Mechanism'': from Memory > Architecture.'
- 'Sections Behaviour: from Memory > VM.'
- 'Section ''Behaviour'': the book says a limit does not cause ballooning (Limit section), but its examples show ballooning under a limit. Open question in docs/todo.md.'
- 'Section ''Behaviour'': the balloon maximum is the Mem.CtlMaxPercent setting, default 65% (Claude''s own knowledge). The book states around 63%.'
status: draft
```
