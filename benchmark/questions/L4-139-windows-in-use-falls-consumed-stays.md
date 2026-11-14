# Windows In use falls after a restart; VM Consumed stays

## Prompt
See [Task Manager before the restart](0386/task-manager-memory-before-restart.png), [Task Manager after the restart](0386/task-manager-memory-after-restart.png) and [the vCenter memory chart of the VM](0386/vcenter-vm-memory-consumed-active-past-day.png).

- A Windows Server VM runs a Java application server.
- Yesterday at about 15:00 the owner restarted the application to free memory.
- The owner writes: "Windows gave the memory back, but vCenter still shows Consumed where it was. Is vCenter wrong, or does the VM leak memory? If Consumed is right, the VM needs more memory."

Which statements are correct?

- A. After the restart, Windows put the freed pages on its own lists, which ESXi cannot see.
- B. Consumed stays where it was because ESXi keeps a VM page mapped once the guest has touched it.
- C. Consumed will follow In use down within a few collection cycles: the gap is collection timing.
- D. VM Active, not Consumed, is the VM counter that tracks Windows In use.
- E. When the application stopped, Windows returned the freed memory to ESXi through VMware Tools.
- F. Consumed that stays up after the application freed memory shows a memory leak inside Windows.
- G. Consumed near the configured size shows that the VM is short of memory: add memory.
- H. Consumed is of no use for this VM now that Windows counters are available.
- I. Windows is sized from its own counters, cache included, not from Consumed.

## Input to supply
- Product: Windows Server 2022 (or 2019) VM with VMware Tools, vSphere Client 9.1. The VM has 16 GB or more and runs an application that holds much of its memory (a Java server with a large heap, or Sysinternals Testlimit with `-d` to touch memory).
- Screen 1: Task Manager > Performance > Memory, a few minutes before the application restart, with the composition bar and the In use, Available, Committed and Cached values visible. Save as `benchmark/questions/0386/task-manager-memory-before-restart.png`.
- Screen 2: the same screen a few minutes after the restart, once the application has started again. Save as `benchmark/questions/0386/task-manager-memory-after-restart.png`.
- Screen 3: vSphere Client > the VM > Monitor > Performance > Advanced > Memory. Chart Options: timespan Past day; counters Consumed and Active (KB); target the VM. Capture after the restart, so the chart covers the hours before and after it. Save as `benchmark/questions/0386/vcenter-vm-memory-consumed-active-past-day.png`.
- Restart the application at about 15:00. If it is restarted at another time, change "about 15:00" in the prompt to that time.
- Condition the key depends on:
  - In use before the restart at 50% or more of the configured memory, and lower after it by at least a quarter of the configured memory;
  - Consumed within 10% of the configured memory before and after the restart, with no drop at the restart;
  - the host not under memory pressure (no balloon, swap or compression on the VM in the day).
- Masking: mask every VM, host, datastore and cluster name (Task Manager shows none; check the vSphere Client header and legend).

## Likely wrong answer
C: "Consumed and In use are the same usage seen from two sides; Consumed will catch up." Or D: "Then In use must map to VM Active."

## Expected key points
- Answer: A, B, I.
- A true: freeing a page only updates the guest's free list, an ordinary memory write that never reaches ESXi. How Windows classifies its pages is an ESXi blind spot.
- B true: ESXi maps a VM page at the guest's first touch and keeps the mapping until it reclaims the page (sharing, balloon, compression, swap). With no host pressure, nothing reclaims it, so Consumed stays near the configured size.
- C false: there is no mapping between In use and Consumed; the two layers manage memory independently, so no amount of time makes them agree.
- D false: the same mistake on another counter. Active is a sampled estimate of recently touched pages for the kernel; it has no mapping to In use either.
- E false: VMware Tools plays no part in Consumed. The only channel for ESXi to take memory from the guest is the balloon driver, and only under host pressure.
- F false: Consumed is not the guest's utilization; it stays high once pages are touched. The fall in In use shows Windows released the memory.
- G false: the wrong action. Consumed near configured is the normal state of a VM that has touched its memory; it is not demand.
- H false: over-correction. Consumed shows the host memory the VM holds: what host capacity and the VM's footprint (for example, for a migration) count.
- I true: Guest OS sizing reads the guest's own counters, with part of the cache; VM counters describe what ESXi does.

## Notes
- Paired with 0095 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item C4.
- Task Manager keeps only 60 seconds of history, so the before and after values come from two captures, and the day from the vCenter chart.
- The key holds whenever the condition of `## Input to supply` holds. No option rests on the Active values.
- Written 2026-11-14 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after approval (design.md, section 6.2).

## Metadata
```yaml
id: "0386"
title: "Windows In use falls after a restart; VM Consumed stays"
product: [vsphere, windows]
technology: [memory]
task: read-metric
level: 400
answer_type: deterministic
input: [screenshot]
object: [guest-os, vm]
tool: [guest-os-tools, vcenter]
knowledge:
  - vsphere/technology/memory/concepts/guest-os-vs-vm-memory
  - vsphere/technology/memory/metrics/virtual-motherboard/consumed
  - vsphere/technology/memory/metrics/virtual-motherboard/active
  - vsphere/technology/memory/metrics/comparisons/vm-memory-metrics
  - guest-os/memory/windows-memory
  - guest-os/system/concepts/guest-os-sizing
knowledge_main: vsphere/technology/memory/concepts/guest-os-vs-vm-memory
attachments:
  - 0386/task-manager-memory-before-restart.png
  - 0386/task-manager-memory-after-restart.png
  - 0386/vcenter-vm-memory-consumed-active-past-day.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C4"
answer: [A, B, I]
misconception: [C, D]
misconception_type: [layer-confusion]
pair: "0095"
status: awaiting-input
```
