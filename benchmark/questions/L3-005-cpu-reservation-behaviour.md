# CPU reservation behaviour

## Prompt
- Host esx-21: 2 sockets of 24 cores, 2.4 GHz base clock, all-core Turbo 3.1 GHz, Hyper-Threading on. It runs vSAN and NSX.
- Its powered-on VMs reserve 98 GHz of CPU in total.
- A new VM with a CPU reservation of 12 GHz fails to power on with "Insufficient resources", while host CPU Usage reads 35%.

Choose all the correct statements:

- A. A host's total CPU reservation is capped at base clock × cores, not at the Turbo clock.
- B. A CPU reservation changes the CPU a running VM receives only when there is contention.
- C. CPU that a VM reserves but does not use is available to other VMs at once.
- D. A CPU reservation is set in MHz, not in vCPUs like allocation.
- E. The total CPU reservation of all VMs on a host can exceed the host's capacity.
- F. The ESXi kernel holds no CPU reservation of its own on the host.
- G. A VM's CPU reservation raises its CPU Usage, even while the guest is idle.
- H. A VM pinned with CPU affinity is admitted only if its pinned CPUs can deliver the reservation.

## Answers
A, B, C, D

## Explanation
- A is correct: only the base frequency is guaranteed, because Turbo is not: here 48 × 2.4 = 115.2 GHz, not 48 × 3.1. A conservative design.
- B is correct: at runtime, if there is enough CPU for every VM, each gets its runtime with or without a reservation; the reservation still counts at power-on and migration (admission control, as in E and F).
- C is correct: CPU is transient: reserved CPU that the VM does not use is used by other VMs.
- D is correct: a CPU reservation is in hertz (MHz in Edit Settings), like CPU utilization; vCPUs are the unit of allocation.
- E is wrong: a reservation is a guarantee, so it cannot be overcommitted; only allocation can. Host, DRS and HA admission control check it before a VM powers on or moves; here 98 + 12 = 110 GHz does not fit what is left.
- F is wrong: the kernel holds a CPU reservation of its own (host/system and host/vim allocation minimum, mostly 6-10 GHz across about 400 hosts, higher with vSAN and NSX); 115.2 GHz minus that leaves less than the 110 GHz asked for, which is why the power-on fails at 35% Usage.
- G is wrong: a CPU reservation is on demand and shows in no utilization metric; an idle VM with a reservation has CPU Usage near 0.
- H is wrong: CPU admission control ignores CPU affinity, so a pinned VM can be admitted and still not get its full reservation.
- Misconception: E (non-sticky read as overcommittable), F (kernel assumed to need no reservation), or G (a reservation read as CPU in use).

## Notes
- Changed in the 2026-11-15 audit: the stem was two lines of definitions (design.md 6.2: no definitions); it now gives a host, the reserved total and a failed power-on, so A, E and F rest on numbers. H added (admission control ignores CPU affinity; second question on it after 0048/L2-010 H).
- Changed in the 2026-11-16 re-review: B now names the runtime effect; "comes into play only under contention" was contradicted by the stem, where the reservation blocks a power-on at 35% Usage.

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
  - vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
knowledge_main: vsphere/architecture/resource-controls
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > CPU > Q8 Reservation"
answer_type: deterministic
level: 300                      # author 2026-11-05
misconception: [E, F, G]
misconception_type: [provider-vs-consumer]
status: draft
```
