# CPU reservation behaviour

## Prompt
- Reservation, shares and limit are the 3 resource management controls.
- Sometimes you need a reservation on a VM or a resource pool.

Choose all the correct statements:

- A. Total reservation at ESXi level is capped at the base nominal clock speed. Because of Turbo Boost, you cannot fully reserve the total possible capacity.
- B. CPU reservation only comes into play during contention. Without contention, the reservation is not used.
- C. VM CPU reservation is not sticky. The moment the vCPU stops using it, it is immediately available to other VMs.
- D. CPU reservation is set in Hertz, not vCPU, because what is reserved is CPU cycles, not a core or thread.
- E. You can overcommit CPU reservation because it is not sticky. Total reservation of all VMs can exceed ESXi capacity.
- F. CPU reservation applies only to VMs. The ESXi kernel has no reservation because kernel processes have higher priority.
- G. With vSAN, NSX and ESXi, total kernel reservation is likely much higher than kernel actual utilization, even when ESXi is highly utilized, to protect the kernel.

## Likely wrong answer
E (non-sticky read as overcommittable), F (kernel assumed to need no reservation), G.

## Expected key points
- Answer: A, B, C, D.
- A: only the base frequency is guaranteed. A conservative design.
- B: if there is enough for everyone, reservation is irrelevant.
- C: CPU is highly transient.
- D: the scheduler runs threads at different speeds, so cycles are reserved.
- E is wrong: HA and DRS use reservation before placing a VM (admission control).
- F is wrong: kernel modules such as vSAN and NSX can have reservations. A storage-only vSAN node fully reserves CPU, so CPU Demand is flat and high.
- G is wrong: utilization can exceed reservation.

## Notes

## Metadata
```yaml
id: vsphere-cpu-011
title: "CPU reservation behaviour"
product: [vsphere]
technology: [cpu]
input: [text]
task: judge-setting
knowledge:
  - vsphere/foundations/resource-controls
  - vsphere/technology/cpu/metrics/host/reserved-capacity
  - vsphere/foundations/overhead
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > CPU > Q8 Reservation"
answer_type: deterministic
level: 300                      # draft by Claude 2026-11-05; author to confirm (Q056)
answer: [A,B,C,D]
trap: [E,F,G]
status: draft
```
