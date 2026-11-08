# Can this cluster take more VMs?

## Symptom
- A request to place N new VMs, or a project, on an existing vSphere cluster; or to upsize a VM on it.
- The answer is yes or no, with the resource that limits it and the reason.
- A closed cluster accepts no new VM and no VM upsize. Once capacity, performance and risk metrics exist, the decision can be automated: self-driving capacity management.

## Flow
```mermaid
flowchart TD
  S1[1. Cluster state green and HA met?] -->|no| E1[No: fix state first]
  S1 -->|yes| S2[2. Overcommit?]
  S2 -->|no| S3[3. Allocation below usable capacity?]
  S3 -->|no| E3[No: closed]
  S3 -->|yes| S6
  S2 -->|yes| S4[4. Capacity Remaining or Performance red?]
  S4 -->|yes| E4[No: closed]
  S4 -->|no| S5[5. Both orange: Risk above the limit for this environment?]
  S5 -->|yes| E5[No: closed]
  S5 -->|no| S6[6. Do the new VMs fit: reservations, overcommit, size?]
  S6 -->|no| E6[No, or change the VM design]
  S6 -->|yes| S7[7. Hosts balanced?]
  S7 --> E7[Yes, with the limiting resource and time remaining]
```

![Cluster closure: Overcommit? No → allocation red closes; Yes → utilization red closes, contention red closes, contention and utilization both orange → risk: red closes in non-production, orange closes in production. Risk is a leading indicator; a critical cluster has a lower risk threshold](../images/cluster-closure-decision-flow-diagram.png)

## Checks, in order
1. Cluster state and HA (ClusterComputeResource). Yellow or red, or HA no longer meets its failover capacity → no; fix the state first. Admission control counts reservations, not usage. See `vsphere/object-types/cluster/concepts/admission-control-and-cluster-state`. Green → step 2.
2. Overcommit (ClusterComputeResource). Cluster planned without overcommit (1:1) → step 3. Overcommitted → step 4.
3. Allocation (ClusterComputeResource). Allocation of powered-on VMs, plus the new VMs, against usable capacity (total − HA − hypervisor − buffer; `operations-management/capacity/capacity-model`). Allocation reaches usable capacity → no: closed. Below → step 6.
4. Capacity and performance (ClusterComputeResource). Either one red → no: closed.
   - Capacity Remaining (%): projected 3 days ahead. Production: red below 10%, orange below 20%. Non-production: red below 15%, orange below 30%.
   - Cluster Performance (%), 95th percentile of the last 24 hours (`vcf-operations/kpis/cluster-performance`). Production: red below 40%, orange below 60%. Non-production: red below 20%, orange below 40%.
   - Neither red → step 5.
5. Risk (ClusterComputeResource). Only when capacity and performance are both orange. Cluster Risk (%), 95th percentile of the last 12 hours (`vcf-operations/kpis/cluster-risk`):
   - production: above 50% (orange or red) → no: closed;
   - non-production: above 75% (red) → no: closed.
   - Read the sub-metrics, not only the score: a worse sub-metric can lower the score.
   - Below the limit, or capacity and performance not both orange → open → step 6.
6. Fit of the new VMs (ClusterComputeResource, VirtualMachine).
   - Reservations: they must fit unreserved capacity; leave at least 10% unreserved (`vsphere/object-types/cluster/concepts/admission-control-and-cluster-state`).
   - Overcommit: the CPU and memory overcommit rows of Cluster Risk after the new VMs (`vcf-operations/kpis/cluster-risk`).
   - Size: a monster VM (more than 50% of a host's physical cores, or more than 40% of its DRAM or 256 GB, whichever is smaller) raises contention risk even at low utilization (`vcf-operations/kpis/cluster-risk`, section Monster VM).
   - Memory: ballooning starts only near 99% host use, so set the normal ceiling from the HA case; with 12 hosts sized for 11, 99% × 11 / 12 = 90.75% (`vsphere/technology/memory/concepts/host-memory-states`).
   - Any no → no, or change the VM design. All fit → step 7.
7. Balance (ClusterComputeResource). Inter-host imbalance red or pink → rebalance first: a hot host suffers while the cluster has room (`vcf-operations/metrics/cluster/cpu-inter-host-imbalance`). Then answer yes, with the resource that fills first and the time remaining from the projection (`operations-management/capacity/capacity-model`, section Capacity Remaining and Time Remaining).

![Closure thresholds. Capacity Remaining (projected 3 days ahead): production red below 10% orange below 20%; non-production red below 15% orange below 30%. Performance (%) (95th percentile, last 24 hours): production red below 40% orange below 60%; non-production red below 20% orange below 40%. Risk (%) (95th percentile, last 12 hours): production above 50%, non-production above 75%](../images/cluster-closure-thresholds-prod-vs-non-prod-table.png)

## Why this order
- State first: in yellow or red, reservations are not met; any capacity number is built on a broken base.
- Overcommit next: without overcommit, utilization, reservation and contention do not decide; allocation against usable capacity is the only input (`operations-management/capacity/capacity-dimensions`).
- Capacity and performance before risk: either one red is enough to close. Risk is a leading indicator that buys time; it decides only the grey case where both are orange.
- Production closes on a lower risk than non-production: a critical cluster has a lower risk threshold.
- Contention overrides utilization: a cluster that cannot serve its current VMs has no remaining capacity, whatever utilization says.
- Fit before balance: balance is fixed by DRS or by moving VMs; a VM that cannot fit is a design question.

## How to read the result
- No at step 1 → the answer is about the current state, not about the new VMs.
- No at steps 3 to 5 → the cluster is closed: name the dimension (allocation, capacity remaining, performance, risk) and the resource (CPU, memory, storage).
- Yes → give the limiting resource and how long the room lasts.

## Traps
- "Cluster CPU at 40%, so there is room" → check contention, risk and HA headroom; one hot host can be full.
- "Memory consumed at 85% means the cluster is full" → consumed is utilization; check saturation rows and contention, and the HA ceiling.
- "Capacity Remaining is orange, so the cluster is closed" → orange alone does not close it; both capacity and performance orange sends the decision to risk.
- "Risk is red, so close the cluster" → risk decides only when capacity and performance are both orange; risk alone is a warning.
- "A cluster without overcommit closes on utilization" → without overcommit, only allocation against usable capacity closes it.
- "Cluster Risk fell after the last VMs, so the risk is lower" → read the sub-metrics; a worse sub-metric can lower the score.
- "The VMs have no reservation, so admission control passes them" → their overhead memory is still checked.

## Metadata
```yaml
id: operations-management/capacity/diagnosis/can-cluster-take-more-vms
retriever_guide: what-to-check
scope: operations-management
technology:
- cpu
- memory
- storage
- system
pillar:
- capacity
- performance
product:
- vsphere
- vcf-operations
object:
- ClusterComputeResource
internal_derive:
- vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
- operations-management/capacity/capacity-dimensions
- vcf-operations/kpis/cluster-performance
- vcf-operations/kpis/cluster-risk
- operations-management/capacity/capacity-model
- vcf-operations/kpis/cluster-consumption
- vsphere/technology/memory/concepts/host-memory-states
- vcf-operations/metrics/cluster/cpu-inter-host-imbalance
related:
- vsphere/object-types/cluster/overview-what-to-monitor
- operations-management/capacity/class-of-service-planning
images:
  - path: ../images/cluster-closure-decision-flow-diagram.png
    product: [vsphere, vcf-operations]
    object: [ClusterComputeResource]
    topic: 'Cluster closure'
    image_type: diagram
  - path: ../images/cluster-closure-thresholds-prod-vs-non-prod-table.png
    product: [vcf-operations]
    object: [ClusterComputeResource]
    metric: ['Capacity Remaining', 'Cluster Performance', 'Cluster Risk']
    image_type: table
source:
  document: PART 1 - Concepts of Operations Management.docx; knowledge base synthesis of the files in internal_derive
  path: 'Capacity Management > Capacity Model > Cluster Closure; Logic. Pages 109-110.'
corrections: []
review_notes:
- 'Steps 2 to 5 and the closure thresholds follow the book (Cluster Closure, Logic) from 2026-11-07. Steps 1, 6 and 7 were drafted by Claude 2026-11-06 from the files in internal_derive (architecture review 2026-11-06, section 3.3); the full order is still to be confirmed by the author (Q061).'
- 'Step 4: non-production closes at a higher Capacity Remaining (15%, 30%) than production (10%, 20%), while it closes later on performance and risk (Q121).'
- 'Step 4: the Performance (%) closure values (production red below 40%) are far below the class-of-service minimum VM Performance (%) of 98-99.5% (operations-management/capacity/class-of-service-planning). Different metrics (cluster KPI vs VM KPI); confirm (Q122).'
- 'Step 5: the book text says the risk check runs when capacity and performance are both orange. One orange and one green is not stated; read as open (Q121).'
status: draft
```
