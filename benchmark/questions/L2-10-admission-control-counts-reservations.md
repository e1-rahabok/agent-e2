# Insufficient Resources on a quiet host

## Prompt
- An ESXi host in a cluster with vSphere HA and DRS runs at 10% CPU usage.
- Powering on a VM with a CPU reservation fails: "Insufficient resources. The available CPU resources are insufficient for the operation."

Which statements about the power-on check are correct?

- A. The check compares the VM's CPU reservation with the CPU capacity of its host or resource pool that other reservations do not already hold.
- B. At power-on, the VM's memory virtualization overhead is checked as reserved memory, on top of its memory reservation.
- C. The power-on can fail only when the host's current CPU usage leaves less free capacity than the reservation.
- D. A VM with no CPU reservation also fails CPU admission control on this host.
- E. A powered-on VM that uses little of its CPU reservation leaves the unused part free for the new VM's reservation.
- F. Turning off HA admission control on the cluster lets the VM power on.
- G. Reserving all of the cluster's CPU costs nothing, since usage plays no part in the check.
- H. A VM pinned with CPU affinity can pass the check and still not receive its full CPU reservation.

## Likely wrong answer
C: expecting admission control to look at usage, so a host at 10% must have room.

## Expected key points
- Answer: A, B, H.
- A is true: admission control counts reservations, not usage; a host at 10% CPU usage can have all of its capacity reserved.
- B is true: the per-VM overhead memory counts as reserved, in addition to the memory reservation.
- C is false: the misconception. Usage plays no part in the check.
- D is false: a VM with no reservation passes CPU and memory admission control; only its overhead memory is still checked.
- E is false: the reservation of every powered-on VM counts in full, whether the VM uses it or not.
- F is false: the wrong action. Host and DRS admission control run at every power-on and cannot be turned off; only HA admission control can be disabled.
- G is false: the over-correction. Near 100% reserved, reservation changes and pool edits fail and DRS cannot migrate VMs; the documentation advises leaving at least 10% unreserved.
- H is true: CPU admission control ignores CPU affinity, so a pinned VM can be admitted and still not get its full reservation.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): A no longer restates the knowledge file nor negates C; one fact per option; wrong action (F) and over-correction (G) added. Key changed from A, B to A, B, H.
- Paired with the table question 0085 (the same mechanism through a resource pool tree).

## Metadata
```yaml
id: "0048"
title: "Insufficient Resources on a quiet host"
product: [vsphere]
technology: [system, cpu, memory]
task: judge-setting
level: 200
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
  - vsphere/architecture/resource-controls
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05"
answer: [A, B, H]
misconception: [C]
object: [esxi, vm]
tool: [none]
knowledge_main: vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
misconception_type: [consumption-as-contention]
pair: "0085"
status: draft
```
