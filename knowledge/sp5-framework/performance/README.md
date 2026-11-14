# Performance management

## Scope
- Quality: are the consumers served well now? Capacity asks quantity: is there enough supply for the demand to come ([`sp5-framework/capacity/capacity-management`](../capacity/README.md)).
- Performance is contention: the time a consumer waited for a resource it demanded. No contention, no performance problem. Utilization is consumption: 100% with no queue is the most work done ([`sp5-framework/concepts/performance-vs-capacity`](../concepts/performance-vs-capacity.md)).
- Measured on the consumer: the VM, the Guest OS, the pod. A provider (ESXi host, cluster) has no contention of its own: its performance is the contention of its consumers ([`vsphere/architecture/provider-consumer`](../../vsphere/architecture/provider-consumer.md)).
- Read against total capacity, at the 20-second peak, over seconds to hours. HA, buffer and usable capacity are capacity ideas.
- Proactive: find the problem before the customer complains. A process that waits for an alert or a complaint is troubleshooting, not performance management. Proactive takes a regular cadence and an internal threshold: the KPI levels.
- Performance first, capacity second: performance is more time sensitive. In a restaurant, the dining area comes before the kitchen.

## Peer pillars
- Performance, capacity and availability are peers ([`sp5-framework/concepts/overview`](../concepts/overview.md), section Relationships). Performance takes one input from each and gives one output back; it does not own them.

| Peer | Performance takes | Performance gives | Stays in the peer |
|---|---|---|---|
| Capacity | Overcommit, VM size, imbalance: the chance of contention | Contention: the override that closes a cluster | Supply, demand, overcommit, forecasting |
| Availability | An object that is up | Slowness so bad it is as good as down | Down flows, HA, availability metrics |
| Configuration | A setting as a cause: limit, shares, version | A finding for the configuration review | The review lists per object |
| Value | The class of service: overcommit and VM size per price | Contention per class, read with one KPI | Price, SLA, chargeback |

- Capacity: Cluster Risk (%) is the leading indicator for both pillars ([`vsphere/object-types/cluster/models/cluster-risk`](../../vsphere/object-types/cluster/models/cluster-risk.md)). Capacity reads Cluster Performance (%) to close a cluster; the KPI design stays here.
- Availability first: a system that is down has no performance problem. Unreachable or failing is down: the availability process, not a slow flow. Errors and drops are contention metrics with an availability impact ([`sp5-framework/observability/triple-see-method`](../observability/triple-see-method.md)).
- Configuration is a drill-down under every pillar, not a pillar: a limit or an outdated version causes contention that load does not explain.
- Value: one set of KPI levels for every class. A Gold VM scores higher because its design causes less contention, not because its target is lower. Performance has no SLA ([`sp5-framework/performance/kpi-vs-sla`](kpi-vs-sla.md)).
- The Guest OS is a separate realm. Slowness inside Windows or Linux is not VM or host health; it has its own KPI and flows ([`sp5-framework/concepts/realms-and-layers`](../concepts/realms-and-layers.md)).

## Two processes
- Monitoring, proactive: one KPI per object, read daily in the health check, at the 20-second peak of each 5-minute interval. It finds whether there is a problem, on which object, and how bad.
- Troubleshooting, reactive: starts from a complaint, an alert or a failed health check step, and asks why. Only two types: down (availability) and slow (performance).
- Both read in the same order: contention, consumption, configuration, known bug, log. The what before the why ([`sp5-framework/concepts/health-check`](../concepts/health-check.md), section Order of checks).
- Comparison of the two processes, primary and secondary metrics, root cause analysis: [`sp5-framework/concepts/monitoring-vs-troubleshooting`](../concepts/monitoring-vs-troubleshooting.md).

## KPIs
| Layer | Object | KPI | How it reads its consumers | File |
|---|---|---|---|---|
| Business | Application | Business application KPI | Tier: average of members; application: worst tier | [`sp5-framework/performance/business-application-kpi`](business-application-kpi.md) |
| Guest OS | Windows, Linux | Guest OS Performance (%) | One operating system | [`guest-os/system/guest-os-performance`](../../guest-os/system/guest-os-performance.md) |
| Consumer | VM | VM Performance (%) | One virtual motherboard | [`vsphere/object-types/vm/vm-performance`](../../vsphere/object-types/vm/vm-performance.md) |
| Provider | ESXi host | ESXi Performance (%) | Worst VM and 90th percentile; host bad packets | [`vsphere/object-types/esxi/esxi-performance`](../../vsphere/object-types/esxi/esxi-performance.md) |
| Provider | Cluster | Cluster Performance (%) | Worst VM and 90th percentile; worst host bad packets | [`vsphere/object-types/cluster/cluster-performance`](../../vsphere/object-types/cluster/cluster-performance.md) |

- Design shared by every KPI (which metrics qualify, 20-second peaks, scoring, the daily actual): [`sp5-framework/performance/performance-kpi-design`](performance-kpi-design.md). Colour levels: `catalog/thresholds-performance`.
- KPI vs SLA, and KPIs per layer of the business: [`sp5-framework/performance/kpi-vs-sla`](kpi-vs-sla.md).
- Not built yet: a datastore KPI, a vSAN KPI (disk latency of every VM on the vSAN datastore), an NSX KPI.

## Question map
| Question or signal | Start with |
|---|---|
| Users say the VM is slow | [`sp5-framework/performance/vm-slow`](vm-slow.md) |
| Windows or Linux is slow | [`guest-os/system/troubleshooting/ms-windows-slow`](../../guest-os/system/troubleshooting/ms-windows-slow.md), [`guest-os/system/troubleshooting/linux-os-slow`](../../guest-os/system/troubleshooting/linux-os-slow.md) |
| VM Performance (%) yellow or worse | [`vsphere/object-types/vm/vm-health-check`](../../vsphere/object-types/vm/vm-health-check.md), steps 2-6 |
| ESXi Performance (%) yellow or worse | [`vsphere/object-types/esxi/esxi-health-check`](../../vsphere/object-types/esxi/esxi-health-check.md), step 3 |
| Cluster Performance (%) yellow or worse | [`vsphere/object-types/cluster/troubleshooting/cluster-vm-contention`](../../vsphere/object-types/cluster/troubleshooting/cluster-vm-contention.md) |
| A VM gets less than it demands in a DRS cluster | [`vsphere/object-types/cluster/troubleshooting/vm-insufficient-resources-in-drs-cluster`](../../vsphere/object-types/cluster/troubleshooting/vm-insufficient-resources-in-drs-cluster.md) |
| CPU Ready, Co-stop or Contention high | [`vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high`](../../vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high.md) |
| CPU Other Wait high | [`vsphere/technology/cpu/troubleshooting/vm-other-wait-high`](../../vsphere/technology/cpu/troubleshooting/vm-other-wait-high.md) |
| CPU Run and Used differ | [`vsphere/technology/cpu/troubleshooting/run-vs-used-gap`](../../vsphere/technology/cpu/troubleshooting/run-vs-used-gap.md) |
| Memory latency high | [`vsphere/technology/memory/vm-memory-latency-high`](../../vsphere/technology/memory/vm-memory-latency-high.md) |
| Is memory tiering slowing this host? | [`vsphere/technology/memory/decision-tree/is-memory-tiering-slowing-host`](../../vsphere/technology/memory/decision-tree/is-memory-tiering-slowing-host.md) |
| Is memory overcommit hurting this VM? | [`vsphere/technology/memory/decision-tree/is-overcommit-affecting-vm`](../../vsphere/technology/memory/decision-tree/is-overcommit-affecting-vm.md) |
| VM disk latency high | [`vsphere/technology/storage/troubleshooting/vm-storage-performance-checks`](../../vsphere/technology/storage/troubleshooting/vm-storage-performance-checks.md) |
| ESXi storage latency high | [`vsphere/technology/storage/troubleshooting/host-storage-latency`](../../vsphere/technology/storage/troubleshooting/host-storage-latency.md) |
| vNIC receive drops | [`vsphere/technology/network/vnic-rx-drops`](../../vsphere/technology/network/vnic-rx-drops.md) |
| One VM hurts the others | [`sp5-framework/performance/noisy-neighbour`](noisy-neighbour.md) |
| Which metric is primary, which secondary? | [`sp5-framework/observability/triple-see-method`](../observability/triple-see-method.md) |
| How the results are shown and alerted | [`sp5-framework/outputs/performance-dashboards`](../outputs/performance-dashboards.md), [`sp5-framework/outputs/alert-design`](../outputs/alert-design.md) |

## Misconceptions
- "The VMs are slow, so add hosts" → only contention from load is fixed by capacity; contention from limits, imbalance or configuration is not.
- "The VM is unreachable: start the slow flow" → unreachable or failing is down: the availability process.
- "Gold has its own, stricter KPI levels" → one set of levels for every class; Gold scores higher because it is overcommitted less.
- "Cluster Performance is red: tune the cluster" → the cluster KPI quantifies; troubleshoot the VMs and hosts its sub-metrics point to.
- "Performance is measured against usable capacity" → usable capacity is a capacity idea; performance is read against total capacity.
- "The application inside the VM is slow, so the VM performs badly" → the Guest OS is a separate realm; read VM Performance (%) and Guest OS Performance (%) apart.

## Metadata
```yaml
id: sp5-framework/performance/performance-management
retriever_guide: how-it-works
scope: sp5-framework
technology:
- cpu
- memory
- storage
- network
- system
pillar:
- performance
product:
- vsphere
- vcf-operations
object:
- VirtualMachine
- HostSystem
- ClusterComputeResource
internal_derive:
- sp5-framework/concepts/performance-vs-capacity
- sp5-framework/concepts/monitoring-vs-troubleshooting
- sp5-framework/concepts/realms-and-layers
related:
- sp5-framework/performance/performance-kpi-design
- sp5-framework/performance/kpi-vs-sla
- sp5-framework/performance/vm-slow
- sp5-framework/performance/noisy-neighbour
- sp5-framework/capacity/capacity-management
- sp5-framework/concepts/health-check
- vsphere/object-types/vm/vm-performance
- vsphere/object-types/esxi/esxi-performance
- vsphere/object-types/cluster/cluster-performance
- guest-os/system/guest-os-performance
- sp5-framework/performance/business-application-kpi
source:
  document: Knowledge base
  path: 'Your Private Cloud > SP5 Framework: Pillars (Performance); Performance Management; SP5 Framework > Monitor | Troubleshoot'
corrections: []
review_notes: []
status: draft
```
