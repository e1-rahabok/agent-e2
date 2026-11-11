# Capacity management process

## Goal
- Balance demand and supply: meet demand at the lowest cost while staying compliant with security and availability practice.
- Optimized capacity: what was bought is fully consumed, without wastage and without a performance compromise.
- Simple goals alone are easy: performance equal to physical (no overcommit, or 100% reservation), monster VMs (many cores per host), high availability (more HA hosts, higher vSAN FTT across racks, more NSX Edges). The work is to meet cost, performance, security and availability together.
- The principle applies beyond a vSphere cluster: Kubernetes, VDI, AI clusters.

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
- A VM affects capacity in two ways: its size (`sp5-framework/capacity/rightsizing`) and whether it is still used (`sp5-framework/capacity/reclamation`).
- Example of a planning-stage cause: a monster VM leaves hosts unbalanced with low ESXi utilization. The fix is horizontal scaling of the application, decided before deployment.

## Four phases
| Phase | What happens |
|---|---|
| Plan | Sizing; how long the infrastructure lasts; What If scenarios; hardware is bought |
| Monitor | Starts after deployment: reality compared with the plan |
| Optimize | Supply: technology refresh. Demand: reclamation and rightsizing |
| Upgrade | End of hardware life: upgrade or migrate; workload moves by vMotion |

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

## Cluster is the unit of capacity
- A vSphere cluster is the smallest logical building block for capacity, because of HA, DRS and DPM. Plan and monitor capacity per cluster, not per host and not per data center.
- Group operations by cluster or by group of interchangeable clusters.
- A vCenter Data Center object can hold clusters with different purposes. One capacity remaining (%) for it is meaningless when its clusters are not interchangeable.
- Example: cluster A low on memory and disk but high on CPU (wastage), cluster B low on CPU and disk, cluster C low on CPU and memory. Each cluster has low capacity remaining and low time remaining; an average across the three shows plenty of every resource.
- Example estate: 2 physical locations, 18 clusters; 7 for business workload, 2 for non-business load (overhead).

## Private cloud components
| Component | Covers | Note |
|---|---|---|
| Compute | ESXi, cluster, resource pool, server | Most attention; a good start with 1:1 compute to storage |
| Storage | Datastore, datastore cluster, vSAN, RDM, array, backup | Equal weight with many-to-many cluster to datastore, or vSAN HCI Mesh |
| Network | Virtual and physical: switch, router, firewall, load balancer | Usually the network architect's; 50 Gb per host is common |

- Storage capacity differs from compute: its shape varies (datastore, vSAN; local datastore and RDM are rare), and thin provisioning exists at both the virtual and the array layer. vSAN adds FTT and depends on compute.
- Network: hosts with 50 Gb rarely hit the limit, unless high-bandwidth VMs (network appliances, web servers) share the same hosts.

## Optimize the provider layer
| Area | Action |
|---|---|
| Compute | Larger clusters; remove host-VM affinity; DRS fully automated |
| Compute | Technology refresh: more supply at the same cost |
| Compute | No CPU pinning |
| Storage | Larger datastores: fewer islands of buffer |
| Storage | Local datastores for agent VMs and applications without HA |
| Storage | Consolidate datastores with low utilization |
| Network | Larger pipes: 2 × 100 Gb instead of 4 × 10 Gb; load-based teaming |
| Network | Remove unused networks: VLAN or VXLAN sprawl makes management and security harder |

- Pockets of resource are the common cause: affinity rules, pinning and small clusters or datastores each hold a buffer that others cannot use.

## Misconceptions
- "The data center has 40% CPU, memory and disk left on average, so there is room" → capacity is per cluster; each cluster can be short of a different resource while the average looks fine.
- "Cluster utilization is 25%, plenty of capacity left, good" → below 40% of usable capacity is wastage, not health (`sp5-framework/capacity/capacity-dimensions`, section Utilization).
- "Plan capacity per host" → HA, DRS and DPM make the cluster the unit.
- "Optimize capacity once a year at budget time" → reclamation and rightsizing run weekly; supply decisions run twice a year.
- "No overcommit means good capacity management" → good or bad is relative to the plan; no overcommit can be wastage.

## Metadata
```yaml
id: sp5-framework/capacity/capacity-management-process
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
- sp5-framework/capacity/capacity-dimensions
- sp5-framework/capacity/class-of-service-planning
- sp5-framework/capacity/capacity-model
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
  path: 'Capacity Management > Overview ("Good" Advice; Concept; Private Cloud Capacity; Stages; The Planning Stage; Architecture Plan; Example; Optimized Capacity)'
corrections: []
review_notes:
- 'Section ''Planning inputs'': the cluster-splitting list is the text of the book image after Architecture Plan; the example estate (18 clusters) is the book image after Example. Neither image is copied: the text holds the facts.'
- 'Section ''Cluster is the unit of capacity'': the three-cluster example is the book table image after The Planning Stage, restated as text.'
- 'To check: Section ''Four phases'': the reason for preventing oversized VMs before provisioning (reclaiming later is harder); not in the book.'
status: draft
```
