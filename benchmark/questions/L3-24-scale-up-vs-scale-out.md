# One large VM or four smaller VMs

## Prompt
- ESXi hosts: 2 sockets of 16 cores, Hyper-Threading on. One NUMA node per socket.
- A web application runs on one 32-vCPU VM. The architect proposes four 8-vCPU VMs behind a load balancer instead.

Which statements are correct?

- A. Each 8-vCPU VM fits in one NUMA node of these hosts, so its memory can stay local.
- B. Both designs total 32 vCPUs, so the choice does not change performance.
- C. The 32-vCPU VM spans both NUMA nodes, so some of its memory accesses can be remote.
- D. vNUMA makes remote memory access free for the 32-vCPU VM.
- E. vCPUs of the 32-vCPU VM that sit idle cost the host nothing.
- F. Each of the four VMs adds its own memory overhead on the host.
- G. Four 8-vCPU VMs are always the faster design on these hosts.
- H. Test both designs with the application's own load before choosing.

## Likely wrong answer
B: the same vCPU total gives the same performance. Or the over-correction G: the design that fits a NUMA node always wins.

## Expected key points
- Answer: A, C, F, H.
- A is true: 8 vCPUs are fewer than the 16 cores of a node, so the VM gets one home node and its memory is allocated there.
- B is false: NUMA fit, cache locality and scheduling differ between one large VM and several small ones.
- C is true: 32 vCPUs are more than the 16 cores of a node; a wide VM is split across nodes and some vCPUs reach remote memory, which raises the average memory latency.
- D is false: vNUMA lets a NUMA-aware guest place threads near their memory; it reduces the cost, it does not make remote access free.
- E is false: idle vCPUs still cost timer interrupts in some guests, upkeep of a consistent memory view, and busy-wait loops in some guests.
- F is true: every VM carries its own per-VM memory overhead (reserved at power-on and written to its vmware.log).
- G is false: the over-correction. Scaling out can perform better and scaling up can perform better; it depends on NUMA node size, cache locality and how the application is built.
- H is true: the vendor guidance is to test with the workload in the environment.

## Notes
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
source_path: "Drafted by Claude 2026-11-12; replaces a CPU Hot Add question (vNUMA behaviour with Hot Add differs by release and hardware version)"
answer: [A, C, F, H]
misconception: [B, G]
misconception_type: [unit-and-normalization]
status: draft
```
