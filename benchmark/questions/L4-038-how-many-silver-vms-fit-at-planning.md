# How many Silver VMs fit at planning

## Prompt
- A new vSphere cluster is being planned. No workload runs yet.
- 6 ESXi hosts. One host's capacity is kept free for HA.
- Each host: 56 cores at 2.4 GHz base clock, Hyper-Threading on, 640 GB of DRAM, no memory tiering.
- ESXi, vSAN and NSX take 16 threads and 48 GB on each host. The system keeps 12 GHz of CPU per host that cannot be reserved.
- All VMs are Silver class: CPU overcommit 2:1 per physical thread, memory overcommit 1.2:1, reservation 25% of CPU and 50% of memory (set at the resource pool), expected concurrent peak 50% of CPU and 85% of memory.
- The typical Silver VM has 8 vCPUs and 32 GB.
- The team's capacity policy: a host is full when any of six numbers would pass 100%: CPU and memory allocation (against the overcommit ratio), CPU and memory reservation, and CPU and memory utilization at the expected concurrent peak. CPU allocation and CPU utilization are counted against physical threads. Each host is checked on its own.

How many Silver VMs can the cluster take?

- A. 60
- B. 105
- C. 108
- D. 110
- E. 120
- F. 126

## Answers
B

## Explanation
- A is wrong: it counts the overcommit per core: (56 - 8) × 2 / 8 = 12 per host, 60 in all. The ratio is per physical thread.
- B is correct: 5 of the 6 hosts carry load (HA is not capacity). Supply per host: 112 threads - 16 = 96 threads; 640 - 48 = 592 GB; reservable CPU 56 × 2.4 - 12 = 122.4 GHz (a reservation is held in MHz at the base clock, per core: Hyper-Threading adds no reservable MHz). VMs per host: CPU allocation 96 × 2 / 8 = 24; memory allocation 592 × 1.2 / 32 = 22.2; CPU reservation 122.4 / (8 × 2.4 × 25%) = 25.5; memory reservation 592 / 16 = 37; CPU utilization 96 / (8 × 50%) = 24; memory utilization 592 / 27.2 = 21.8. Memory utilization binds at 21 whole VMs per host (a 22nd would need 598 GB of 592), so 5 × 21 = 105.
- C is wrong: 5 × 592 / 27.2 = 108.8 treats the cluster as one pool; on each host the 22nd VM passes 100%.
- D is wrong: memory allocation, 22 per host, taken as the capacity.
- E is wrong: CPU allocation, 24 per host, taken as the capacity.
- F is wrong: the HA host counted as load capacity, 6 × 21.
- Misconception: D or E: the overcommit ratio (allocation) taken as the capacity. Allocation is one of six numbers, and at planning it is often not the one that binds.

## Reasoning path
1. Count the hosts that carry load: 6 - 1 = 5.
2. Subtract the hypervisor from each host's threads and DRAM.
3. Compute the six numbers per host; take the smallest, in whole VMs.
4. Name the binding resource and model: memory utilization.

## Notes
- Synthetic, 2026-11-11, from Capacity Planning Stage.xlsx (sheet Read Me, the 6-number example); checked with harness/capacity.py (`vms_per_host`). Counts only after the author's approval.
- The six-number policy is stated in the prompt (a team policy, design.md section 6.1 F3). The key is per host in whole VMs.
- Changed in the 2026-11-15 audit: host and cluster numbers differ from the knowledge-base example (F5), and the stem no longer explains what one busy vCPU fills.

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
source_path: "Capacity Planning Stage.xlsx, sheet Read Me; Capacity Management > Capacity Model > Planning Phase"
misconception: [D, E]
misconception_type: [unit-and-normalization]
status: draft
```
