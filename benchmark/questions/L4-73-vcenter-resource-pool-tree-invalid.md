# A red cluster with free capacity

## Prompt
The attached screenshot is the vSphere Client Resource Allocation view of a DRS cluster: the resource pool tree with reservation, reservation type and limit per pool.

- All hosts are connected; none is in maintenance.
- The cluster shows red, while its CPU and memory usage are below 40%.
- The platform team proposes adding a host to clear the red state.

Will adding a host fix it? Explain the state, the risk to running VMs, and the fix.

## Input to supply
- Tool: vSphere Client 9.1, cluster > Monitor > Resource Allocation > CPU (or Memory), plus the cluster Summary with the red state.
- Must show the pool tree with Reservation, Reservation Type (Expandable or Fixed), Limit and Shares per pool and per VM.
- Condition for the key: one parent pool has a fixed reservation smaller than the sum of its child reservations; the cluster is red (Invalid); all hosts are connected.
- How to produce it: in a lab, set a child pool reservation above the parent's fixed reservation while a VM fails over, or edit the pools from the API.
- Save as `benchmark/questions/73/vcenter-cluster-resource-allocation.png`.

## Likely wrong answer
"Yes: add a host, the cluster is short of capacity."

## Expected key points
- No. Red (Invalid) means the resource pool tree is inconsistent: the children reserve more than a parent fixed reservation. It happens at any level, even with free capacity at the root.
- Adding capacity does not fix red. Yellow (Overcommitted) is the state that adding hosts fixes: there the tree is consistent but the cluster no longer covers the reservations.
- Risk: some running VMs may not get their reservations.
- Fix: lower the children reservations, raise the parent reservation, or make the parent expandable; or power off or move VMs.
- Admission control counts reservations, not usage: usage below 40% says nothing about this state.

## Notes
- Previous id: question-0073 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "73"
title: "A red cluster with free capacity"
product: [vsphere]
technology: [system]
task: judge-setting
level: 400
answer_type: judged
input: [screenshot]
knowledge:
  - vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
  - vsphere/foundations/resource-controls
attachments:
  - 73/vcenter-cluster-resource-allocation.png
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
status: awaiting-input
```
