# How many Silver VMs fit at planning

## Prompt
- A new vSphere cluster is being planned. No workload runs yet.
- 5 ESXi hosts, one host's capacity kept for HA.
- Each host: 64 cores at 2.5 GHz base clock, Hyper-Threading on, 768 GB of DRAM, no memory tiering.
- ESXi, vSAN and NSX take 14 threads and 64 GB on each host. The system keeps 10 GHz of CPU per host that cannot be reserved.
- All VMs are Silver class: CPU overcommit 2:1 per physical thread, memory overcommit 1.2:1, reservation 25% of CPU and 50% of memory set at the resource pool, expected concurrent peak 50% of CPU and 85% of memory.
- The typical Silver VM has 8 vCPU and 32 GB.

How many Silver VMs can the cluster take without any capacity dimension passing 100%?

- A. 57
- B. 103
- C. 105
- D. 114
- E. 129
- F. 176

## Likely wrong answer
D or C: the overcommit ratio (allocation) is taken as the capacity. CPU at 2:1 gives 114 VMs on 4 hosts, memory at 1.2:1 gives 105. Allocation is one of six numbers, and at planning it is often not the one that binds.

## Expected key points
- Per host, three models for each of CPU and memory: allocation, reservation, utilization. The cluster is full at the first of the six to reach 100%.
- HA is not capacity: 4 of the 5 hosts carry load.
- Supply per host: 128 threads - 14 = 114 threads; 768 - 64 = 704 GB; reservable CPU 64 × 2.5 - 10 = 150 GHz (reservation is capped at the base clock, per core).
- VMs per host: allocation CPU 114 × 2 / 8 = 28.5; allocation memory 704 × 1.2 / 32 = 26.4; reservation CPU 150 / (8 × 0.25 × 2.5) = 30; reservation memory 704 / 16 = 44; utilization CPU 114 / 4 = 28.5; utilization memory 704 / 27.2 = 25.9.
- Memory utilization binds: 4 × 704 / 27.2 = 103.5, so 103 VMs (B).
- The overcommit is per physical thread, not per core: per core it would give 57 (A).

## Reasoning path
1. Count the hosts that carry load: 5 - 1 = 4.
2. Subtract the hypervisor from each host's threads and DRAM.
3. Compute the six numbers; take the smallest.
4. Name the binding resource and model: memory utilization.

## Notes
- Distractors: A counts the CPU overcommit per core; C is memory allocation; D is CPU allocation; E counts all 5 hosts (HA forgotten); F is memory reservation.
- Drafted by Claude 2026-11-11 from the author's working model (project/sources/Capacity Planning Stage.xlsx, sheet Read Me, the 6-number example) and checked with harness/capacity.py. Counts only after author approval.

## Metadata
```yaml
id: "0097"
title: "How many Silver VMs fit at planning"
product: [vsphere]
technology: [cpu, memory]
task: decide-capacity
level: 400
answer_type: deterministic
input: [text]
knowledge:
  - sp5-framework/capacity/class-of-service-planning
attachments: []
origin: synthetic
source_path: "Capacity Planning Stage.xlsx (author's working model), sheet Read Me; Capacity Management > Capacity Model > Planning Phase"
answer: [B]
misconception: [C, D]
status: draft
```
