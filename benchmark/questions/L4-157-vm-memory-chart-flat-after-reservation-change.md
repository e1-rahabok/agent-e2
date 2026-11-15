# VM memory chart flat after a reservation change

## Prompt
- The VM sun05-acepod03-linux-jump-copy has 8 GB of configured memory. Its ESXi 9.1 host has free memory and no memory pressure.
- An administrator reconfigured the VM's memory reservation twice. [The vSphere Client task list of the VM](0442/vcenter-vm-reconfigure-tasks.png) shows both tasks. The vSphere Client shows times in UTC+8.
- [The attached chart export](0442/vm-memory-trend.csv) holds the VM's memory counters for the same hour, one row per minute, in UTC. Consumed, Entitlement, Granted and Overhead consumed are in KB.
- The administrator says: "The memory chart did not move when I set the reservation, and did not move when I removed it. Did the reservation not apply? Is the VM now guaranteed its memory?"

Which statements are correct?

- A. Consumed did not rise when the reservation was set, so the reservation was not applied.
- B. The task list shows the reservation set from 0 to 8,192 MB and later back to 0, both tasks completed.
- C. Entitlement rose to 8 GB while the reservation was set and fell back when it was removed.
- D. In UTC the changes fall at about 04:06 and 04:22, and Consumed at those minutes stays inside its range for the hour.
- E. Ballooned memory of 0 all hour shows that the reservation kept ESXi from ballooning the VM.
- F. Granted stays below 8 GB in every row, so the VM had touched less memory than it reserved.
- G. The reservation did nothing, so it can be set on every VM to its full memory at no cost.
- H. Overhead consumed fell when the reservation was removed, because the reservation had raised it.
- I. The host side of the reservation sits in the host's reservation counters, not in this VM chart.

## Likely wrong answer
- A: "Consumed should jump to the reservation; it did not, so the reservation failed."
- C: "A reservation raises the entitlement to its size."

## Expected key points
- Answer: B, D, F, I.
- A false: a reservation does not back pages, so VM Consumed does not rise with it; the tasks completed.
- B true: the task events show `config.memoryAllocation.reservation: 0 -> 8192` and later `8192 -> 0`, both Completed.
- C false: Entitlement stays between 6,359,036 and 6,438,876 KB (about 6.1 GiB) in every row, below 8 GB; it follows Consumed, not the reservation.
- D true: 12:06 and 12:22 in UTC+8 are 04:06 and 04:22 in UTC; Consumed at those minutes (5,791,872 and 5,814,256 KB) sits inside the hour's range (5,758,392 to 5,830,972 KB).
- E false: Ballooned memory is 0 before the first change as well; with free host memory nothing was ballooned, so the reservation shows no effect on it.
- F true: Granted is flat at 6,356,764 KB (6.06 GiB), below 8 GB (8,388,608 KB); Granted counts the pages the VM has mapped, so the VM had touched less than its reservation.
- G false: the over-correction. A reservation shows in no VM counter but it counts against the host's unreserved memory at power-on and limits overcommit; it is not free.
- H false: Overhead consumed is 58,460 KB in every row.
- I true: a reservation is a host-side guarantee; Reservation consumed and Reservation available of the host take it, while the VM's memory counters measure pages.

## Notes
- Pair with 0441 (theory). Wrong on both: a knowledge gap. Right on theory and wrong on practical: a reading failure (the time zone, the unit, or taking a flat chart for a failed change).
- Attachments: the author's lab capture of 2026-11-15 (one VM, vCenter 9.1). The export is the real-time chart of the VM downsampled to one row per minute (60 rows, 03:28 to 04:27 UTC); the task screenshot is cropped to the task list. Lab VM and host names stay (design.md, section 13).
- The condition the key depends on holds in the export: Consumed 5,758,392 to 5,830,972 KB, Entitlement 6,359,036 to 6,438,876 KB, Granted 6,356,764 KB and Overhead consumed 58,460 KB in every row, Ballooned memory 0.
- No option rests on whether the host's Reservation consumed counts the reservation as set (open author question Q231) or on the Entitlement formula (Q230). I states only that the host counters take the reservation.
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
  - vsphere/technology/memory/metrics/virtual-motherboard/entitlement
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
answer: [B, D, F, I]
misconception: [A, C]
misconception_type: [provider-vs-consumer]
pair: "0441"
status: draft
```
