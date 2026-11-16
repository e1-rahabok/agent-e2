# Host Granted above physical memory

## Prompt
- Host esx-12 runs ESXi 9.1 with 768 GB of physical memory. 58 VMs run on it, with 1,160 GB of memory configured in total. No VM has a memory limit.
- The esxtop memory state of esx-12 is clear for most of the day.
- A capacity report built from vCenter shows these Past day averages:

| Object | Granted | Consumed | Shared | Ballooned memory | Compressed | Swapped |
|---|---|---|---|---|---|---|
| Host esx-12 | 1,025 GB | 752 GB | | 0 | 0 | 0 |
| Sum of the 58 VMs | 1,024 GB | 719 GB | 352 GB | 0 | 0 | 0 |

- The report's author flags esx-12: "Granted is 1,025 GB on a 768 GB host. Either the counter is broken or the host is over its memory. Sharing at least saves us 352 GB."

Which statements are correct?

- A. Granted of 1,025 GB on a host with 768 GB of memory is a counter error.
- B. Granted can pass physical memory: it counts every mapped VM page, zero and shared pages too, before savings.
- C. Host Consumed can also pass 768 GB in the same way, as the VMs go on touching more of their configured memory.
- D. Page sharing saves about 305 GB on this host: the VMs' Granted minus their Consumed.
- E. Page sharing saves about 352 GB on this host: the sum of the VMs' Shared.
- F. Host Consumed is higher than the VMs' sum because it also holds the kernel's memory and the VMs' overhead.
- G. Host Granted also holds the kernel's own memory, which is why it reads above the VMs' sum.
- H. Host Granted sits slightly above the VMs' sum, as it also counts non-VM processes like the management agents.
- I. Granted is the figure to plan this host's capacity on, because it shows the memory the VMs hold on the host right now.
- J. Move VMs off esx-12 with vMotion until its Granted falls below the 768 GB of physical memory.

## Likely wrong answer
A: "Granted cannot be larger than the memory in the host, so the counter is broken." E: "Shared is the memory sharing saves."

## Expected key points
- Answer: B, D, F, H.
- A is wrong: the misconception of ESXi Memory Granted ("Granted above capacity is impossible"). Granted is the VMs' view and can exceed total capacity.
- B is correct: Granted counts VM pages that have an ESXi page mapped, zero and shared pages included; it ignores physical savings, so the sum over VMs can pass the host's memory.
- C is wrong: over-correction. Host Consumed is physical memory minus free memory, ESXi pages in DIMM; it cannot pass 768 GB.
- D is correct: VM Consumed = Granted - sharing savings, so the saving is 1,024 - 719 = 305 GB.
- E is wrong: the misconception of VM Memory Shared ("Shared = memory saved"; "Sum VM Shared for host savings"). VM Shared is the amount subjected to sharing, the input: 352 GB of VM pages are backed by 352 - 305 = 47 GB of ESXi pages.
- F is correct: ESXi Memory Consumed holds VMs, the kernel's own memory and VM overhead; VM Consumed excludes overhead. 752 - 719 = 33 GB.
- G is wrong: host Granted excludes kernel space; privileged processes get memory without the granting process.
- H is correct: host Granted is the sum of the running VMs' Granted plus non-VM user worlds; the management agents (host/vim) are in it. 1,025 - 1,024 = 1 GB.
- I is wrong: Granted has no use for capacity; it is the VMs' view. Capacity reads ESXi Memory Consumed (or ESXi Memory Utilization in the VCF Operations capacity engine).
- J is wrong: the wrong action. Granted above physical memory is no fault to fix; nothing is ballooned, compressed or swapped.

## Notes
- Sources: the knowledge base, ESXi Memory Granted (VMs' view, can exceed capacity, excludes kernel space, includes the management agents), VM Memory Shared (input, not savings; savings = Granted - Consumed), VM Memory Consumed (Consumed = Granted - sharing savings; excludes overhead), ESXi Memory Consumed (physical minus free; includes the kernel and VM overhead).
- The host is in the clear state so that the 305 GB of sharing is plausible: large pages are broken into 4 KB pages there, which can share. No option rests on it.
- The values keep away from the knowledge-base example (1,053 GB granted on a 755 GB host; 7,505 VMs).

## Metadata
```yaml
id: "0451"
title: Host Granted above physical memory
product: [vsphere]
technology: [memory]
task: read-metric
level: 400
answer_type: deterministic
input: [text]
object: [esxi, vm]
tool: [vcenter, esxtop]
knowledge:
  - vsphere/technology/memory/metrics/host/granted
  - vsphere/technology/memory/metrics/virtual-motherboard/shared
  - vsphere/technology/memory/metrics/virtual-motherboard/granted
  - vsphere/technology/memory/metrics/virtual-motherboard/consumed
  - vsphere/technology/memory/metrics/host/consumed
knowledge_main: vsphere/technology/memory/metrics/host/granted
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-15, question bank audit gap: vsphere/technology/memory/metrics/host/granted"
answer: [B, D, F, H]
misconception: [A, E]
misconception_type: [provider-vs-consumer, same-name-other-object]
status: draft
```
