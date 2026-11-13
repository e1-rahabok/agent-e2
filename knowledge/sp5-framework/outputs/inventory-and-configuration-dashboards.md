# Inventory and configuration dashboards

## Inventory dashboards
- Goals: check that the inventory matches expectation, both the count and the change; cover every VCF object where inventory matters.
- Questions: what VMs do I have, where are they, what changed that I should know?
- Used with the configuration dashboards.
- Users: the platform team.
- Frequency: mostly ad hoc; daily for VM inventory changes.
- Features: the relationships between objects shown visually; fast traversal of the inventory hierarchy; the count of objects at each level, ideally with their movement over time.
- Inventory gets no alert: it is an account of what exists, not good or bad. Changes are watched on the NOC screen ([`sp5-framework/outputs/alert-design`](alert-design.md)).

## Configuration dashboards
- Goals: fix configuration issues before they cause impact; when an issue occurs, check whether configuration plays a part.
- Questions: does configuration match best practice? Are settings consistent and up to date with the plan? Are there undesirable drifts?
- Assumes the enterprise standard and policy are documented.
- Users: the platform team.
- Frequency: daily for urgent settings, weekly for non-urgent ones.
- Features:
  - what needs attention first, then the overall configuration, so the dashboard drives action;
  - a balance between ease of use, page load time and completeness. Not every setting of every object fits; screen space is the other limit.
- What to review per object: [`sp5-framework/concepts/configuration-management`](../concepts/configuration-management.md) and the object review lists, such as [`vsphere/object-types/vm/configuration/vm-configuration-review`](../../vsphere/object-types/vm/configuration/vm-configuration-review.md).

## The configuration dashboard set
- VM Configuration and VM Storage Configuration work together. The second was split out because one dashboard was too large to use.
- ESXi Configuration and vSphere Cluster Configuration work together. The cluster one carries the vSphere prefix because cluster is a generic English word. A drill-down from cluster to ESXi would help but adds UI complexity.
- vSphere Resource Management is separate: its settings span VMs, resource pools and clusters, and their flexibility and complexity need their own dashboard.
- vSphere Network Configuration and vSAN Configuration are basic and due for enhancement.
- With a larger screen, add checks or legends to the pie charts.
- In a large environment, add a filter by class of service (Gold, Silver, Bronze), defaulting to Gold, so less critical workloads do not clutter the view.

## Misconceptions
- "Alert on inventory changes" → inventory has no good or bad; watch changes on dashboards.
- "Show every setting" → show what needs attention first; completeness costs page speed and space.
- "Configuration dashboards without a standard" → drift has no meaning until the standard is documented.
- "Resource settings fit in the VM dashboard" → shares, reservations and limits span VMs, resource pools and clusters; they need their own dashboard.
- "Default the filter to all workloads" → default to Gold; the critical workloads come first.

## Metadata
```yaml
id: sp5-framework/outputs/inventory-and-configuration-dashboards
retriever_guide: how-it-works
scope: sp5-framework
technology:
- system
pillar:
- security
- availability
- performance
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
- sp5-framework/outputs/dashboard-design
- sp5-framework/concepts/configuration-management
related:
- vsphere/object-types/vm/configuration/vm-configuration-review
- vsphere/object-types/esxi/configuration/esxi-configuration-review
- vsphere/object-types/cluster/configuration/cluster-configuration-review
- vsphere/object-types/vm/configuration/resource-settings-guidance
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: 'Overall Design Approach > Overall Design: Inventory Dashboards; Overall Design: Configuration Dashboard'
corrections: []
review_notes:
- 'To check: Section ''The configuration dashboard set'': whether the VCF Operations 9.1 dashboards changed since the source said in future I would enhance them (written as due for enhancement).'
- 'Section ''Configuration dashboards'': the source question reads "Are the settings consistent when they have and up to date as per our plan?"; written as consistent and up to date with the plan.'
status: draft
```
