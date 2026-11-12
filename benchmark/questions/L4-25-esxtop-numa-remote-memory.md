# Remote memory in the esxtop NUMA columns

## Prompt
- ESXi 9.1 host: 2 sockets of 16 cores, Hyper-Threading on, 768 GB of DRAM (384 GB per NUMA node). Advanced settings at their defaults.
- The database VM `db-ora-07` has 12 vCPUs and 512 GB of memory. Its owner reports that query times vary from day to day, worse since the memory was raised from 320 GB to 512 GB last month.
- esxtop, memory panel (m) with the NUMA fields added, at 14:00:

```text
NAME         MEMSZ     NHN  NMIG  NRMEM    N%L  GST_ND0  GST_ND1
db-ora-07    524288    0    4     186368   64   337920   186368
app-web-01   16384     1    1     0        100  0        16384
app-web-02   16384     0    0     0        100  16384    0
etl-03       65536     1    2     0        100  0        65536
vdi-pool-11  8192      0    0     0        100  8192     0
```

- The same panel at 14:10:

```text
NAME         MEMSZ     NHN  NMIG  NRMEM    N%L  GST_ND0  GST_ND1
db-ora-07    524288    0    4     186368   64   337920   186368
app-web-01   16384     1    1     0        100  0        16384
app-web-02   16384     0    0     0        100  16384    0
etl-03       65536     1    2     0        100  0        65536
vdi-pool-11  8192      0    0     0        100  8192     0
```

What do the NUMA columns show for `db-ora-07`, why, and what do you recommend?

## Likely wrong answer
"NMIG is 4, so the VM keeps moving between nodes right now: pin it to node 0 with CPU and memory affinity."

## Expected key points
- The vCPUs have one home node (NHN 0), but 182 GB of the 512 GB is on node 1: N%L 64%, NRMEM 186,368 MB. About a third of its memory is remote, and accesses to it are slower.
- Cause: the memory is larger than what one 384 GB node can hold. 12 vCPUs fit in 16 cores, so ESXi keeps the VM as one NUMA client on node 0; the memory that does not fit there lands on node 1.
- The raise to 512 GB caused it; before, 320 GB fitted in one node.
- NMIG did not change between the two samples (4 at 14:00 and at 14:10), and NHN and N%L are the same: no migration now. The remote memory is steady, not a rebalancing in progress.
- Recommend: size the memory to fit one node, from what the database needs inside the guest; or, if it needs more than a node, split the VM so that each part's memory is local (two NUMA clients, two vNUMA nodes the database can use).
- Do not set CPU or memory affinity: the VM then leaves NUMA management, with no rebalancing or memory migration.

## Notes
- The split: `maxPerMachineNode` limits the vCPUs per NUMA node, so ESXi places the VM as two NUMA clients with local memory each, and vNUMA shows two nodes ([`vsphere/technology/cpu/configuration/numa-settings`](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/configuration/numa-settings.md)). Sizing a VM larger than one node to split evenly across as few nodes as possible: Performance Best Practices for vSphere 9.1, vNUMA.
- Revised 2026-11-12 (question set 1.0): the esxtop screenshot that was to be supplied is now an esxtop excerpt typed as text. The cause changed from vCPU count (tested by L4-22, wide VM placement) to memory size larger than a node.

## Metadata
```yaml
id: "0067"
title: "Remote memory in the esxtop NUMA columns"
product: [vsphere]
technology: [memory, cpu]
task: troubleshoot
level: 400
answer_type: judged
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
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
misconception_type: [cumulative-vs-current]
status: draft
```
