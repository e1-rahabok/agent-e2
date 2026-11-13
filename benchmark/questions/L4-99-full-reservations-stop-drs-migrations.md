# Full memory reservations and DRS migrations

## Prompt
- A DRS cluster of 4 identical hosts. DRS is fully automated, the migration threshold is at the default (3), there are no VM-host rules and no host is in maintenance mode. vSphere HA admission control is turned off.
- Each host has 1,024 GB of memory, of which 1,000 GB are available to VMs.
- Host 1 shows high CPU Ready on several VMs. Hosts 2 and 3 are in the same state. Host 4 runs at 20% CPU utilization, and DRS has produced no recommendation for a long time.
- Reserved memory (VM reservations plus VM overhead) per host: host 1 holds 998 GB, host 2 holds 996 GB, host 3 holds 995 GB, host 4 holds 850 GB.
- A vMotion to host 4 is possible for every VM in the cluster: CPU compatibility, networks, datastores and hardware versions all match.
- The VMs on host 1 that DRS considers moving, with the VM overhead that vmware.log prints at power-on (VMMEM):

| VM | Configured memory | Memory reservation | VM overhead |
|---|---|---|---|
| VM-1 | 512 GB | 144 GB | 23 GB |
| VM-2 | 128 GB | 128 GB | 6.5 GB |
| VM-3 | 256 GB | 0 GB | 11.5 GB |
| VM-4 | 64 GB | 32 GB | 3.5 GB |
| VM-5 | 192 GB | 150 GB | 9 GB |

Ignore the extra memory that a vMotion operation itself needs. Considering only the memory admission check at the destination, which VMs can DRS move to host 4 as a single migration each?

- A. VM-1, VM-2, VM-3, VM-4 and VM-5, because each reservation is not larger than the 150 GB unreserved on host 4.
- B. VM-2, VM-3 and VM-4.
- C. VM-2 and VM-4, because the configured memory of the VM must fit into the unreserved memory of host 4.
- D. VM-3 and VM-4, because DRS keeps at least 100 GB (10%) unreserved on every host.
- E. Only VM-3, because a VM with a memory reservation cannot be migrated by DRS.

## Likely wrong answer
A, because the overhead is left out of the check. Or C and E: the check is read as a comparison with configured memory, or a reservation is read as pinning the VM.

## Expected key points
- Answer: B.
- A migration is admitted at the destination like a power-on: the destination must have enough unreserved memory for the VM reservation plus the VM overhead. Host 4 has 1,000 - 850 = 150 GB unreserved.
- VM-2 needs 128 + 6.5 = 134.5 GB (fits). VM-3 has no reservation, so it needs only its overhead of 11.5 GB (fits; its 256 GB of configured memory is not compared). VM-4 needs 32 + 3.5 = 35.5 GB (fits).
- VM-1 needs 144 + 23 = 167 GB and VM-5 needs 150 + 9 = 159 GB. Both are over 150 GB, although the reservation of VM-1 alone (144 GB) is below 150 GB and that of VM-5 alone is exactly 150 GB. A is wrong because it leaves out the overhead.
- C is wrong: the configured memory is not part of the admission check, only the reservation and the overhead. E is wrong: a VM with a reservation can move when the destination can admit it.
- D is wrong: the vendor advice to leave at least 10% unreserved is a planning guideline, not a rule that DRS enforces when it chooses a destination.
- Hosts 1 to 3 are at 99.5% reserved or more, so the vendor warning applies: reservations that fully commit individual hosts can prevent DRS from migrating VMs. Host 4 is the only destination, and only the VMs that fit are candidates.

## Notes
- Public source: VMware vSphere 9.1 PDF (build of 2026-11-02), Resource Management, "Resource Allocation Settings Suggestions": "plan to leave at least 10% unreserved" and "reservations that fully commit the capacity of the cluster or of individual ESX hosts in the cluster can prevent DRS from migrating virtual machines between ESX hosts". Same PDF, "Overhead Memory on Virtual Machines" (overhead printed to vmware.log, search VMMEM). Performance Best Practices for VMware vSphere 9.1, revision 20260624, p. 36: ESX keeps enough host memory to fulfil all reservations, both for VMs and for overhead, and does not power on a VM if that would reduce the available memory below the reserved amount.
- Why one answer: the check is reservation plus overhead against unreserved memory, the same rule as power-on admission. The numbers decide each VM. Overhead values in the table are inputs, chosen near the representative values in the documentation (about 4.5% of VM memory at 256 GB, 5.5% at 64 GB).
- Debatable risk: the documents state the effect (reservations that fully commit a host stop migrations) and the power-on rule, not a formula for the migration check in these words. The question rests on the admission rule being the same as at power-on and on overhead counted as reserved (knowledge file admission-control-and-cluster-state, section Admission control). The prompt tells the reader to ignore the extra memory of the vMotion operation itself; it would not change the outcome (VM-2 keeps 15.5 GB of room, VM-1 is over the limit by 17 GB).
- Rewritten 2026-11-13 to raise difficulty: from a single documented statement to a per-VM calculation with a table, where overhead, configured size, the 10% guideline and "reserved VMs cannot move" are separate traps.

## Metadata
```yaml
id: "0292"
title: Full memory reservations and DRS migrations
product: [vsphere]
technology: [memory, system]
task: judge-setting
level: 400
answer_type: deterministic
input: [text]
object: [cluster, esxi, vm]
tool: [vcenter]
knowledge:
  - vsphere/object-types/vm/configuration/resource-settings-guidance
  - vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
  - vsphere/object-types/cluster/concepts/drs-overview
  - vsphere/technology/memory/concepts/memory-overhead
knowledge_main: vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
answer: [B]
misconception: [A, E]
misconception_type: []
status: draft
```
