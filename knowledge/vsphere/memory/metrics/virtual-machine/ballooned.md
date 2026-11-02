# VM Memory Ballooned

## Meaning
- Past tense. A non-zero value does not mean ballooning is happening now.
- Ballooning may have happened days ago. The page stays ballooned while idle, because the Guest OS has not asked for it.
- Some ballooning is normal. See `vsphere/memory/diagnosis/overcommit-indicators`.

## Traps
- "Ballooned > 0, so the host is under memory pressure now" → not necessarily.

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
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Other Nuances
corrections: []
review_notes:
- metric_class set to contention. Author to confirm.
status: draft
```
