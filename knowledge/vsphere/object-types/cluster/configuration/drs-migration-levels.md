# DRS migration threshold

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
- VM DRS Score = VM happiness, a measure of the VM's execution efficiency. DRS recommendations aim to raise individual VM scores.
- Cluster DRS Score = weighted average of the VM DRS Scores of all powered-on VMs. A good cluster score can hide a few VMs with low scores; the VM list under Monitor > vSphere DRS sorts VMs by score, lowest first.
- vCenter stores both scores as level 1 counters, so their history exists by default: `clusterServices.vmDrsScore` on the VM and `clusterServices.clusterDrsScore` on the cluster (percent, rollup latest).
- DRS scans the cluster every minute for load-balancing recommendations.
- DRS also weighs host network saturation in initial placement.
- A VM that becomes incompatible with its current host (HA agent error, lost storage path, NSX component down) triggers DRS migrations to compatible hosts. Since vCenter 8.0 Update 3 the default of CompatCheckTransientFailureTimeSeconds is -1: DRS no longer moves a VM out only because of incompatibility with its current host. Earlier default: 600 seconds of tolerance.
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

## Misconceptions
- "A Cluster DRS Score of 85% and one of 95% differ in performance" → the source says the range matters, not the exact value. Scores above 80% indicate no performance impact.
- "DRS Level 3 reacts to every spike" → Level 3 is tuned for mostly stable workloads. Bursty or dynamic workloads are served by Level 4 or 5.

## Metadata
```yaml
id: vsphere/object-types/cluster/configuration/drs-migration-levels
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
- vsphere/object-types/cluster/concepts/drs-overview
- vsphere/object-types/resource-pool/resource-pool-design
- vsphere/object-types/cluster/concepts/dpm
source:
  document: Performance Best Practices for VMware vSphere 9.1 (revision 20260624)
  path: VMware Distributed Resource Scheduler (DRS) > DRS Performance Tuning (pp. 78-79); Cluster DRS Score (p. 79)
corrections: []
review_notes:
- 'Section ''Cluster DRS Score'': counter names, level and rollup from the vCenter 9.1.0 API export, https://github.com/e1-rahabok/Observability-vSphere/blob/main/vsphere-metrics.csv.'
- 'Section ''Cluster DRS Score'': VM happiness, weighted average, one-minute scan, network-aware placement and the compatibility-check option from the vSphere 9.1 documentation, vSphere Resource Management > Admission Control and Initial Placement, DRS Migration Threshold > DRS Score, VM migrations initiated by DRS due to incompatibility (pp. 1894, 1896, 1954-1955).'
- 'Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-9-1-performance-best-practices'
- 'To check: Predictive DRS: the source requires VMware vRealize Operations 6.4 or later, an old product version; whether the feature applies to vSphere 9.0 and VCF Operations.'
status: draft
```
