# VM Memory Overhead

## Meaning
- ESXi memory for virtualization data structures of the VM: metadata and index information, such as nested (EPT or RVI) page-table mappings and the frame buffer.
- vCenter counters: Overhead reserved, Overhead consumed, Overhead active.
- Rises with more vCPUs and more configured memory.
- Operationally negligible.
- Not visible to the Guest OS. Excluded from Consumed and from configured memory.
- A VM memory limit does not cap Overhead: ESXi bounds Overhead with a separate overhead limit, which DRS sets ([`vsphere/technology/memory/concepts/memory-overhead`](../../concepts/memory-overhead.md)).
- Under a VM limit, VCF Operations Memory|Effective limit reads the configured limit plus Overhead ([`vsphere/technology/memory/concepts/memory-limit`](../../concepts/memory-limit.md), section Signs in the counters).

## Misconceptions
- "Overhead explains a large memory gap" → it is negligible.
- "A VM memory limit covers the VM overhead" → the limit caps Consumed only; Overhead sits on top of it, under its own overhead limit.

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
- vsphere/technology/memory/metrics/comparisons/vm-memory-metrics
- vsphere/technology/memory/metrics/virtual-motherboard/entitlement
- vsphere/technology/memory/metrics/virtual-motherboard/consumed
- vsphere/technology/memory/concepts/memory-limit
source:
  document: Knowledge base; vSphere 9.1 documentation (PDF built 2026-11-02)
  path: Memory > VM > Consumption Metrics; Limit; Resource Management, Virtual Machine Memory (pp. 1833-1834), DRS Overhead Memory Management for VMs (p. 1902)
corrections: []
review_notes: []
status: draft
```
