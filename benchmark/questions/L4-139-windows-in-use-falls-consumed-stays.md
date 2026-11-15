# Windows In use falls after a restart; VM Consumed stays

## Prompt
See [Task Manager before the restart](0386/task-manager-memory-before-restart.png), [Task Manager after the restart](0386/task-manager-memory-after-restart.png) and [the vCenter memory chart of the VM](0386/vcenter-vm-memory-consumed-active-past-day.png).

- A Windows Server VM runs a Java application server. Yesterday afternoon its owner restarted the application to free memory.
- The owner writes: "Windows gave the memory back, but vCenter did not notice. Either vCenter is broken, or the VM leaks. And if vCenter is right, the VM is short of memory."

Which statements are correct?

- A. In use is lower after the restart by at least a quarter of the VM's memory.
- B. The vCenter chart shows Consumed dropping at about the time of the restart.
- C. After the restart, Windows keeps the freed pages on its own lists, which ESXi has no view of.
- D. ESXi keeps a VM page mapped once the guest has touched it, so Consumed has no reason to fall.
- E. The flat Consumed line is vCenter lagging behind Windows; a later collection will catch up.
- F. The Active line in vCenter is the VM-side copy of the In use value in Task Manager.
- G. A leak inside Windows is what holds Consumed up after the restart.
- H. The VM needs more memory, because Consumed sits close to its configured size.
- I. With Task Manager at hand, the Consumed line of this VM can be ignored for every purpose.
- J. The guest's memory is sized from Windows counters, part of the cache included.

## Input to supply
- Product: Windows Server 2022 (or 2019) VM with VMware Tools, vSphere Client 9.1. The VM has 16 GB or more and runs an application that holds much of its memory (a Java server with a large heap, or Sysinternals Testlimit with `-d` to touch memory).
- Screen 1: Task Manager > Performance > Memory, a few minutes before the application restart, with the composition bar, In use, Available, Committed and Cached visible, and the Windows taskbar clock visible. Save as `benchmark/questions/0386/task-manager-memory-before-restart.png`.
- Screen 2: the same screen a few minutes after the restart, once the application has started again, with the taskbar clock visible. Save as `benchmark/questions/0386/task-manager-memory-after-restart.png`.
- Screen 3: vSphere Client > the VM > Monitor > Performance > Advanced > Memory. Chart Options: timespan Past day; counters Consumed and Active (KB); target the VM. Capture after the restart, so the chart covers the hours before and after it. Save as `benchmark/questions/0386/vcenter-vm-memory-consumed-active-past-day.png`.
- Condition the key depends on:
  - In use before the restart at 50% or more of the configured memory, and lower after it by at least a quarter of the configured memory;
  - Consumed within 10% of the configured memory at every point of the day, with no step down at the restart;
  - no balloon, swap or compression on the VM at any point of the day (the host is not under memory pressure).
- Masking: mask every VM, host, datastore and cluster name (Task Manager shows none; check the vSphere Client header and legend).

## Likely wrong answer
E: "vCenter is just behind; Consumed will follow Windows down." Or F: "The VM counter for In use is Active."

## Expected key points
- Answer: A, C, D, J.
- A true: the two Task Manager screens show In use falling by a quarter of the VM's memory or more.
- B false: the Consumed line stays level through the restart.
- C true: freeing a page only updates the guest's free list, an ordinary memory write that never reaches ESXi. How Windows classifies its pages is an ESXi blind spot.
- D true: ESXi maps a VM page at the guest's first touch and keeps the mapping until it reclaims the page (sharing, balloon, compression, swap). With no host pressure nothing is reclaimed, so Consumed stays near the configured size.
- E false: there is no mapping between In use and Consumed; the layers manage memory independently, so waiting does not make them agree.
- F false: the same mistake on another counter. Active is a sampled ESXi estimate of recently touched pages; it has no mapping to In use.
- G false: Consumed is not the guest's utilization; it stays high once pages are touched. The fall in In use shows that Windows released the memory.
- H false: the wrong action. Consumed near the configured size is the normal state of a VM that has touched its memory; it is not demand.
- I false: over-correction. Consumed shows the host memory the VM holds: what host capacity and the VM's footprint (for example, for a migration) count.
- J true: Guest OS sizing reads the guest's own counters, with part of the cache; VM counters describe what ESXi does.

## Notes
- Paired with 0095 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item C4.
- Task Manager keeps only 60 seconds of history, so the before and after values come from two captures (their clocks place the restart), and the day from the vCenter chart.
- Review fixes 2026-11-15: options reworded away from 0095; two screen readings added (A true, B false); the restart time moved from the stem to the taskbar clock. Key A, B, I → A, C, D, J.
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
  - guest-os/system/guest-os-sizing
knowledge_main: vsphere/technology/memory/concepts/guest-os-vs-vm-memory
attachments:
  - 0386/task-manager-memory-before-restart.png
  - 0386/task-manager-memory-after-restart.png
  - 0386/vcenter-vm-memory-consumed-active-past-day.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C4"
answer: [A, C, D, J]
misconception: [E, F]
misconception_type: [layer-confusion]
pair: "0095"
status: awaiting-input
```
