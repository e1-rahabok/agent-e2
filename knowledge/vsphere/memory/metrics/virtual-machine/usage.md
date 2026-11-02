# VM Memory Usage

## Meaning
- Maps to Active: what the VM is physically using. Related to performance.
- VCF Operations uses Guest OS data for VM memory Usage. It falls back to Active when Guest OS data is not available.

## Why it differs from ESXi and cluster Usage
- Two-level memory hierarchy in virtualization.
- ESXi and cluster Usage map to Consumed, which is related to capacity.

## Traps
- Comparing VM Usage with ESXi Usage as if they measure the same thing. This confusion has led customers to buy more RAM than required.

## Metadata
```yaml
id: vsphere/memory/metrics/virtual-machine/usage
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
metric_class: consumption
internal_derive:
- foundations/resource-nature
same_name:
- vsphere/memory/metrics/host/usage
- vsphere/memory/metrics/cluster/usage
same_meaning: []
related:
- vsphere/memory/metrics/virtual-machine/consumed
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity
corrections: []
review_notes: []
status: draft
```
