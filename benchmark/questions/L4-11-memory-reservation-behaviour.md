# Memory reservation behaviour

## Prompt
- Reservation, shares and limit are the 3 resource management controls.

Choose the correct statements:

- A. Memory reservation differs from CPU reservation because it is sticky. Once used, the consumed page can stay for days. It does not immediately become available to other VMs.
- B. Use reservation at VM level sparingly: it directly limits your ability to overcommit. It also affects DRS.
- C. Only VMs have reservation. A resource pool has no setting of its own and aggregates its member VMs.
- D. Kernel reservation means the amount is not available to VMs, whether or not the kernel actually uses it.
- E. With vSAN, NSX and ESXi, total kernel reservation is likely much higher than kernel actual utilization, even when ESXi is highly utilized, to protect the kernel.

## Likely wrong answer
D (reservation assumed to block memory before use) or C.

## Expected key points
- Answer: A, B.
- A: memory is a form of storage; CPU is running instructions.
- B: correct.
- C is wrong: plan both reservation and share settings at resource pool level and VM level as one design.
- D is wrong: reserved memory must be used first before it is held.
- E is wrong: utilization can exceed reservation.

## Notes
- Previous id: vsphere-memory-005 (renamed 2026-11-05).
- The knowledge base (`vsphere/foundations/overhead`) says kernel memory reservation stays steady even when kernel use drops 90%. Check E's key against it during review.

## Metadata
```yaml
id: "0024"
title: "Memory reservation behaviour"
product: [vsphere]
technology: [memory]
input: [text]
task: judge-setting
knowledge:
  - vsphere/foundations/resource-controls
  - vsphere/technology/memory/metrics/host/reservation
  - vsphere/technology/memory/concepts/memory-as-storage
  - vsphere/foundations/overhead
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > Memory > Q4 Memory Reservation"
answer_type: deterministic
level: 400                      # author 2026-11-05
answer: [A,B]
trap: [C,D]
status: draft
```
