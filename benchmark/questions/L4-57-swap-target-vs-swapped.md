# Swap Target, Swapped, Granted and Consumed

## Prompt
- A Windows VM with 8 GB of memory. It has no memory limit and is not in a resource pool.
- [The attached vSphere Client export](0142/vm-memory-real-time-1-hour.csv) is the VM's real-time memory chart for the last hour (20-second samples).
- In the same hour, the vSphere Client also shows, flat for the whole hour: Compressed 644,556 KB; Ballooned memory 0; Swap in rate, Swap out rate, Compression rate and Decompression rate 0.
- The application owner sees Swapped at 6.2 GB and Swap target at 6.5 GB and asks: "Is ESXi swapping my VM right now? Will it swap another 6.5 GB? Is that why the VM is slow?"

Which statements are correct?

- A. ESXi is not swapping the VM now: every swap and compression rate is 0, and Swapped is flat for the whole hour.
- B. ESXi will swap about 6.5 GB more of the VM, the amount shown in Swap target.
- C. Swap target is the level of reclamation ESXi aims at for this VM, not a queue of pages that adds to Swapped.
- D. The gap of about 300 MB between Swap target and Swapped is pages still waiting to be swapped out.
- E. Swap target moves against Consumed in most samples: when Consumed rises, the target falls.
- F. Granted is flat for the hour: the guest is not asking ESXi for more pages.
- G. The VM is not waiting for its swapped pages now: the swap-in and decompression rates are 0.
- H. The VM is slow because it is short of memory, so it needs more memory or another host.
- I. The swapped pages stay out until the guest touches them; with no limit or pool, they come from past host pressure or a vMotion.
- J. A memory limit on the VM is the likely source of the 6.2 GB that are swapped out.
- K. With swap-in and swap-out rates both at 0, Swapped should read 0, so the 6.2 GB is a counter error.
- L. Active at about 82 MB is the memory the VM needs, so it can be resized to a few hundred MB.

## Likely wrong answer
- B: "It will swap another 6.5 GB."
- H: "The VM is slow because it is short of memory: add memory or move it to another host."
- D: "The rest of the swap target is still queued to go out."

## Expected key points
- Answer: A, C, E, F, G, I.
- A true: Swap in rate, Swap out rate, Compression rate and Decompression rate are 0 all hour; Swapped is 6,520,964 KB in every sample (maximum = minimum).
- B false: Swap target is an input, not pages queued on top of Swapped; with every rate at 0, nothing goes out.
- C true: ESXi need not reach the target if it does not have to; it is a compress-swap target.
- D false: the target is not the same thing as Swapped, and no page is going out: every rate is 0.
- E true: in the export the target moves against Consumed in 136 of the 179 steps (the two mirror each other), and changes by less than 1 MB.
- F true: Granted is 1,223,088 KB in every sample.
- G true: swap-in is the contention; at 0, the guest does not wait for these pages now. A wait would show as swap-in, decompression and memory latency.
- H false: nothing is swapped in or out now; the swapped pages are history that the guest does not touch.
- I true: Swapped pages stay out until the guest asks for them; a vMotion can bring pages already swapped.
- J false: the VM has no memory limit and no resource pool.
- K false: Swapped is not Swap in - Swap out; it is what is out now, built up in the past, and the rates show only the present.
- L false: Active is a sampled estimate for the kernel; neither Active nor Consumed suits sizing.

## Notes
- From the author's samples (docx, 2026-11-12): a vSphere Client table of one hour: Swap target about 6,816,000 KB changing every 20 seconds, Swapped 6,520,964 KB flat, Granted 1,223,088 KB flat, Consumed 931,340-939,272 KB, Compressed 644,556 KB, Active 83,884 KB, every rate 0. "The patterns of Consumed and Swap Target are mirror image." The CSV is generated to reproduce them. Granted + Swapped + Compressed = 8 GB exactly.
- Swap target is compared with Swapped (vSphere Monitoring and Performance, memory counters; Broadcom KB 374743, esxtop SWTGT vs SWCUR: https://knowledge.broadcom.com/external/article/374743). In the author's data the target sits above Swapped while every rate is 0; the key relies on the zero rates, not on the gap.
- Converted from judged to multiple choice (Q199 F, 2026-11-14). The owner's three questions are answered by the options. Dropped from the old key: "Active is tiny and flat: the guest barely touches memory" (Active is a sampled kernel estimate with no operational use: VM Memory Active) and "a reboot clears them" (no knowledge file states it).

## Metadata
```yaml
id: "0142"
title: "Swap Target, Swapped, Granted and Consumed"
product: [vsphere, windows]
technology: [memory]
task: read-metric
level: 400
answer_type: deterministic
answer: [A,C,E,F,G,I]
misconception: [B,D,H]
input: [table]
object: [vm]
tool: [vcenter]
knowledge:
  - vsphere/technology/memory/metrics/virtual-motherboard/swap-target
  - vsphere/technology/memory/metrics/virtual-motherboard/swapped
  - vsphere/technology/memory/metrics/virtual-motherboard/swap-in-rate
  - vsphere/technology/memory/metrics/virtual-motherboard/granted
  - vsphere/technology/memory/metrics/virtual-motherboard/active
knowledge_main: vsphere/technology/memory/metrics/virtual-motherboard/swap-target
attachments:
  - 0142/vm-memory-real-time-1-hour.csv
origin: book
source_path: "Author samples (docx, 2026-11-12) > Swap target, swapped, granted, consumed (Line 1 to Line 4)"
misconception_type: [cumulative-vs-current, reclamation-as-contention]
status: draft
```
