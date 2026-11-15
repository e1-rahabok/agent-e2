# vNUMA after a move to an older host

## Prompt
- A cluster in the middle of a hardware refresh:
  - 6 old hosts: 2 sockets of 12 cores, 192 GB per socket. One NUMA node per socket.
  - 4 new hosts: 2 sockets of 32 cores, 512 GB per socket. One NUMA node per socket.
- A new SQL Server VM, 20 vCPUs and 160 GB, was first powered on on a new host. DRS later moved it to an old host. It has not been powered off since.
- Since the move, query times vary from day to day, and esxtop shows part of the VM's memory as remote.
- The DBA says SQL Server sees one NUMA node.

Why does the guest see one node, what does that cost on the old host, and what do you do until the refresh ends? Which statements are correct?

- A. The layout was built at power-on from the host the VM started on: 20 vCPUs fit one 32-core node, so the guest got one node.
- B. vMotion does not rebuild the virtual NUMA layout: a running guest cannot take a change of its NUMA topology.
- C. vMotion rebuilds the virtual NUMA layout for the destination host, so the guest always sees the layout of the host it runs on.
- D. On an old host ESXi spreads the VM over two nodes while the guest places work as if all memory were local: some access is remote.
- E. On an old host ESXi keeps all 20 vCPUs in one 12-core node by using its hyper-threads, so all the memory stays local.
- F. The remote memory in esxtop shows that the NUMA scheduler keeps moving the VM from one node to the other.
- G. The guest sees a single node, so NUMA cannot explain the variation, and storage is the next suspect to check.
- H. Setting 10 cores per socket on the VM makes the guest see two NUMA nodes, matching the old hosts.
- I. The guest sees one node because virtual NUMA is active by default only on VMs with more than 32 vCPUs.
- J. Until the refresh ends, keep the VM on hosts with the same NUMA layout: a DRS VM/Host rule, or a separate cluster.
- K. If the workload allows, sizing the VM to fit a 12-core node avoids the mismatch on both kinds of host.

## Likely wrong answer
- C: "vMotion rebuilds the virtual NUMA layout for the new host, so the guest is always right."
- G: "The variation must come from storage."

## Expected key points
- Answer: A, B, D, J, K.
- A true: the layout comes from the NUMA topology of the host at power-on, the VM's vCPU count and its memory; a VM that fits one node is presented as one node.
- B true: the layout stays through the move.
- C false: vMotion does not rebuild the layout.
- D true: 20 vCPUs are more than the 12 cores of an old node, so the VM is wide there; the guest, told it has one node, does not place work for two. Remote memory gives higher and uneven memory latency.
- E false: a VM with more vCPUs than cores per node runs on two or more nodes; using hyper-threads to stay in one node is a per-VM setting, not the default, and esxtop shows remote memory.
- F false: the remote memory comes from a wide VM whose guest does not know it spans two nodes, not from repeated moves between nodes.
- G false: the move to a host with a different NUMA layout explains remote memory and uneven query times.
- H false: since vSphere 6.5, cores per socket changes only how vCPUs are presented to the guest, not the virtual NUMA layout.
- I false: by default virtual NUMA is active on VMs with more than 8 vCPUs; the one node comes from the host the VM first started on.
- J true: clusters of hosts with the same NUMA layout give the best results.
- K true: at most 12 vCPUs and 160 GB fit one node of either host; a change of the vCPU count rebuilds the layout.

## Notes
- Converted from judged to multiple choice (Q199 F, 2026-11-14). Left out of the options: whether the next power cycle on an old host rebuilds the layout (and `VPXD_PersistVnuma`): open author question Q216 (the vSphere 9.1 TechDocs say the topology does not change unless the vCPU count changes).

## Metadata
```yaml
id: "0113"
title: "vNUMA after a move to an older host"
product: [vsphere, windows]
technology: [cpu, memory]
task: decide-capacity
level: 400
answer_type: deterministic
answer: [A,B,D,J,K]
misconception: [C,G]
input: [text]
object: [vm, esxi, cluster]
tool: [esxtop]
knowledge:
  - vsphere/technology/cpu/concepts/virtual-numa
  - vsphere/technology/cpu/concepts/numa
knowledge_main: vsphere/technology/cpu/concepts/virtual-numa
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
misconception_type: [threshold-transplanted]
status: draft                     # reviewed as a free-text question; converted to multiple choice 2026-11-14 (Q199): review again
```
