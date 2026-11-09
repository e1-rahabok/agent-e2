# Capacity dashboards

## Goals and users
- Goals:
  - overall capacity of compute, storage and network. Network covers the ESXi physical NICs, NSX Edge and NSX Manager;
  - optimization: reclaim, rightsize, redistribute.
- Questions they answer:
  - Is there enough CPU, memory, disk and network for today's demand and the near future?
  - Any hot spot? Rebalance?
  - How large is the wastage? How much can be reclaimed within a month, and how much takes longer?
- They complement the built-in capacity pages; they do not replace them.
- Users:
  - Capacity team, the main user: owns the capacity life cycle from planning to upgrade. Long-term and top down: future expansion and hardware refresh. Not interested in a host going down or into maintenance. Focus: the provider.
  - Operations team: runs day-to-day operations; not interested in the long-term past or future. Focus: the consumer, above all oversized VMs.
  - Storage team: a specialist team; collaboration matters most when the architecture is thin on thin (thin VMDKs on thin-provisioned LUNs).
- Frequency: weekly and quarterly.

## Design
- Same layout as the performance dashboards: the two pillars have much in common.
- Top down, in two sections: a summary for the big picture, then a detail section to drill into one object, such as the capacity of one VM.
- Quick context switch: cycle through objects without changing screens or opening windows.
- Progressive disclosure keeps the page fast and the content light; the browser session remembers the last selection.
- Colour: high remaining capacity can be wastage, shown in dark grey. Low utilization can also be a performance problem: a bottleneck elsewhere holds the load down.
- Beyond the built-in pages: reclamation sizes grouped into buckets, to start with the largest; trend charts in the same view to see growth.

## Consumer vs provider capacity
- Consumer: one VM, container or application; rightsize it and reclaim what is unused (`operations-management/capacity/rightsizing`, `operations-management/capacity/reclamation`).
- Provider: the shared infrastructure, because a shortage hits many consumers (`operations-management/capacity/capacity-model`).
- Special clusters change the capacity model. A stretched cluster gets its own model and view: one object or custom group per site, shown side by side.

## Traps
- "High remaining capacity is good" → it can be wastage, and low use can hide a bottleneck elsewhere.
- "One capacity number for a stretched cluster" → each site gets its own group and view.
- "Capacity dashboards replace the built-in pages" → they complement them with buckets, trends and customization.
- "The operations team plans capacity" → the capacity team plans; operations watches consumers, above all oversized VMs.
- "Storage capacity is the storage team's alone" → with thin on thin, VM and array views must be read together.

## Metadata
```yaml
id: vcf-operations/concepts/capacity-dashboards
retriever_guide: how-it-works
scope: vcf-operations
technology:
- cpu
- memory
- storage
- network
pillar:
- capacity
product:
- vcf-operations
- vsphere
- nsx
object:
- VirtualMachine
- ClusterComputeResource
- Datastore
internal_derive:
- vcf-operations/concepts/dashboard-design
- operations-management/capacity/capacity-model
related:
- operations-management/capacity/rightsizing
- operations-management/capacity/reclamation
- vcf-operations/concepts/performance-dashboards
- vcf-operations/concepts/it-leaders-dashboards
source:
  document: PART 2 - Consumption for Agent E2.docx
  path: 'Overall Design Approach > Overall Design: Capacity Dashboard (pp. 38-40)'
corrections: []
review_notes:
- 'Section ''Goals and users'': thin on thin explained as thin VMDKs on thin-provisioned LUNs is Claude''s knowledge.'
status: draft
```
