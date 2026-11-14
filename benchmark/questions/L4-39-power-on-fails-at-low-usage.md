# Power-on fails at 30% usage

## Prompt
- DRS cluster prod-cl07: 4 hosts, 640 GHz of CPU. Cluster CPU usage is about 30%.
- You power on vm-kid-db02 in resource pool RP-KID. It has a CPU reservation of 2,000 MHz.
- The vSphere Client shows: "Power On virtual machine vm-kid-db02: Insufficient resources. The available CPU resources in the parent resource pool are insufficient for the operation."
- [The attached export](0085/resource-pool-tree.csv) lists the resource pools and VMs of the cluster with their reservations, limits and shares.

Why does the power-on fail when the cluster is at 30%, what do you change, and what do you advise for the reservation design? Which statements are correct?

- A. The check compares the 2,000 MHz reservation with capacity not yet reserved; the 30% CPU usage plays no part.
- B. Adding a fifth host lets vm-kid-db02 power on, because the cluster has run out of unreserved CPU.
- C. vm-kid-db01 already holds the 2,000 MHz of RP-KID, so the request goes up to RP-MOM because RP-KID is expandable.
- D. vm-kid-db01 is mostly idle, so the part of its reservation it does not use is free for vm-kid-db02 at power-on.
- E. RP-MOM has about 1,000 MHz unreserved: 6,000 MHz minus 3,000 MHz for its own VMs minus 2,000 MHz for RP-KID.
- F. As the reservation of RP-MOM is fixed, the check stops there and never reaches the unreserved CPU of the root.
- G. The 10,000 MHz reservation of RP-OPS takes the unreserved CPU that vm-kid-db02 needs at power-on.
- H. Turning off HA admission control on the cluster removes the check, so vm-kid-db02 powers on.
- I. Raising the CPU reservation of RP-MOM to 7,000 MHz or more lets vm-kid-db02 power on.
- J. Raising the CPU reservation of RP-KID to 4,000 MHz lets vm-kid-db02 power on without any change to RP-MOM.
- K. Setting RP-MOM to an expandable reservation lets the request reach the cluster root, which has CPU to spare.
- L. Setting RP-KID to a fixed reservation lets vm-kid-db02 power on from the reservation of RP-KID alone.
- M. Removing the CPU reservation of vm-kid-db02 lets it pass CPU admission control.
- N. The error is transient: a retry or a restart of vCenter lets the power-on through.
- O. An expandable reservation isolates the VMs of a pool from the demands of the sibling pools under the same parent.
- P. Keep part of the cluster capacity unreserved; the vSphere documentation advises at least 10%.

## Likely wrong answer
- B: "The cluster is short of CPU: add a host."
- N: "The cluster is at 30% CPU, so it is a glitch: retry, or restart vCenter."
- D: "db01 is idle, so its reservation is free for db02."

## Expected key points
- Answer: A, C, E, F, I, K, M, P.
- A true: admission control counts reservations, not usage.
- B false: the cluster root has over 600 GHz unreserved; the walk stops at the fixed reservation of RP-MOM, so a host adds nothing that RP-MOM can reach.
- C true: RP-KID reserves 2,000 MHz and vm-kid-db01 holds all of it; an expandable pool asks its parent for the rest.
- D false: admission control counts the reservation of every powered-on VM in full, whether the VM uses it or not.
- E true: 6,000 - (1,500 + 1,500 + 0) - 2,000 = 1,000 MHz, less than the 2,000 MHz asked.
- F true: a fixed reservation admits only from the pool's own unreserved capacity; the walk up the tree continues only while each ancestor is expandable.
- G false: RP-OPS is a sibling of RP-MOM under the root, and the root has plenty unreserved; the check never reaches the root.
- H false: the error names the parent resource pool: resource pool (DRS) admission control, which runs at every power-on and cannot be turned off. Only HA admission control can be disabled.
- I true: 7,000 - 3,000 - 2,000 = 2,000 MHz, enough; the root has the extra 1,000 MHz to give.
- J false: a pool reservation is taken from the parent when it is set; RP-MOM has only 1,000 MHz unreserved, so the 2,000 MHz increase itself fails admission control.
- K true: an expandable RP-MOM borrows from the root; the cost is that RP-MOM no longer isolates its VMs.
- L false: a fixed RP-KID admits only from its own unreserved capacity, which is 0.
- M true: a VM with no reservation passes CPU admission control (its overhead memory is still checked; the memory side reaches the root, every pool there is expandable for memory).
- N false: the failure is deterministic, from the reservations in the tree.
- O false: only a fixed reservation isolates; with an expandable one, a child can take all of the parent's spare reservation and leave none for its siblings.
- P true: headroom for reservation changes, pool edits, overhead and DRS migrations.

## Notes
- Revised 2026-11-12: the tree as a CSV export, the error as text; no screenshot.
- Expandable reservations walk up the tree while each ancestor is expandable (vSphere 9.1 Resource Management, Expandable Reservations Example).
- Admission control questions test different facts: L2-10 (reservations, not usage), L4-30 (Invalid vs Overcommitted), this one (the walk up the tree stops at a fixed reservation).
- Converted from judged to multiple choice (Q199 F, 2026-11-14).

## Metadata
```yaml
id: "0085"
title: "Power-on fails at 30% usage"
product: [vsphere]
technology: [system, cpu]
task: judge-setting
level: 400
answer_type: deterministic
answer: [A,C,E,F,I,K,M,P]
misconception: [B,D,N]
input: [table]
object: [resource-pool, cluster, vm]
tool: [vcenter]
knowledge:
  - vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
  - vsphere/object-types/resource-pool/resource-pool-design
  - vsphere/architecture/resource-controls
knowledge_main: vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
attachments:
  - 0085/resource-pool-tree.csv
origin: synthetic
source_path: "Drafted by Claude 2026-11-05; revised 2026-11-12"
misconception_type: [consumption-as-contention]
status: draft
```
