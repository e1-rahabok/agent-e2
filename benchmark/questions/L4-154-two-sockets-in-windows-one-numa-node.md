# Two sockets in Windows, one NUMA node in esxtop

## Prompt
- The database administrator of a SQL Server VM sends [the Task Manager CPU page](0436/task-manager-cpu-two-sockets.png): "The VM is split over both host CPUs; fix the socket setting."
- You add [the Coreinfo output from the same VM](0436/coreinfo-numa-nodes.png) and [the esxtop memory panel with the NUMA fields](0436/esxtop-memory-numa-fields.png) of its host.

Which statements are correct?

- A. Windows lays out its memory in two NUMA nodes, one per socket it shows.
- B. esxtop shows the VM with one home node and all of its memory local to that node.
- C. Coreinfo shows that the guest sees a single NUMA node.
- D. esxtop shows part of the VM's memory on a remote node.
- E. Change the socket setting and reboot, so that the memory moves back onto one host CPU.
- F. Since the memory is already local, the two sockets Windows shows are of no consequence for SQL Server.
- G. The home node esxtop shows can change later with no change to the VM's settings.

## Input to supply
- Product and version: ESXi 9.1 host whose NUMA node has at least 16 cores and more memory than the VM; vSphere Client 9.1; a Windows Server 2022 or 2025 VM.
- VM: 16 vCPUs with cores per socket set by hand to 8 (2 virtual sockets), memory well within one node (for example 64-128 GB), no CPU Hot Add, no affinity.
- Screen 1: Task Manager > Performance > CPU, showing Sockets 2 and Logical processors 16. Save as `0436/task-manager-cpu-two-sockets.png`.
- Screen 2: Sysinternals Coreinfo run in the VM (`coreinfo -n`, or `coreinfo` with the NUMA section visible), showing one NUMA node with all 16 logical processors. Save as `0436/coreinfo-numa-nodes.png`.
- Screen 3: esxtop on the host, memory panel (`m`), NUMA STATS fields on (`f`, then the NUMA field letter), the VM's row with NHN, NMIG, NRMEM, NLMEM and N%L. Save as `0436/esxtop-memory-numa-fields.png`.
- Condition the key depends on: Task Manager Sockets 2, Logical processors 16; Coreinfo one NUMA node; esxtop NHN a single node number and N%L 100 (99 or more), NRMEM 0 or near 0.
- Masking: mask every VM, host, datastore and cluster name, including the VM's row name in esxtop and the computer name in the guest tools.

## Likely wrong answer
A: the socket count read as the NUMA layout, and E, the change that follows from it.

## Expected key points
- Answer: B, C, G.
- A false: the misconception. Cores per socket only changes how the vCPUs are presented to the guest as sockets; Coreinfo shows one NUMA node.
- B true: one number in NHN is one home node (the VM is one NUMA client); N%L at 100 means all memory is local.
- C true: the guest's NUMA node count, not its socket count, shows the layout it sees; a VM that fits one physical node gets one virtual node.
- D false: NRMEM is 0 or near 0 and N%L is 100.
- E false: the wrong action. The memory is already on one node, and cores per socket does not decide where ESXi places memory.
- F false: the over-correction. The socket count is what per-socket software licensing reads, and some cores per socket values still give the guest a sub-optimal topology.
- G true: the NUMA rebalancer checks node loads every 2 seconds and can move a VM to a less loaded node; its memory then follows page by page.

## Notes
- Review 2026-11-15: the administrator's quote and every option reworded away from the theory half 0267; D added as a false reading of esxtop; G added (the home node can move). Key changed from B, C, F to B, C, G.
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
answer: [B, C, G]
misconception: [A, E]
misconception_type: [layer-confusion, same-name-other-object]
pair: "0267"
status: awaiting-input
```
