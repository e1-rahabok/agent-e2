# vSphere cluster: what to monitor, in priority order

## Answers
- Which metrics are most important to monitor on a vSphere cluster: performance, capacity, availability.

## Principle
- The cluster is the sweet spot for monitoring and troubleshooting. Manage at cluster level, drill to hosts and VMs when troubleshooting.
- Cluster metrics are averages, even totals. One suffering VM is hidden. Low cluster utilization does not rule out contention. See `vsphere/object-types/cluster/concepts/cluster-utilization-vs-contention`.
- Two dimensions of performance: depth (the worst VM) and breadth (how many VMs).

## 1. Performance
- Cluster Performance (%): depth from the worst VM, breadth from the 90th percentile, aggregated directly from VMs. See `vcf-operations/kpis/cluster-performance`.
- Flow: `vsphere/object-types/cluster/diagnosis/cluster-vm-contention`.
- VMs short of CPU or memory in a DRS cluster: `vsphere/object-types/cluster/diagnosis/vm-insufficient-resources-in-drs-cluster`.

## 2. Capacity
- Cluster Consumption (%): utilization and saturation. See `vcf-operations/kpis/cluster-consumption`.
- Cluster Risk (%): highest host, reservation, overcommit, monster VMs. See `vcf-operations/kpis/cluster-risk`.
- Imbalance between hosts: a hot host causes contention while cluster totals stay low. See `vcf-operations/metrics/cluster/cpu-inter-host-imbalance`.
- Memory: `vsphere/technology/memory/metrics/cluster/consumed`.
- HA and admission control reserve capacity that utilization does not show. See `vsphere/object-types/cluster/concepts/admission-control-and-cluster-state`.
- Capacity model across products: `operations-management/capacity/capacity-model`.

## 3. Availability and service level
- Cluster and ESXi availability: `vsphere/object-types/cluster/metrics/comparisons/availability`.
- SLA and SLI (30-day, lagging): `vcf-operations/kpis/cluster-sla-sli`.

## 4. Context
- DRS Score is about demand met, not contention. See `vsphere/object-types/cluster/configuration/drs-migration-levels`.
- VM operations counts (vMotion, power, reconfigure): `vsphere/object-types/cluster/metrics/vm-operations`.
- Features that raise operational complexity (HA, DRS, vSAN, resource pools): `vsphere/object-types/cluster/concepts/cluster-operations`.

## Traps
- "Cluster CPU at 40%, so no VM waits" → check worst VM Ready and the share of VMs with Ready.
- "Few VMs affected, so the cluster is fine" → depth matters: one VM can be badly hit.
- "Average the VM KPIs to get the cluster KPI" → aggregate from VMs by worst and 90th percentile.
- "DRS Score 80%+ means no contention" → DRS Score is about demand, not contention.

## Metadata
```yaml
id: vsphere/object-types/cluster/overview-what-to-monitor
retriever_guide: what-to-check
scope: vsphere
technology:
- cpu
- memory
- storage
- network
pillar:
- performance
- capacity
- availability
product:
- vsphere
- vcf-operations
object:
- ClusterComputeResource
internal_derive:
- vsphere/object-types/cluster/concepts/cluster-utilization-vs-contention
- vcf-operations/kpis/cluster-performance
- vcf-operations/kpis/cluster-consumption
- vcf-operations/kpis/cluster-risk
related:
- vsphere/object-types/vm/overview-what-to-monitor
- vsphere/object-types/esxi/overview-what-to-monitor
- vsphere/object-types/cluster/diagnosis/cluster-vm-contention
- operations-management/capacity/capacity-model
source:
  document: Knowledge base synthesis of the linked files (author's book; vSphere 9.1 documentation)
  path: Linked files in each section
corrections: []
review_notes:
- 'Whole file: the priority order is Claude''s synthesis of the linked files (contention before consumption before context, README rule). Each statement restates a linked file. Author to confirm the order.'
status: draft
```
