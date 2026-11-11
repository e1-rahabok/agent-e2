# Cluster configuration review

## The cluster as one computer
- A cluster is the smallest logical building block of compute: one computer made of physically independent parts for availability.
- Give it enough cores, GHz and memory. Typical ESXi in 2024: 1 TB of memory, so a 12-node cluster has 12 TB, enough room for DRS to place and balance many VMs.

## HA
- HA disabled: each application must protect itself from infrastructure failure.
- Admission control disabled: failover capacity for the VMs' reservations is no longer kept.
- Failover capacity (%) matches the design.
- VMs with overrides of the cluster default: each exception complicates operations.

## DRS
- DRS disabled: DRS covers performance and capacity, HA covers availability. Without DRS every host must keep its own buffer for peak demand.
- DRS in manual mode: recommendations wait for an administrator; DRS recalculates every minute, so a late approval acts on a condition that has changed. Details: `vsphere/object-types/cluster/configuration/drs-migration-levels`.
- Automation level matches the cluster's purpose.
- EVC mode: the cluster cannot use newer CPU capabilities.
- VMs with overrides of the cluster default.

## DPM
- Settings match expectation: `vsphere/object-types/cluster/concepts/dpm`.

## Cluster variants
- **Sub-cluster** (VM-host affinity): operational complexity; performance problems despite enough cluster capacity.
- **Small cluster**: higher HA overhead (3 nodes: 33%; 10 nodes: 10%). vSAN: fewer hosts, fewer failures-to-tolerate options. Many small clusters create resource silos.
- **Large cluster**: more redundancy per host. Three clusters of 6+1 use 21 hosts; one cluster of 18+2 uses 20 and tolerates two failures. From 32 nodes, harder to operate.
- **vSAN cluster**: a VM has a compute host and storage hosts, which can differ.
- **Multi-cluster**: clusters balanced as one; each keeps its own capacity remaining.
- **Stretched cluster**: more complex. It gives disaster avoidance, not disaster recovery; DR is still required.
- **Site Recovery cluster**: protected VMs from the other site must be counted in capacity.
- Cluster size cap from business continuity: `sp5-framework/concepts/purpose-driven-architecture`.

## Misconceptions
- "HA is off but every host runs, so availability is fine" → availability today is fine; the risk is in future health. Each application must now protect itself.
- "DRS manual mode is safer" → recommendations expire within minutes; without automation every host must keep its own peak buffer.
- "Three small clusters are safer than one large one" → 3 × (6+1) uses one more host than 18+2 and tolerates fewer failures per cluster.
- "A stretched cluster replaces DR" → it avoids disasters; recovery from one still requires DR.
- "VM-host rules keep the cluster balanced" → they create sub-clusters that can starve VMs while the cluster has capacity.

## Metadata
```yaml
id: vsphere/object-types/cluster/configuration/cluster-configuration-review
retriever_guide: what-to-set
scope: vsphere
technology:
- cpu
- memory
- system
pillar:
- availability
- performance
- capacity
product:
- vsphere
- vsan
object:
- ClusterComputeResource
internal_derive:
- sp5-framework/concepts/configuration-management
related:
- vsphere/object-types/cluster/configuration/drs-migration-levels
- vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
- vsphere/object-types/cluster/concepts/drs-overview
- vsphere/object-types/cluster/concepts/dpm
- sp5-framework/capacity/capacity-model
- sp5-framework/concepts/health-risk-efficiency
source:
  document: PART 1 - Concepts of Operations Management.docx
  path: 'Configuration Management > Review List > Cluster; vSphere Cluster Variation (pp. 144-145)'
corrections: []
review_notes:
- 'To check: Section ''HA'': the book says reservation is respected only when admission control is enabled. Host admission control enforces reservations at power-on whatever the HA setting (vsphere/object-types/cluster/concepts/admission-control-and-cluster-state); HA admission control keeps failover capacity for them. Written that way. (Q110).'
status: draft
```
