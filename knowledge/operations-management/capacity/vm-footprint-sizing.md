# VM footprint sizing

## Purpose
- Size what the VM costs the underlying ESXi: its footprint.
- A narrow use case: useful mainly when the VM migrates to a different ESXi host or cluster.
- For the usual sizing question (how many vCPU and how much memory the workload demands), size the Guest OS (Windows or Linux) instead: `guest-os/system/concepts/guest-os-sizing`.

- One of two sizing jobs. The other is Guest OS sizing (Windows or Linux demand). There is no single "VM rightsizing": see `guest-os/system/concepts/guest-os-sizing`, section No such thing as VM rightsizing.
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
- CPU generation and speed (for example SPEC CPU 2017) can refine sizing. Risk: an application that prefers many slow threads may perform worse with fewer, faster vCPUs.

## Memory
```text
VM Memory Needed = Consumed + Overhead + Swapped + Compressed + Ballooned
```
- Include all pages tied to the VM.
- TPS effects likely persist after vMotion and are included. Intra-VM and inter-VM sharing cannot be separated.
- Memory contention is excluded: it measures speed, not space.

## Traps
- "Footprint = Guest OS size" → the footprint adds HT, frequency, contention and overhead.

## Metadata
```yaml
id: operations-management/capacity/vm-footprint-sizing
retriever_guide: how-it-works
scope: operations-management
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
  document: PART 3 - Counters.docx
  path: 'Consumer Objects > Capacity: Guest OS > VM Footprint'
corrections:
- 'Sections ''Purpose'' and ''CPU'': formula grouping and the narrow use case from the author answer Q027 (2026-11-05). The book prints System / 20,000 without the grouping.'
review_notes:
- 'Section ''CPU'': divisor 20,000 × vCPU and the System reason from the author answer Q055 (2026-11-05), quoting the book.'
status: draft
```
