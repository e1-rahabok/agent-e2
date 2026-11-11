# VM Memory Overhead

## Meaning
- ESXi memory for virtualization data structures of the VM: metadata and index information, such as shadow page tables.
- vCenter counters: Overhead reserved, Overhead consumed, Overhead active.
- Rises with more vCPUs and more configured memory.
- Operationally negligible.
- Not visible to the Guest OS. Excluded from Consumed and from configured memory.
- Under a limit, Consumed sits just below the limit plus overhead (example: 2 GB limit shows as 2.12 GB).

## Misconceptions
- "Overhead explains a large memory gap" → it is negligible.

## Metadata
```yaml
id: vsphere/technology/memory/metrics/virtual-motherboard/overhead
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
layer:
- virtual-motherboard
metric_class: context
internal_derive:
- vsphere/technology/memory/concepts/memory-overhead
same_name: []
same_meaning: []
related:
- vsphere/technology/memory/metrics/virtual-motherboard/entitlement
- vsphere/technology/memory/metrics/virtual-motherboard/consumed
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: Memory > VM > Consumption Metrics; Limit
corrections: []
review_notes: []
status: draft
```
