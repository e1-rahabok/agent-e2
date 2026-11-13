# VM footprint sizing

## Purpose
- Size what the VM costs the underlying ESXi: its footprint.
- A narrow use case: useful mainly when the VM migrates to a different ESXi host or cluster.
- For the usual sizing question (how many vCPU and how much memory the workload demands), size the Guest OS (Windows or Linux) instead: [`guest-os/system/concepts/guest-os-sizing`](../../guest-os/system/concepts/guest-os-sizing.md).

- One of two sizing jobs. The other is Guest OS sizing (Windows or Linux demand). There is no single "VM rightsizing": see [`guest-os/system/concepts/guest-os-sizing`](../../guest-os/system/concepts/guest-os-sizing.md), section VM rightsizing: two jobs.
- Examples: migration to faster or slower CPUs, VMFS to vSAN (FTT policy), thin to thick disks.

## CPU
| Rule | Reason |
|---|---|
| Include Hyper-Threading | A thread with a busy sibling gets fewer cycles. |
| Include CPU frequency | Moving to a slower cluster can require more vCPUs. |
| Include contention | Runtime the VM demanded but the hypervisor blocked. Add Overlap: Used excludes it. |
| Include VM overhead | Significant in cases such as Fault Tolerance. |
| Exclude Guest OS queue | Transparent to the VM. |

```text
VM CPU Needed = (Sum over all vCPUs of (Used + Overlap + Co-stop + Ready + Other Wait) + System) / (20,000 × vCPU)
```
- System has no per-vCPU value: the physical core that does IO for the VM can do it for more than one vCPU, so it cannot be split per vCPU. So the per-vCPU states are summed one by one, and System is added once, at VM level.
- 20,000 is the 20-second real-time sample in milliseconds: the summation counters are in ms per sample.
- Dividing by 20,000 × vCPU gives the share of the VM's vCPU capacity, 0-1. Above 1 is possible: System and Overlap are on top of the vCPUs.
- Example: 4 vCPUs, each with 10,000 ms of Used + Overlap + Co-stop + Ready + Other Wait, and 2,000 ms System: (40,000 + 2,000) / 80,000 = 0.525, so 52.5% of 4 vCPUs.
- Express in GHz (utilization model) and vCPU (allocation model).
- GHz: multiply by the nominal (static) clock speed. Required when migrating to hosts with a different clock speed.
- Used, not Run, carries the work. Run is time on a physical thread: the same work takes more Run on a slower clock or on a core shared with a busy Hyper-Threading sibling. Used is converted to ms at the nominal clock and adjusted for the actual frequency and for Hyper-Threading, so Used ÷ 20,000 × nominal GHz is the work in GHz. See [`vsphere/technology/cpu/metrics/virtual-motherboard/used`](../../vsphere/technology/cpu/metrics/virtual-motherboard/used.md).
- Ready and Co-stop are runtime the vCPUs demanded and did not get. A co-stopped vCPU had work but was held back for its siblings, so Co-stop is unmet demand as much as Ready. Leaving them out sizes the VM to what it got, not to what it demanded.
- System is VMkernel work the target host must also supply for the VM, so it counts in the footprint in GHz and in vCPU equivalents.
- VM-level Used already holds System. Add System only when Used is the sum of the vCPU instances; do not add it twice to the VM-level value.
- vCPUs needed on the target = footprint in GHz ÷ nominal clock of the target, rounded up, before headroom. The ratio holds when both clusters have the same CPU generation, power policy and Hyper-Threading load.
- The footprint is the load on the infrastructure. Whether the Guest OS has enough vCPUs (its run queue) is a separate check: [`guest-os/system/concepts/guest-os-sizing`](../../guest-os/system/concepts/guest-os-sizing.md).
- CPU generation and speed (for example SPEC CPU 2017) can refine sizing. Risk: an application that prefers many slow threads may perform worse with fewer, faster vCPUs.

## Memory
```text
VM Memory Needed = Consumed + Overhead + Swapped + Compressed + Ballooned
```
- Include all pages tied to the VM.
- TPS effects likely persist after vMotion and are included. Intra-VM and inter-VM sharing cannot be separated.
- Memory contention is excluded: it measures speed, not space.

## Misconceptions
- "Footprint = Guest OS size" → the footprint adds HT, frequency, contention and overhead.
- "Run ÷ 20,000 gives the vCPUs to keep on the new cluster" → Run counts time, not work. On a slower clock the same work takes more time; size from Used in GHz and divide by the target clock.
- "Co-stop is scheduling skew, not demand" → a co-stopped vCPU had runtime to do and was stopped; add Co-stop with Ready.
- "System is overhead, so it does not count toward the vCPU count" → the target host runs it for the VM; it is part of the footprint.

## Metadata
```yaml
id: sp5-framework/capacity/vm-footprint-sizing
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
- VirtualMachine
internal_derive:
- vsphere/technology/cpu/metrics/virtual-motherboard/used
related:
- guest-os/system/concepts/guest-os-sizing
- vsphere/technology/memory/metrics/virtual-motherboard/consumed
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: 'Consumer Objects > Capacity: Guest OS > VM Footprint'
corrections:
- 'Sections ''Purpose'' and ''CPU'': formula grouping and the narrow use case. The book prints System / 20,000 without the grouping.'
review_notes: []
status: draft
```
