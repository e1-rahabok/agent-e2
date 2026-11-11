# Cluster Consumption (%) (capacity model, vCommunity management pack for VCF Operations)

## Thresholds (book)
- Colour bands: `catalog/thresholds-capacity`, rows with this file as `kb`. They are shown with this file; this file holds the reasons.

## Meaning
- Saturation is not contention: no slowness yet. It is real consumption, tracked with dedicated metrics.

## Misconceptions
- "Saturation means VMs are slow" → check Cluster Performance (%).

## Metadata
```yaml
id: vsphere/object-types/cluster/models/cluster-consumption
retriever_guide: metric-meaning
scope: vsphere
technology:
- cpu
- memory
- system
pillar:
- capacity
product:
- vcf-operations
object:
- ClusterComputeResource
metric_class: consumption
internal_derive: []
same_name: []
same_meaning: []
related:
- vsphere/object-types/cluster/models/cluster-risk
- vsphere/object-types/cluster/kpis/cluster-performance
- sp5-framework/capacity/capacity-model
images:
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: Provider Objects > Other Metrics > Cluster Consumption (%)
corrections: []
review_notes: []
status: draft
```
