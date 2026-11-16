# HA slot policy with one large memory reservation

## Prompt
- A vSphere 9.1 cluster with 6 identical ESX hosts. Each host offers 512 GB of memory to VMs (the memory of its root resource pool) and 96 GHz of CPU.
- vSphere HA is on. Admission control uses the Slot Policy, with Host Failures Cluster Tolerates set to 1. The slot size is calculated from the powered-on VMs (no fixed slot size and no das.slotmeminmb or das.slotcpuinmhz option).
- One database VM has a 200 GB memory reservation. No other VM has a CPU or memory reservation.
- The database VM was powered on first. The administrator then powers on small VMs, each with 4 GB of configured memory and no reservation. After about nine small VMs, the next power-on fails with an insufficient resources message about the vSphere HA failover level.
- At that moment the VMs consume less than 15% of the cluster memory. No VM shows ballooning or swapping.

Which statements explain the failed power-on?

- A. The slot size takes its memory component from the largest memory reservation plus overhead among the powered-on VMs.
- B. HA compares the memory the VMs consume with the memory that remains after one host fails, and the database VM consumes too much.
- C. Host admission control refuses the power-on, because the 200 GB reservation leaves too little unreserved memory on every host.
- D. HA counts the 200 GB reservation on every host, because it must be able to restart the database VM on any of them.
- E. The slot size takes its memory component from the average memory reservation of all VMs, and the database VM lifts the average above what a host can hold.
- F. Every powered-on VM takes at least one slot, so a 4 GB VM without a reservation costs as much as the database VM.

## Likely wrong answer
B or C: HA admission control is read as a check on consumed memory, or as the per-host reservation check. A reader who knows only the Cluster Resource Percentage policy expects a reservation to cost only its own size.

## Expected key points
- Answer: A, F.
- A is correct: with the Slot Policy, the memory component of the slot is the largest memory reservation plus its overhead among the powered-on VMs: about 200 GB here.
- B is wrong: HA admission control counts reservations and overhead, not consumed memory; under 15% consumed plays no part.
- C is wrong: host admission control checks one host's unreserved memory, and 512 GB minus 200 GB (plus overhead) leaves room on every host; the message names the HA failover level.
- D is wrong: the reserve is counted in slots, not as the database VM's reservation on every host.
- E is wrong: the slot size uses the largest reservation, not the average.
- F is correct: one slot size applies to every VM, so a small VM with no reservation still takes a slot of about 200 GB. A host holds 2 such slots, 12 in the cluster, 10 after one host fails: the database VM and about nine small VMs.

## Notes
- Synthetic, 2026-11-13, for the coverage gap (project/plan.md).
- Public source: vSphere 9.1 documentation (VMware vSphere 9.1 PDF, build of 2026-11-02), vSphere Availability, "Slot Policy Admission Control", "Slot Size Calculation" and "Using Slots to Compute the Current Failover Capacity". Online: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-1.html
- The question asks for the cause, not for the fix, so the two valid fixes (das.slotmeminmb cap, Cluster Resource Percentage policy) are not options. "About nine" follows from 2 slots per host and one tolerated failure; the exact count depends on the overhead of the database VM, so the prompt does not ask for it.
- 2026-11-15 audit: old A held two facts and was the longest option; it is split into A (slot memory = largest reservation plus overhead) and new F (every VM takes a slot). Key changed from A to A, F.

## Metadata
```yaml
id: "0290"
title: HA slot policy with one large memory reservation
product: [vsphere]
technology: [memory, system]
task: troubleshoot
level: 400
answer_type: deterministic
input: [text]
object: [cluster, vm]
tool: [vcenter]
knowledge:
  - vsphere/object-types/cluster/configuration/cluster-configuration-review
  - vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
  - vsphere/architecture/resource-controls
knowledge_main: vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-13"
answer: [A, F]
misconception: [B, C]
misconception_type: [consumption-as-contention]
status: draft
```
