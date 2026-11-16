# HA admission green on a tiered cluster

## Prompt
- Cluster cl-tier-01 has four hosts, esx-41 to esx-44, on ESXi 9.1 and vCenter 9.1. The update to 9.1.1 is planned for next quarter.
- Each host has 512 GB of DRAM and memory tiering on a 512 GB NVMe partition at the default 1:1 ratio, so the host shows 1,024 GB of memory.
- vSphere HA admission control: cluster resource percentage, 25% of CPU and 25% of memory reserved for failover. The vSphere HA summary shows Current CPU Failover Capacity 52% and Current Memory Failover Capacity 41%, with no warning. No VM has a memory reservation.
- vCenter, Tier memory consumed (tier.consumed), Past day averages:

| Host | Tier 0 (DRAM) consumed | Tier 1 (NVMe) consumed |
|---|---|---|
| esx-41 | 478 GB | 150 GB |
| esx-42 | 482 GB | 165 GB |
| esx-43 | 476 GB | 140 GB |
| esx-44 | 484 GB | 180 GB |

- The operations manager writes: "41% memory failover capacity against 25% configured, and no warning. If a host fails, every VM restarts."

Which statements are correct?

- A. The green admission status shows that the surviving hosts have the DRAM to restart a failed host's VMs.
- B. On this release, admission control counts each host's NVMe tier in its memory capacity, as if it were DRAM.
- C. A restarted VM needs DRAM at power-on: its overhead memory cannot be placed on the NVMe tier.
- D. If esx-44 fails, the three other hosts hold about 100 GB of unconsumed DRAM between them.
- E. Current Memory Failover Capacity of 41% means that 41% of the cluster's DRAM is unconsumed.
- F. From 9.1.1, admission control tracks DRAM on its own, as Current DRAM Failover Capacity.
- G. Switch admission control to the slot policy, so that it counts DRAM on its own.
- H. Admission control on this release leaves the NVMe tier out, so the green status understates the cluster's room.
- I. The VMs on these hosts wait on NVMe now, because Tier 1 consumed is 140-180 GB per host.

## Likely wrong answer
A: "Admission control is green with spare failover capacity, so every VM will restart after a host failure."

## Expected key points
- Answer: B, C, D, F.
- A is wrong: the misconception of memory tiering ("HA admission control is green, so the VMs will restart"). Up to and including 9.1, admission control counted DRAM and NVMe as one pool; it could show green while the surviving hosts lacked the DRAM to restart the VMs.
- B is correct: before 9.1.1, admission control counted DRAM and NVMe as one pool.
- C is correct: DRAM is required to power on a VM; its overhead memory always sits in DRAM, and NVMe cannot replace DRAM at restart.
- D is correct: three hosts hold 3 × 512 = 1,536 GB of DRAM, with 478 + 482 + 476 = 1,436 GB consumed: 100 GB unconsumed.
- E is wrong: unconsumed DRAM is 2,048 - 1,920 = 128 GB, about 6% of the cluster's DRAM; the 41% is computed on DRAM and NVMe together, from reservations and overhead, not from consumed memory.
- F is correct: from vSphere 9.1.1, admission control tracks DRAM as its own resource, with Current DRAM Failover Capacity beside CPU and memory (cluster resource percentage and dedicated failover hosts policies).
- G is wrong: the wrong action. The DRAM check is not supported with the slot policy; do not use the slot policy on a tiered cluster.
- H is wrong: over-correction in the wrong direction. Admission control counted the NVMe tier, so the green status overstates the room for restarts.
- I is wrong: the misconception of memory tiering ("Tier 1 consumed means the VMs are slow"). Tier 1 consumed holds cold pages: it is saturation, not a wait. The performance signals are active memory against DRAM and NVMe reads.

## Notes
- Sources: the knowledge base, Memory tiering (sections HA admission control, Capacity management, Misconceptions); vSphere 9.1 documentation, vSphere Availability, Memory Tiering and HA Admission Control (pp. 1969-1971).
- The question does not ask whether every VM restarts: with about 100 GB of DRAM free on the survivors and new pages placed on tier 1 above 80% DRAM, the outcome depends on the restarting VMs' overhead. The options ask what the green status proves and what restarts need.

## Metadata
```yaml
id: "0456"
title: HA admission green on a tiered cluster
product: [vsphere]
technology: [memory, system]
task: judge-setting
level: 400
answer_type: deterministic
input: [text]
object: [cluster, esxi]
tool: [vcenter]
knowledge:
  - vsphere/technology/memory/concepts/memory-tiering
knowledge_main: vsphere/technology/memory/concepts/memory-tiering
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-15, question bank audit gap: vsphere/technology/memory/concepts/memory-tiering"
answer: [B, C, D, F]
misconception: [A]
misconception_type: [label-read-as-model, consumption-as-contention]
status: draft
```
