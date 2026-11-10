# Cluster SLA and SLI

## Cluster SLA
- Derived from VM SLAs: the percentage of VMs that fail their SLA.
- Pass or fail only; how badly or comfortably each VM fails or passes does not matter at cluster level.
- Not the average of VM SLA values: an average reacts too late unless the SLA is 100%.
- A 30-day, lagging indicator. Next step: identify failing VMs and a common cause.

## Cluster SLI
- An indicator, not in the SLA contract. Acts before the 30-day SLA.
- Each VM has 4 IaaS SLIs (CPU, memory, disk, network). A VM must pass all four.

| IaaS | VM counter |
|---|---|
| CPU | Ready |
| RAM | Contention |
| Disk | Latency |
| Network | TX dropped packets |

- SLI thresholds: `catalog/thresholds-performance`, rows `vm-sli-*`. They are shown with this file.

```text
Cluster SLI (%) = 100 - ( (Sum [VM] Performance|Number of KPIs Breached + Sum [Pod] Performance|Number of KPIs Breached)
                          / (Summary|Number of Running VMs + Summary|Number of Pods) × 100 / 4 )
```
- Normalized by actual breaches: 1 VM with 4 breaches scores the same as 4 VMs with 1 breach each.
- One threshold set for all classes of service.
- SLA, SLI and KPI differences: `sp5-framework/performance/kpi-vs-sla`. Implemented with VCF Operations super metrics and dashboards.

## Traps
- "Cluster SLA = average VM SLA" → it is the share of VMs failing.

## Metadata
```yaml
id: vsphere/object-types/cluster/kpis/cluster-sla-sli
retriever_guide: metric-meaning
scope: vsphere
technology:
- cpu
- memory
- storage
- network
- system
pillar:
- performance
- value
product:
- vcf-operations
- kubernetes
object:
- ClusterComputeResource
metric_class: contention
internal_derive: []
same_name: []
same_meaning: []
related:
- sp5-framework/concepts/sla-metrics
- vsphere/object-types/cluster/kpis/cluster-performance
- observability/thresholds
images: []
source:
  document: PART 3 - Counters.docx
  path: Provider Objects > Performance > Service Level Metrics
corrections: []
review_notes:
- 'To check: Section ''Cluster SLI'': ''A VM must pass all four'' vs the book''s VM SLI as the average of four pass/fail values (0-100% in steps of 25%), and the normalized formula below, which counts breaches. (Q095).'
status: draft
```
