# ESXi Memory Usage

## Meaning
- Maps to ESXi Memory Consumed: the pages the host holds for VMs, VM overhead, the kernel, vSAN and NSX ([`vsphere/technology/memory/metrics/host/consumed`](consumed.md)).
- Memory is a cache, so values near 100% are expected.
- Memory pressure shows in ballooning, compression, swapping and VM Memory Contention, not in Usage (%).
- Relevance for operations: capacity reporting. Not a shortage signal and not the capacity demand: VCF Operations plans on ESXi Memory Utilization ([`vsphere/technology/memory/metrics/host/utilization`](utilization.md), section Reason).

## Formula (VCF Operations)
```text
Usage (%) = Consumed / Total Capacity
```

## Misconceptions
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
- sp5-framework/observability/resource-nature
same_name:
- vsphere/technology/memory/metrics/virtual-motherboard/usage
- vsphere/technology/memory/metrics/cluster/usage
same_meaning: []
related:
- vsphere/technology/memory/metrics/host/consumed
- vsphere/tools/vsphere-client/performance-guidance
source:
  document: Knowledge base
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity; Memory > ESXi > Consumed
corrections: []
review_notes: []
status: draft
```
