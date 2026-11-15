# Cluster Memory Consumed

## Meaning
- Includes only memory consumed by VMs.
- Includes VM overhead.
- Excludes memory consumed by ESXi itself.
- Relevance for operations: capacity reporting of the VMs' footprint in the cluster's physical memory. Not the capacity demand (VCF Operations plans on ESXi Memory Utilization, [`vsphere/technology/memory/metrics/host/utilization`](../host/utilization.md)) and not a performance counter.

## Misconceptions
- "Cluster Consumed near the cluster's total memory means the cluster is out of memory" → Consumed holds every page the VMs touched, mostly guest cache and inactive pages. Check host Ballooned and VM Memory Contention, and plan capacity on ESXi Memory Utilization.

## Metadata
```yaml
id: vsphere/technology/memory/metrics/cluster/consumed
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
- vsphere/architecture/provider-consumer
same_name:
- vsphere/technology/memory/metrics/host/consumed
- vsphere/technology/memory/metrics/virtual-motherboard/consumed
same_meaning: []
related: []
source:
  document: Knowledge base; vSphere 9.1 documentation (PDF built 2026-11-02)
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity; Monitoring and Performance, Clusters, Memory (MB) (pp. 2027, 2036-2038, 2040, 2043)
corrections: []
review_notes:
- 'To check: Section ''Meaning'': vSphere 9.1 documentation disagrees with itself. The cluster memory chart text (pp. 2027, 2037, 2043) says VM consumed plus VM overhead, without the VMkernel; the cluster Memory (MB) counter tables (pp. 2038, 2040) say it includes VMkernel memory and equals total minus free host memory. knowledge/catalog/vcenter-counters.yaml holds rows of both. Check on a live 9.1 cluster: cluster Consumed against the sum of host Consumed and against the sum of VM Consumed plus overhead.'
status: draft
```
