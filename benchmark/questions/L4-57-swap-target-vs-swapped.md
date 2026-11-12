# Swap Target, Swapped, Granted and Consumed

## Prompt
- A Windows VM with 8 GB of memory. It has no memory limit and is not in a resource pool.
- [The attached vSphere Client export](0142/vm-memory-real-time-1-hour.csv) is the VM's real-time memory chart for the last hour (20-second samples).
- In the same hour, the vSphere Client also shows, flat for the whole hour: Compressed 644,556 KB; Ballooned memory 0; Swap in rate, Swap out rate, Compression rate and Decompression rate 0.
- The application owner sees Swapped at 6.2 GB and Swap target at 6.5 GB and asks: "Is ESXi swapping my VM right now? Will it swap another 6.5 GB? Is that why the VM is slow?"

Answer the owner. Explain what each line of the export shows.

## Likely wrong answer
"Yes: ESXi is swapping the VM now, it has already swapped 6.2 GB and will swap 6.5 GB more. The VM is slow because it is short of memory: add memory or move it to another host."

## Expected key points
- ESXi is not swapping the VM now: every swap and compression rate is 0 all hour, and Swapped is flat (maximum = minimum).
- Swap target is not a queue of pages and is not added to Swapped: it is the level ESXi aims at for this VM. It barely moves (about 6.5 GB, changing by less than 1 MB) and mirrors Consumed: when Consumed rises, the target falls. With every rate at 0, nothing goes out now.
- Granted is flat: the guest is not asking for more pages.
- The VM is not waiting for these pages now: swap-in rate is 0. A wait would show as swap-in, decompression and memory latency (contention).
- Swapped pages stay out until the guest touches them. With no limit and no resource pool, they come from past host pressure (or were brought by a vMotion); a reboot in a maintenance window clears them.
- Active is tiny (82 MB) and flat: the guest barely touches memory.

## Notes
- From the author's samples (docx, 2026-11-12): a vSphere Client table of one hour: Swap target about 6,816,000 KB changing every 20 seconds, Swapped 6,520,964 KB flat, Granted 1,223,088 KB flat, Consumed 931,340-939,272 KB, Compressed 644,556 KB, Active 83,884 KB, every rate 0. "The patterns of Consumed and Swap Target are mirror image." The CSV is generated to reproduce them. Granted + Swapped + Compressed = 8 GB exactly.
- Swap target is compared with Swapped (vSphere Monitoring and Performance, memory counters; Broadcom KB 374743, esxtop SWTGT vs SWCUR: https://knowledge.broadcom.com/external/article/374743). In the author's data the target sits above Swapped while every rate is 0; the key relies on the zero rates, not on the gap.

## Metadata
```yaml
id: "0142"
title: "Swap Target, Swapped, Granted and Consumed"
product: [vsphere, windows]
technology: [memory]
task: read-metric
level: 400
answer_type: judged
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
