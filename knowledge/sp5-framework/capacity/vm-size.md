# VM size

## Host limits on VM size
- The right size of a VM depends on the ESXi host it runs on and on the CPU and NUMA architecture of that host, not on the VM alone.
- A large VM is harder to schedule: its vCPUs compete for threads at the same time, and a VM larger than a NUMA node spans nodes and reads remote memory ([`vsphere/technology/cpu/concepts/numa`](../../vsphere/technology/cpu/concepts/numa.md), [`vsphere/technology/cpu/concepts/virtual-numa`](../../vsphere/technology/cpu/concepts/virtual-numa.md)).
- A VM large against its host raises contention even at low utilization: the monster VM of Cluster Risk ([`vsphere/object-types/cluster/models/cluster-risk`](../../vsphere/object-types/cluster/models/cluster-risk.md), section Monster VM).
- The CPU overcommit ratio is per physical thread, not per core ([`sp5-framework/capacity/overcommit`](overcommit.md)).

## Maximum VM size
Below is what is technically possible. This is the technical ceiling, counted in threads. The size per class (section Size per class) binds far below it. Aim to run within one L3 domain and one NUMA node: at default BIOS settings an AMD CCD is an L3 boundary, not a NUMA boundary.
| Overcommit Ratio | Maximum VM size |
|---|---|
| 1:1 | ESXi physical threads - hypervisor overhead |
| 2:1 | Above, divided by 2 |
| 3:1 | Above, divided by 3 |

- Hypervisor includes kernel modules of vSAN and NSX.
- 1:1: mind the Hyper-Threading throughput penalty and NUMA, as the VM vCPU will be sharing physical cores
- 2:1: two large VMs on one host each demand whole cores, and both get the 37.5% Hyper-Threading penalty.
- 3:1 is the highest CPU overcommit of any class (Bronze); higher ratios are not used.
- These effects follow from overcommit on shared resources, not from a defect in vSphere.

## Size per class
- Not a fixed number: it follows the CPU architecture of the host. A VM size calculator is planned after release 1.0.
- General advice, counted in vCPUs against the physical cores of one CPU building block: an AMD EPYC CCD or an Intel Xeon compute tile. Cores, not threads: a vCPU on a busy sibling thread pays the Hyper-Threading penalty.

| Class | Maximum vCPU | Memory |
|---|---|---|
| Gold | 2 × the cores of one CCD or compute tile | 4 GB per vCPU |
| Silver | 1 × | 4 GB per vCPU |
| Bronze | 0.5 × | 4 GB per vCPU |

- Memory stays within the memory of the VM's NUMA node; more fetches remote memory across the fabric.
- Why: NUMA optimization keeps the vCPU threads next to the memory controllers they use. Threads that cross a die boundary to reach remote memory spend clock cycles crossing the fabric, and the application slows.
- The unit is the L3 cache domain. On most EPYC generations one CCD is one L3 domain; on Zen 4c a 16-core CCD holds two 8-core L3 domains (CCX), so the CCX is the unit. On Zen 5c one 16-core CCX fills a CCD, so the CCD is the unit again.
- Intel Xeon: a compute tile is its own L3 domain and NUMA node only with sub-NUMA clustering (SNC) on. With SNC off the socket shares one L3 and one NUMA node, so the tile is a softer boundary than an AMD CCD.
- Two limits, both read from the host: above the L3 domain a VM pays a cache cost; above the cores of its NUMA node it reads remote memory. With NPS-1 an AMD NUMA node is the whole socket (up to 128 cores on Zen 5, 192 on Zen 5c).

### Example: AMD EPYC 9996 in NPS2
- 256 cores per socket: 8 CCDs of 32 cores; 2 IODs; 16 DDR5 channels, 8 per IOD.
- NPS2: 2 NUMA nodes per socket, each with 128 cores (4 CCDs) and half of the socket's memory.
- 32 vCPU: fits one CCD, the best case. One NUMA node; all vCPUs share one L3; local memory is the half behind its IOD (1 TB of a 2 TB socket).
- 64 vCPU: needs two CCDs. Keep them behind the same IOD, inside one NUMA node; size memory within that node (at most half of the socket's memory), or ESXi fetches remote memory from the other IOD.
- 64 vCPU in a 128-core node: the guest sees one NUMA node, a uniform machine; no vNUMA topology is needed.
- Cache: an L3 hit stays inside its CCD; data shared between the two CCDs moves through the IOD. Slower than a hit in the same L3, far faster than a remote NUMA access; guest schedulers place threads to reduce it.

## Size as a class of service fence
- In a mixed cluster (Gold, Silver, Bronze on the same hosts), a lower class must not become the noisy neighbour of a higher one. Mixed clusters are common but a compromise: the design is one class per cluster ([`sp5-framework/capacity/demand`](demand.md), section Overcommit: several classes).
- Technique: Gold is entitled to larger VM configurations; Bronze is kept small. A small Bronze VM cannot take a large share of a host's threads at once, so its peaks hurt Gold less.
- The class sets both the overcommit ratio and the maximum VM size, so the maximum VM size of a class follows from section Size per class, bounded by the technical ceiling of section Maximum VM size ([`sp5-framework/concepts/class-of-service`](../concepts/class-of-service.md), [`sp5-framework/performance/noisy-neighbour`](../performance/noisy-neighbour.md)).

## Misconceptions
- "A VM can be as large as its host" → by count at 1:1, yes; but the VM then pays the Hyper-Threading penalty and spans NUMA nodes. Size it against the host's NUMA node.
- "Bronze is cheap, so a Bronze VM can be any size" → a large Bronze VM is the noisy neighbour of a mixed cluster; keep Bronze small and give large sizes to Gold.
- "Bronze at 3:1 per thread is 3:1 per core" → 6:1 per core: each core has two threads, so a ratio per core is twice the ratio per thread.
- "Low utilization, so the large VM is harmless" → a monster VM raises contention risk at low utilization.
- "The maximum VM size per class is a fixed vCPU number" → it follows the host's CPU: count CCDs or compute tiles of the host the VM runs on.
- "A VM inside one NUMA node needs no care" → memory larger than the node's share still comes from the other node.

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
- 'To check: Section ''Size per class'', Intel: compute tile as L3 domain and NUMA node only with SNC on, against the Intel Xeon 6 documentation.'
- 'To check: Section ''Example: AMD EPYC 9996'': the CPU figures (8 CCDs of 32 cores, 2 IODs, 16 channels) against the AMD product specification.'
status: draft
```
