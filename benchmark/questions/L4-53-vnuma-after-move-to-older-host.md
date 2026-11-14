# vNUMA after a move to an older host

## Prompt
- A cluster in the middle of a hardware refresh:
  - 6 old hosts: 2 sockets of 12 cores, 192 GB per socket. One NUMA node per socket.
  - 4 new hosts: 2 sockets of 32 cores, 512 GB per socket. One NUMA node per socket.
- A new SQL Server VM, 20 vCPUs and 160 GB, was first powered on on a new host. DRS later moved it to an old host. It has not been powered off since.
- Since the move, query times vary from day to day, and esxtop shows part of the VM's memory as remote.
- The DBA says SQL Server sees one NUMA node.

Why does the guest see one node? What does that cost on the old host, and what do you do until the refresh ends?

## Likely wrong answer
"vMotion rebuilds the virtual NUMA layout for the new host, so the guest is always right. The variation must come from storage."

## Expected key points
- vNUMA is built at power-on, from the host the VM starts on: 20 vCPUs fit one 32-core node, so the guest got one virtual node.
- The layout does not follow the VM across vMotion: a running guest cannot take a NUMA change. In vSphere 9.1 (virtual hardware 20 and later) the next power cycle rebuilds it for the host the VM powers on, unless the cluster keeps layouts (`VPXD_PersistVnuma`).
- On an old host the 20 vCPUs do not fit a 12-core node: ESXi splits the VM over two physical nodes, but the guest still schedules as if all its memory were local. Threads read remote memory without knowing: higher and uneven memory latency.
- Until the refresh ends, keep the VM on hosts with the same NUMA layout: a DRS VM/Host rule to the new hosts, or a separate cluster. Clusters of hosts with the same NUMA layout avoid the problem.
- If the VM must run on the old hosts: a power cycle there rebuilds the layout to match them (two virtual nodes, 10 vCPUs and 80 GB each); or size it to fit a 12-core node. A later power-on on a new host rebuilds it again.

## Metadata
```yaml
id: "0113"
title: "vNUMA after a move to an older host"
product: [vsphere, windows]
technology: [cpu, memory]
task: decide-capacity
level: 400
answer_type: judged
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
status: reviewed
```
