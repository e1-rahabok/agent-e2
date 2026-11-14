# Power-on fails at 30% usage

## Prompt
- DRS cluster prod-cl07: 4 hosts, 640 GHz of CPU. Cluster CPU usage is about 30%.
- You power on vm-kid-db02 in resource pool RP-KID. It has a CPU reservation of 2,000 MHz.
- The vSphere Client shows: "Power On virtual machine vm-kid-db02: Insufficient resources. The available CPU resources in the parent resource pool are insufficient for the operation."
- [The attached export](0085/resource-pool-tree.csv) lists the resource pools and VMs of the cluster with their reservations, limits and shares.

Why does the power-on fail when the cluster is at 30%? What do you change, and what do you advise for the reservation design?

## Likely wrong answer
"The cluster is at 30% CPU, so it is a glitch: retry, or restart vCenter." Or "The cluster is short of CPU: add a host."

## Expected key points
- Admission control checks unreserved capacity, not usage: 30% usage does not matter.
- RP-KID reserves 2,000 MHz and vm-kid-db01 already uses all of it. RP-KID is expandable, so vm-kid-db02 asks its parent, RP-MOM, for the 2,000 MHz.
- RP-MOM has a fixed (not expandable) reservation of 6,000 MHz: its VMs reserve 3,000 MHz and RP-KID takes 2,000 MHz, so 1,000 MHz is unreserved. 1,000 < 2,000: the power-on fails.
- The cluster root has plenty unreserved, but a fixed reservation stops the walk up the tree: RP-MOM cannot borrow from the root.
- Fix, one of: raise RP-MOM to at least 7,000 MHz; make RP-MOM expandable (it then borrows from the root, and no longer isolates its VMs); lower other reservations in RP-MOM; or lower or remove the reservation of vm-kid-db02 if it is not justified.
- Design: a fixed reservation isolates a pool and caps what its children can borrow; an expandable one is flexible, but one child can take all of the parent's spare reservation. Keep part of the capacity unreserved (the documentation advises at least 10%).

## Notes
- Revised 2026-11-12: the tree as a CSV export, the error as text; no screenshot.
- Expandable reservations walk up the tree while each ancestor is expandable (vSphere 9.1 Resource Management, Expandable Reservations Example).
- Admission control questions test different facts: L2-10 (reservations, not usage), L4-30 (Invalid vs Overcommitted), this one (the walk up the tree stops at a fixed reservation).

## Metadata
```yaml
id: "0085"
title: "Power-on fails at 30% usage"
product: [vsphere]
technology: [system, cpu]
task: judge-setting
level: 400
answer_type: judged
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
