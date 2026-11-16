# Three small clusters or one large one

## Prompt
- A design review for the next hardware refresh: identical hosts, and a workload that needs 21 hosts' worth of capacity.
  - Proposal 1: three clusters of 8 hosts, each with vSphere HA admission control reserving one host (7+1).
  - Proposal 2: one cluster of 23 hosts, with HA admission control reserving two hosts (21+2).
- The architect of proposal 1 argues that smaller clusters are safer, and wants DRS in manual mode in all clusters, "as today, to stay in control".
- Today's clusters run DRS in manual mode. On the busiest one the vSphere Client lists 40 DRS recommendations, the oldest from 3 hours ago.

Which statements are correct?

- A. Proposal 1 uses 24 hosts and proposal 2 uses 23 for the same workload.
- B. Proposal 2 tolerates two host failures in its one cluster; each cluster of proposal 1 tolerates one.
- C. Proposal 1 is the safer design, since a host failure touches only one of three small clusters.
- D. Proposal 1 has the lower HA overhead: one host per cluster, against two hosts in proposal 2.
- E. Applying the 40 pending recommendations now, oldest first, brings today's cluster back to the balance DRS wanted.
- F. In manual mode no move happens until someone approves it, so each host keeps its own buffer for peak demand.
- G. With DRS fully automated, proposal 2 needs no HA failover hosts, because DRS moves VMs off a host before it fails.
- H. In proposal 1, a VM in one cluster cannot use the free capacity of the other two clusters.
- I. A 23-host cluster is past the size DRS can balance, so proposal 2 must be split however the hosts are counted.

## Likely wrong answer
C and D: "Smaller clusters are safer, and each needs only one spare host." E is the wrong action on manual DRS; G is the over-correction.

## Expected key points
- Answer: A, B, F, H.
- A is correct: 3 × (7 + 1) = 24 hosts against 21 + 2 = 23.
- B is correct: proposal 2 reserves two hosts in one cluster; each cluster of proposal 1 reserves one.
- C is wrong: the misconception that three small clusters are safer than one large one: proposal 1 uses one host more and tolerates fewer failures per cluster.
- D is wrong: the HA overhead is 3 of 24 hosts (12.5%) in proposal 1 against 2 of 23 (about 8.7%) in proposal 2. Smaller clusters carry a larger share of failover capacity (3 nodes: 33%; 10 nodes: 10%).
- E is wrong: DRS recalculates every minute, so recommendations made hours ago act on a state that has changed. Read the current recommendations, or let DRS run automated.
- F is correct: without automation the load does not move until an administrator approves; every host must keep its own buffer for peak demand.
- G is wrong: DRS covers performance and capacity, HA covers availability; DRS cannot move VMs off a host that fails without warning, and HA restarts them.
- H is correct: many small clusters create resource silos; DRS balances inside a cluster, not across clusters.
- I is wrong: 23 hosts is well inside a cluster's limit; operations get harder only from about 32 nodes.

## Notes
- Cluster maximum: vSphere 9.1 Configuration Maximums (hosts per cluster), https://configmax.broadcom.com.

## Metadata
```yaml
id: "0470"
title: "Three small clusters or one large one"
product: [vsphere]
technology: [system]
task: judge-setting
level: 300
answer_type: deterministic
input: [text]
object: [cluster]
tool: [vcenter]
knowledge:
  - vsphere/object-types/cluster/configuration/cluster-configuration-review
knowledge_main: vsphere/object-types/cluster/configuration/cluster-configuration-review
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-15, question bank audit gap: vsphere/object-types/cluster/configuration/cluster-configuration-review"
answer: [A, B, F, H]
misconception: [C, D]
misconception_type: [unit-and-normalization]
status: draft
```
