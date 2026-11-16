# Two sockets in Windows, one NUMA node in esxtop

## Prompt
- The database administrator of the SQL Server VM sql-prd-04 (16 vCPUs, 96 GB) writes: "Task Manager shows Sockets: 2. The VM is split over both host CPUs; fix the socket setting."
- The host has 2 sockets of 24 cores and 768 GB of memory (384 GB per NUMA node).
- You run `coreinfo -s -n` in the guest; the socket and NUMA sections:

```text
Logical Processor to Socket Map:
********--------  Socket 0
--------********  Socket 1

Logical Processor to NUMA Node Map:
****************  NUMA Node 0
```

- And esxtop on its host, memory panel with the NUMA fields added:

```text
(generated)
```

Which statements are correct?

- A. Windows lays out its memory in two NUMA nodes, one per socket it shows.
- B. esxtop shows the VM with one home node and all of its memory local to that node.
- C. Coreinfo shows that the guest sees a single NUMA node.
- D. esxtop shows part of the VM's memory on a remote node.
- E. Change the socket setting and reboot, so that the memory moves back onto one host CPU.
- F. Since the memory is already local, the two sockets Windows shows are of no consequence for SQL Server.
- G. The home node esxtop shows can change later with no change to the VM's settings.

## Likely wrong answer
A: the socket count read as the NUMA layout, and E, the change that follows from it.

## Expected key points
- Answer: B, C, G.
- A false: the misconception. Cores per socket only changes how the vCPUs are presented to the guest as sockets; Coreinfo maps all 16 logical processors to NUMA Node 0.
- B true: the sql-prd-04 row has one number in NHN (1): one home node, the VM is one NUMA client. NRMEM is 0.00, NLMEM holds its memory and N%L is 100: all memory is local.
- C true: the guest's NUMA node count, not its socket count, shows the layout it sees; a VM that fits one physical node gets one virtual node. Coreinfo lists one node with all 16 logical processors.
- D false: reading. On the sql-prd-04 row NRMEM is 0.00 and N%L is 100. Another VM on the host (etl-big-02) has remote memory; sql-prd-04 has none.
- E false: the wrong action. The memory is already on one node, and cores per socket does not decide where ESXi places memory.
- F false: the over-correction. The socket count is what per-socket software licensing reads, and some cores per socket values still give the guest a sub-optimal topology.
- G true: the NUMA rebalancer checks node loads every 2 seconds and can move a VM to a less loaded node; its memory then follows page by page.

## Notes
- Review 2026-11-15: the administrator's quote and every option reworded away from the theory half 0267; D added as a false reading of esxtop; G added (the home node can move). Key changed from B, C, F to B, C, G.
- Practical half of 0267 (pair: design.md, section 3.9).
- No option rests on `numa.*` advanced options or on when ESXi rebuilds the vNUMA layout (open question Q216), nor on NMIG (not in the vSphere 9.1 documentation's esxtop memory panel).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item C35). Counts only after author approval.
- Converted to exports 2026-11-15 (project/practical-questions-as-exports-2026-11-15.md): Task Manager has no export, so its Sockets label stays in the administrator's words; Coreinfo as literal text, esxtop memory panel as generated text. No option changed.

## Metadata
```yaml
id: "0436"
title: "Two sockets in Windows, one NUMA node in esxtop"
product: [vsphere, windows]
technology: [cpu, memory]
task: troubleshoot
level: 400
answer_type: deterministic
input: [text]
object: [vm, guest-os, esxi]
tool: [guest-os-tools, esxtop]
knowledge:
  - vsphere/technology/cpu/concepts/virtual-numa
  - vsphere/technology/cpu/concepts/numa
  - vsphere/tools/esxtop/memory
knowledge_main: vsphere/technology/cpu/concepts/virtual-numa
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C35"
answer: [B, C, G]
misconception: [A, E]
misconception_type: [layer-confusion, same-name-other-object]
pair: "0267"
status: draft
```
