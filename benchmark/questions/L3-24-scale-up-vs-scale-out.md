# One large VM or four smaller VMs

## Prompt
- ESXi hosts: 2 sockets of 16 cores, Hyper-Threading on. One NUMA node per socket.
- A web application runs on one 32-vCPU VM. The architect proposes four 8-vCPU VMs behind a load balancer instead.

Which statements are correct?

- A. One large VM can perform better when the application's threads share a lot of data in memory.
- B. The total is 32 vCPUs either way, so the choice does not change performance.
- C. Which design is faster depends on the workload: how the application scales, its cache locality and its fit in a NUMA node. Test both.
- D. vNUMA removes every NUMA cost of the 32-vCPU VM, so both designs perform the same.
- E. Splitting the VM raises the clock speed each vCPU gets.
- F. Four VMs need four guest operating systems: more memory, more overhead and, under per-instance licensing, more licences.

## Likely wrong answer
B: the same vCPU total gives the same performance. Or D: vNUMA makes a wide VM as good as one that fits a node.

## Expected key points
- Answer: A, C, F.
- A: threads that share data gain from one shared memory image and cache; scaling up can perform better for them.
- B is wrong: NUMA fit, cache locality and scheduling differ between one large VM and several small ones.
- C: scaling out can perform better and scaling up can perform better; it depends on NUMA node size, cache locality and the application. The vendor guidance is to test the workload.
- D is wrong: vNUMA helps a NUMA-aware guest place threads near memory; it does not make remote access free.
- E is wrong: the clock speed comes from the host's cores and power policy, not from how the vCPUs are split into VMs.
- F: each VM carries its own guest OS and memory overhead; licences grow where they are counted per instance.

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
knowledge_main: vsphere/technology/cpu/concepts/idle-and-unused-vcpus
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12 for the CPU slots (project/plan.md, M2); replaces the CPU Hot Add slot (vNUMA behaviour with Hot Add differs by release and hardware version)"
answer: [A, C, F]
misconception: [B, D]
misconception_type: [unit-and-normalization]
status: draft
```
