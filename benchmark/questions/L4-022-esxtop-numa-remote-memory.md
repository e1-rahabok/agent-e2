# Remote memory in the esxtop NUMA columns

## Prompt
- ESXi 9.1 host: 2 sockets of 16 cores, Hyper-Threading on, 768 GB of DRAM (384 GB per NUMA node). Advanced settings at their defaults.
- The database VM `db-ora-07` has 12 vCPUs and 512 GB of memory. Its owner reports that query times vary from day to day.
- esxtop, memory panel (m) with the NUMA fields added, at 14:00:

```text
NAME         MEMSZ     NHN  NRMEM    N%L  GST_ND0  GST_ND1
db-ora-07    524288    0    186368   64   337920   186368
app-web-01   16384     1    0        100  0        16384
app-web-02   16384     0    0        100  16384    0
etl-03       65536     1    0        100  0        65536
vdi-pool-11  8192      0    0        100  8192     0
```

- The same panel at 14:10:

```text
NAME         MEMSZ     NHN  NRMEM    N%L  GST_ND0  GST_ND1
db-ora-07    524288    0    186368   64   337920   186368
app-web-01   16384     1    0        100  0        16384
app-web-02   16384     0    0        100  16384    0
etl-03       65536     1    0        100  0        65536
vdi-pool-11  8192      0    0        100  8192     0
```

Which statements about the NUMA columns of `db-ora-07`, their cause and the fix are correct?

- A. The vCPUs of db-ora-07 have one home node, node 0: one NUMA client, not a wide VM.
- B. The remote memory shows that ESXi keeps moving the VM between the two nodes of the host.
- C. About 182 GB of the VM's 512 GB sits on node 1, remote to its vCPUs.
- D. N%L of 64 means that 64% of the VM's memory is remote to its vCPUs.
- E. The cause is memory larger than one node: 512 GB does not fit in a 384 GB node.
- F. 12 vCPUs are more than one NUMA node holds, so ESXi splits the VM across both nodes.
- G. The same NHN, NRMEM and N%L at 14:00 and 14:10 show steady placement, not a migration.
- H. The NUMA rebalancer will make the remote memory local within minutes once the host is quiet.
- I. Pinning the VM to node 0 with CPU and memory affinity would put all 512 GB of its memory on node 0.
- J. Size the memory to fit one node, from what the database needs inside the guest.
- K. For a database that needs more memory than one node, split the VM into NUMA clients that each fit a node.
- L. A VM with manual CPU or memory affinity gets no NUMA rebalancing and no memory migration.
- M. Configured with 320 GB of memory, the same VM would fit one node, with no remote memory.

## Answers
A, C, E, G, J, K, L, M

## Explanation
- A is correct: NHN shows one number. 12 vCPUs fit in 16 cores, so ESXi keeps the VM as one NUMA client on node 0.
- B is wrong: NHN, NRMEM and N%L are the same in both samples: no migration now.
- C is correct: NRMEM 186,368 MB is about 182 GB; GST_ND1 shows the same amount on node 1. About a third of the memory is remote, and accesses to it are slower.
- D is wrong: N%L is the local share: 64% local, 36% remote.
- E is correct: the memory that does not fit in node 0 lands on node 1.
- F is wrong: each node has 16 cores; 12 vCPUs fit one node, and NHN shows a single home node.
- G is correct: a migration shows N%L climbing between samples; steady values are placement.
- H is wrong: the home node cannot hold 512 GB, so no rebalancing makes the remote part local.
- I is wrong: node 0 holds 384 GB, so no affinity can make 512 GB local; affinity also takes the VM out of NUMA management.
- J is correct: size from the guest's need, not from the configured 512 GB.
- K is correct: two NUMA clients, each with local memory, and two vNUMA nodes the database can use. Size it to split evenly across as few nodes as possible.
- L is correct: manual CPU or memory affinity removes the VM from NUMA scheduling.
- M is correct: 320 GB fits in one 384 GB node (with the 24 GB of the other VMs on node 0), so a VM of 12 vCPUs and 320 GB stays local; remote memory starts when memory is raised past one node's capacity.
- Misconception: B: "The remote memory means ESXi keeps moving the VM between nodes." - I: "Pin it to node 0 with CPU and memory affinity, and its memory becomes local."

## Notes
- NMIG left out (author, Q-E2-191 e: its meaning is unsure; not in the benchmark before 1.0).
- The split: `maxPerMachineNode` limits the vCPUs per NUMA node, so ESXi places the VM as two NUMA clients with local memory each, and vNUMA shows two nodes ([`vsphere/technology/cpu/configuration/numa-settings`](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/configuration/numa-settings.md)). Sizing a VM larger than one node to split evenly across as few nodes as possible: Performance Best Practices for vSphere 9.1, vNUMA.
- Revised 2026-11-12: the esxtop screenshot that was to be supplied is now an esxtop excerpt typed as text. The cause changed from vCPU count (tested by L4-22, wide VM placement) to memory size larger than a node.
- Converted from judged to multiple choice (Q-E2-199 F, 2026-11-14). No option names a `numa.*` setting or the vNUMA rebuild at power cycle (open author question Q-E2-216).
- Changed in the 2026-11-15 audit: K lost its hedge ("If the database needs ...") and stays an action; misconception_type cumulative-vs-current removed (no option reads a running total as current).
- A, E, G, H and M rest on the numa line for a VM whose vCPUs fit one node but whose memory does not (vsphere/technology/cpu/concepts/numa, open review note: lab test on a 9.1 host); vsphere/tools/esxtop/memory (NRMEM) states the same reading as settled.
- Changed 2026-11-16: the stem no longer tells the story of the raise from 320 GB to 512 GB (it restated the knowledge base's typical cause and pointed at E and M). M now asks whether the same VM at 320 GB would fit one node, true as before.

## Metadata
```yaml
id: "0067"
title: "Remote memory in the esxtop NUMA columns"
product: [vsphere]
technology: [memory, cpu]
task: troubleshoot
level: 400
answer_type: deterministic
misconception: [B,I]
input: [text]
object: [vm, esxi]
tool: [esxtop]
knowledge:
  - vsphere/tools/esxtop/memory
  - vsphere/technology/cpu/concepts/numa
  - vsphere/technology/cpu/concepts/virtual-numa
  - vsphere/technology/cpu/configuration/numa-settings
knowledge_main: vsphere/tools/esxtop/memory
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-05"
misconception_type: []
status: draft
```
