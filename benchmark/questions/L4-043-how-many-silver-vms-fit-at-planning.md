# How many Silver VMs fit at planning

## Prompt
- A new vSphere cluster is being planned. No workload runs yet.
- 5 ESXi hosts. One host's capacity is kept free for HA.
- Each host: 64 cores at 2.5 GHz base clock, Hyper-Threading on, 768 GB of DRAM, no memory tiering.
- ESXi, vSAN and NSX take 14 threads and 64 GB on each host. The system keeps 10 GHz of CPU per host that cannot be reserved.
- All VMs are Silver class: CPU overcommit 2:1 per physical thread, memory overcommit 1.2:1, reservation 25% of CPU and 50% of memory (set at the resource pool), expected concurrent peak 50% of CPU and 85% of memory.
- The typical Silver VM has 8 vCPUs and 32 GB.
- The team's capacity policy: a host is full when any of six numbers would pass 100%: CPU and memory allocation (against the overcommit ratio), CPU and memory reservation, and CPU and memory utilization at the expected concurrent peak. CPU allocation and CPU utilization are counted against physical threads: one vCPU busy 100% fills one thread. Each host is checked on its own, and a VM runs on one host.

How many Silver VMs can the cluster take?

- A. 56
- B. 100
- C. 103
- D. 104
- E. 112
- F. 125

## Likely wrong answer
D or E: the overcommit ratio (allocation) taken as the capacity. Allocation is one of six numbers, and at planning it is often not the one that binds.

## Expected key points
- Answer: B.
- HA is not capacity: 4 of the 5 hosts carry load.
- Supply per host: 128 threads - 14 = 114 threads; 768 - 64 = 704 GB; reservable CPU 64 × 2.5 - 10 = 150 GHz (a reservation is capped at the base clock, per core).
- VMs per host: allocation CPU 114 × 2 / 8 = 28.5; allocation memory 704 × 1.2 / 32 = 26.4; reservation CPU 150 / (8 × 2.5 × 25%) = 30; reservation memory 704 / 16 = 44; utilization CPU 114 / (8 × 50%) = 28.5; utilization memory 704 / 27.2 = 25.9.
- Memory utilization binds: 25 whole VMs per host (a 26th would need 707 GB of 704), so 4 × 25 = 100 (B).
- A is wrong: overcommit counted per core: (64 - 7) × 2 / 8 = 14 per host, 56 in all. The ratio is per thread.
- C is wrong: 4 × 704 / 27.2 = 103.5 treats the cluster as one pool; on each host the 26th VM passes 100%.
- D is wrong: memory allocation, 26 per host. E is wrong: CPU allocation, 28 per host. F is wrong: the HA host counted, 5 × 25.

## Reasoning path
1. Count the hosts that carry load: 5 - 1 = 4.
2. Subtract the hypervisor from each host's threads and DRAM.
3. Compute the six numbers per host; take the smallest, in whole VMs.
4. Name the binding resource and model: memory utilization.

## Notes
- Drafted by Claude 2026-11-11 from the author's working model (project/sources/Capacity Planning Stage.xlsx, sheet Read Me, the 6-number example) and checked with harness/capacity.py. Counts only after author approval.
- Revised 2026-11-12: the six-number policy is stated in the prompt (a team policy, not public knowledge, design.md section 6.1 F3); the key is per host in whole VMs, as the knowledge base example says (25 per host). The earlier key (103) pooled the cluster, which a 26th VM on one host would break.

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
object: [cluster, esxi]
tool: [none]
knowledge:
  - sp5-framework/capacity/class-of-service-planning
  - sp5-framework/capacity/overcommit
  - vsphere/technology/cpu/metrics/host/reserved-capacity
knowledge_main: sp5-framework/capacity/class-of-service-planning
attachments: []
origin: synthetic
source_path: "Capacity Planning Stage.xlsx (author's working model), sheet Read Me; Capacity Management > Capacity Model > Planning Phase"
answer: [B]
misconception: [D, E]
misconception_type: [unit-and-normalization]
status: draft
```
