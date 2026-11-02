---
id: vsphere/cluster-resource-management/configuration/drs-migration-levels
retriever_guide: what-to-set
scope: vsphere
technology:
- cpu
- memory
- network
pillar:
- performance
product:
- vsphere
object:
- ClusterComputeResource
- VirtualMachine
internal_derive: []
related:
- vsphere/cluster-resource-management/concepts/drs-overview
- vsphere/cluster-resource-management/concepts/scalable-shares
- vsphere/cluster-resource-management/concepts/dpm
source:
  document: Performance Best Practices for VMware vSphere 9.1 (revision 20260624)
  path: VMware Distributed Resource Scheduler (DRS) > DRS Performance Tuning (pp. 78-79); Cluster DRS Score (p. 79)
corrections: []
review_notes:
- Checked against 9.1 (revision 20260624). Pages 78-79. Migration levels, Cluster DRS Score causes and Predictive DRS unchanged.
- 'Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-9-1-performance-best-practices'
- Predictive DRS requires VMware vRealize Operations 6.4 or later, per the source. This product version is old. Author to confirm whether the feature applies to vSphere 9.0 and VCF Operations.
status: draft
---

# DRS migration threshold levels and Cluster DRS Score

## Migration threshold levels (since vSphere 7.0)
- Before vSphere 7.0: one migration threshold controlled how aggressively fully automated DRS moved VMs.
- Since vSphere 7.0: the threshold is workload-focused. Each level is tuned for a kind of workload.
- Level 1: DRS recommends only mandatory moves. These fix rule violations, or move VMs off a host entering Maintenance Mode. DRS does not move VMs to improve resource availability at this level.
- Level 2: tuned for highly stable workloads. DRS recommends vMotion only when the cluster is at or close to contention.
- Level 3: the default. Tuned for mostly stable workloads.
- Level 4: for bursty workloads, where occasional spikes in utilization may require DRS to react to sudden load changes.
- Level 5: for dynamic workloads, where utilization varies significantly. DRS reacts to workload changes every time.

## Advanced options
- VM Distribution: DRS distributes VMs evenly across hosts in the cluster. Purpose: availability.
- Network Congestion (since vSphere 7.0): DRS considers network bandwidth usage, in addition to CPU and memory, when it computes vMotion recommendations.
- Network Congestion tunes how aggressively DRS balances network bandwidth utilization.
- Location in the vSphere Client: cluster, Configure tab, Services, vSphere DRS, Edit, Additional Options.

## Cluster DRS Score
- Since vSphere 7.0, the Cluster DRS Score replaces the cluster load balance metric as the indicator of cluster balance and health.
- Higher values are better. The exact value matters less than the range.
- Score above 80%: the source indicates no performance impact.
- Score below 80%: potential performance degradation in one or more cluster workloads.
- Lower score: higher potential performance impact on the workloads.
- Ways to raise the score:
  - relax rules,
  - adjust the migration threshold,
  - reduce resource demands on the cluster.
- Causes of a low score that the source lists:
  - migrations filtered out by affinity or anti-affinity rules,
  - migrations filtered out by VM-host incompatibilities,
  - cost estimate for potential migrations, based on the costs of previous migrations, exceeds the expected benefit of the migrations,
  - all hosts in the cluster are network saturated,
  - the cluster does not have enough usable resources to meet VM demands.

## Predictive DRS
- Predictive DRS can receive predictions from VMware vRealize Operations and use them for vMotion decisions.
- Requires vRealize Operations 6.4 or later, per the source.

## Traps
- "A Cluster DRS Score of 85% and one of 95% differ in performance" → the source says the range matters, not the exact value. Scores above 80% indicate no performance impact.
- "DRS Level 3 reacts to every spike" → Level 3 is tuned for mostly stable workloads. Bursty or dynamic workloads are served by Level 4 or 5.
