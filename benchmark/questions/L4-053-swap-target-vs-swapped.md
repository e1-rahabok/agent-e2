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
- E. In most 20-second steps of the export, Swap target and Consumed change in opposite directions.
- F. Granted stays the same all hour, so ESXi mapped no new pages for the guest in that hour.
- G. Granted leaves out the swapped and compressed pages; the three add up to the VM's 16 GB.
- H. Add memory to the VM: it is short of memory.
- I. A memory limit on the VM is the likely source of the swapped memory.
- J. Swapped above 0 while the swap-in and swap-out rates are both 0 is a counter error.
- K. The VM can be cut to a few hundred MB, the size of its Active memory.

## Answers
A, C, E, F, G

## Explanation
- A true: Swap in rate, Swap out rate, Compression rate and Decompression rate are 0 all hour; Swapped is 9,486,212 KB in every sample (maximum = minimum).
- B false: Swap target is a level that ESXi compares with Swapped, not pages queued on top of Swapped; above Swapped, ESXi can swap when it must, and with every rate at 0 nothing goes out.
- C true: the target is a compress-swap target, an input; ESXi need not reach it if it does not have to.
- D false: no page is queued or going out: Swap out rate and Compression rate are 0 in every sample of the hour.
- E true: in the export the target moves against Consumed in 161 of the 179 steps (the two mirror each other), and changes by less than 0.1 MB per step.
- F true: Granted is 6,118,124 KB in every sample.
- G true: Granted counts mapped VM pages and excludes swapped and compressed pages; 6,118,124 + 9,486,212 + 1,172,880 KB = 16,777,216 KB, the configured 16 GB.
- H false: nothing is swapped in or out now; the swapped pages are history that the guest does not touch, and a VM with pages swapped out is not short of memory by that alone.
- I false: the VM has no memory limit and no resource pool; the swapped pages come from past host pressure (or arrived with a vMotion).
- J false: Swapped is not Swap in - Swap out; it is what is out now, built up in the past, and the rates show only the present.
- K false: Active is a sampled estimate for the kernel; neither Active nor Consumed suits sizing. Size from Guest OS counters.
- Misconception: B: "It will swap another 9.5 GB." - H: "The VM is slow because it is short of memory: add memory." - D: "The rest of the swap target is still queued to go out."

## Notes
- From the author's samples (docx, 2026-11-12): a vSphere Client table of one hour with Swap target changing every 20 seconds, Swapped, Granted and Active flat, Consumed moving a little, every rate 0, and "The patterns of Consumed and Swap Target are mirror image." The knowledge base keeps that example (VM Memory Swap Target).
- The CSV was regenerated 2026-11-14 with new numbers and another VM (a 16 GB Linux log collector instead of the 8 GB Windows VM of the author's sample), so that no value of the attachment is in the knowledge base (project/question-pairing-2026-11-14.md, section 1, item 3; pair A11). Generator: a seeded script (seed 14220261114). Granted + Swapped + Compressed = 16 GB exactly, as in the author's data.
- Swap target is compared with Swapped (vSphere Monitoring and Performance, memory counters; Broadcom KB 374743, esxtop SWTGT vs SWCUR: https://knowledge.broadcom.com/external/article/374743). Here the target sits above Swapped while every rate is 0; the key relies on the zero rates, not on the gap.
- Left out: "Active is tiny and flat: the guest barely touches memory" (Active is a sampled kernel estimate with no operational use: VM Memory Active) and "a reboot clears them" (no knowledge file states it).
- Options rewritten 2026-11-14 to one fact each (design.md 3.9; project/question-pairing-2026-11-14.md) (author approved, 2026-11-14): A, C, F, H, I, K and L no longer carry a second clause; the vMotion clause moved to the reason of the limit option.
- Review 2026-11-15: E and F paraphrased (they restated sentences of the knowledge example); the reasons for B and D follow the corrected swap-and-compression.md (Swap target is a level compared with Swapped; vSphere Web Services API 9.1, memory counters, swaptarget). Key unchanged.
- Paired with 0143 (theory and practical; design.md, section 3.9).
- Changed in the 2026-11-15 audit (redundancy cap: "swapped pages are past reclamation and stay out until touched" is kept in the pair 0025/0391): G (no wait now) replaced by Granted excluding swapped and compressed pages; old I (pages stay out until touched) dropped. Letters: old J, K, L are now I, J, K. Key point D rests on the zero rates only.

## Metadata
```yaml
id: "0142"
title: "Swap Target, Swapped, Granted and Consumed"
product: [vsphere, linux]
technology: [memory]
task: read-metric
level: 400
answer_type: deterministic
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
