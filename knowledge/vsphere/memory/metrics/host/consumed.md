# ESXi Memory Consumed

## Meaning
- Includes memory consumed by ESXi itself.

## Scope
- ESXi pages, summed at host level: VMs plus the kernel's own memory plus VM overhead.
- Physical memory is shared by VMs and the hypervisor. Manage them as one.
- Very high Consumed triggers compression and swapping proactively. That alone does not mean VMs contend for RAM.

## Traps
- Summing VM Consumed and expecting ESXi Consumed.

## Metadata
```yaml
id: vsphere/memory/metrics/host/consumed
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
- vsphere/foundations/provider-consumer
same_name:
- vsphere/memory/metrics/cluster/consumed
- vsphere/memory/metrics/virtual-machine/consumed
same_meaning: []
related:
- vsphere/memory/concepts/memory-layers
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity; Memory > Architecture > Virtual Memory; Relationship
corrections: []
review_notes:
- 'Section ''Scope'': from Memory > Architecture.'
status: draft
```
