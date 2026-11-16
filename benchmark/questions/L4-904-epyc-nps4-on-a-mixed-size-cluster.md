# NPS-4 on an AMD EPYC 9005 cluster of mixed VM sizes

## Prompt
- New cluster db-02, ESXi 9.1, 6 hosts. Each host: 2 × AMD EPYC 9005 with 96 cores per socket (12 CCDs of 8 cores around one I/O die), 12 DDR5 channels per socket, 1.5 TB of memory, Hyper-Threading on.
- The server team set NUMA Nodes per Socket to NPS-4 in the BIOS "for memory locality". CCX as NUMA Domain is off.
- The cluster runs VMs of mixed sizes. db-sql-01 has 40 vCPUs and 160 GB of memory.
- esxtop memory panel, two samples 10 minutes apart:
  - db-sql-01: NHN 0,1; N%L 54 in both samples.
  - the 8-vCPU VMs: one home node each; N%L 100.
- The DBA asks whether NPS-4 was the right choice for this cluster.

Which statements are correct?

- A. At NPS-4 each NUMA node holds 24 cores and 3 of the socket's 12 memory channels.
- B. NPS-4 gives every VM local memory, because each quarter of the socket has its own memory controllers.
- C. On this processor the NPS-4 boundaries remove no die-to-die hop: every CCD reaches every memory controller through the one I/O die.
- D. At NPS-1, db-sql-01 fits in one NUMA node whose memory is interleaved over all 12 channels.
- E. Turn on CCX as NUMA Domain as well, so that ESX keeps each VM's vCPUs inside one L3 cache.
- F. Even at NPS-1, the 40 vCPUs of db-sql-01 span several CCDs, so they do not share one L3 cache.
- G. Inside one NUMA node every core reaches every other core at the same cost.
- H. N%L of 54 in both samples shows a NUMA migration in progress that will finish without action.
- I. Set numa.migThreshold to 50 or more, so that db-sql-01 keeps its memory local.
- J. Return the cluster to NPS-1 with CCX as NUMA Domain off, the default for a general-purpose cluster.

## Likely wrong answer
"NPS-4 matches the four quadrants of the socket, so every VM gets local memory (B), and the cores of one node are all alike (G); so only db-sql-01 needs a NUMA tweak (I)." B and G are the misconceptions.

## Expected key points
- Answer: A, C, D, F, J.
- A is correct: NPS-4 divides the socket into 4 NUMA domains: 96 / 4 = 24 cores and 12 / 4 = 3 channels per node (192 GB of the socket's 768 GB).
- B is wrong: a VM wider than a quarter of the socket spans NPS-4 nodes; db-sql-01 (40 vCPUs > 24 cores) shows two home nodes and N%L 54. EPYC 9005 has one central I/O die, not four separate memory domains on separate dies.
- C is correct: a node boundary inside one I/O die removes no die-to-die hop; a local access saves only part of the path across that die.
- D is correct: at NPS-1 each socket is one node with all 12 channels interleaved: 40 vCPUs ≤ 96 cores and 160 GB ≤ 768 GB.
- E is wrong: Broadcom KB 432801 says to deactivate CCX as NUMA Domain, as it skews the scheduler's model of memory; from vSphere 7.0 Update 2 the ESX scheduler already keeps the vCPUs of a VM within one CCX or CCD.
- F is correct: one CCD has 8 cores and its own L3 cache; 40 vCPUs cannot fit in one, so locality differs inside the socket even when the VM is in one NUMA node.
- G is wrong: CCD and L3 boundaries create locality inside a socket and inside a node.
- H is wrong: the same N%L in two samples is steady placement; a migration shows N%L climbing. The remote share comes from the VM spanning two nodes.
- I is wrong: the migration threshold is advice for Intel Granite Rapids to reduce VM moves between nodes; it does not shrink db-sql-01 into one node.
- J is correct: Performance Best Practices for vSphere 9.1, AMD's vSphere tuning guide for EPYC 9005 and KB 432801 give NPS-1 with CCX as NUMA Domain off for a general-purpose cluster with VMs of mixed or unknown sizes.

## Metadata
```yaml
id: "0446"
title: "NPS-4 on an AMD EPYC 9005 cluster of mixed VM sizes"
product: [vsphere]
technology: [cpu, memory]
task: judge-setting
level: 400
answer_type: deterministic
input: [text]
object: [esxi, vm, cluster]
tool: [esxtop]
knowledge:
  - vsphere/technology/cpu/concepts/cpu-topology
  - vsphere/technology/cpu/configuration/numa-settings
  - vsphere/technology/cpu/concepts/numa
  - vsphere/tools/esxtop/memory
knowledge_main: vsphere/technology/cpu/concepts/cpu-topology
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-15, question bank audit gap: vsphere/technology/cpu/concepts/cpu-topology"
answer: [A, C, D, F, J]
misconception: [B, G]
misconception_type: [threshold-transplanted]
status: draft
```
