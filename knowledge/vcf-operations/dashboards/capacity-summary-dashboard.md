# Capacity Summary dashboard

## Purpose
- VCF Operations ships two sample dashboards for presenting live information to senior management: Inventory Summary and Capacity Summary. They are for the operations team to present, not for self-service.
- Capacity Summary explains remaining capacity and time; Inventory Summary explains available resources and what runs on them.
- How to design dashboards for IT leaders (layers of management, requirements, reports): [`sp5-framework/outputs/it-leaders-dashboards`](../../sp5-framework/outputs/it-leaders-dashboards.md).

## Top section: vSphere World summary
- Weekly average VM growth across all data centres, running and powered off. VM count rising without utilization rising means the new VMs are not yet used.
- Overcommit ratio: the efficiency of running many workloads on shared hosts. Read it together with contention (performance dashboards). Overcommit is what makes a private cloud cheaper than the public cloud.
- VCF Operations counts physical cores, not logical (hyper-threaded) cores, in all CPU capacity calculations.
- Capacity remaining is not shown at the World level: it misleads in a large or global estate, and clusters serve different purposes and are not interchangeable.

## Bottom section: compute and storage
- Two columns, compute and storage, with the same design.
- Network is left out: it is an interconnect, not a node, so its capacity is much harder to compute.
- The words compute and storage replace vSphere cluster and datastore to keep it simple.
- A heat map sized by capacity and coloured by time remaining. Compute boxes have a fixed size: no single metric sizes a cluster (hosts, CPU GHz, CPU cores, memory).
- Selecting a cluster or datastore drills down to remaining capacity and time remaining in days.
- With on-premises and public cloud (for example VMware Cloud on AWS), split the dashboard into two columns, given the screen space.

## Misconceptions
- "Show capacity remaining for the whole World" → clusters are not interchangeable; show it per cluster and datastore.
- "VM count growth means demand growth" → without utilization growth, the new VMs are not yet used.
- "A high overcommit ratio is a problem" → it is efficiency; read it with contention.
- "CPU capacity counts hyper-threads" → VCF Operations counts physical cores (Total Capacity (GHz) = cores × base frequency: capacity at base clock); plan capacity per physical thread.

## Metadata
```yaml
id: vcf-operations/dashboards/capacity-summary-dashboard
retriever_guide: how-it-works
scope: vcf-operations
technology:
- cpu
- memory
- storage
pillar:
- capacity
product:
- vcf-operations
- vsphere
object:
- ClusterComputeResource
- Datastore
internal_derive:
- sp5-framework/outputs/it-leaders-dashboards
- sp5-framework/outputs/capacity-dashboards
related:
- vcf-operations/features/capacity-forecast
- sp5-framework/capacity/supply
- sp5-framework/capacity/overcommit
source:
  document: Knowledge base
  path: 'Overall Design Approach > Overall Design: IT Leaders Dashboard (Sample Dashboards: Capacity Summary, How to Use, Points to Note)'
corrections: []
review_notes: []
status: draft
```
