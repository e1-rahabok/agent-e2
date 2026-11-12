# Wide VM placement on a two-socket host

## Prompt
- ESXi 9.1 host: 2 sockets, 32 cores per socket, Hyper-Threading on (64 threads per socket).
- 768 GB of DRAM, 384 GB per socket. One NUMA node per socket.
- Advanced settings are at their defaults.
- A new database VM is planned: 40 vCPUs, 300 GB of memory. The database is NUMA-aware.

Which statements are correct?

- A. The VM is wider than a NUMA node: ESXi splits it into NUMA clients on both nodes, because 40 vCPUs exceed the 32 cores of one node.
- B. The VM fits in one NUMA node: 40 vCPUs are fewer than the 64 hardware threads of one socket.
- C. 300 GB fits in the 384 GB of one node, so every vCPU of the VM reads its memory locally.
- D. vNUMA presents two NUMA nodes to the guest, so the database can keep each thread near its memory.
- E. With `numa.vcpu.preferHT` set on the VM, ESXi can keep it in one node with local memory, at the cost of its vCPUs sharing cores.

## Likely wrong answer
B: placement counted in hardware threads. Or C: the VM fits because its memory fits one node.

## Expected key points
- Answer: A, D, E.
- A: by default, the NUMA scheduler sizes a NUMA client by physical cores per node, not threads. 40 vCPUs > 32 cores, so the VM is split into clients on both nodes.
- B is wrong: threads count only with `numa.vcpu.preferHT`.
- C is wrong: the vCPUs sit on two nodes. A vCPU on one node reading memory on the other node reads remotely; memory size alone does not decide locality.
- D: vNUMA is on by default for VMs with more than 8 vCPUs and follows the host topology, so a NUMA-aware guest keeps threads and memory together.
- E: preferHT places the 40 vCPUs on the 64 threads of one node with local memory. The vCPUs then share cores, so each gets less than a full core when its sibling thread is busy.

## Notes
- Revised 2026-11-12: the earlier version used a management pack's monster VM rule (not public). The question now tests NUMA placement, which is public (vSphere 9.1 resource management, NUMA; Performance Best Practices for vSphere 9.1).

## Metadata
```yaml
id: "0063"
title: "Wide VM placement on a two-socket host"
product: [vsphere]
technology: [cpu, memory]
task: decide-capacity
level: 400
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/technology/cpu/concepts/numa
  - vsphere/technology/cpu/concepts/virtual-numa
  - vsphere/technology/cpu/configuration/numa-settings
knowledge_main: vsphere/technology/cpu/concepts/numa
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12 for the CPU slots (benchmark/design.md, section 3)"
answer: [A, D, E]
misconception: [B, C]
misconception_type: [frequency-and-hyper-threading]
status: draft
```
