# Two sockets in Windows, one NUMA node

## Prompt
- VMware ESXi 9.1 host: 2 sockets, 20 cores per socket, 512 GB of DRAM per socket. One NUMA node per socket.
- A SQL Server VM on Windows Server 2022: 16 vCPUs, 128 GB of memory.
- For licensing, the VM's cores per socket was set by hand to 8. Windows Task Manager shows 2 sockets and 16 logical processors.
- esxtop, memory panel with the NUMA columns, VM row: NHN 1, N%L 100.
- The database administrator says: "Windows shows two sockets, so the VM spans two NUMA nodes and half of its memory is remote. Set cores per socket to 16 to fix it."

Which statements are correct?

- A. The administrator is right: two sockets in Windows mean two NUMA nodes, with half of the memory remote.
- B. NHN 1 and N%L 100 in esxtop show one home node, with all of the VM's memory local to that node.
- C. Since vSphere 6.5, cores per socket still sets the virtual NUMA layout when it is set by hand, as here for licensing.
- D. ESXi builds the virtual NUMA layout from the host's nodes; 16 vCPUs and 128 GB fit one node, so the VM gets one virtual node.
- E. To see the NUMA layout from inside the guest, read the NUMA node count in Windows, not the socket count.
- F. Setting cores per socket to 16 is needed so that ESXi keeps the VM's memory within one node.
- G. Virtual NUMA is off for this VM by default, because it applies only to VMs of 8 vCPUs or fewer.
- H. With cores per socket at 8, ESXi creates two virtual NUMA nodes of 8 vCPUs each and splits the memory between them.
- I. Pinning the VM to node 1 with CPU and memory affinity is the safe way to keep its memory local.
- J. A remote-memory value that stays the same across two esxtop samples means ESXi keeps migrating the VM between nodes.
- K. With 16 vCPUs on 20-core nodes the VM must run on hyper-threads, which spreads it over both sockets.

## Likely wrong answer
- A: "Two sockets in Windows mean two NUMA nodes and remote memory."
- F: "Set cores per socket to 16 to fix it."

## Expected key points
- Answer: B, D, E.
- A false: the VM runs in one NUMA node with all memory local (NHN 1, N%L 100); the socket count is a presentation for licensing.
- B true: one number in NHN is one home node; N%L 100 is all memory local.
- C false: from vSphere 6.5 cores per socket, set by hand or not, only changes how the vCPUs are presented to the guest as sockets, which can matter for licensing; vNUMA takes its layout from the host.
- D true: vNUMA takes its topology from the host; 16 vCPUs and 128 GB fit one node of 20 cores and 512 GB.
- E true: Windows sees two sockets but one NUMA node; the node count, or the esxtop NUMA columns, show the layout.
- F false: cores per socket changes the socket count Windows and SQL Server see, not where ESXi places the memory.
- G false: by default vNUMA is active only for VMs with more than 8 vCPUs, so it is on for this 16-vCPU VM.
- H false: that was the behaviour before vSphere 6.5; now the VM fits one physical node and gets one virtual node.
- I false: affinity takes the VM out of NUMA management (no rebalancing, no memory migration).
- J false: steady remote memory over samples is placement (memory larger than the node), not a migration; a migration shows N%L climbing.
- K false: hyper-threads come into play by size when the vCPU count is above the physical core count of the node; 16 vCPUs fit its 20 cores, and NHN 1 shows one home node.

## Notes
- Sources: the knowledge base (virtual NUMA, section corespersocket: from vSphere 6.5 corespersocket no longer changes the vNUMA topology; the 16-vCPU example that fits one node); Performance Best Practices for VMware vSphere 9.1, virtual NUMA. Replaces a draft on Task Manager vs Performance Monitor whose key could not be verified in a VM (ESXi does not show the guest the host clock registers).
- No option touches `numa.*` options in Advanced Parameters or when ESXi rebuilds the vNUMA layout: both are open (Q216).
- Converted from judged to multiple choice (Q199 F, 2026-11-14).
- Review 2026-11-14: option C turned from a true statement into a false near-miss (cores per socket set by hand) that tests the same fact, so fewer options are true.

## Metadata
```yaml
id: "0267"
title: "Two sockets in Windows, one NUMA node"
product: [windows, vsphere]
technology: [cpu, memory]
task: explain-mechanism
level: 400
answer_type: deterministic
answer: [B, D, E]
misconception: [A, F]
input: [text]
object: [guest-os, vm, esxi]
tool: [guest-os-tools, esxtop]
knowledge:
  - vsphere/technology/cpu/concepts/virtual-numa
  - vsphere/technology/cpu/concepts/numa
  - vsphere/tools/esxtop/memory
knowledge_main: vsphere/technology/cpu/concepts/virtual-numa
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
misconception_type: [layer-confusion]
status: draft                     # reviewed as a free-text question; converted to multiple choice 2026-11-14 (Q199): review again
```
