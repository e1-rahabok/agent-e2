# A red cluster with free capacity

## Prompt
- DRS cluster prod-cl04: 6 hosts, all connected, none in maintenance mode.
- Last night one host failed. vSphere HA restarted its VMs on the other hosts, and the host came back an hour later.
- During the failover, a change edited the CPU reservations of the resource pools.
- This morning the cluster shows red. Its CPU and memory usage are below 40%.
- The CPU resource pool tree, from the vSphere Client Resource Allocation view:

| Pool | Parent | CPU reservation | Reservation type | Limit |
|---|---|---|---|---|
| Prod | cluster root | 100 GHz | Fixed | Unlimited |
| Prod-DB | Prod | 70 GHz | Expandable | Unlimited |
| Prod-App | Prod | 45 GHz | Expandable | Unlimited |
| Test | cluster root | 20 GHz | Expandable | Unlimited |

- The cluster has 480 GHz of CPU capacity.
- The platform team proposes adding a seventh host to clear the red state.

Which statements about the red state, the risk to the running VMs and the fix are correct?

- A. Red here is the Invalid state: Prod-DB and Prod-App reserve 115 GHz under a parent with a Fixed reservation of 100 GHz.
- B. Red means the cluster is short of capacity, so a seventh host clears it.
- C. CPU and memory usage are below 40%, so the red state is a false alarm.
- D. Yellow (Overcommitted) is the state that more capacity fixes: the tree is consistent, but capacity no longer covers it.
- E. While the cluster is red, some running VMs may not get their reservations.
- F. Raising the reservation of Prod to at least 115 GHz makes the tree valid again.
- G. Making Prod expandable clears red, but Prod then borrows from the root and no longer isolates its pools.
- H. The red state comes from Test, whose expandable reservation borrows from the cluster root.
- I. Editing pool reservations while VMs fail over can turn a cluster red: a failing-over VM is not charged to its pool until the failover completes.
- J. Once the failed host came back, the cluster should have returned to green by itself.

## Likely wrong answer
- B: "Red means the cluster is short of capacity, so add a host."
- C: "The usage is below 40%, so the red state is a false alarm."

## Expected key points
- Answer: A, D, E, F, G, I.
- A true: the resource pool tree is inconsistent: 70 + 45 = 115 GHz of children under a Fixed 100 GHz.
- B false: red does not depend on cluster capacity: 480 GHz with usage below 40% is plenty, and the tree is still invalid. Adding a host does not fix red.
- C false: the state is about reservations in the tree, not usage; it has a real effect on the running VMs.
- D true: yellow means cluster capacity no longer covers the pool reservations, for example after a host failure. Add hosts or lower the reservations.
- E true: in the Invalid state, DRS cannot guarantee every reservation.
- F true: the children then fit within the parent. Lowering Prod-DB or Prod-App is the other way to bring the children within the parent.
- G true: an expandable Prod borrows from the root, and loses its isolation.
- H false: Test's 20 GHz fits easily in the 480 GHz root; the conflict is under Prod.
- I true: the likely origin here: reservations changed while VMs were failing over.
- J false: red is an inconsistency in the tree; it stays until the reservations are fixed, whatever the host count.

## Notes
- Revised 2026-11-12: the screenshot became the tree as text. A DRS cluster turns red (Invalid) when the tree is inconsistent; yellow (Overcommitted) when capacity no longer covers the reservations (vSphere 9.1 Resource Management, Valid, Overcommitted and Invalid DRS clusters).
- Admission control questions test different facts: L2-10 (reservations, not usage), this one (Invalid vs Overcommitted), L4-39 (expandable reservations walk up the tree).
- Converted from judged to multiple choice (Q199 F, 2026-11-14).

## Metadata
```yaml
id: "0073"
title: "A red cluster with free capacity"
product: [vsphere]
technology: [system]
task: judge-setting
level: 400
answer_type: deterministic
answer: [A,D,E,F,G,I]
misconception: [B,C]
input: [text]
object: [cluster, resource-pool]
tool: [vcenter]
knowledge:
  - vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
  - vsphere/object-types/resource-pool/resource-pool-design
knowledge_main: vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05; revised 2026-11-12"
misconception_type: [consumption-as-contention]
status: draft
```
