# Two sockets in Windows, one NUMA node in esxtop

## Prompt
- The database administrator of a SQL Server VM sends [the Task Manager CPU page](0436/task-manager-cpu-two-sockets.png): "Windows shows two sockets, so the VM spans two NUMA nodes and half of its memory is remote. Set cores per socket so Windows shows one socket."
- You add [the Coreinfo output from the same VM](0436/coreinfo-numa-nodes.png) and [the esxtop memory panel with the NUMA fields](0436/esxtop-memory-numa-fields.png) of its host.

Which statements are correct?

- A. Two sockets in Task Manager mean the VM spans two physical NUMA nodes.
- B. esxtop shows the VM with one home node and all of its memory local to that node.
- C. Coreinfo shows that the guest sees a single NUMA node.
- D. Change cores per socket so that ESXi keeps the VM's memory within one node.
- E. Cores per socket matters only for licensing and has no other effect.
- F. ESXi built the VM's virtual NUMA layout from the host's NUMA nodes and the VM's vCPU count and memory.
- G. Pin the VM to its node with CPU and memory affinity to keep its memory local.
- H. At 16 vCPUs, virtual NUMA is not active for this VM.

## Input to supply
- Product and version: ESXi 9.1 host whose NUMA node has at least 16 cores and more memory than the VM; vSphere Client 9.1; a Windows Server 2022 or 2025 VM.
- VM: 16 vCPUs with cores per socket set by hand to 8 (2 virtual sockets), memory well within one node (for example 64-128 GB), no CPU Hot Add, no affinity.
- Screen 1: Task Manager > Performance > CPU, showing Sockets 2 and Logical processors 16. Save as `0436/task-manager-cpu-two-sockets.png`.
- Screen 2: Sysinternals Coreinfo run in the VM (`coreinfo -n`, or `coreinfo` with the NUMA section visible), showing one NUMA node with all 16 logical processors. Save as `0436/coreinfo-numa-nodes.png`.
- Screen 3: esxtop on the host, memory panel (`m`), NUMA STATS fields on (`f`, then the NUMA field letter), the VM's row with NHN, NMIG, NRMEM, NLMEM and N%L. Save as `0436/esxtop-memory-numa-fields.png`.
- Condition the key depends on: Task Manager Sockets 2, Logical processors 16; Coreinfo one NUMA node; esxtop NHN a single node number and N%L 100 (99 or more), NRMEM 0 or near 0.
- Masking: mask every VM, host, datastore and cluster name, including the VM's row name in esxtop and the computer name in the guest tools.

## Likely wrong answer
A: the socket count read as the NUMA layout, and D, the change that follows from it.

## Expected key points
- Answer: B, C, F.
- A false: the misconception. From vSphere 6.5, cores per socket only changes how the vCPUs are presented to the guest as sockets; the NUMA layout comes from the host.
- B true: one number in NHN is one home node (the VM is one NUMA client); N%L at 100 means all memory is local.
- C true: the guest's NUMA node count, not its socket count, shows the layout it sees; a VM that fits one physical node gets one virtual node.
- D false: the wrong action. Cores per socket does not decide where ESXi places the memory; the memory is already local.
- E false: the over-correction. Some cores per socket values still give the guest a sub-optimal topology and can cost performance.
- F true: vNUMA takes its topology from the host's NUMA layout and the VM's vCPU count and memory.
- G false: affinity takes the VM out of NUMA management: no rebalancing, no memory migration.
- H false: by default vNUMA is active for VMs with more than 8 vCPUs.

## Notes
- Practical half of 0267 (pair: design.md, section 3.9).
- No option rests on `numa.*` advanced options or on when ESXi rebuilds the vNUMA layout (open question Q216).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item C35). The options hold for any capture that meets the condition above. Counts only after author approval.

## Metadata
```yaml
id: "0436"
title: "Two sockets in Windows, one NUMA node in esxtop"
product: [vsphere, windows]
technology: [cpu, memory]
task: troubleshoot
level: 400
answer_type: deterministic
input: [screenshot]
object: [vm, guest-os, esxi]
tool: [guest-os-tools, esxtop]
knowledge:
  - vsphere/technology/cpu/concepts/virtual-numa
  - vsphere/technology/cpu/concepts/numa
  - vsphere/tools/esxtop/memory
knowledge_main: vsphere/technology/cpu/concepts/virtual-numa
attachments:
  - 0436/task-manager-cpu-two-sockets.png
  - 0436/coreinfo-numa-nodes.png
  - 0436/esxtop-memory-numa-fields.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C35"
answer: [B, C, F]
misconception: [A, D]
misconception_type: [layer-confusion, same-name-other-object]
pair: "0267"
status: awaiting-input
```
