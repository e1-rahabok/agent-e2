# Insufficient Resources on a quiet host

## Prompt
- An ESXi host in a cluster with vSphere HA and DRS runs at 10% CPU usage.
- Each host's Resource Allocation tab shows about 1.2 GHz of CPU unreserved; the VM reserves 4 GHz of CPU.
- Powering on the VM fails: "Insufficient resources. The available CPU resources are insufficient for the operation."

Which statements about the power-on check are correct?

- A. The check compares the VM's CPU reservation with the host's or pool's CPU not yet held by other reservations.
- B. Capacity of hosts in DPM standby counts as available; DRS recommends powering one on to admit a VM.
- C. The power-on fails when the host's current CPU usage leaves less free capacity than the reservation.
- D. A VM with no CPU reservation would also fail CPU admission control on this host right now.
- E. A powered-on VM that uses little of its CPU reservation leaves the unused part free for the new VM's reservation.
- F. Turning off HA admission control on the cluster lets the VM power on at the next attempt.
- G. Reserving all of the cluster's CPU has no side effect as long as the VMs' usage stays low.
- H. A VM pinned with CPU affinity can pass the check and still not receive its full CPU reservation.
- I. A request an expandable pool cannot meet climbs the tree and stops at the first ancestor with a fixed reservation.

## Answers
A, B, H, I

## Explanation
- A is correct: admission control counts reservations, not usage; a host at 10% CPU usage can have all of its capacity reserved.
- B is correct: with DPM, the capacity of standby hosts counts as available; when a VM cannot be admitted without it, DRS recommends powering a host on.
- C is wrong: the misconception. Usage plays no part in the check.
- D is wrong: a VM with no reservation passes CPU and memory admission control; only its overhead memory is still checked.
- E is wrong: the reservation of every powered-on VM counts in full, whether the VM uses it or not.
- F is wrong: the wrong action. Host and DRS admission control run at every power-on and cannot be turned off; only HA admission control can be disabled. No host has 4 GHz unreserved, so the host check refuses the VM whatever HA admission control does.
- G is wrong: the over-correction. Near 100% reserved, reservation changes and pool edits fail admission control, and DRS cannot migrate VMs because no destination can admit them.
- H is correct: CPU admission control ignores CPU affinity, so a pinned VM can be admitted and still not get its full reservation.
- I is correct: an expandable pool admits from its own unreserved capacity, then its parent's, up the tree while each ancestor is expandable; a fixed ancestor admits only from its own unreserved capacity.
- Misconception: C: expecting admission control to look at usage, so a host at 10% must have room.

## Notes
- Synthetic, 2026-11-05. Counts only after author approval.
- Paired with the table question 0085 (the same mechanism through a resource pool tree).
- 2026-11-15 audit: B now tests the DPM standby line (the overhead fact is kept by 0152 and 0292); the stem gives the hosts' unreserved CPU so F is decided by the host check; C and G lost their absolutes.

## Metadata
```yaml
id: "0048"
title: "Insufficient Resources on a quiet host"
product: [vsphere]
technology: [system, cpu]
task: judge-setting
level: 200
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
  - vsphere/architecture/resource-controls
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-05"
misconception: [C]
object: [esxi, vm]
tool: [none]
knowledge_main: vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
misconception_type: [consumption-as-contention]
pair: "0085"
status: draft
```
