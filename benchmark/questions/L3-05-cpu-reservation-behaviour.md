# CPU reservation behaviour

## Prompt
- Reservation, shares and limit are the 3 resource management controls.
- Sometimes you need a reservation on a VM or a resource pool.

Choose all the correct statements:

- A. The total CPU reservation on a host is capped at base clock speed × cores, below what Turbo Boost delivers.
- B. A CPU reservation comes into play only under contention.
- C. CPU that a VM reserves but does not use is available to other VMs at once.
- D. CPU reservation is set in MHz, not in vCPUs.
- E. The total CPU reservation of all VMs on a host can exceed the host's capacity.
- F. The ESXi kernel holds no CPU reservation of its own.
- G. A VM's CPU reservation raises its CPU Usage, even while the guest is idle.

## Likely wrong answer
E (non-sticky read as overcommittable), F (kernel assumed to need no reservation), or G (a reservation read as CPU in use).

## Expected key points
- Answer: A, B, C, D.
- A: only the base frequency is guaranteed, because Turbo is not. A conservative design.
- B: if there is enough CPU for every VM, each gets its runtime with or without a reservation.
- C: CPU is transient: reserved CPU that the VM does not use is used by other VMs.
- D: a CPU reservation is in hertz (MHz in Edit Settings), like CPU utilization; vCPUs are the unit of allocation.
- E is wrong: a reservation is a guarantee, so it cannot be overcommitted; only allocation can. HA and DRS check it before placing a VM (admission control).
- F is wrong: the kernel holds a CPU reservation (System Resource Reservation): several GHz on hosts with vSAN and NSX.
- G is wrong: a CPU reservation is on demand and shows in no utilization metric; an idle VM with a reservation has CPU Usage near 0.

## Notes
- Options rewritten 2026-11-14 (design.md 3.9; project/question-pairing-2026-11-14.md): one fact each and similar length; D without a reason clause the knowledge base does not state; F one fact; old G (kernel reservation above kernel use) removed because it repeats option E of 0024; new G tests whether a reservation shows in utilization. Key unchanged (author approved, 2026-11-14).

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
