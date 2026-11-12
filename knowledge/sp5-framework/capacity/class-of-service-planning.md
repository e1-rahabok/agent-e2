# Class of service in capacity planning

## Step per class
- Gold, Silver and Bronze require a relative value that tenants understand.
- The step follows the CPU overcommit ratio, 1:1, 2:1, 3:1 per physical thread: Silver has 2 consumers per thread, Bronze 3. So Bronze has about 3x the chance of contention of Gold, and costs a third.
- A step tied to one setting is easy to explain to senior leadership and application teams, and easy to run at scale.
- Price follows the same step: Gold price = 2x Silver = 3x Bronze ([`sp5-framework/concepts/class-of-service`](../concepts/class-of-service.md), section Generic guideline).
- The steps are a goal, not a rule: memory allocation (1:1, 1.2:1, 1.4:1), shares and utilization do not follow them exactly.
- Price, SLA numbers per class, size limits and soft products: [`sp5-framework/concepts/class-of-service`](../concepts/class-of-service.md). This file holds the capacity settings.

## Promise vs technique
- What is sold: a Gold VM has the lowest chance of contention; Silver about 2x Gold's, Bronze about 3x.
- Contention cannot be guaranteed directly. So the provider proves the promise with four techniques, each stepping with the class:
  - a lower overcommit ratio;
  - a larger reservation;
  - more shares, so a higher class wins under contention;
  - a larger maximum VM size, so a lower class cannot become the noisy neighbour ([`sp5-framework/capacity/vm-size`](vm-size.md)).

| Relative value | Gold | Silver | Bronze |
|---|---|---|---|
| Relative contention | 1x | 2x | 3x |
| Maximum VM size | 4x | 2x | 1x |
| VM reservation | 4x | 2x | 1x |
| VM share | 4-8x | 2-4x | 1x |
| VM to ESXi overcommit ratio | 1x | 2x | 3x |

- Maximum VM size steps 4x, 2x, 1x: 2, 1 and 0.5 CPU building blocks ([`sp5-framework/capacity/vm-size`](vm-size.md), section Size per class).
- Reservation steps 4x, 2x, 1x: 50%, 25%, 12.5% CPU and 100%, 50%, 25% memory (section Example implementation). A reservation guards against starvation; it does not have to step with the overcommit ratio.
- Contention is promised as a relative step, not as an absolute number per class. The KPI levels are the same for every class; Gold scores higher because it has less contention by design ([`sp5-framework/performance/performance-kpi-design`](../performance/performance-kpi-design.md), section Reading a KPI over time).

## Example implementation
![Planning values per class, Gold, Silver, Bronze. Typical VM (average for planning, not the maximum; 4 GB RAM per vCPU): 16 vCPU 64 GB, 8 vCPU 32 GB, 4 vCPU 16 GB. Reservation (relative to VM configured size, set at resource pool): 50% CPU 100% RAM, 25% CPU 50% RAM, 12.5% CPU 25% RAM. Allocation (thread, usable capacity; RAM against DRAM, memory tiering not in the ratio): CPU 1:1 RAM 1:1, CPU 2:1 RAM 1.2:1, CPU 3:1 RAM 1.4:1. Utilization, expected concurrent peak of the VMs: CPU 35% RAM 85%, CPU 50% RAM 85%, CPU 65% RAM 85%](images/class-of-service-planning-values-vm-reservation-allocation-utilization-table.png)

- **Typical VM** (the average for planning, not the maximum size; 4 GB RAM per vCPU)
  - Gold: 16 vCPU, 64 GB
  - Silver: 8 vCPU, 32 GB
  - Bronze: 4 vCPU, 16 GB
- **Reservation**
  - Gold: 50% CPU, 100% RAM
  - Silver: 25% CPU, 50% RAM
  - Bronze: 12.5% CPU, 25% RAM
  - Relative to the VM's configured size. Set at the resource pool, not the VM.
- **Allocation (overcommit, virtual : physical)**
  - Gold: CPU 1:1, RAM 1:1
  - Silver: CPU 2:1, RAM 1.2:1
  - Bronze: CPU 3:1, RAM 1.4:1
  - CPU per thread, not per core. 3:1 is the highest CPU overcommit of any class: 6:1 per core with Hyper-Threading. Against usable capacity, not total capacity. RAM is against DRAM: memory tiering is not part of the ratio and not part of the plan ([`sp5-framework/capacity/overcommit`](overcommit.md)).
- **Utilization: expected concurrent peak of the VMs**
  - Gold: CPU 35%, RAM 85%
  - Silver: CPU 50%, RAM 85%
  - Bronze: CPU 65%, RAM 85%
  - The share of configured size busy at the same time across the VMs of a class. Against ESXi physical threads, not cores; against usable capacity, not total.

- Reservation and allocation are the settings; relative contention is the promise they keep. Utilization is the expected demand; the host utilization it produces is a result.
- Gold fills on CPU allocation, well before its threads are busy: on a 64-core, 768 GB host (Hyper-Threading on), 7 Gold VMs reach 98% CPU allocation and 93% CPU reservation at 34% CPU utilization.
- Bronze fills on CPU utilization: on the same host, 43 Bronze VMs reach 98% CPU utilization at 50% CPU allocation. Its threads are planned to be busy; above that, contention risk rises.

## Planning calculator
- At the planning stage there is no workload, so the plan is a simulation. What the planning and running stages each use: [`sp5-framework/capacity/capacity-management`](README.md), section Two stages. Agent E2 runs it with the `capacity_plan` tool; the model gathers the inputs and explains the result. Defaults per class are catalog rows `planning-*`.
- Inputs: per host the cores, base GHz, DRAM, Hyper-Threading, hypervisor overhead (threads and GB), system CPU reservation; the number of hosts and HA hosts; per class the typical VM (vCPU, GB per vCPU), overcommit, reservation and expected concurrent peak.
- Supply per host, by model (usable capacity: [`sp5-framework/capacity/supply`](supply.md)):
  - utilization: threads - hypervisor threads; DRAM - hypervisor GB;
  - allocation: the utilization supply × the class overcommit;
  - reservation: CPU cores × base GHz - system reservation, because a reservation is capped at the base clock; memory as in utilization.
- Demand per model: allocation = configured size; reservation = configured size × reserved share; utilization = configured size × expected concurrent peak.
- Six numbers per host: three models × CPU and memory. The host is full at the first to reach 100%; it decides how many VMs fit and which resource binds.
- Mixed classes: in the allocation model each class's demand is divided by its overcommit ratio, so a Gold vCPU weighs 3 Bronze vCPUs.
- HA: not subtracted per host. A cluster carries load on hosts - HA hosts; the HA hosts are added on top.
- Aim for 90-110% at planning: the plan is an estimate, and reality will vary. Contention cannot be modelled; in a running cluster, read Cluster Performance (%).
- Example: 64 cores, 2.5 GHz, 768 GB, Hyper-Threading on, overhead 14 threads and 64 GB. Silver VMs of 8 vCPU and 32 GB: allocation CPU 28.5, memory 26.4; reservation CPU 30, memory 44; utilization CPU 28.5, memory 25.9. 25 VMs fit per host; memory utilization binds.

## Misconceptions
- "Our Bronze plan of 3:1 shows red overcommit in Cluster Risk, so the plan is wrong" → the ratio is a planning input tied to price; Cluster Risk reads the running cluster, where Bronze is expected to score higher than Gold.
- "Keep exactly the same step on every row" → the step is a goal, not a rule.
- "Gold gets 2x the performance of Silver" → Gold gets about half the chance of contention; speed is not doubled.
- "Each class has a minimum VM Performance (%)" → the promise is relative contention (1x, 2x, 3x). One set of KPI levels for every class; compare the class groups.
- "Set the Gold reservation on each VM" → set it on the resource pool; VM-level reservation changes HA admission control and restart.
- "A Bronze cluster at 90% CPU is overloaded" → a mostly Bronze cluster is planned to run near 100% of its usable threads; contention decides: read Cluster Performance (%).
- "Overcommit ratio per core" → the plan counts threads, not cores; 3:1 per thread is 6:1 per core with Hyper-Threading.
- "The host fits as many VMs as its allocation allows" → allocation is one of six numbers; at planning, memory utilization or CPU reservation often binds first.
- "Memory tiering lets Silver and Bronze reach their memory ratio" → the ratio is against DRAM; NVMe is about 1,000x slower and is left out of the plan. Tiering is measured in the running stage, with its own risk and performance signals ([`vsphere/technology/memory/concepts/memory-tiering`](../../vsphere/technology/memory/concepts/memory-tiering.md)).

## Metadata
```yaml
id: sp5-framework/capacity/class-of-service-planning
retriever_guide: how-it-works
scope: sp5-framework
technology:
- cpu
- memory
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
internal_derive:
- sp5-framework/capacity/supply
- sp5-framework/capacity/demand
- sp5-framework/capacity/overcommit
related:
- sp5-framework/capacity/capacity-management
- sp5-framework/concepts/class-of-service
- sp5-framework/performance/noisy-neighbour
- sp5-framework/capacity/vm-size
- sp5-framework/capacity/host-spec-from-class-of-service
- sp5-framework/performance/kpi-vs-sla
- vsphere/object-types/cluster/models/cluster-risk
- vsphere/object-types/vm/vm-performance
images:
  - path: images/class-of-service-planning-values-vm-reservation-allocation-utilization-table.png
    product: [vsphere]
    object: [ClusterComputeResource, ResourcePool]
    topic: 'Class of service planning values'
    image_type: table
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download); Capacity Planning Stage (spreadsheet, 2026-11-11)
  path: 'Capacity Management > Capacity Model > Planning Phase; Planning Template'
corrections:
- 'Section ''Example implementation'': the book table gives a minimum Performance (%) per class (Gold 99.5%, Silver 99%, Bronze 98%), labelled KPI, not SLA. Not used: the KPI has no class of service, and the numbers sit on the older Performance (%) scale (100 minus the share of time waiting), not on the banded score (Q162).'
review_notes:
- 'Section ''Example implementation'': Silver 2:1 and Bronze 3:1 per thread are 4 and 6 vCPUs per core with Hyper-Threading; Cluster Risk (%) marks 3-4 vCPUs per core as red, so a Bronze cluster built to this plan scores red on the CPU overcommit row. Memory 1.4:1 stays below the memory red band (1.8-2.2).'
status: draft
```
