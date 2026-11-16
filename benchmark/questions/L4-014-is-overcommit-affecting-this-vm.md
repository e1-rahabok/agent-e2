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

- A. Swap activity inside Linux is, on its own, proof that host overcommit affects the VM.
- B. The balloon pushed Linux to page Java memory out to its own swap; the threads wait on the page-ins.
- C. The 6 GB in the balloon may have freed less than 6 GB of host memory, if some of those pages were shared.
- D. Linux gave the balloon its free and cache pages first; it paged out used memory only when those ran short.
- E. The guest is sized too small for Java; adding 8 GB to the VM removes the cause.
- F. Swapped and Compressed at 0 prove the host has enough physical memory, since ESXi would compress before it balloons.

## Likely wrong answer
A: "Linux is swapping, so the host is overcommitted: that settles it."

## Expected key points
- Answer: B, C, D.
- A is wrong: swap inside the guest can have other causes (another guest issue, a guest sized too small), so the host indicators come first: ballooning, host swap or compression, then swap inside the Guest OS. Here the balloon at 09:00 ties the guest swap to the host.
- B is correct: the balloon driver allocates memory inside Linux; when free and cache pages are not enough, Linux pages out used memory, and every page-in is a wait the application feels. Memory Latency stays at 0% because it counts only waits on ESXi (swap-in, decompression), not paging inside the guest.
- C is correct: a balloon page whose ESXi page was shared with other pages frees less than its size; a 6 GB balloon can free less than 6 GB.
- D is correct: the Guest OS hands the balloon free pages first, then cache, then modified and in-use pages. Paging of used memory starts only when the first two run short.
- E is wrong: the cause is host overcommit, a provider event; the fix for the balloon is on the provider side. Before 09:00 the same 32 GB guest did not page.
- F is wrong: ballooning comes before compression and swap; 0 there does not mean there is no pressure.

## Notes
- Changed in the 2026-11-15 audit: C (VM Memory Latency cannot see guest paging, redundancy #36, homed in 0265/0383) replaced by the shared-pages fact (ballooning, Mechanism); A (the same fact as the misconception) replaced by the decision tree's misconception "Guest swap activity proves host overcommitment" ("No ballooning means no memory problem", the report's proposal, is arguable on a VM whose driver demonstrably works); E (undecidable: adding memory to a ballooned VM) rewritten to the guest-too-small belief, false by guest-os-sizing ("The fix for the balloon is on the provider side"); B shortened.

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
  - guest-os/system/guest-os-sizing
knowledge_main: vsphere/technology/memory/decision-tree/is-overcommit-affecting-vm
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-05"
answer: [B, C, D]
misconception: [A]
misconception_type: [layer-confusion, reclamation-as-contention]
status: draft
```
