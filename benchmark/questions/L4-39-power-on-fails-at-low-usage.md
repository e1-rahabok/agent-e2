# Power-on fails at 30% usage

## Prompt
- DRS cluster cl-east-02: 6 hosts, about 880 GHz of CPU. Cluster CPU usage is about 25%.
- You power on fin-batch02 in resource pool RP-FIN-BATCH. It has a CPU reservation of 2,400 MHz.
- The vSphere Client shows: "Power On virtual machine fin-batch02: Insufficient resources. The available CPU resources in the parent resource pool are insufficient for the operation."
- [The attached export](0085/resource-pool-tree.csv) lists the resource pools and VMs of the cluster with their reservations, limits and shares.

Why does the power-on fail when the cluster is at 25%, what do you change, and what do you advise for the reservation design? Which statements are correct?

- A. The check compares the 2,400 MHz reservation with capacity not yet reserved; the 25% CPU usage plays no part.
- B. Adding a seventh host lets fin-batch02 power on, because the cluster has run out of unreserved CPU.
- C. fin-batch01 already holds the 3,200 MHz of RP-FIN-BATCH, so the request goes up to RP-FIN because RP-FIN-BATCH is expandable.
- D. fin-batch01 is mostly idle, so the part of its reservation it does not use is free for fin-batch02 at power-on.
- E. RP-FIN has about 1,600 MHz unreserved: 9,600 MHz minus 4,800 MHz for its own VMs minus 3,200 MHz for RP-FIN-BATCH.
- F. As the reservation of RP-FIN is fixed, the check stops there and never reaches the unreserved CPU of the root.
- G. The 14,000 MHz reservation of RP-INFRA takes the unreserved CPU that fin-batch02 needs at power-on.
- H. Turning off HA admission control on the cluster removes the check, so fin-batch02 powers on.
- I. Raising the CPU reservation of RP-FIN to 11,000 MHz lets fin-batch02 power on.
- J. Raising the CPU reservation of RP-FIN-BATCH to 5,600 MHz lets fin-batch02 power on without any change to RP-FIN.
- K. Setting RP-FIN to an expandable reservation lets the request reach the cluster root, which has CPU to spare.
- L. Setting RP-FIN-BATCH to a fixed reservation lets fin-batch02 power on from the reservation of RP-FIN-BATCH alone.
- M. Removing the CPU reservation of fin-batch02 lets it pass CPU admission control.
- N. The error is transient: a retry or a restart of vCenter lets the power-on through.
- O. An expandable reservation isolates the VMs of a pool from the demands of the sibling pools under the same parent.
- P. Keep part of the cluster capacity unreserved; the vSphere documentation advises at least 10%.
- Q. Lowering the CPU reservation of fin-erp-app01 from 2,400 to 1,800 MHz lets fin-batch02 power on.

## Likely wrong answer
- B: "The cluster is short of CPU: add a host."
- N: "The cluster is at 25% CPU, so it is a glitch: retry, or restart vCenter."
- D: "batch01 is idle, so its reservation is free for batch02."

## Expected key points
- Answer: A, C, E, F, I, K, M, P.
- A true: admission control counts reservations, not usage.
- B false: the cluster root has well over 800 GHz unreserved; the walk stops at the fixed reservation of RP-FIN, so a host adds nothing that RP-FIN can reach.
- C true: RP-FIN-BATCH reserves 3,200 MHz and fin-batch01 holds all of it; an expandable pool asks its parent for the rest.
- D false: admission control counts the reservation of every powered-on VM in full, whether the VM uses it or not.
- E true: 9,600 - (2,400 + 1,800 + 0 + 600 + 0) - 3,200 = 1,600 MHz, less than the 2,400 MHz asked.
- F true: a fixed reservation admits only from the pool's own unreserved capacity; the walk up the tree continues only while each ancestor is expandable.
- G false: RP-INFRA is a sibling of RP-FIN under the root, and the root has plenty unreserved; the check never reaches the root.
- H false: the error names the parent resource pool: resource pool (DRS) admission control, which runs at every power-on and cannot be turned off. Only HA admission control can be disabled.
- I true: 11,000 - 4,800 - 3,200 = 3,000 MHz, enough for 2,400; the root has the extra 1,400 MHz to give.
- J false: a pool reservation is taken from the parent when it is set; RP-FIN has only 1,600 MHz unreserved, so the 2,400 MHz increase itself fails admission control.
- K true: an expandable RP-FIN borrows from the root; the cost is that RP-FIN no longer isolates its VMs.
- L false: a fixed RP-FIN-BATCH admits only from its own unreserved capacity, which is 0.
- M true: a VM with no reservation passes CPU admission control (its overhead memory is still checked; the memory side reaches the root, every pool there is expandable for memory).
- N false: the failure is deterministic, from the reservations in the tree.
- O false: only a fixed reservation isolates; with an expandable one, a child can take all of the parent's spare reservation and leave none for its siblings.
- P true: headroom for reservation changes, pool edits, overhead and DRS migrations.
- Q false: RP-FIN would then have 9,600 - 4,200 - 3,200 = 2,200 MHz unreserved, still less than the 2,400 MHz asked; lowering the reservations of RP-FIN's own VMs by 800 MHz or more in total would work.

## Notes
- Revised 2026-11-12: the tree as a CSV export, the error as text; no screenshot.
- Expandable reservations walk up the tree while each ancestor is expandable (vSphere 9.1 Resource Management, Expandable Reservations Example).
- Admission control questions test different facts: L2-10 (reservations, not usage), L4-30 (Invalid vs Overcommitted), this one (the walk up the tree stops at a fixed reservation).
- Converted from judged to multiple choice (Q199 F, 2026-11-14). Review 2026-11-14: option Q added for the old key point "lower other reservations in the fixed parent pool", as a near miss (a cut too small to be enough).
- CSV regenerated 2026-11-14 (project/question-pairing-2026-11-14.md, section 1, item 3): the old tree carried the knowledge example's numbers (6 - 3 - 2 = 1 GHz). New cluster, pools, VMs and numbers from a seeded script; the options and key follow the new numbers. Key letters unchanged.
- Paired with 0048 (the same mechanism as theory).

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
pair: "0048"
status: draft
```
