# CPU hot add and the NUMA topology

## Prompt
- A Linux VM with 20 vCPUs and 128 GB of memory, virtual hardware version 19, runs a NUMA-aware database.
- The ESX host has 2 sockets. Each socket is one NUMA node with 16 cores and 256 GB of memory.
- CPU Hot Plug is enabled on the VM. The numa.allowHotadd advanced parameter is not set.
- The VM was powered on after CPU Hot Plug was enabled.

What does the Guest OS see, and what follows for the database?

- A. Two virtual NUMA nodes of 10 vCPUs each, because the VM has more than 8 vCPUs and does not fit one host NUMA node.
- B. One NUMA node. The Guest OS cannot place threads and memory by node, while the 20 vCPUs cannot fit in one physical node of 16 cores.
- C. Two virtual NUMA nodes, one for each virtual socket, because cores per socket sets the virtual NUMA topology.
- D. One NUMA node, and ESX keeps the whole VM in one physical node, so all memory access stays local.
- E. One NUMA node at power-on. A second virtual node appears when the first vCPU is hot added.

## Likely wrong answer
A or C: virtual NUMA is exposed to every VM with more than 8 vCPUs, so the Guest OS sees the host layout.

## Expected key points
- Answer: B.
- Enabling CPU Hot Plug deactivates virtual NUMA: the VM gets a single NUMA node and the hot-added CPUs run in that node. The vSphere documentation says so, and Broadcom KB 321931 adds that the guest sees a flat layout.
- A VM with more than 8 vCPUs gets virtual NUMA by default, but not with hot add (A and C are wrong). Cores per socket does not set the virtual NUMA topology on current ESX versions.
- 20 vCPUs exceed the 16 cores of one physical node, so ESX cannot keep the VM in one node (D is wrong). The database sees no node boundary and can access memory of the other node.
- Virtual NUMA with hot add needs the numa.allowHotadd parameter, and a manual NUMA configuration (E is wrong without it).
- Use CPU Hot Plug only on VMs that need it and where the loss of virtual NUMA does not matter.

## Notes
- Public source: vSphere 9.1 documentation (VMware vSphere 9.1 PDF, build of 2026-11-02), vSphere Resource Management, "Using Virtual NUMA" ("Enabling CPU HotAdd deactivates virtual NUMA", virtual NUMA is active by default above eight vCPUs, topology not influenced by cores per socket), and vSphere Virtual Machine Administration, "CPU Hot Plug" and "Virtual Topology in ESX". Broadcom KB 321931 (ESXi 7.x and 8.x; "Updated On" field empty).
- Why one answer: the documentation states the hot add effect, the default threshold, and that cores per socket does not influence the topology. The 20 vCPUs against 16 cores is arithmetic.
- Debatable risk: the 9.1 page "Virtual Topology in ESX" says ESX 8.0 and later (hardware version 20 or later) can expose NUMA for virtual devices and a vNUMA topology with CPU hotplug enabled, and that by default a VM with hotplug enforces a single NUMA node. The question uses hardware version 19, where the older rule holds, and does not set numa.allowHotadd, so the guest sees one node on every reading.

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
answer: [B]
misconception: [A, C]
misconception_type: []
status: draft
```
