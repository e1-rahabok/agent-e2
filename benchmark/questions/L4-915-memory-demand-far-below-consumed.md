# Memory Demand far below Consumed

## Prompt
- Host esx-31 runs ESXi 9.1 with 1,024 GB of memory. VCF Operations 9.1 and vCenter monitor it. VMware Tools runs in every VM.
- Past 7 days, averages (values converted to GB):
  - vCenter, host: Consumed 940 GB (92%). Ballooned memory, Compressed and Swapped 0 all week.
  - vCenter, host system resource pools (host/system, host/vim, host/iofilters): Consumed about 21 GB together.
  - VCF Operations, host: Memory|Utilization 610 GB, Memory|Machine Demand 562 GB, Memory|ESX System Usage 48 GB.
  - VCF Operations, the capacity page of esx-31: memory Demand 610 GB.
  - VCF Operations, VMs: Memory Contention (%) 0 for every VM on esx-31.
  - VM db-01 on esx-31: 256 GB configured, memory reservation 256 GB, VCF Operations Memory|Utilization 140 GB.
- The platform team writes: "vCenter says 940 GB and VCF Operations says 610 GB, so one tool is wrong. The host is at 92%, so we order more memory. And VCF Operations counts 48 GB for the kernel when the kernel uses only 21 GB."

Which statements are correct?

- A. The memory Demand of 610 GB on the capacity page is the host's Memory|Utilization metric.
- B. Utilization reads below Consumed mainly because it builds on each VM's Guest OS need, which leaves out cache and inactive pages that Consumed holds.
- C. Consumed at 92% shows that esx-31 is short of memory.
- D. Utilization adds the kernel's reservation, 48 GB, not the 21 GB the kernel consumes.
- E. ESX System Usage should match the 21 GB the kernel consumes, so the 610 GB is inflated by an error.
- F. db-01 counts in the host's Utilization at no less than its 256 GB reservation, although its own Utilization is 140 GB.
- G. Utilization of 610 GB means the VMs hold 610 GB of the host's physical memory.
- H. Because Utilization leaves out guest cache, it can never read above Consumed on any host.
- I. With every VM on esx-31 powered off, its Utilization would sit at about 48 GB.
- J. Order more memory for esx-31, since Consumed is above 90%.
- K. Machine Demand of 562 GB plus ESX System Usage of 48 GB gives the 610 GB of Utilization.

## Likely wrong answer
C: "92% Consumed means the host is nearly out of memory." E: "Utilization should add what the kernel actually uses."

## Expected key points
- Answer: A, B, D, F, I, K.
- A is correct: the VCF Operations capacity pages show host Memory|Utilization under the name Demand (Broadcom KB 439253).
- B is correct: VM Memory Utilization comes from Guest OS Needed Memory, read through VMware Tools; it removes cache and inactive pages that ESXi Memory Consumed holds. The two tools measure different things; neither is wrong.
- C is wrong: the misconception of ESXi Memory Consumed and Utilization ("ESXi Memory Consumed near 100% means the host is out of memory"). Consumed holds guest cache and inactive pages; the saturation counters (Ballooned, Compressed, Swapped) are 0 and Memory Contention is 0 for every VM.
- D is correct: ESX System Usage is the kernel reservation, taken whether consumed or not, the same rule as a VM reservation.
- E is wrong: the misconception "Host memory Utilization adds what the kernel consumes". It adds the reservation (ESX System Usage), not the 21 GB the kernel consumes.
- F is correct: VCF Operations bases host Utilization on the VMs' utilization including their reservations; a reservation above the VM's Utilization raises the VM's term to the reservation (plus overhead).
- G is wrong: Utilization is demand built from the Guest OS need, raised to reservations; what the VMs hold in physical memory is Consumed (940 GB with the kernel).
- H is wrong: over-correction. Reservations count whether consumed or not: on a host with no running VMs, Utilization equals ESX System Usage (48 GB here) while the kernel consumes about 21 GB.
- I is correct: with no running VMs, Machine Demand is 0 and Utilization equals ESX System Usage.
- J is wrong: the wrong action. Nothing is reclaimed and no VM waits; 92% Consumed on its own is not a reason to add memory.
- K is correct: Utilization = Machine Demand + ESX System Usage: 562 + 48 = 610 GB.

## Notes
- Sources: the knowledge base, ESXi Memory Utilization (Formula; Reason; Misconceptions), Memory capacity (section Demand: the three formulas that share the word Demand), ESXi Memory Consumed (cache and inactive pages; read the saturation counters). VCF Operations 9.1 documentation, Host System Metrics (Mem|Utilization based on the VMs' utilization, including reservations, limits and overhead); Broadcom KB 439253.
- F is worded "at no less than its reservation": the published description includes reservations but gives no formula, and the option holds under any formula that includes the reservation.

## Metadata
```yaml
id: "0454"
title: Memory Demand far below Consumed
product: [vsphere, vcf-operations]
technology: [memory]
task: decide-capacity
level: 400
answer_type: deterministic
input: [text]
object: [esxi, vm]
tool: [vcf-operations, vcenter]
knowledge:
  - vsphere/technology/memory/metrics/host/utilization
  - vsphere/technology/memory/concepts/memory-capacity
  - vsphere/technology/memory/metrics/host/consumed
  - vsphere/technology/memory/metrics/virtual-motherboard/utilization
knowledge_main: vsphere/technology/memory/metrics/host/utilization
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-15, question bank audit gap: vsphere/technology/memory/metrics/host/utilization"
answer: [A, B, D, F, I, K]
misconception: [C, E]
misconception_type: [consumption-as-contention, tool-confusion]
status: draft
```
