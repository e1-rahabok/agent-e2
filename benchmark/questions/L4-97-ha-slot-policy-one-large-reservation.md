# HA slot policy with one large memory reservation

## Prompt
- A vSphere 9.1 cluster with 6 identical ESX hosts. Each host offers 512 GB of memory to VMs (the memory of its root resource pool) and 96 GHz of CPU.
- vSphere HA is on. Admission control uses the Slot Policy, with Host Failures Cluster Tolerates set to 1. The slot size is calculated from the powered-on VMs (no fixed slot size and no das.slotmeminmb or das.slotcpuinmhz option).
- One database VM has a 200 GB memory reservation. No other VM has a CPU or memory reservation.
- The database VM was powered on first. The administrator then powers on small VMs, each with 4 GB of configured memory and no reservation. After about nine small VMs, the next power-on fails with an insufficient resources message about the vSphere HA failover level.
- At that moment the VMs consume less than 15% of the cluster memory. No VM shows ballooning or swapping.

What explains the failed power-on?

- A. The slot size takes its memory component from the largest memory reservation plus overhead in the cluster, and every powered-on VM needs at least one slot, so each host holds only a few slots.
- B. HA compares the memory the VMs consume with the memory that remains after one host fails, and the database VM consumes too much.
- C. Host admission control refuses the power-on, because the 200 GB reservation leaves too little unreserved memory on every host.
- D. HA counts the 200 GB reservation on every host, because it must be able to restart the database VM on any of them.
- E. The slot size takes its memory component from the average memory reservation of all VMs, and the database VM lifts the average above what a host can hold.

## Likely wrong answer
B or C: HA admission control is read as a check on consumed memory, or as the per-host reservation check. A reader who knows only the Cluster Resource Percentage policy expects a reservation to cost only its own size.

## Expected key points
- Answer: A.
- With the Slot Policy, the memory component of the slot is the largest memory reservation plus memory overhead among the powered-on VMs. The CPU component is the largest CPU reservation, 32 MHz by default for a VM with none.
- Every powered-on VM takes at least one slot, whatever its own reservation. A 4 GB VM with no reservation takes a 200 GB slot.
- A host holds its memory divided by the slot memory, rounded down: 2 slots per host here. HA must still leave enough slots after one host fails, so about ten VMs in all (6 hosts x 2 slots = 12 slots, 10 after one failure) are admitted while most of the memory is free.
- HA admission control uses reservations and overhead, not consumed memory (B is wrong). Host admission control checks one host's unreserved memory, and 512 GB minus 200 GB leaves room (C is wrong). The slot size uses the largest value, not the average (E is wrong), and the reservation is not counted on every host (D is wrong).
- Ways out: cap the memory slot with das.slotmeminmb, or use the Cluster Resource Percentage policy, where a reservation costs only its own size.

## Notes
- Public source: vSphere 9.1 documentation (VMware vSphere 9.1 PDF, build of 2026-11-02), vSphere Availability, "Slot Policy Admission Control", "Slot Size Calculation" and "Using Slots to Compute the Current Failover Capacity". Online: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-1.html
- Why one answer: the documentation defines the memory slot as the largest reservation plus overhead and says each VM uses a slot. The other options contradict a stated rule (consumed memory is not used; the average is not used).
- Debatable risk: none on the cause. The question asks for the cause, not for the fix, so the two valid fixes (slot cap, other policy) are not compared. "About nine" follows from 2 slots per host and one tolerated failure; the exact count depends on the overhead of the database VM, so the prompt does not ask for it.

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
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
answer: [A]
misconception: [B, C]
misconception_type: [consumption-as-contention]
status: draft
```
