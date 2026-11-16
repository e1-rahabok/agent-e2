# CPU hot add and the NUMA topology

## Prompt
- A Linux VM with 20 vCPUs and 128 GB of memory, virtual hardware version 19, runs a NUMA-aware database.
- The ESX host has 2 sockets. Each socket is one NUMA node with 16 cores and 256 GB of memory.
- CPU Hot Plug is enabled on the VM.
- The VM was powered on after CPU Hot Plug was enabled.

Which statements are correct?

- A. The Guest OS sees a single NUMA node.
- B. The Guest OS sees two virtual NUMA nodes of 10 vCPUs each, because the VM has more than 8 vCPUs.
- C. Cores per socket sets the virtual NUMA layout of this VM.
- D. CPU Hot Plug changes nothing for the Guest OS until a vCPU is actually hot added.
- E. ESX runs the 20 vCPUs across both physical nodes, because they do not fit one node of 16 cores.
- F. A vCPU hot added later joins the single node the Guest OS already sees.
- G. Part of the database's memory access goes to the other node's memory.
- H. Pin the VM to one socket with CPU and memory affinity so that all of its memory stays local.
- I. Adding `numa.allowHotadd = TRUE` in Advanced Parameters gives this VM two virtual nodes and keeps CPU Hot Plug.
- J. Upgrading the VM to hardware version 20 alone still leaves one virtual node while CPU Hot Plug is on.

## Answers
A, E, F, G, J

## Explanation
- A is true: enabling CPU Hot Plug deactivates virtual NUMA at power-on, whether or not a vCPU is ever added; the guest sees a flat layout.
- B is false: a VM with more than 8 vCPUs gets virtual NUMA by default, but not with hot add enabled.
- C is false: cores per socket does not set the virtual NUMA topology on current ESX versions.
- D is false: the topology is set at power-on, so hot add deactivates virtual NUMA from that moment, before any vCPU is added.
- E is true: 20 vCPUs exceed the 16 cores of one physical node, so ESX splits the VM over both nodes.
- F is true: with virtual NUMA off, hot-added vCPUs join the one node the guest sees.
- G is true: the database sees no node boundary, so it cannot place threads and memory by node; some of its memory is on the other node (remote).
- H is false: 20 vCPUs do not fit the 16 cores of one node, and affinity takes the VM out of NUMA management (no rebalancing, no memory migration). The fix is to turn CPU Hot Plug off (or size the VM to fit one node) and power-cycle it.
- I is false: `numa.allowHotadd` keeps virtual NUMA with CPU Hot Add only on virtual hardware 20 and later; on version 19 the guest still sees one node. The Advanced Parameters tab accepts any key without validating it, so an accepted key is no proof that ESX honors it.
- J is true: even on virtual hardware 20 and later, a VM with CPU Hot Plug gets one NUMA node by default; a virtual NUMA layout with hot plug needs a manual NUMA configuration (`numa.allowHotadd`).
- Misconception: B: virtual NUMA is exposed to every VM with more than 8 vCPUs, so the Guest OS sees the host layout. Or D: hot add costs nothing until it is used. Or I: the hot-add NUMA parameter taken to work on any hardware version.

## Notes
- Public source: vSphere 9.1 documentation (VMware vSphere 9.1 PDF, build of 2026-11-02), vSphere Resource Management, "Using Virtual NUMA" ("Enabling CPU HotAdd deactivates virtual NUMA", virtual NUMA is active by default above eight vCPUs, topology not influenced by cores per socket), and vSphere Virtual Machine Administration, "CPU Hot Plug" and "Virtual Topology in ESX". Broadcom KB 321931 (ESXi 7.x and 8.x; "Updated On" field empty).
- The stem keeps virtual hardware version 19, where CPU Hot Plug gives the guest one node on every reading (numa, virtual-numa).
- Changed in the 2026-11-15 audit: stem asks one question; tool `none` (no tool output is shown); I (false) and J (true) added on the hardware-version rule (virtual-numa, CPU Hot Add; numa, line on hot plug at hardware 20). Q216 (a), the lab check of `numa.allowHotadd`, is still open: I stays false on hardware 19 whatever it finds, and J rests on the default without the parameter.

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
tool: [none]
knowledge:
  - vsphere/object-types/vm/configuration/vm-configuration-review
  - vsphere/technology/cpu/concepts/virtual-numa
  - vsphere/technology/cpu/concepts/numa
knowledge_main: vsphere/object-types/vm/configuration/vm-configuration-review
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
misconception: [B, D, I]
misconception_type: [layer-confusion]
status: draft
```
