# Cluster and ESXi availability metrics

## Two kinds of availability
| Metric | Meaning |
|---|---|
| Operational availability (%) | Primary. Reflects operations maturity. A host can have perfect hardware but be in maintenance mode, quarantine or disconnected. |
| Hardware availability (%) | Redundant components (power, NICs, fans, memory) let a host keep running through component failures. Causes: manufacturing batch, heat, wear (finite SSD writes). |

## ESXi operational availability (%)
| State | Score |
|---|---|
| Powered off | 0% |
| Powered on | 25% |
| + not in maintenance mode | +25% |
| + not in quarantine | +25% |
| + connected to vCenter | +25% |

- VCF Operations super metric: 1 point per condition met (0-4), × 25.
![ESXi operational availability states](../../images/esxi-operational-availability-scoring-states.png)

## Restarts: sys.uptime
- vCenter stores `sys.uptime` on every VM and ESXi host at level 1: seconds since the last start, rollup latest.
- Uptime falls back toward 0 at every restart. A drop between two samples marks a reboot or power cycle, even when the object was down for less than one sample.
- The VM counter restarts with the VM (power cycle, reset, HA restart). A Guest OS reboot without a VM power cycle is a Guest OS event. See `vsphere/object-types/cluster/metrics/vm-operations`.

## Cluster availability
- Not the average of hosts: HA matters.

| Metric | Rule |
|---|---|
| Operational availability (%) | Considers HA: N+1 reports 100% with 1 host unavailable (ignore the worst host, average the rest). Excludes approved planned downtime (requires authoritative start and end times). Ignores hardware issues. |
| Actual availability (%) | Reality: a down is a down. Per host: average of operational and hardware availability (not the lowest). Cluster: average of all hosts, no HA. |

- Capped at 100%. Uncapped, a small N+1 cluster could exceed a large N+2 cluster (a 2-node cluster would show 200%). The cap allows averaging and needs no explanation.
- Operational availability should be near 100%. 99.9% in a month signals operations to improve.
- Actual availability is likely lower.
- In VM-as-a-service, a cluster is internal: no official SLA.
![Cluster availability with HA](../../images/cluster-operational-availability-with-ha.png)

## Roll-up (Datacenter, vCenter, vSphere World)
| Roll-up | Use |
|---|---|
| Average of cluster operational availability | Should be high except during large upgrade windows. |
| Worst cluster operational availability | Practical with a few dozen clusters. |
| Count of clusters below 100% | Best with hundreds of clusters. |

## Traps
- "Cluster availability = average host availability" → HA changes it.

## Metadata
```yaml
id: vsphere/object-types/cluster/metrics/comparisons/availability
retriever_guide: metric-meaning
scope: vsphere
technology:
- system
pillar:
- availability
product:
- vsphere
- vcf-operations
object:
- ClusterComputeResource
- HostSystem
metric_class: context
internal_derive: []
same_name: []
same_meaning: []
related:
- vsphere/object-types/cluster/metrics/vm-operations
- operations-management/capacity/capacity-model
- vsphere/object-types/cluster/concepts/cluster-operations
images:
  - path: ../../images/esxi-operational-availability-scoring-states.png
    product: [vcf-operations]
    object: [HostSystem]
    metric: ['ESXi Operational Availability']
    image_type: table
  - path: ../../images/cluster-operational-availability-with-ha.png
    product: [vcf-operations]
    object: [ClusterComputeResource]
    metric: ['Cluster Operational Availability']
    image_type: diagram
source:
  document: PART 3 - Counters.docx
  path: Provider Objects > Other Metrics > Availability
corrections: []
review_notes:
- 'Section ''Restarts: sys.uptime'': counter, level, rollup and summary from the author''s vCenter 9.1.0 API export, https://github.com/e1-rahabok/Observability-vSphere/blob/main/vsphere-metrics.csv. Reading a drop toward 0 as a restart: confirmed by the author (2026-11-04). Whether a Guest OS reboot without a VM power cycle resets the VM counter is Claude''s own knowledge, not yet confirmed.'
status: draft
```
