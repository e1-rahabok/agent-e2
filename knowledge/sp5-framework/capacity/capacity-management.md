# Capacity management

## What it answers
- Quantity: is there enough supply for the demand to come, at the lowest cost? Performance asks quality: are the consumers served well now?
- Supply is the provider side (ESXi hosts, clusters, datastores). Demand is the consumer side (VMs, pods).
- The unit of capacity is the vSphere cluster (section Cluster is the unit of capacity). Supply: [`sp5-framework/capacity/supply`](supply.md). Demand: [`sp5-framework/capacity/demand`](demand.md).
- Balance demand and supply: meet demand at the lowest cost while staying compliant with security and availability practice.
- Optimized capacity: what was bought is fully consumed, without wastage and without a performance compromise.
- Simple goals alone are easy: performance equal to physical (no overcommit, or 100% reservation), monster VMs (many cores per host), high availability (more HA hosts, higher vSAN FTT across racks, more NSX Edges). The work is to meet cost, performance, security and availability together.
- The principle applies beyond a vSphere cluster: Kubernetes, VDI, AI clusters.

## Peer pillars
- Capacity, availability and performance are peers ([`sp5-framework/concepts/overview`](../concepts/overview.md), section Relationships). Capacity does not own the other two: it takes one output from each and gives one input back.

| Peer | Capacity takes | Capacity gives | Stays in the peer |
|---|---|---|---|
| Availability | HA hosts, DR load, maintenance: taken out of supply | Room to lose a host | HA design, admission control, availability metrics |
| Performance | Cluster Performance (%): the override | Overcommit, VM size, imbalance: the chance of contention | Contention metrics, KPI design, noisy neighbour |
| Value | The price, which sets the overcommit ratio | Waste: the efficiency verdict | Cost, price, chargeback |

- Availability: the planned part (HA host, DR, maintenance) is subtracted from total capacity as availability protection ([`sp5-framework/capacity/supply`](supply.md), section Usable capacity). Admission control and cluster state are availability mechanisms that capacity reads as a gate ([`vsphere/object-types/cluster/concepts/admission-control-and-cluster-state`](../../vsphere/object-types/cluster/concepts/admission-control-and-cluster-state.md)). Actual and Operational Availability (%) are availability metrics ([`sp5-framework/concepts/sla-metrics`](../concepts/sla-metrics.md)).
- Performance: a cluster that cannot serve its current VMs is full, whatever its utilization. Capacity reads the KPI; its design and its contention metrics stay in performance ([`sp5-framework/performance/performance-kpi-design`](../performance/performance-kpi-design.md), [`sp5-framework/performance/noisy-neighbour`](../performance/noisy-neighbour.md)).
- How each of the two pillars reads the same utilization: [`sp5-framework/concepts/performance-vs-capacity`](../concepts/performance-vs-capacity.md).
- Cluster Risk (%) is a leading indicator for both pillars: overcommit, monster VM, reservation, the hottest host ([`vsphere/object-types/cluster/models/cluster-risk`](../../vsphere/object-types/cluster/models/cluster-risk.md)).
- Value: the class of service ties price to the overcommit ratio ([`sp5-framework/concepts/class-of-service`](../concepts/class-of-service.md)). Waste is read as efficiency, next to health and risk ([`sp5-framework/concepts/health-risk-efficiency`](../concepts/health-risk-efficiency.md)).

## Two stages: planning and running
| Aspect | Planning stage | Running stage |
|---|---|---|
| Workload | None yet; the cluster may not be bought | Runs; reality overrides the plan |
| Method | Simulation by a calculator | Measurement: VCF Operations metrics and models |
| Allocation | Input: the overcommit ratio, tied to the VM price | Leading indicator only: the scheduler does not use it |
| Reservation | Input per class, set at the resource pool | Used sparingly: absolute, with side effects |
| Share | Not used | The quality of service lever: DRS and ESXi tell the classes apart by it |
| Utilization | Input: the expected concurrent peak | A result: consumption, measured |
| Hypervisor overhead | Subtracted from supply: no load is measured yet | Already in the measured load: not subtracted again |
| Contention | Cannot be modelled | The override: it decides closure |
| Verdict | The first of six numbers to reach 100% | Can the cluster take more VMs; how long until it is full |

- Reservation in the planning stage becomes share in the running stage.
- The overcommit ratio is a planning input tied to the VM price, not to the Cluster Risk (%) score. Running, a Bronze cluster is expected to score a higher Cluster Risk than a Gold cluster.
- The calculator and its six numbers: [`sp5-framework/capacity/class-of-service-planning`](class-of-service-planning.md), section Planning calculator. Which model applies (overcommit or not, one class or several): [`sp5-framework/capacity/demand`](demand.md).
- The running stage has two horizons:

| Item | Short term | Long term |
|---|---|---|
| Question | Can more workload go on now? Can a host be taken out? | When must hardware be bought? |
| Performed by | Day-to-day operations | Capacity planner |
| Decision | Stop provisioning new load | Buy hardware |
| Ties to | Availability, performance | Value (cost) |
| Timeline | Now; no projection | Future; projection mandatory |
| Scope | Resources provisioned within an hour | Resources not yet purchased |
| Focus | The consumer; hardware | The provider; software (costs more) |

- Short term: automation deploys, so it must be blocked when a deployment would cause a problem. Check the present and the projected state. A host taken out (ESXi maintenance mode, cluster upgrade) lowers usable capacity.
- Long term: lead time follows procurement, months.

## Where each question is answered
| Question | Stage | File |
|---|---|---|
| How many VMs fit on a host or a cluster? | Planning | [`sp5-framework/capacity/class-of-service-planning`](class-of-service-planning.md) (tool `capacity_plan`) |
| Overcommit, reservation and expected peak per class? | Planning | [`sp5-framework/capacity/class-of-service-planning`](class-of-service-planning.md) |
| Which host specification? | Planning | [`sp5-framework/capacity/host-spec-from-class-of-service`](host-spec-from-class-of-service.md) |
| Largest VM per class? | Planning | [`sp5-framework/capacity/vm-size`](vm-size.md) |
| Total, usable, buffer, HA? | Both | [`sp5-framework/capacity/supply`](supply.md) |
| Which demand model, and why? | Both | [`sp5-framework/capacity/demand`](demand.md) |
| Overcommit ratio per resource and class? | Both | [`sp5-framework/capacity/overcommit`](overcommit.md) |
| Can this cluster take more VMs? | Running, short term | [`vsphere/object-types/cluster/decision-tree/can-cluster-take-more-vms`](../../vsphere/object-types/cluster/decision-tree/can-cluster-take-more-vms.md) |
| Is the cluster closed for business? | Running, short term | [`vsphere/object-types/cluster/models/close-for-business`](../../vsphere/object-types/cluster/models/close-for-business.md) |
| Does this ESXi host have CPU headroom? | Running, short term | [`vsphere/technology/cpu/decision-tree/host-cpu-capacity-headroom`](../../vsphere/technology/cpu/decision-tree/host-cpu-capacity-headroom.md) |
| Can this cluster take a host out (maintenance, upgrade)? | Running, short term | [`vsphere/object-types/cluster/decision-tree/can-cluster-take-a-host-out`](../../vsphere/object-types/cluster/decision-tree/can-cluster-take-a-host-out.md) |
| Will this datastore run out of space? | Running | [`vsphere/technology/storage/decision-tree/datastore-space-headroom`](../../vsphere/technology/storage/decision-tree/datastore-space-headroom.md) |
| When does the cluster run out? | Running, long term | [`sp5-framework/capacity/forecasting`](forecasting.md); [`vcf-operations/features/capacity-forecast`](../../vcf-operations/features/capacity-forecast.md) |
| What can be reclaimed? | Running | [`sp5-framework/capacity/reclamation`](reclamation.md), [`sp5-framework/capacity/unused-vm`](unused-vm.md) |
| Should this VM be resized? | Running | [`sp5-framework/capacity/rightsizing`](rightsizing.md); [`guest-os/system/concepts/guest-os-sizing`](../../guest-os/system/concepts/guest-os-sizing.md); [`sp5-framework/capacity/vm-footprint-sizing`](vm-footprint-sizing.md) |
| How are the results shown? | Running | [`sp5-framework/outputs/capacity-dashboards`](../outputs/capacity-dashboards.md) |

- Network capacity has no file of its own yet: hosts with 50 Gb rarely hit the limit ([`sp5-framework/capacity/supply`](supply.md), section Private cloud components).

## Six steps
![Six steps: demand side 2 Control demand by the pricing model, 3 Optimize demand by reclamation, 4 Account for latent, potential and unmet demand, 5 Monitor demand by tracking excessive usage; supply side 1 Plan supply by class of service, 6 Monitor with demand or performance plus allocation together](images/capacity-management-six-steps-demand-and-supply-diagram.png)

| Step | Side | Action |
|---|---|---|
| 1 | Supply | Plan supply by class of service |
| 2 | Demand | Control demand by the pricing model |
| 3 | Demand | Optimize demand by reclamation |
| 4 | Demand | Account for latent, potential and unmet demand |
| 5 | Demand | Monitor demand by tracking excessive usage |
| 6 | Supply | Monitor with demand or performance plus allocation, together |

- Steps 1 and 2 are done together, at planning. Steps 3 to 6 run in parallel.
- Starting at step 6 without steps 1 and 2 leaves many oversized VMs. They are usually the larger and more important VMs. Fixing them in production takes downtime, the burden of proof that performance does not drop, and makes the team that sized and paid for them look wrong. Prevention costs less.
- A VM affects capacity in two ways: its size ([`sp5-framework/capacity/rightsizing`](rightsizing.md)) and whether it is still used ([`sp5-framework/capacity/reclamation`](reclamation.md)).
- Example of a planning-stage cause: a monster VM leaves hosts unbalanced with low ESXi utilization. The fix is horizontal scaling of the application, decided before deployment.

## Four phases
| Phase | What happens |
|---|---|
| Plan | Sizing; how long the infrastructure lasts; What If scenarios; hardware is bought |
| Monitor | Starts after deployment: reality compared with the plan |
| Optimize | Supply: technology refresh. Demand: reclamation and rightsizing |
| Upgrade | End of hardware life: upgrade or migrate; workload moves by vMotion |

- Plan is the planning stage. Monitor, Optimize and Upgrade are the running stage.

- The plan spans years, not months. Provider side: rack, top-of-rack switch, cabling and cooling have physical limits. Consumer side: production workload lives for years and changes.
- The longer the plan, the larger the margin, and the higher the risk of excess capacity.
- Good or bad is relative to the plan. A plan with no overcommit never runs out of capacity; in another plan the same result is wastage.
- Monitor example: capacity for a new DaaS project planned for 1 year; after 3 months 25% of users are on it and utilization is already 70%. The plan is off by a wide margin.
- Optimize supply: newer hardware can give about 2x the capacity at the same cost.
- Optimize demand at the source: solve the oversized VM before it is provisioned. Progressive pricing makes smaller configurations cheaper per unit, so requesters choose them; reclaiming later is harder.

## Cadence
![Annual cadence: demand management runs reclamation and rightsizing weekly all year, gather and estimate in January to March, check points in June and December, adjustment in August; supply management runs procurement, lead time and onboarding twice a year, with a technology refresh decision before each](images/capacity-management-annual-cadence-demand-and-supply-timeline.png)

- Reclamation and rightsizing: a weekly cadence, all year. Wastage builds up without it.
- Demand: gather and estimate (January to March), check point (June), adjustment (August), check point (December).
- Supply: procurement, lead time and onboarding twice a year, each after a technology refresh decision.
- Large estate example: 1,200 ESXi hosts, 5-year depreciation and warranty → 240 hosts replaced per year, about 20 per month on a monthly cadence.
- Set the hardware standard once per year: fewer variations, and still new technology (lower cost, more capacity, faster, more secure).

## Planning inputs
Capacity planning starts from a business plan: which class of service serves which location.

| Input | Consideration |
|---|---|
| Location | Data sovereignty, network latency |
| Cost | Drives architecture and location |
| Class of service | IaaS, VDI, Database as a Service, Kubernetes as a Service |
| Security | Physical or air-gap separation |
| Availability | HA, DR, business continuity policy |
| Environment | Production, test, development, staging |

- Availability and security policy examples:
  - blast radius: no large cluster holding many VMs, as a cluster can go down;
  - concentration risk: fewer than 250 mission-critical VMs per datastore;
  - security risk: Internet-facing and internal VMs do not share a network.
- Scalability test of a revenue application cannot run in production. Option: a DR cluster with three purposes (DR, development, test), sized larger. Otherwise burst to public cloud: the load is temporary.
- DR (for example Site Recovery Manager) adds demand twice: the DR test and the real DR.
- Inputs that split clusters: OS license (Windows, RHEL), environment (production, test/dev), network (NSX Edge, DMZ, internal), location, licensed software (Oracle, SQL Server), service tier (Tier 1, 2, 3), function (management, NSX Edge).
- The plan changes yearly: what worked last year may not work next year.
- Do not add lanes for congestion that is short or rare. A revenue peak (annual sale, 1 day in 365) can be served by burst capacity in the cloud or on premises, by limiting, powering off or moving other workloads, or by borrowing hosts from other clusters for that day.

## Cluster is the unit of capacity
- A vSphere cluster is the smallest logical building block for capacity, because of HA, DRS and DPM. Plan and monitor capacity per cluster, not per host and not per data center.
- Group operations by cluster or by group of interchangeable clusters.
- A vCenter Data Center object can hold clusters with different purposes. One capacity remaining (%) for it is meaningless when its clusters are not interchangeable.
- Example: cluster A low on memory and disk but high on CPU (wastage), cluster B low on CPU and disk, cluster C low on CPU and memory. Each cluster has low capacity remaining and low time remaining; an average across the three shows plenty of every resource.
- Example estate: 2 physical locations, 18 clusters; 7 for business workload, 2 for non-business load (overhead).

## Misconceptions
- "The data center has 40% CPU, memory and disk left on average, so there is room" → capacity is per cluster; each cluster can be short of a different resource while the average looks fine.
- "Cluster utilization is 25%, plenty of capacity left, good" → utilization that stays low is wastage, not health, unless the cluster is new and growing or holds DR protection ([`sp5-framework/capacity/demand`](demand.md), section Consumption).
- "Plan capacity per host" → HA, DRS and DPM make the cluster the unit.
- "Optimize capacity once a year at budget time" → reclamation and rightsizing run weekly; supply decisions run twice a year.
- "No overcommit means good capacity management" → good or bad is relative to the plan; no overcommit can be wastage.
- "Plan the hypervisor overhead into utilization, then subtract it from measured utilization too" → planning subtracts it from supply because nothing is measured yet; measured utilization already holds it.
- "Model contention in the capacity plan" → contention does not exist before workload runs; it overrides the plan in the running stage.
- "Capacity management owns HA and the performance KPI" → they are peers: capacity subtracts the HA design from supply and reads the KPI as the override.

## Metadata
```yaml
id: sp5-framework/capacity/capacity-management
retriever_guide: how-it-works
scope: sp5-framework
technology:
- system
pillar:
- capacity
- value
product:
- vsphere
- vsan
- nsx
- vcf-operations
object:
- ClusterComputeResource
- Datacenter
internal_derive: []
related:
- sp5-framework/concepts/overview
- sp5-framework/concepts/performance-vs-capacity
- sp5-framework/concepts/sla-metrics
- sp5-framework/concepts/class-of-service
- sp5-framework/concepts/health-risk-efficiency
- vsphere/object-types/cluster/models/cluster-risk
- vsphere/object-types/cluster/models/close-for-business
- vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
- vsphere/technology/cpu/decision-tree/host-cpu-capacity-headroom
- vsphere/object-types/cluster/decision-tree/can-cluster-take-a-host-out
- vsphere/technology/storage/decision-tree/datastore-space-headroom
- sp5-framework/capacity/host-spec-from-class-of-service
- sp5-framework/capacity/vm-size
- sp5-framework/capacity/unused-vm
- sp5-framework/capacity/vm-footprint-sizing
- sp5-framework/outputs/capacity-dashboards
- sp5-framework/capacity/demand
- sp5-framework/capacity/overcommit
- sp5-framework/capacity/forecasting
- sp5-framework/capacity/class-of-service-planning
- sp5-framework/capacity/supply
- sp5-framework/capacity/reclamation
- sp5-framework/capacity/rightsizing
- vsphere/object-types/cluster/decision-tree/can-cluster-take-more-vms
images:
  - path: images/capacity-management-six-steps-demand-and-supply-diagram.png
    product: [vsphere]
    object: [ClusterComputeResource]
    topic: 'Capacity management steps'
    image_type: diagram
  - path: images/capacity-management-annual-cadence-demand-and-supply-timeline.png
    product: [vsphere]
    object: [ClusterComputeResource]
    topic: 'Capacity management cadence'
    image_type: timeline
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: 'Your Private Cloud > SP5 Framework: Pillars (Capacity); Capacity Management > Capacity Model (planning stage vs operating stage); Capacity Management > Overview ("Good" Advice; Concept; Private Cloud Capacity; Stages; The Planning Stage; Architecture Plan; Example; Optimized Capacity)'
corrections: []
review_notes:
- 'Section ''Planning inputs'': the cluster-splitting list is the text of the book image after Architecture Plan; the example estate (18 clusters) is the book image after Example. Neither image is copied: the text holds the facts.'
- 'Section ''Cluster is the unit of capacity'': the three-cluster example is the book table image after The Planning Stage, restated as text.'
- 'To check: Section ''Four phases'': the reason for preventing oversized VMs before provisioning (reclaiming later is harder); not in the book.'
status: draft
```
