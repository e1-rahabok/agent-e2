# VM balloon flat for days

## Prompt
See [the vCenter chart of the VM's balloon and memory latency](0388/vcenter-vm-balloon-latency-past-week.png) and [the vCenter chart of its swap rates](0388/vcenter-vm-swap-rates-past-week.png).

- A Linux VM runs an order-processing application.
- The owner says the application has been slow since the balloon appeared, and asks for 4 GB more memory: "the host is taking memory away from the VM."

Which statements are correct?

- A. The flat balloon line shows that the reclaimed amount has not changed for days.
- B. Balloon above 0 shows that ESXi is taking memory from the VM right now.
- C. Memory Latency at 0 shows that no vCPU of the VM waited on a page fault this week.
- D. Memory Latency would include the time Linux spent paging out to make room for the balloon.
- E. Linux gave the balloon its free and cache pages before pages its processes were using.
- F. Ballooning cannot slow a VM, whatever share of its memory the balloon holds.
- G. Adding 4 GB to the VM will cure the slowness the owner reports.
- H. ESXi keeps physical pages behind the ballooned memory, ready to hand back to this VM.

## Input to supply
- Product: vSphere Client 9.1; a Linux VM with the `vmw_balloon` driver loaded, 8 GB or more.
- Screen 1: vSphere Client > the VM > Monitor > Performance > Advanced > Memory. Chart Options: timespan Past week; counters Balloon (KB) and Latency (%); target the VM. Save as `benchmark/questions/0388/vcenter-vm-balloon-latency-past-week.png`.
- Screen 2: the same chart with counters Swap in rate and Swap out rate (KBps). Save as `benchmark/questions/0388/vcenter-vm-swap-rates-past-week.png`.
- Condition the key depends on:
  - Balloon rises once and then stays flat (within 2%) for at least the last 3 days, at 15% or more of the configured memory;
  - Latency 0 (below 0.1%) for the whole week;
  - Swap in rate 0 for the whole week.
- How to produce it: a field VM that matches, or in a lab, host memory pressure that inflates the balloon while the guest keeps its working set inside the memory left to it (an idle or lightly loaded guest).
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
B: "Balloon above 0, so the host is taking memory now and the VM is slow: give it more memory."

## Expected key points
- Answer: A, C, E.
- A true: Ballooned is a held amount in the past tense; a flat line means nothing was reclaimed or given back, and the guest has not asked for those pages again.
- B false: a balloon above 0 says ESXi reclaimed memory at some point, not that it is reclaiming now; it can date from pressure days old.
- C true: Memory Latency is the share of time a vCPU waits for a page fault ESXi resolves (mostly swap-in, plus decompression). At 0, with swap-in at 0, the VM did not wait on memory.
- D false: Latency excludes balloon activity; the hypervisor cannot see what the guest does to fill the balloon.
- E true: the guest gives the balloon the pages it values least: free pages first, then cache, then modified, then in use.
- F false: over-correction. A hit comes when the guest needs a ballooned page again; the more is ballooned, the higher the chance, and the same amount hurts a small VM more than a large one.
- G false: the wrong action. Latency and swap-in are 0 all week, so memory is not why the application is slow; look elsewhere.
- H false: ballooned pages map to no ESXi page; ESXi gave their physical pages to other uses.

## Notes
- Paired with 0052 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item C12.
- The plan proposed Balloon target 0 at the end of the chart. Left out: no option needs the target, and a balloon that stays flat for days while its target reads 0 is hard to find or produce. The condition rests on Balloon, Latency and swap-in only.
- Left out of the options: whether a memory limit causes ballooning (open author question Q214) and whether more memory stops the balloon. G is false for a reason that stands without them: the VM did not wait on memory.
- The key holds whenever the condition of `## Input to supply` holds.
- Written 2026-11-14 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after approval (design.md, section 6.2).

## Metadata
```yaml
id: "0388"
title: "VM balloon flat for days"
product: [vsphere, linux]
technology: [memory]
task: read-metric
level: 300
answer_type: deterministic
input: [screenshot]
object: [vm]
tool: [vcenter]
knowledge:
  - vsphere/technology/memory/metrics/virtual-motherboard/ballooned
  - vsphere/technology/memory/concepts/ballooning
  - vsphere/technology/memory/metrics/virtual-motherboard/latency
knowledge_main: vsphere/technology/memory/metrics/virtual-motherboard/ballooned
attachments:
  - 0388/vcenter-vm-balloon-latency-past-week.png
  - 0388/vcenter-vm-swap-rates-past-week.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C12"
answer: [A, C, E]
misconception: [B]
misconception_type: [reclamation-as-contention]
pair: "0052"
status: awaiting-input
```
