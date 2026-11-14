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
- F. The ESXi kernel holds no CPU reservation of its own, so the VMs can reserve the host's whole base capacity.
- G. A VM's CPU reservation raises its CPU Usage, even while the guest is idle, because reserved cycles are charged to it.

## Likely wrong answer
E (non-sticky read as overcommittable), F (kernel assumed to need no reservation), or G (a reservation read as CPU in use).

## Expected key points
- Answer: A, B, C, D.
- A: only the base frequency is guaranteed, because Turbo is not. A conservative design.
- B: if there is enough for everyone, reservation is irrelevant.
- C: CPU is transient: reserved CPU that the VM does not use is used by other VMs.
- D: the scheduler runs threads at different speeds, so cycles are reserved.
- E is wrong: a reservation is a guarantee, so it cannot be overcommitted; HA and DRS check it before placing a VM (admission control).
- F is wrong: the kernel holds a CPU reservation (System Resource Reservation): several GHz on hosts with vSAN and NSX.
- G is wrong: a CPU reservation is on demand and shows in no utilization metric; an idle VM with a reservation has CPU Usage near 0.

## Notes
- Options F and G rewritten 2026-11-14 (design.md 3.9; project/question-pairing-2026-11-14.md): F one fact; old G (kernel reservation above kernel use) removed because it repeats option E of 0024; new G tests whether a reservation shows in utilization. Key unchanged (author approved, 2026-11-14).

## Metadata
```yaml
id: "0011"
title: "CPU reservation behaviour"
product: [vsphere]
technology: [cpu]
input: [text]
task: judge-setting
object: [vm, resource-pool, esxi]
tool: [none]
knowledge:
  - vsphere/architecture/resource-controls
  - vsphere/technology/cpu/metrics/host/reserved-capacity
  - vsphere/architecture/overhead
knowledge_main: vsphere/architecture/resource-controls
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > CPU > Q8 Reservation"
answer_type: deterministic
level: 300                      # author 2026-11-05
answer: [A, B, C, D]
misconception: [E, F, G]
misconception_type: [provider-vs-consumer]
status: draft
```
