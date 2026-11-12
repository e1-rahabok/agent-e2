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

Will adding a host fix it? Explain the state, the risk to the running VMs, and the fix.

## Likely wrong answer
"Yes: red means the cluster is short of capacity, so add a host." Or "The usage is below 40%, so the red state is a false alarm."

## Expected key points
- No. Red is the Invalid state: the resource pool tree is inconsistent. Prod-DB and Prod-App reserve 115 GHz under a parent with a Fixed reservation of 100 GHz.
- It does not depend on cluster capacity: 480 GHz with usage below 40% is plenty, and the tree is still invalid. Adding a host does not fix red.
- Yellow (Overcommitted) is the state that more capacity fixes: the tree is consistent, but the cluster no longer covers the reservations, for example after a host failure.
- Risk: some running VMs may not get their reservations, and DRS cannot guarantee them.
- Fix: bring the children within the parent: lower Prod-DB or Prod-App, raise Prod to at least 115 GHz, or make Prod expandable (it then borrows from the root, and loses its isolation).
- Likely origin: reservations changed while VMs were failing over; a VM in failover is not charged to its pool until the failover completes.

## Notes
- Revised 2026-11-12 (question set 1.0): the screenshot became the tree as text. A DRS cluster turns red (Invalid) when the tree is inconsistent; yellow (Overcommitted) when capacity no longer covers the reservations (vSphere 9.1 Resource Management, Valid, Overcommitted and Invalid DRS clusters).
- Admission control questions test different facts: L2-10 (reservations, not usage), this one (Invalid vs Overcommitted), L4-39 (expandable reservations walk up the tree).

## Metadata
```yaml
id: "0073"
title: "A red cluster with free capacity"
product: [vsphere]
technology: [system]
task: judge-setting
level: 400
answer_type: judged
input: [text]
object: [cluster, resource-pool]
tool: [vcenter]
knowledge:
  - vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
  - vsphere/object-types/resource-pool/resource-pool-design
knowledge_main: vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation; revised 2026-11-12 (question set 1.0)"
misconception_type: [consumption-as-contention]
status: draft
```
