# Virtual sockets and virtual NUMA nodes

## Prompt
- ESXi 9.1 hosts: 2 sockets of 24 cores, one NUMA node per socket, 384 GB of memory per node.
- A Windows Server 2022 VM: 12 vCPUs, 64 GB of memory, virtual hardware version 21. Cores per socket is set by hand to 6, so the VM has 2 virtual sockets. CPU Hot Add is off.

Which statements about how the guest sees this VM, and how ESXi places it, are correct?

- A. Two virtual sockets give the guest two virtual NUMA nodes.
- B. ESXi sizes the virtual NUMA layout from the host's physical NUMA nodes and the VM's vCPU count.
- C. The guest sees one NUMA node: the 12 vCPUs and 64 GB fit one physical node.
- D. Windows reports the VM's NUMA node count, which follows the virtual NUMA layout.
- E. Task Manager in the Windows guest shows 2 sockets for this VM's CPU.
- F. Cores per socket has no effect on the guest beyond licensing.
- G. Set cores per socket to 12 so that ESXi keeps the VM's memory within one physical node.
- H. Virtual NUMA is off for this VM: its 12 vCPUs are below the default threshold.
- I. Pin the VM to one physical node with CPU and memory affinity to keep its memory local.
- J. A 12-vCPU VM on 24-core nodes runs on the hyper-threads of both sockets.

## Likely wrong answer
- A: "Two sockets in Windows mean two NUMA nodes."
- G: "Set cores per socket to the vCPU count to fix the memory placement."

## Expected key points
- Answer: B, C, D, E.
- A false: from vSphere 6.5 cores per socket does not set the virtual NUMA topology; it only sets how the vCPUs are presented to the guest as sockets.
- B true: the vNUMA topology is built at power-on from the NUMA topology of the host and the VM's vCPU count and memory.
- C true: a VM that fits one physical node is presented to the guest as one node; 12 vCPUs and 64 GB fit a node of 24 cores and 384 GB.
- D true: the guest's NUMA node count (Windows, or Coreinfo) shows the virtual NUMA layout; the socket count shows only the presentation.
- E true: 12 vCPUs at 6 cores per socket are presented as 2 sockets, which can matter for software licensing.
- F false: the over-correction. Some cores per socket values still give the guest a sub-optimal topology and can reduce performance.
- G false: cores per socket changes the socket count the guest sees, not where ESXi places the memory; the VM already fits one node.
- H false: by default vNUMA is active for VMs with more than 8 vCPUs, so it is on for this 12-vCPU VM.
- I false: affinity takes the VM out of NUMA management (no rebalancing, no memory migration).
- J false: a VM uses hyper-threads by size only when its vCPU count is above the physical core count of the node; 12 vCPUs fit 24 cores.

## Notes
- Sources: the knowledge base (virtual NUMA, section corespersocket: from vSphere 6.5 corespersocket no longer changes the vNUMA topology); Performance Best Practices for VMware vSphere 9.1, virtual NUMA; vSphere 9.1 Resource Management, Virtual NUMA ("not influenced by the number of virtual sockets and number of cores per socket").
- No option touches `numa.*` options in Advanced Parameters or when ESXi rebuilds the vNUMA layout: both are open (Q216).
- Changed in the 2026-11-15 audit: C and H reworded without "because" and "only"; E lengthened (it was the shortest option); key point B names the memory too.
- Converted from judged to multiple choice (Q199 F, 2026-11-14).
- Rewritten 2026-11-15 as the theory half of 0436 (design.md 3.9; review of the practical halves): the old text was the same case as 0436 (the DBA quote and the esxtop NHN and N%L values). Now a different VM (12 vCPUs, 6 cores per socket, 24-core nodes), no screen values, and options on the mechanism: virtual sockets, virtual NUMA nodes, physical nodes. Key changed from B, D, E to B, C, D, E.

## Metadata
```yaml
id: "0267"
title: "Virtual sockets and virtual NUMA nodes"
product: [windows, vsphere]
technology: [cpu, memory]
task: explain-mechanism
level: 400
answer_type: deterministic
answer: [B, C, D, E]
misconception: [A, G]
input: [text]
object: [guest-os, vm, esxi]
tool: [guest-os-tools]
knowledge:
  - vsphere/technology/cpu/concepts/virtual-numa
  - vsphere/technology/cpu/concepts/numa
knowledge_main: vsphere/technology/cpu/concepts/virtual-numa
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
misconception_type: [layer-confusion]
pair: "0436"
status: draft                     # reviewed as a free-text question; converted to multiple choice 2026-11-14 (Q199): review again
```
