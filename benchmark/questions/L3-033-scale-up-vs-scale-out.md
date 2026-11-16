# One large VM or four smaller VMs

## Prompt
- ESXi hosts: 2 sockets of 16 cores, Hyper-Threading on, 512 GB of memory. One NUMA node per socket, 256 GB each.
- A web application runs on one 32-vCPU VM with 128 GB. The architect proposes four 8-vCPU VMs of 32 GB each behind a load balancer instead.

Which statements are correct?

- A. Each 8-vCPU VM fits in one NUMA node of these hosts, so it gets one home node for its memory.
- B. Both designs total 32 vCPUs, so the choice does not change performance.
- C. The 32-vCPU VM spans both NUMA nodes, so part of its memory is remote to some of its vCPUs.
- D. The 32-vCPU VM is split over both nodes only if its memory exceeds one node.
- E. Idle vCPUs of the 32-vCPU VM are de-scheduled, so they add no overhead on the host or in the guest.
- F. Each of the four VMs adds its own memory overhead on the host.
- G. Four 8-vCPU VMs give the better performance here, since each fits a NUMA node.
- H. Test both designs with the application's own load before choosing.

## Answers
A, C, F, H

## Explanation
- A is true: 8 vCPUs are fewer than the 16 cores of a node, so the VM gets one home node and its memory is allocated there.
- B is false: NUMA fit, cache locality and scheduling differ between one large VM and several small ones.
- C is true: 32 vCPUs are more than the 16 cores of a node; a wide VM is split across nodes and some vCPUs reach remote memory, which raises the average memory latency.
- D is false: the split is decided by vCPUs against the cores of a node. 32 vCPUs are more than 16 cores, so the VM spans both nodes although its 128 GB fit one node (a VM whose vCPUs fit stays on one home node even when its memory does not).
- E is false: ESX de-schedules vCPUs that halt with HLT or MWAIT, which keeps the cost small, but idle vCPUs still cost timer interrupts in some guests, upkeep of a consistent memory view in the guest and in ESX, and busy-wait loops in some guests.
- F is true: every VM carries its own per-VM memory overhead (reserved at power-on and written to its vmware.log).
- G is false: the over-correction. NUMA fit alone does not decide it: scaling out can perform better and scaling up can perform better; it depends on NUMA node size, cache locality and how the application is built.
- H is true: the vendor guidance is to test with the workload in the environment.
- Misconception: B: the same vCPU total gives the same performance. Or the over-correction G: the design that fits a NUMA node wins.

## Notes
- Changed 2026-11-16 (re-review): "can" removed from the correct A and C (hedge cue against the absolutes of B, D and E); truth unchanged.
- Changed in the 2026-11-15 audit: memory sizes added to the stem; throwaway D ("vNUMA makes remote access free") replaced by the memory-split misconception; E and G reworded so absolutes are not only in wrong options; misconception type unit-and-normalization removed (it did not fit B).
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): C ("it depends: test both", vague and compound) replaced by the NUMA facts A and C and the action H; the old A (shared data) and F (licences) were not in the knowledge base; E (clock speed) replaced by the idle vCPU cost; G added as the over-correction. Key changed from A, C, F to A, C, F, H (new letters).

## Metadata
```yaml
id: "0114"
title: "One large VM or four smaller VMs"
product: [vsphere]
technology: [cpu, memory]
task: decide-capacity
level: 300
answer_type: deterministic
input: [text]
object: [vm, esxi]
tool: [none]
knowledge:
  - vsphere/technology/cpu/concepts/idle-and-unused-vcpus
  - vsphere/technology/cpu/concepts/numa
  - vsphere/technology/cpu/concepts/virtual-numa
  - vsphere/technology/memory/concepts/memory-overhead
knowledge_main: vsphere/technology/cpu/concepts/idle-and-unused-vcpus
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-12; replaces a CPU Hot Add question (vNUMA behaviour with Hot Add differs by release and hardware version)"
misconception: [B, G]
misconception_type: []
status: draft
```
