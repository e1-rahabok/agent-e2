# ESXi host specification from class of service

## Why Day 2 sets the hardware
- The host specification is best chosen with two Day 2 inputs: the typical VM of each class (vCPU, GB per vCPU) and the planning settings of the class (overcommit, reservation, expected concurrent peak).
- CPU, memory and storage are sold together: a VM consumes all three. A host with more of one than the others can sell leaves capacity unsold.
- Day 2 → Day 0 → Day 1: [`sp5-framework/concepts/purpose-driven-architecture`](../concepts/purpose-driven-architecture.md).
- One class per cluster is the design, so each class gets its own host specification ([`sp5-framework/capacity/demand`](demand.md), section Overcommit: several classes).

## Method
- CPU decides how many VMs of the class fit on the host: the first of its three CPU numbers to reach 100% ([`sp5-framework/capacity/class-of-service-planning`](class-of-service-planning.md), section Planning calculator).
- Memory is bought to match those VMs. Each VM needs the largest of its three memory needs.

```text
VMs per host   = min(CPU allocation, CPU reservation, CPU utilization)
Memory per VM  = max(configured GB / memory overcommit,
                     configured GB × memory reservation,
                     configured GB × expected memory concurrent peak)
Host RAM (GB)  = VMs per host × memory per VM + hypervisor memory
```
- CPU allocation = (threads − hypervisor threads) × CPU overcommit / vCPU per VM. CPU reservation = (cores × base GHz − system reservation) / (vCPU × reserved share × base GHz). CPU utilization = (threads − hypervisor threads) / (vCPU × expected CPU concurrent peak).
- Overcommit is per physical thread, not per core: with Hyper-Threading the two differ by 2x ([`sp5-framework/capacity/overcommit`](overcommit.md)).
- Hypervisor share: VMkernel, vSAN, NSX, vSphere Replication and kernel IO work run on every host. Planning default: 14 threads and 64 GB per host (catalog rows `planning-hypervisor-*`); measure the real value ([`vsphere/architecture/overhead`](../../vsphere/architecture/overhead.md)).
- 4 GB per vCPU is a planning guideline. Customers may buy more or less memory per vCPU: measure the real ratio in VCF Operations.
- Memory tiering is not counted: the plan sizes DRAM. Tiering belongs to the running stage ([`sp5-framework/capacity/overcommit`](overcommit.md), section Per resource).
- The `capacity_plan` tool computes it: give cores, base GHz and the class, without RAM.

## Example: 64 cores, 2.5 GHz, Hyper-Threading on
| Class | Typical VM | VMs per host (CPU binds on) | Memory per VM (binds on) | Host RAM |
|---|---|---|---|---|
| Gold | 16 vCPU, 64 GB | 7.1 (allocation) | 64 GB (allocation, reservation) | 520 GB |
| Silver | 8 vCPU, 32 GB | 28.5 (allocation, utilization) | 27.2 GB (utilization) | 839 GB |
| Bronze | 4 vCPU, 16 GB | 43.9 (utilization) | 13.6 GB (utilization) | 660 GB |

- Supply: 128 threads − 14 = 114 threads; 64 × 2.5 − 10 = 150 GHz reservable.
- Gold: 114 threads at 1:1 hold 7.1 VMs of 16 vCPU; each needs its full 64 GB (1:1, 100% reserved). 456 + 64 = 520 GB.
- Silver: 114 × 2 / 8 = 28.5 VMs, and 114 / (8 × 50%) = 28.5 too. Each needs 85% of 32 GB = 27.2 GB at peak, more than 32 / 1.2 = 26.7 GB. 775 + 64 = 839 GB.
- Bronze: 114 / (4 × 65%) = 43.9 VMs, far below 3:1 allocation (85.5). Each needs 85% of 16 GB = 13.6 GB. 596 + 64 = 660 GB.

## Reading the example
- Silver needs the most RAM, not Bronze. Bronze VMs peak at 65% of their vCPUs, so CPU utilization fills the host at 175 vCPU, long before 3:1 allocation (342 vCPU).
- Sizing on allocation alone (vCPU sold × GB per vCPU / memory overcommit + hypervisor) overbuys for Bronze: 342 × 4 / 1.4 + 64 = 1,041 GB, 381 GB that the plan never uses.
- Gold takes the least RAM: 1:1 sells the fewest vCPUs per host, and RAM follows the vCPUs sold.
- Round up to a DIMM configuration the server supports. Less RAM than the match makes memory bind first: Silver on 768 GB fits 25.9 VMs instead of 28.5, 9% fewer.
- The answer moves with the planning settings. A higher expected CPU peak lowers the VMs per host and the RAM with them; recompute when the class settings change.
- Licensing: VCF 9 is licensed per physical core, with a minimum of 16 cores per CPU. No core count above 16 per CPU has a licence advantage; keep Hyper-Threading on, since the licence counts cores and capacity counts threads.

## Misconceptions
- "Buy as much RAM as the host takes; memory is cheap" → RAM is sold with vCPUs. Beyond the VMs the CPU can hold × their memory need + the hypervisor share, it cannot be sold.
- "Gold hosts take the most RAM" → Gold sells the fewest vCPUs per host, so it takes the least RAM.
- "Bronze overcommits the most, so Bronze hosts need the most RAM" → Bronze fills on CPU utilization long before its allocation; sized on allocation, a Bronze host overbuys RAM.
- "4:1 overcommit means the same capacity on every host" → say whether it is per core or per physical thread; with Hyper-Threading the two differ by 2x.
- "All cores of the host can be sold" → vSAN, NSX, replication and kernel IO work take a share of every host; subtract it first.
- "A 64-core host maximizes the licence" → VCF 9 counts cores, with a 16-core minimum per CPU; core count above 16 per CPU has no licence sweet spot.

## Metadata
```yaml
id: sp5-framework/capacity/host-spec-from-class-of-service
retriever_guide: how-it-works
scope: sp5-framework
technology:
- cpu
- memory
pillar:
- capacity
- value
product:
- vsphere
- vsan
- nsx
object:
- HostSystem
internal_derive:
- sp5-framework/concepts/purpose-driven-architecture
- sp5-framework/capacity/class-of-service-planning
related:
- sp5-framework/capacity/capacity-management
- sp5-framework/capacity/overcommit
- sp5-framework/capacity/supply
- sp5-framework/concepts/class-of-service
- sp5-framework/concepts/iaas-business
- vsphere/architecture/overhead
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download); Capacity Planning Stage (spreadsheet, 2026-11-11)
  path: 'Your Private Cloud > Purpose-Driven Architecture > Begin with The End in Mind > Day 0 | Day 1 | Day 2; Service Level Agreement > Price & SLA; Planning Template'
corrections:
- 'Section ''Method'': the book sizes RAM from the vCPUs sold at the allocation ratio (Silver 4:1 per core, memory 2:1: 512 GB). The class settings are now per thread with three models; the RAM follows the binding CPU model.'
review_notes:
- 'Section ''Reading the example'', licensing: per-core licensing with a 16-core minimum per CPU, Broadcom KB 313548 (https://knowledge.broadcom.com/external/article/313548) and the VCF 9.0 Licensing Model page (https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-0/licensing/licensing-overview/licensing-model.html).'
status: draft
```
