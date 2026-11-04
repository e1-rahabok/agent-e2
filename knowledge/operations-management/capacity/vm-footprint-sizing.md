# VM footprint sizing

## Purpose
- Size what the VM costs the underlying platform, for example to place or migrate it.

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
VM CPU Needed = (Used + Overlap + Co-stop + Ready + Other Wait) + System / 20,000
```
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
corrections: []
review_notes:
- 'Section ''CPU'': the formula''s grouping is unclear (System / 20,000 or the whole sum / 20,000), and VM-level Used already includes System. Open question in project/author-questions.md.'
status: draft
```
