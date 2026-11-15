# Configuration dashboards (VCF Operations)

## The configuration dashboard set
- VM Configuration and VM Storage Configuration work together. The second was split out because one dashboard was too large to use.
- ESXi Configuration and vSphere Cluster Configuration work together. The cluster one carries the vSphere prefix because cluster is a generic English word. A drill-down from cluster to ESXi would help but adds UI complexity.
- vSphere Resource Management is separate: its settings span VMs, resource pools and clusters, and their flexibility and complexity need their own dashboard.
- vSphere Network Configuration and vSAN Configuration are basic and due for enhancement.
- How to design configuration dashboards (goals, users, frequency, what needs attention first): [`sp5-framework/outputs/inventory-and-configuration-dashboards`](../../sp5-framework/outputs/inventory-and-configuration-dashboards.md).

## Misconceptions
- "Resource settings fit in the VM dashboard" → shares, reservations and limits span VMs, resource pools and clusters; they need their own dashboard, vSphere Resource Management.

## Metadata
```yaml
id: vcf-operations/dashboards/configuration-dashboards
retriever_guide: how-it-works
scope: vcf-operations
technology:
- system
pillar:
- performance
- availability
- security
product:
- vcf-operations
- vsphere
- vsan
object:
- VirtualMachine
- HostSystem
- ClusterComputeResource
- ResourcePool
internal_derive:
- sp5-framework/outputs/inventory-and-configuration-dashboards
related:
- vsphere/object-types/vm/configuration/vm-configuration-review
- vsphere/object-types/esxi/configuration/esxi-configuration-review
- vsphere/object-types/cluster/configuration/cluster-configuration-review
- vsphere/object-types/vm/configuration/resource-settings-guidance
source:
  document: Knowledge base
  path: 'Overall Design Approach > Overall Design: Configuration Dashboard'
corrections: []
review_notes:
- 'To check: Section ''The configuration dashboard set'': the configuration dashboards in VCF Operations 9.1 (names, and whether vSphere Network Configuration and vSAN Configuration were enhanced); a live VCF Operations 9.1 instance.'
status: draft
```
