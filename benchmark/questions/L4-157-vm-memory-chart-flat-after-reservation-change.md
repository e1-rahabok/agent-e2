# VM memory chart flat after a reservation change

## Prompt
- The VM sun05-acepod03-linux-jump-copy has 8 GB of configured memory. Its ESXi 9.1 host has free memory and no memory pressure.
- An administrator reconfigured the VM's memory reservation twice. [The vSphere Client task list of the VM](0442/vcenter-vm-reconfigure-tasks.png) shows both tasks. The vSphere Client shows times in UTC+8.
- [The attached chart export](0442/vm-memory-trend.csv) holds the VM's memory counters for the same hour, one row per minute, in UTC. Consumed, Entitlement, Granted and Overhead consumed are in KB.
- The administrator says: "The memory chart did not move when I set the reservation, and did not move when I removed it. Did the reservation not apply? Is the VM now guaranteed its memory?"

Which statements are correct?

- A. Consumed did not rise when the reservation was set, so the reservation was not applied.
- B. The task list shows the reservation set from 0 to 8,192 MB and later back to 0, both tasks completed.
- C. Removing the reservation let ESXi reclaim the VM's pages, even though the host had free memory.
- D. In UTC the two reservation changes fall at about 04:06 and 04:22.
- E. Ballooned memory is 0 only while the reservation is set, so the reservation kept ESXi from ballooning the VM.
- F. Granted stays below 8 GB in every row, so the VM had touched less memory than it reserved.
- G. The reservation did nothing, so it can be set on every VM to its full memory at no cost.
- H. While the reservation was set, its untouched part could not back the pages of other VMs.
- I. The host side of the reservation sits in the host's reservation counters, not in this VM chart.
- J. No step of Consumed between neighbouring rows reaches 1% in the hour, 04:06 and 04:22 included.

## Likely wrong answer
- A: "Consumed should jump to the reservation; it did not, so the reservation failed."
- C: "Removing a reservation lets ESXi take the memory back."
- H: "A reservation sets its memory aside for the VM, so no other VM can use it."

## Expected key points
- Answer: B, D, F, I, J.
- A false: a reservation does not back pages, so VM Consumed does not rise with it; the tasks completed.
- B true: the task events show `config.memoryAllocation.reservation: 0 -> 8192` and later `8192 -> 0`, both Completed.
- C false: with free host memory ESXi has no reason to reclaim, and removing a reservation does not take memory back; the mapping of a touched page stays until ESXi reclaims it. The export shows a 0.34% dip one row after 04:22 (5,814,256 to 5,794,752 KB), inside the hour's normal noise of up to 0.44%.
- D true: the tasks ran at 12:06 and 12:22 in UTC+8, which are 04:06 and 04:22 in UTC.
- E false: Ballooned memory is 0 in every row, before the first change and after the removal too; with free host memory nothing was ballooned, so the reservation shows no effect on it.
- F true: Granted is flat at 6,356,764 KB (6.06 GiB), below 8 GB (8,388,608 KB); Granted counts the pages the VM has mapped, so the VM had touched less than its reservation.
- G false: the over-correction. A reservation shows in no VM counter but it counts against the host's unreserved memory at power-on and limits overcommit; it is not free.
- H false: until the VM touches its reserved memory, the untouched part can back other VMs' pages; a reservation is held as pages only once used. Admission control is what counts the full amount at power-on.
- I true: a reservation is a host-side guarantee; Reservation consumed and Reservation available of the host take it, while the VM's memory counters measure pages.
- J true: the largest change of Consumed between two neighbouring rows in the hour is 0.44% (at 03:47); the steps at 04:06 and 04:22 are 0.38% and 0.20%, so no step shows at either change.

## Notes
- Pair with 0441 (theory). Wrong on both: a knowledge gap. Right on theory and wrong on practical: a reading failure (the time zone, the unit, or taking a flat chart for a failed change).
- Attachments: the author's lab capture of 2026-11-15 (one VM, vCenter 9.1). The export is the real-time chart of the VM downsampled to one row per minute (60 rows, 03:28 to 04:27 UTC); the task screenshot is cropped to the task list. Lab VM and host names stay (design.md, section 13).
- The condition the key depends on holds in the export: Consumed 5,758,392 to 5,830,972 KB, Granted 6,356,764 KB and Overhead consumed 58,460 KB in every row, Ballooned memory 0.
- No option rests on whether the host's Reservation consumed counts the reservation as set (Q231, answered 2026-11-15: counted as set). No option uses Entitlement, a kernel value (Q230, answered 2026-11-15). I states only that the host counters take the reservation.
- Leak guard: the knowledge base does not state this capture's values (checked 2026-11-15; the VM-level lab lines in vm-memory-metrics, entitlement and resource-controls carry no numbers).
- Written 2026-11-15 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after approval (design.md, section 6.2).

## Metadata
```yaml
id: "0442"
title: VM memory chart flat after a reservation change
product: [vsphere]
technology: [memory]
task: read-metric
level: 400
answer_type: deterministic
input: [table, screenshot]
object: [vm, esxi]
tool: [vcenter]
knowledge:
  - vsphere/technology/memory/metrics/comparisons/vm-memory-metrics
  - vsphere/technology/memory/metrics/virtual-motherboard/granted
  - vsphere/technology/memory/metrics/virtual-motherboard/consumed
  - vsphere/technology/memory/metrics/host/reservation
  - vsphere/architecture/resource-controls
knowledge_main: vsphere/technology/memory/metrics/comparisons/vm-memory-metrics
attachments:
  - 0442/vcenter-vm-reconfigure-tasks.png
  - 0442/vm-memory-trend.csv
origin: synthetic
source_path: "Author's lab capture 2026-11-15"
answer: [B, D, F, I, J]
misconception: [A, C, H]
misconception_type: [provider-vs-consumer]
pair: "0441"
status: draft
```
