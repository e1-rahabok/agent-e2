# ESXi Memory Usage

## Meaning
- Maps to Consumed: what the VMs have claimed. Related to capacity management.
- Memory is a cache, so values near 100% are expected.

## Formula (VCF Operations)
```text
Usage (%) = Consumed / Total Capacity
```

## Traps
- "Host Usage at 95% means the host is short of memory" → Usage is Consumed, not Active. Check contention metrics.

## Metadata
```yaml
id: vsphere/technology/memory/metrics/host/usage
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
- observability/resource-nature
same_name:
- vsphere/technology/memory/metrics/virtual-motherboard/usage
- vsphere/technology/memory/metrics/cluster/usage
same_meaning: []
related:
- vsphere/technology/memory/metrics/host/consumed
- vsphere/tools/vsphere-client/performance-guidance
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity; Memory > ESXi > Consumed
corrections: []
review_notes:
- 'Section ''Formula'': from Memory > ESXi.'
status: draft
```
