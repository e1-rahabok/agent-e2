# Cluster Memory Usage

## Meaning
- Maps to Consumed (VM overhead included): the share of the cluster's physical memory consumed (vSphere Web Services API 9.1, `mem.usage`), the reading of [`vsphere/technology/memory/metrics/cluster/consumed`](consumed.md) as a percentage.
- Memory is a cache, so values near 100% are expected.
- Relevance for operations: capacity reporting. Not a shortage signal: pressure shows in ballooning, compression, swapping and VM Memory Contention.

## Misconceptions
- "Cluster Memory Usage (%) and VM Memory Usage (%) measure the same thing" → cluster Usage is Consumed; VM Usage is Active in vCenter and Guest OS Needed Memory in VCF Operations ([`vsphere/technology/memory/metrics/virtual-motherboard/usage`](../virtual-motherboard/usage.md)).

## Metadata
```yaml
id: vsphere/technology/memory/metrics/cluster/usage
retriever_guide: metric-meaning
scope: vsphere
technology:
- memory
pillar:
- capacity
product:
- vsphere
object:
- ClusterComputeResource
metric_class: consumption
internal_derive:
- sp5-framework/observability/resource-nature
same_name:
- vsphere/technology/memory/metrics/virtual-motherboard/usage
- vsphere/technology/memory/metrics/host/usage
same_meaning: []
related:
- vsphere/technology/memory/metrics/cluster/consumed
source:
  document: Knowledge base; vSphere Web Services API 9.1
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity; API 9.1 memory counters, usage (https://developer.broadcom.com/xapis/vsphere-web-services-api/9.1/memory_counters.html)
corrections: []
review_notes: []
status: draft
```
