# Swap Target, Swapped, Granted and Consumed

## Prompt
- A Linux VM with 16 GB of memory runs a log collector. It has no memory limit and is not in a resource pool.
- [The attached vSphere Client export](0142/vm-memory-real-time-1-hour.csv) is the VM's real-time memory chart for the last hour (20-second samples).
- In the same hour, the vSphere Client also shows, flat for the whole hour: Compressed 1,172,880 KB; Ballooned memory 0; Swap in rate, Swap out rate, Compression rate and Decompression rate 0.
- The application owner sees Swapped at about 9 GB and Swap target at about 9.5 GB and asks: "Is ESXi swapping my VM right now? Will it swap another 9.5 GB? Is that why the VM is slow?"

Which statements are correct?

- A. ESXi is not swapping or compressing the VM's memory during this hour.
- B. ESXi will swap about 9.5 GB more of the VM, the amount shown in Swap target.
- C. Swap target is the reclamation level ESXi aims at for this VM, which it need not reach.
- D. The gap of about 440 MB between Swap target and Swapped is pages still waiting to be swapped out.
- E. Swap target moves against Consumed in most samples: when Consumed rises, the target falls.
- F. The flat Granted shows that the guest did not ask ESXi for new pages during the hour.
- G. The VM is not waiting for its swapped pages during this hour.
- H. Add memory to the VM: it is short of memory.
- I. The swapped pages stay out until the guest touches them.
- J. A memory limit on the VM is the likely source of the swapped memory.
- K. Swapped above 0 while the swap-in and swap-out rates are both 0 is a counter error.
- L. The VM can be cut to a few hundred MB, the size of its Active memory.

## Likely wrong answer
- B: "It will swap another 9.5 GB."
- H: "The VM is slow because it is short of memory: add memory."
- D: "The rest of the swap target is still queued to go out."

## Expected key points
- Answer: A, C, E, F, G, I.
- A true: Swap in rate, Swap out rate, Compression rate and Decompression rate are 0 all hour; Swapped is 9,486,212 KB in every sample (maximum = minimum).
- B false: Swap target is an input, not pages queued on top of Swapped; with every rate at 0, nothing goes out.
- C true: the target is a compress-swap target, an input; ESXi need not reach it if it does not have to.
- D false: the target is not the same thing as Swapped, and no page is going out: every rate is 0.
- E true: in the export the target moves against Consumed in 161 of the 179 steps (the two mirror each other), and changes by less than 0.1 MB per step.
- F true: Granted is 6,118,124 KB in every sample.
- G true: swap-in is the contention; at 0, the guest does not wait for these pages now. A wait would show as swap-in, decompression and memory latency.
- H false: nothing is swapped in or out now; the swapped pages are history that the guest does not touch, and a VM with pages swapped out is not short of memory by that alone.
- I true: swapped and compressed pages stay out until the guest requests them; ESXi does not bring them back on its own.
- J false: the VM has no memory limit and no resource pool; the swapped pages come from past host pressure (or arrived with a vMotion).
- K false: Swapped is not Swap in - Swap out; it is what is out now, built up in the past, and the rates show only the present.
- L false: Active is a sampled estimate for the kernel; neither Active nor Consumed suits sizing. Size from Guest OS counters.

## Notes
- From the author's samples (docx, 2026-11-12): a vSphere Client table of one hour with Swap target changing every 20 seconds, Swapped, Granted and Active flat, Consumed moving a little, every rate 0, and "The patterns of Consumed and Swap Target are mirror image." The knowledge base keeps that example (VM Memory Swap Target).
- The CSV was regenerated 2026-11-14 with new numbers and another VM (a 16 GB Linux log collector instead of the 8 GB Windows VM of the author's sample), so that no value of the attachment is in the knowledge base (project/question-pairing-2026-11-14.md, section 1, item 3; pair A11). Generator: a seeded script (seed 14220261114). Granted + Swapped + Compressed = 16 GB exactly, as in the author's data.
- Swap target is compared with Swapped (vSphere Monitoring and Performance, memory counters; Broadcom KB 374743, esxtop SWTGT vs SWCUR: https://knowledge.broadcom.com/external/article/374743). Here the target sits above Swapped while every rate is 0; the key relies on the zero rates, not on the gap.
- Converted from judged to multiple choice (Q199 F, 2026-11-14). Dropped from the old key: "Active is tiny and flat: the guest barely touches memory" (Active is a sampled kernel estimate with no operational use: VM Memory Active) and "a reboot clears them" (no knowledge file states it).
- Options rewritten 2026-11-14 to one fact each (design.md 3.9; project/question-pairing-2026-11-14.md) (author approved, 2026-11-14): A, C, F, H, I, K and L no longer carry a second clause; the vMotion clause of old I moved to the reason of J. Key unchanged: A, C, E, F, G, I.
- Paired with 0143 (theory and practical; design.md, section 3.9).

## Metadata
```yaml
id: "0142"
title: "Swap Target, Swapped, Granted and Consumed"
product: [vsphere, linux]
technology: [memory]
task: read-metric
level: 400
answer_type: deterministic
answer: [A,C,E,F,G,I]
misconception: [B,D,H]
pair: "0143"
input: [table]
object: [vm]
tool: [vcenter]
knowledge:
  - vsphere/technology/memory/metrics/virtual-motherboard/swap-target
  - vsphere/technology/memory/metrics/virtual-motherboard/swapped
  - vsphere/technology/memory/metrics/virtual-motherboard/swap-in-rate
  - vsphere/technology/memory/metrics/virtual-motherboard/granted
  - vsphere/technology/memory/metrics/virtual-motherboard/active
  - vsphere/technology/memory/concepts/swap-and-compression
knowledge_main: vsphere/technology/memory/metrics/virtual-motherboard/swap-target
attachments:
  - 0142/vm-memory-real-time-1-hour.csv
origin: book
source_path: "Author samples (docx, 2026-11-12) > Swap target, swapped, granted, consumed (Line 1 to Line 4)"
misconception_type: [cumulative-vs-current, reclamation-as-contention]
status: draft
```
