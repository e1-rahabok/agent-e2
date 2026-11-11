# VM size

## Size is set by the host
- The right size of a VM depends on the ESXi host it runs on and on the CPU and NUMA architecture of that host, not on the VM alone.
- A large VM is harder to schedule: its vCPUs compete for threads at the same time, and a VM larger than a NUMA node spans nodes and reads remote memory ([`vsphere/technology/cpu/concepts/numa`](../../vsphere/technology/cpu/concepts/numa.md), [`vsphere/technology/cpu/concepts/virtual-numa`](../../vsphere/technology/cpu/concepts/virtual-numa.md)).
- A VM large against its host raises contention even at low utilization: the monster VM of Cluster Risk ([`vsphere/object-types/cluster/models/cluster-risk`](../../vsphere/object-types/cluster/models/cluster-risk.md), section Monster VM).
- The CPU overcommit ratio is per physical thread, not per core ([`sp5-framework/capacity/overcommit`](overcommit.md)).

## Maximum VM size
| Overcommit Ratio | Maximum VM size |
|---|---|
| 1:1 | ESXi logical CPUs (48 cores, 96 threads → 96) |
| 2:1 | 0.5 × logical CPUs; 0.4 × for 20% headroom |
| 3:1 | 0.33 × logical CPUs (96 threads → 32) |

- 1:1: mind the Hyper-Threading throughput penalty and NUMA.
- 2:1: two large VMs on one host each demand whole cores, and both get the 37.5% Hyper-Threading penalty.
- 3:1 is the highest CPU overcommit of any class (Bronze); higher ratios are not used.
- These effects follow from overcommit on shared resources, not from a defect in vSphere.

## Size as a class of service fence
- In a mixed cluster (Gold, Silver, Bronze on the same hosts), a lower class must not become the noisy neighbour of a higher one. Mixed clusters are common but a compromise: the design is one class per cluster ([`sp5-framework/capacity/demand`](demand.md), section Overcommit: several classes).
- Technique: Gold is entitled to larger VM configurations; Bronze is kept small. A small Bronze VM cannot take a large share of a host's threads at once, so its peaks hurt Gold less.
- The class sets both the overcommit ratio and the maximum VM size, so the maximum VM size of a class follows from its ratio in the table above ([`sp5-framework/concepts/class-of-service`](../concepts/class-of-service.md), [`sp5-framework/performance/noisy-neighbour`](../performance/noisy-neighbour.md)).

## Misconceptions
- "A VM can be as large as its host" → by count at 1:1, yes; but the VM then pays the Hyper-Threading penalty and spans NUMA nodes. Size it against the host's NUMA node.
- "Bronze is cheap, so a Bronze VM can be any size" → a large Bronze VM is the noisy neighbour of a mixed cluster; keep Bronze small and give large sizes to Gold.
- "Bronze at 3:1 per thread is 3:1 per core" → 6:1 per core: each core has two threads, so a ratio per core is twice the ratio per thread.
- "Low utilization, so the large VM is harmless" → a monster VM raises contention risk at low utilization.

## Metadata
```yaml
id: sp5-framework/capacity/vm-size
retriever_guide: how-it-works
scope: sp5-framework
technology:
- cpu
- memory
pillar:
- capacity
- performance
product:
- vsphere
- vcf-operations
object:
- VirtualMachine
- HostSystem
internal_derive:
- vsphere/technology/cpu/concepts/numa
- vsphere/object-types/cluster/models/cluster-risk
- sp5-framework/capacity/overcommit
related:
- sp5-framework/concepts/class-of-service
- sp5-framework/performance/noisy-neighbour
- sp5-framework/capacity/class-of-service-planning
- sp5-framework/capacity/rightsizing
- vsphere/technology/cpu/concepts/virtual-numa
- vsphere/technology/cpu/concepts/hyper-threading
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: 'Noisy Neighbour > Maximum VM size; Class of Service'
corrections: []
review_notes:
- 'To check: Section ''Maximum VM size per overcommit'': the size is counted in logical CPUs (threads); whether a ceiling at the physical cores applies at 1:1 (Q111 a).'
- 'To check: Section ''Size is set by the host'': the NUMA node and L3 domain limits per CPU family (Q125).'
status: draft
```
