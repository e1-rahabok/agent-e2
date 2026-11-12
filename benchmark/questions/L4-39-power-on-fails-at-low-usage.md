# Power-on fails at 30% usage

## Prompt
The attached table is an export of the resource pool tree of a DRS cluster: per pool and per VM, the CPU and memory reservation, reservation type, limit and shares. The screenshot is the vSphere Client error when a VM in pool RP-KID is powered on.

- Cluster CPU usage is about 30%.
- The VM has a CPU reservation of 2 GHz.

Why does the power-on fail? What do you change, and what do you advise for the reservation design?

## Input to supply
- Table: export of the resource pool tree (PowerCLI or vSphere Client), one row per pool and per VM: name, parent, CPU reservation (GHz), memory reservation (GB), reservation type (Fixed or Expandable), limit, shares.
- Condition for the key: parent RP-MOM has a fixed 6 GHz reservation and runs VMs with 3 GHz reserved; child RP-KID is expandable with 2 GHz reserved, already used by a running VM. The new VM in RP-KID reserves 2 GHz.
- Screenshot: vSphere Client 9.1 power-on error "Insufficient resources" for that VM.
- Save as `benchmark/questions/85/resource-pool-tree.xlsx` and `benchmark/questions/85/vcenter-insufficient-resources.png`.

## Likely wrong answer
"The cluster is at 30% CPU, so it is a bug: retry or restart vCenter."

## Expected key points
- Admission control counts reservations, not usage: 30% usage does not matter.
- RP-KID is expandable: its own 2 GHz is used, so the VM borrows from RP-MOM. RP-MOM has 6 - 3 - 2 = 1 GHz unreserved, less than 2 GHz: the power-on fails.
- The VM overhead memory also counts as reserved, on top of its memory reservation.
- Fix: raise the RP-MOM reservation, lower other reservations, or remove the reservation from the new VM if it is not justified.
- Design: leave at least 10% of capacity unreserved; near 100% reserved, power-ons and pool edits fail and DRS cannot migrate VMs. Expandable reservations give flexibility but lose isolation between sibling pools.

## Notes
- Previous id: question-0085 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0085"
title: "Power-on fails at 30% usage"
product: [vsphere]
technology: [system]
task: judge-setting
level: 400
answer_type: judged
input: [table, screenshot]
knowledge:
  - vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
  - vsphere/architecture/resource-controls
attachments:
  - 0085/resource-pool-tree.xlsx
  - 0085/vcenter-insufficient-resources.png
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
status: awaiting-input
```
