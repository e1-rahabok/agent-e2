# CPU hot add and the NUMA topology

## Prompt
- A Linux VM with 20 vCPUs and 128 GB of memory, virtual hardware version 19, runs a NUMA-aware database.
- The ESX host has 2 sockets. Each socket is one NUMA node with 16 cores and 256 GB of memory.
- CPU Hot Plug is enabled on the VM.
- The VM was powered on after CPU Hot Plug was enabled.

What does the Guest OS see, and what follows for the database? Which statements are correct?

- A. The Guest OS sees a single NUMA node.
- B. The Guest OS sees two virtual NUMA nodes of 10 vCPUs each, because the VM has more than 8 vCPUs.
- C. Cores per socket sets the virtual NUMA layout of this VM.
- D. CPU Hot Plug changes nothing for the Guest OS until a vCPU is actually hot added.
- E. ESX runs the 20 vCPUs across both physical nodes, because they do not fit one node of 16 cores.
- F. A vCPU hot added later joins the single node the Guest OS already sees.
- G. Part of the database's memory access goes to the other node's memory.

## Likely wrong answer
B: virtual NUMA is exposed to every VM with more than 8 vCPUs, so the Guest OS sees the host layout. Or D: hot add costs nothing until it is used.

## Expected key points
- Answer: A, E, F, G.
- A is true: enabling CPU Hot Plug deactivates virtual NUMA at power-on, whether or not a vCPU is ever added; the guest sees a flat layout.
- B is false: a VM with more than 8 vCPUs gets virtual NUMA by default, but not with hot add enabled.
- C is false: cores per socket does not set the virtual NUMA topology on current ESX versions.
- D is false: the topology is set at power-on, so hot add deactivates virtual NUMA from that moment, before any vCPU is added.
- E is true: 20 vCPUs exceed the 16 cores of one physical node, so ESX splits the VM over both nodes.
- F is true: with virtual NUMA off, hot-added vCPUs join the one node the guest sees.
- G is true: the database sees no node boundary, so it cannot place threads and memory by node; some of its memory is on the other node (remote).

## Notes
- Public source: vSphere 9.1 documentation (VMware vSphere 9.1 PDF, build of 2026-11-02), vSphere Resource Management, "Using Virtual NUMA" ("Enabling CPU HotAdd deactivates virtual NUMA", virtual NUMA is active by default above eight vCPUs, topology not influenced by cores per socket), and vSphere Virtual Machine Administration, "CPU Hot Plug" and "Virtual Topology in ESX". Broadcom KB 321931 (ESXi 7.x and 8.x; "Updated On" field empty).
- Debatable risk: the 9.1 page "Virtual Topology in ESX" says ESX 8.0 and later (hardware version 20 or later) can expose NUMA for virtual devices and a vNUMA topology with CPU hotplug enabled, and that by default a VM with hotplug enforces a single NUMA node. The question uses hardware version 19, where the older rule holds, so the guest sees one node on every reading.
- Rewritten 2026-11-14 to one fact per option (design.md 3.9; project/question-pairing-2026-11-14.md): the stem line on an advanced NUMA parameter was removed (it touched open author question Q216); D, F and G are new. Key changed from B to A, E, F, G.

## Metadata
```yaml
id: "0293"
title: CPU hot add and the NUMA topology
product: [vsphere, linux]
technology: [cpu, memory]
task: explain-mechanism
level: 400
answer_type: deterministic
input: [text]
object: [vm, guest-os, esxi]
tool: [guest-os-tools]
knowledge:
  - vsphere/object-types/vm/configuration/vm-configuration-review
  - vsphere/technology/cpu/concepts/virtual-numa
  - vsphere/technology/cpu/concepts/numa
knowledge_main: vsphere/object-types/vm/configuration/vm-configuration-review
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
answer: [A, E, F, G]
misconception: [B, D]
misconception_type: []
status: draft
```
