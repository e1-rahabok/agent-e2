# Capacity demand

## Model choice

![Planning stage, theory before workload: Overcommit? No (business value far exceeds infrastructure cost) → buffer, then allocation in operation. Yes (majority of cases) → workload type Mono (one class, equal treatment) or Mix (Gold, Silver, Bronze on the same infrastructure; same technique to mix Kubernetes and VMs). Planning parameters: buffer cluster wide, utilization as the expected concurrent peak, allocation through the VM price (overcommit ratio justifies pricing to the tenant), reservation in mixed-class planning. Operating stage, actual metrics for an automated system: Buffer (%), Consumption (%) as an average against usable, Contention (%) as the brake, Risk (%) from monster VM, imbalance, overcommit ratio and reservation; share replaces reservation as the QoS lever, because a reservation can starve a lower class. Most common path: overcommit, mixed workload, VMs given for free](images/capacity-model-planning-vs-operating-stage-diagram.png)

- There are only 2 main models: overcommit or not-overcommit.
- Automated capacity management requires a model: for each dimension, a formula for total capacity, usable capacity ([`sp5-framework/capacity/supply`](supply.md)) and consumption.
- The model follows the goal. Two questions pick it: overcommit or not, and one class of service or several.
- Multi-cluster load balancing: every member cluster has the same settings.

### No overcommit

- Simplest and most expensive model: consumer to provider 1:1. Used where the business value of the workload far exceeds the infrastructure cost.
- Utilization, reservation and contention do not matter: each VM gets the runtime and memory it demands, when it demands it.
- Allocation is the only input. Measure it against usable capacity, not total capacity: usable already holds HA and DR.
- The cluster is closed when allocation equals usable capacity.

### Overcommit: one class (Mono)

- All VMs are Gold, or all Silver, or all Bronze. No reservation or share settings: all VMs are equal.
- Plan utilization for the concurrent peak of the combined workload, not the peak of each VM.

### Overcommit: several classes (Mix)

- Planning uses utilization, allocation and reservation; running uses share. What each stage uses and why: [`sp5-framework/capacity/capacity-management`](README.md), section Two stages.
- Price per class follows the overcommit ratio ([`sp5-framework/capacity/overcommit`](overcommit.md), section Ratio and price).
- Most common case: overcommit, mixed classes, VMs given for free (no chargeback). Common because of limited budget and physical constraints, not because it is the design.
- The design is one class per cluster: shares and reservations inside one cluster give no predictable difference between classes ([`sp5-framework/concepts/class-of-service`](../concepts/class-of-service.md), section Compute and storage design). Mixed classes are a compromise to plan and run with care.
- Planning fills the cluster to 100% of the first dimension reached: utilization, allocation or reservation.
- A cluster of mostly Gold VMs holds fewer VMs, scores a lower Risk (%) and a higher Performance (%).
- The same technique mixes Kubernetes and VMs as Kubernetes Node takes the shape of a vSphere VM.
- Gold VMs get higher shares under contention. Avoid absolute reservation at run time.

## Four dimensions


| Dimension | Role | Used for |
|---|---|---|
| Consumption | Primary metric | Against usable capacity, which holds availability and buffer |
| Contention | Override | Stop provisioning: the main input to closing the cluster |
| Allocation | Leading indicator | Protect the shared infrastructure from sudden demand |
| Reservation | Guarantee | Planning. At run time use it sparingly; use shares |

## Consumption

- Consumption consists of Utilization and Saturation.
- Live use of the resource. High utilization means the cluster is full, even with overcommit ratio and reservation below target.
- Ideal: 100% utilization, 0% saturation.
- Low utilization that stays low is wastage, unless the object is new and still growing, or holds DR protection.
- Accounting:
  - relative utilization, against usable capacity: exclude the HA host;
  - keep the hypervisor overhead of the other hosts: it is part of the load.


## Contention

- When the cluster cannot serve its current workload, remaining capacity is 0 in practice: provisioning stops.
- Two metrics:
  - Performance (%): the actual performance ([`vsphere/object-types/cluster/cluster-performance`](../../vsphere/object-types/cluster/cluster-performance.md));
  - Stop Provisioning (yes or no): the cluster is closed for new VMs or pods, decided from Cluster Consumption (%), Cluster Performance (%) and Cluster Risk (%) ([`vsphere/object-types/cluster/models/close-for-business`](../../vsphere/object-types/cluster/models/close-for-business.md)). Flow: [`vsphere/object-types/cluster/decision-tree/can-cluster-take-more-vms`](../../vsphere/object-types/cluster/decision-tree/can-cluster-take-more-vms.md).
- A leading indicator would let VMs already in the queue be provisioned, or give a week of notice. Performance and risk do not project well: a projection of them can be wrong.

## Reservation and share

Reviewed together: each covers what the other lacks.


| Aspect | Reservation | Share |
|---|---|---|
| Nature | Absolute; a guarantee, so no overcommit | Relative; overcommit does not apply |
| Focus | Throughput: CPU cycles (Hz) | Runtime: CPU time slices; memory apportioned |
| Drawback | At VM level it affects HA and DRS | No guarantee |
| Use | Conservatively; not the full value | Aggressively: a wide Gold to Silver ratio |
| Stage | Planning | Running |
| Where | Indirectly: resource pool | Directly: VM |

- A reservation set on the VM changes HA admission control and HA restart: unreserved capacity left after host failures decides placement. Set it on a resource pool instead.
- VM-level reservation leads to lower provider utilization and higher consumer contention: placement becomes unbalanced.
- Through a resource pool, a Gold VM may not get its reserved share on time: the DRS scheduler lags the ESXi scheduler.
- Turbo gives spare CPU at ESXi level above the reservable base clock ([`vsphere/architecture/resource-controls`](../../vsphere/architecture/resource-controls.md), section Reservation: CPU vs memory).
- Both add operational work: over time nobody knows which VM or pool has which reservation or share, or since when.
- No deterministic link to performance: doubling a VM's CPU reservation or shares does not halve its CPU Ready.
- Reservation adds complexity because it has two parts (allocated and used), and a resource pool and its child VMs carry independent settings.

## Demand

```text
Demand = Max (Utilization, Reservation)
```

- This Demand is the capacity model, not the vCenter counter `cpu.demand`, which leaves reservations out. ESXi CPU Demand in VCF Operations does add the reservations of running VMs and of the kernel (ESXi CPU Demand, section vCenter vs VCF Operations).
- A reservation not yet consumed affects capacity, not performance.
- Example: a VM using 4 GHz with a 5 GHz reservation counts as 5 GHz: the extra 1 GHz is guaranteed to it.
- Compute per VM, then sum at the ESXi host. A sum of utilization and a sum of reservation taken separately gives a different, wrong number.
- Powered-on VMs only. Powered-off VMs can be started any time, but counting them gives an over-conservative capacity.
- Restaurant: two floors, the first full of diners, the second empty but booked and paid for a wedding. Is it full? For a wedding guest, no; for anyone else, yes. Can the diners be served well? Yes: the second floor is empty, staff serve the first. Capacity is full while performance is fine.
- Who holds a reservation not yet consumed:
  - compute: powered-on VMs below their reserved CPU or memory;
  - storage: thin-provisioned virtual disks below their configured size. Not called a reservation, but it acts as one.

## Allocation

- The metric used to sell capacity: the price per class follows its overcommit ratio.
- Leading indicator: total demand can exceed visible demand, because part of the demand has no utilization yet.
- Not in-line: ESXi and vCenter do not schedule by allocation. So allocation can be overcommitted ([`vsphere/architecture/resource-controls`](../../vsphere/architecture/resource-controls.md), section Allocation vs reservation).
- Usable capacity applies here too: deduct the hypervisor (VMkernel, vSAN, NSX, vSphere Replication) from total capacity.
- Counted only for powered-on VMs.
- The ratio of allocation to supply is the overcommit ratio: per thread for CPU, against DRAM for memory, per resource and per class in [`sp5-framework/capacity/overcommit`](overcommit.md).

### Invisible demand


| Demand | Example | Response |
|---|---|---|
| Rare | Annual sales; a market crash | Set an overcommit ratio and drive by allocation |
| Unexpected | DR drill or real DR wakes protected VMs | Count Site Recovery Manager recovery plans |
| Potential | New VMs take months to reach full load | Plan for their final size |
| Unmet | Demand the VM or the host cannot serve | Count undersized VMs in cluster capacity |

- Rare demand of a group of VMs can hurt the whole cluster or datastore at once. Paying ahead for a disaster is a business decision, not the capacity planner's.
- Recovery plans: one recovery plan holds many protection groups, and one protection group can sit in many recovery plans. Count each VM once.
- New VMs are often idle for months, then grow fast.
- Unmet demand has two parts:
  - inside the VM: an undersized VM queues inside the Guest OS; the infrastructure never sees it;
  - outside the VM: contention, visible to the infrastructure and part of the IaaS KPI ([`sp5-framework/performance/kpi-vs-sla`](../performance/kpi-vs-sla.md)).

### Limitations of allocation


| Limitation | Effect |
|---|---|
| VM size ignored | Two monster VMs count the same as many small VMs of equal total; the scheduler fits small VMs more easily, more so when they peak at different times |
| Utilization ignored | Only configured size counts; extra load makes allocation report less consumption than real |
| Overhead ignored | vSAN keeps protection data on the same datastore: consumption doubles inside it |
| IaaS workload counted | Agent VMs count as demand, though they often use a local datastore |

## Misconceptions

- "Memory usage is 90%; aim for 80% because of HA" → Consumed is unaware of HA, and high Consumed is not a worry: memory is a cache and should be high, else the DIMMs, which are expensive, are wasted. HA is accounted in usable capacity.
- "Memory Active should stay below 50-60% to keep a buffer to Consumed" → Active is not a capacity counter. It serves VMkernel memory management and has no use for capacity unless memory tiering is on ([`vsphere/technology/memory/concepts/memory-tiering`](../../vsphere/technology/memory/concepts/memory-tiering.md)).
- "Each host should run in the high memory state" → High means much free memory: wastage for capacity. ESXi reclaims only near the top ([`vsphere/technology/memory/concepts/host-memory-states`](../../vsphere/technology/memory/concepts/host-memory-states.md)).
- "Mixed classes are the most common case, so they are the recommended design" → common because of budget and physical constraints; the design is one class per cluster.
- "UAT at 70% CPU is fine until 85%" → not wrong but misleading: utilization alone does not close a cluster; read contention and risk.
- "Utilization is low, so the reservation does not matter" → demand is the higher of utilization and reservation; an unused reservation is still taken.
- "Doubling the CPU shares halves CPU Ready" → no deterministic link between shares or reservation and contention.
- "Count powered-off VMs in demand to be safe" → powered-on VMs only; counting powered-off VMs makes capacity too conservative.
- "A thin disk that is not full has free space to give away" → its unwritten part is a reservation in effect: it grows to its configured size.

## Metadata

```yaml
id: sp5-framework/capacity/demand
retriever_guide: how-it-works
scope: sp5-framework
technology:
- cpu
- memory
- storage
- system
pillar:
- capacity
- performance
- value
product:
- vsphere
- vcf-operations
object:
- ClusterComputeResource
- ResourcePool
- VirtualMachine
internal_derive:
- sp5-framework/capacity/supply
- vsphere/architecture/resource-controls
related:
- vsphere/technology/cpu/metrics/host/demand
- sp5-framework/capacity/capacity-management
- sp5-framework/capacity/overcommit
- sp5-framework/capacity/forecasting
- sp5-framework/capacity/class-of-service-planning
- vsphere/object-types/cluster/decision-tree/can-cluster-take-more-vms
- sp5-framework/concepts/performance-vs-capacity
- vsphere/technology/memory/concepts/host-memory-states
- vsphere/technology/memory/concepts/memory-tiering
images:
  - path: images/capacity-model-planning-vs-operating-stage-diagram.png
    product: [vsphere]
    object: [ClusterComputeResource]
    topic: 'Capacity model choice'
    image_type: diagram
source:
  document: Knowledge base
  path: 'Capacity Management > Capacity Model (Workload Level; Workload Type; VM Price; 4 Dimensions of Capacity: Utilization, Performance, Reservation | Share, Allocation, Invisible Demand, Limitation)'
corrections: []
review_notes:
- 'To check: Section ''Consumption'': the 80-100% zone has no numbers yet; Cluster Consumption (%) uses different bands (CPU green 0-55) (Q116).'
- 'Section ''Reservation and share'': the resource-pool advice quotes Frank Denneman, frankdenneman.nl, vSphere 7 DRS Scalable Shares deep dive (2020-05-27). Paraphrased, not copied.'
- 'To check: Section ''Demand'': "a sum of utilization and a sum of reservation taken separately gives a different number" explains why computes per VM first; the explanation has no source yet.'
status: draft
```
