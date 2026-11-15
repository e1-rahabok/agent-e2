# Is memory overcommit affecting this VM?

## Prompt
- A 32 GB Linux VM runs a Java application on an ESXi host whose VMs are configured with 1.5 times its physical memory.
- vSphere Client, last 24 hours, for the VM:
  - Ballooned memory: rose from 0 to 6 GB at 09:00, flat since.
  - Swapped: 0. Compressed: 0. Swap in rate: 0.
  - Memory Latency: 0% the whole day.
- Inside Linux, from 09:00: major page faults per second rose from near 0 to about 400, and swap used grew from 0 to 3 GB.
- Since 09:00, users see response times double.

Which statements are correct?

- A. Overcommit is not affecting this VM: Memory Latency is 0%, and nothing is swapped or compressed at host level.
- B. The balloon took 6 GB inside Linux; Linux then paged part of the Java memory out to its own swap, and the threads wait for those page-ins.
- C. VM Memory Latency counts waits for ESXi to bring back swapped or compressed pages; it cannot see paging inside the Guest OS.
- D. Linux gave the balloon its free and cache pages first; it paged out used memory only when those ran short.
- E. Adding 8 GB to the VM fixes it, because the balloon would then take the extra memory first and Java keeps its pages.
- F. Swapped and Compressed at 0 prove the host has enough physical memory, since ESXi would compress before it balloons.

## Likely wrong answer
A: Memory Latency is 0%, so memory is not the cause.

## Expected key points
- Answer: B, C, D.
- The overcommit indicators, in order: ballooning, host swap and compression, then swap inside the Guest OS. Here the last one is active: the balloon is now hurting the guest.
- B: the balloon driver allocates memory inside Linux. When free and cache pages are not enough, Linux pages out used memory; every page-in is a wait the application feels.
- C: VM Memory Latency is the share of time a vCPU waits for ESXi to bring a page back (swap-in, decompression). Guest paging happens above ESXi; ESXi cannot see it.
- D: the Guest OS hands the balloon free pages first, then cache, then modified and in-use pages. Paging of used memory starts only when the first two run short.
- A is wrong: Latency 0% rules out host-level waits only.
- E is wrong: the balloon follows host pressure, not the VM's size; more configured memory adds to the overcommit.
- F is wrong: ballooning comes before compression and swap; 0 there does not mean there is no pressure.

## Notes
- Revised 2026-11-12: the earlier version repeated "balloon above 0 is normal" (also in L2-13); now the indicator that matters is the last one, guest paging.

## Metadata
```yaml
id: "0054"
title: "Is memory overcommit affecting this VM?"
product: [vsphere, linux]
technology: [memory]
task: troubleshoot
level: 400
answer_type: deterministic
input: [text]
object: [vm, guest-os]
tool: [vcenter, guest-os-tools]
knowledge:
  - vsphere/technology/memory/decision-tree/is-overcommit-affecting-vm
  - vsphere/technology/memory/concepts/ballooning
  - vsphere/technology/memory/metrics/virtual-motherboard/latency
knowledge_main: vsphere/technology/memory/decision-tree/is-overcommit-affecting-vm
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05"
answer: [B, C, D]
misconception: [A]
misconception_type: [layer-confusion, reclamation-as-contention]
status: draft
```
