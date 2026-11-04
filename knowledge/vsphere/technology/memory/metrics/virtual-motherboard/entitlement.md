# VM Memory Entitlement

## Formula
```text
Entitlement = Granted + Overhead
```

## Meaning
- ESXi memory the VM deserves, as determined by the ESXi scheduler.
- The book's assumption: it excludes memory above a limit, since the VM is not entitled beyond its limit.

## Traps
- "Entitlement is what the VM uses" → it is a scheduler value.

## Metadata
```yaml
id: vsphere/technology/memory/metrics/virtual-motherboard/entitlement
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
layer:
- virtual-motherboard
metric_class: context
internal_derive: []
same_name: []
same_meaning: []
related:
- vsphere/technology/memory/metrics/virtual-motherboard/granted
- vsphere/technology/memory/metrics/virtual-motherboard/overhead
source:
  document: PART 3 - Counters.docx
  path: Memory > VM > Consumption Metrics
corrections: []
review_notes:
- 'Section ''Meaning'': the limit behaviour is the book''s guess. Author to confirm.'
status: draft
```
