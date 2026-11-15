# Memory reservation behaviour

## Prompt
- Reservation, shares and limit are the 3 resource management controls.

Choose the correct statements:

- A. Memory reservation differs from CPU reservation because it is sticky. Once used, the consumed page can stay for days. It does not immediately become available to other VMs.
- B. Use reservation at VM level sparingly: it directly limits your ability to overcommit. It also affects DRS.
- C. Only VMs have reservation. A resource pool has no setting of its own and aggregates its member VMs.
- D. The kernel reservation is set aside as physical pages at boot: VMs cannot consume that memory, even the part the kernel has not touched.
- E. With vSAN, NSX and ESXi, the kernel memory reservation is a cap: kernel memory use stays under it, even when ESXi is highly utilized.

## Likely wrong answer
D (reservation assumed to block memory before use) or C.

## Expected key points
- Answer: A, B.
- A: memory is a form of storage; CPU is running instructions.
- B: correct.
- C is wrong: plan both reservation and share settings at resource pool level and VM level as one design.
- D is wrong: reserved memory must be used first before it is held. The part the kernel has not consumed is free memory that VMs can consume; only admission control withholds the full kernel reservation, from VM reservations.
- E is wrong: utilization can exceed reservation. A reservation is a minimum, not a cap, and the kernel reservation covers host/system only; the NSX agents and vSAN services run in host/vim and host/opt, outside it.

## Notes
- D and E reworded 2026-11-15 (author questions Q201 and Q202, settled from the knowledge base and vendor documents). Old D ("the amount is not available to VMs, whether or not the kernel actually uses it") was true in the admission sense and false in the page sense; it now states the page sense, which the key marks false. The admission sense (the kernel reservation is not available for VM reservations) is true and not tested here. Old E (reservation "much higher than kernel actual utilization") could read true for memory: on the hosts measured, the kernel memory reservation sat above kernel use. It now states the reservation as a cap, which the key marks false. Key unchanged: A, B. Knowledge: [`vsphere/architecture/overhead`](../../knowledge/vsphere/architecture/overhead.md), section Memory metrics.

## Metadata
```yaml
id: "0024"
title: "Memory reservation behaviour"
product: [vsphere]
technology: [memory]
input: [text]
task: judge-setting
knowledge:
  - vsphere/architecture/resource-controls
  - vsphere/technology/memory/metrics/host/reservation
  - vsphere/technology/memory/concepts/memory-as-storage
  - vsphere/architecture/overhead
object: [vm, esxi, resource-pool]
tool: [none]
knowledge_main: vsphere/architecture/resource-controls
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > Memory > Q4 Memory Reservation"
answer_type: deterministic
level: 400                      # author 2026-11-05
answer: [A,B]
misconception: [C,D]
misconception_type: [provider-vs-consumer]
status: draft
```
