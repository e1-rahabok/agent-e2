# VM Memory Overhead

## Meaning
- ESXi memory for virtualization data structures of the VM: metadata and index information, such as shadow page tables.
- vCenter counters: Overhead reserved, Overhead consumed, Overhead active.
- Rises with more vCPUs and more configured memory.
- Operationally negligible.
- Not visible to the Guest OS. Excluded from Consumed and from configured memory.
- Under a limit, Consumed sits just below the limit plus overhead (example: 2 GB limit shows as 2.12 GB).

## Traps
- "Overhead explains a large memory gap" → it is negligible.

## Metadata
```yaml
id: vsphere/memory/metrics/virtual-machine/overhead
retriever_guide: metric-meaning
scope: vsphere
technology:
- memory
pillar:
- capacity
product:
- vsphere
object:
- VirtualMachine
metric_class: context
internal_derive:
- vsphere/memory/concepts/memory-overhead
same_name: []
same_meaning: []
related:
- vsphere/memory/metrics/virtual-machine/entitlement
- vsphere/memory/metrics/virtual-machine/consumed
source:
  document: PART 3 - Counters.docx
  path: Memory > VM > Consumption Metrics; Limit
corrections: []
review_notes: []
status: draft
```
