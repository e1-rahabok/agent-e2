# Two sockets in Windows, one NUMA node

## Prompt
- ESXi 9.1 host: 2 sockets, 20 cores per socket, 512 GB of DRAM per socket. One NUMA node per socket.
- A SQL Server VM on Windows Server 2022: 16 vCPUs, 128 GB of memory.
- For licensing, the VM's cores per socket was set by hand to 8. Windows Task Manager shows 2 sockets and 16 logical processors.
- esxtop, memory panel with the NUMA columns, VM row: NHN 1, N%L 100.
- The database administrator says: "Windows shows two sockets, so the VM spans two NUMA nodes and half of its memory is remote. Set cores per socket to 16 to fix it."

Is the administrator right? What decides the NUMA layout the VM gets, and what does cores per socket change?

## Likely wrong answer
"Two sockets in Windows mean two NUMA nodes and remote memory; set cores per socket to 16."

## Expected key points
- No: the VM runs in one NUMA node with all of its memory local (one home node, N%L 100).
- Since vSphere 6.5, cores per socket does not set the NUMA layout. It only sets how the vCPUs are presented to the guest as sockets, which matters for licensing.
- ESXi builds the VM's virtual NUMA layout from the host's physical NUMA nodes. 16 vCPUs and 128 GB fit one node of 20 cores and 512 GB, so the VM gets one NUMA node.
- Windows sees two sockets but one NUMA node: read the NUMA node count in Windows, or the esxtop NUMA columns, not the socket count.
- Changing cores per socket to 16 changes the socket count Windows and SQL Server see, not where ESXi places the memory; it fixes nothing here.

## Notes
- Sources: the knowledge base (virtual NUMA, section corespersocket: from vSphere 6.5 corespersocket no longer changes the vNUMA topology; the 16-vCPU example that fits one node); Performance Best Practices for VMware vSphere 9.1, virtual NUMA. Replaces a draft on Task Manager vs Performance Monitor whose key could not be verified in a VM (ESXi does not show the guest the host clock registers).

## Metadata
```yaml
id: "0267"
title: "Two sockets in Windows, one NUMA node"
product: [windows, vsphere]
technology: [cpu, memory]
task: explain-mechanism
level: 400
answer_type: judged
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
source_path: "Drafted by Claude 2026-11-12 for the Guest OS slots (project/plan.md, M2)"
misconception_type: [layer-confusion]
status: draft
```
