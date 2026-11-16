# Wide VM placement on a two-socket host

## Prompt
- ESXi 9.1 host: 2 sockets, 32 cores per socket, Hyper-Threading on (64 threads per socket).
- 768 GB of DRAM, 384 GB per socket. One NUMA node per socket.
- Advanced settings are at their defaults.
- A new database VM is planned: 40 vCPUs, 300 GB of memory. The database is NUMA-aware.

Which statements are correct?

- A. ESXi splits the VM into NUMA clients that sit on both nodes of the host.
- B. The VM fits in one NUMA node: 40 vCPUs are fewer than the 64 hardware threads of one socket.
- C. 300 GB fits in the 384 GB of one node, so every vCPU of the VM reads its memory locally.
- D. vNUMA presents two NUMA nodes to the guest, so the database can keep each thread near its memory.
- E. With `numa.vcpu.preferHT` set, ESXi keeps the VM on one node with local memory, its vCPUs sharing cores.

## Answers
A, D, E

## Explanation
- A: by default, the NUMA scheduler sizes a NUMA client by physical cores per node, not threads. 40 vCPUs > 32 cores, so the VM is split into clients on both nodes.
- B is wrong: threads count only with `numa.vcpu.preferHT`.
- C is wrong: the vCPUs sit on two nodes. A vCPU on one node reading memory on the other node reads remotely; memory size alone does not decide locality.
- D: vNUMA is on by default for VMs with more than 8 vCPUs and follows the host topology: the 40 vCPUs split evenly as 20 + 20 and the 300 GB as 150 + 150, so a NUMA-aware guest keeps threads and memory together.
- E: preferHT places the 40 vCPUs on the 64 threads of one node with local memory. The vCPUs then share cores, so each gets less than a full core when its sibling thread is busy.
- Misconception: B: placement counted in hardware threads. Or C: the VM fits because its memory fits one node.

## Notes
- Changed in the 2026-11-15 audit: A without its reason clause and E without its hedge (the two longest options were the correct ones); no option added: the proposed "NRMEM above 0 means ESXi keeps moving the VM" is already L4-025 B and 0113 F.
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
object: [vm, esxi]
tool: [none]
knowledge:
  - vsphere/technology/cpu/concepts/numa
  - vsphere/technology/cpu/concepts/virtual-numa
  - vsphere/technology/cpu/configuration/numa-settings
knowledge_main: vsphere/technology/cpu/concepts/numa
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-12"
misconception: [B, C]
misconception_type: [frequency-and-hyper-threading]
status: draft
```
