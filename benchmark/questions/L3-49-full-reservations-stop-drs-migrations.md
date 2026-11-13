# Full memory reservations and DRS migrations

## Prompt
- A DRS cluster with 4 hosts, DRS automation level fully automated, migration threshold at the default.
- Every VM in the cluster has a memory reservation. On each host, the reservations plus the memory overhead of its VMs add up to about 99.5% of the memory the host offers to VMs.
- Host 1 shows high CPU Ready on several VMs while host 4 runs at low CPU utilization. DRS applies no migration and reports no recommendation, and no host is in maintenance mode or has a connection problem.

Which statement about the effect of these reservations on DRS is correct?

- A. A VM can move only to a host that can admit its reservation. With about 0.5% of memory unreserved on every host, no host can admit a migrating VM, so DRS has no valid move.
- B. DRS ignores any host with more than 90% of its memory reserved, so the load across the other hosts is balanced without host 1.
- C. A memory reservation pins the VM to its host, as a "must run on" VM-host rule does, until the reservation is removed.
- D. DRS never migrates a VM that has a reservation, so the VMs on host 1 would move only if they had none.
- E. Memory reservations count only for vSphere HA admission control. They have no effect on where DRS can place a VM.

## Likely wrong answer
E, or D: reservations are seen as an HA topic only, or as a property that excludes a VM from DRS.

## Expected key points
- Answer: A.
- A migration needs the destination to admit the VM's memory reservation and its overhead, as a power-on does. A host with almost nothing unreserved cannot admit any reserved VM.
- The vSphere documentation says reservations that fully commit the capacity of the cluster, or of individual hosts, can prevent DRS from migrating VMs.
- A reserved VM is not pinned or excluded (C and D are wrong): it can move when a destination has enough unreserved memory.
- The documentation advises leaving at least 10% of the capacity unreserved.

## Notes
- Public source: vSphere 9.1 documentation (VMware vSphere 9.1 PDF, build of 2026-11-02), vSphere Resource Management, "Resource Allocation Settings Suggestions": "In a DRS-enabled cluster, reservations that fully commit the capacity of the cluster or of individual ESX hosts in the cluster can prevent DRS from migrating virtual machines between ESX hosts." Same page: "plan to leave at least 10% unreserved". Online: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-1.html
- Why one answer: the documentation names the effect. Admission of a reservation at the destination is the same rule that governs power-on. The prompt rules out other reasons for the missing recommendation (maintenance mode, connection problems, a VM without reservation).
- Debatable risk: a reader could name VM-host rules or a high migration threshold as other causes of no recommendation. The prompt fixes the threshold at the default and asks about the effect of the reservations, not for the single cause. Option B is invented, so it cannot be argued for.

## Metadata
```yaml
id: "0292"
title: Full memory reservations and DRS migrations
product: [vsphere]
technology: [memory, system]
task: judge-setting
level: 300
answer_type: deterministic
input: [text]
object: [cluster, esxi, vm]
tool: [vcenter]
knowledge:
  - vsphere/object-types/vm/configuration/resource-settings-guidance
  - vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
  - vsphere/object-types/cluster/concepts/drs-overview
knowledge_main: vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
answer: [A]
misconception: [D, E]
misconception_type: []
status: draft
```
