# What a VM memory reservation changes

## Prompt
- A running VM has 16 GB of configured memory and has consumed about 9 GB. Its memory reservation is 0.
- Its ESXi 9.1 host has free memory and no memory pressure.
- An administrator edits the VM and sets the memory reservation to 12 GB. The Reconfigure virtual machine task completes.
- The administrator then opens the vSphere Client memory charts of the VM and of the host and asks: "What did the reservation change, and where do I see it?"

Which statements are correct?

- A. The VM's Consumed rises to 12 GB, because ESXi now backs the whole reservation with host memory.
- B. The host's Total reservation rises by 12 GB, the amount the VM now reserves.
- C. The VM's Consumed and Granted stay at their level when the task completes.
- D. The host's Reservation consumed rises and its Reservation available falls by the same amount.
- E. The VM's Entitlement chart rises to 12 GB and shows the new reservation.
- F. The reservation is a setting of the VM: Edit Settings and the reconfigure task show it.
- G. The host's Consumed rises by about 3 GB, the part of the reservation the VM has not touched yet.
- H. Consumed did not move, so the change was not applied; the administrator should repeat it.
- I. Power-on of other VMs on this host is now checked against unreserved memory that is 12 GB smaller.
- J. The host's kernel reservation, System Resource Reservation, grows by the VM's 12 GB.

## Likely wrong answer
- A: "Consumed jumps to the reservation."
- G: the over-correction: "only the untouched part of the reservation is backed at once".

## Expected key points
- Answer: C, D, F, I.
- A false: Consumed counts the pages the VM has touched; a reservation alone does not back pages, so Consumed rises only as the guest touches memory.
- B false: Total reservation is the host's reservable capacity (Reservation consumed plus Reservation available). It does not follow the VMs' reservations.
- C true: a reservation changes no page, so Consumed and Granted keep their level.
- D true: the host's reservation counters take the change: Reservation consumed rises, and Reservation available falls by the same amount because Total reservation stays the same.
- E false: Entitlement is a scheduler value that follows the VM's consumption; it did not rise to a reservation on the lab VM.
- F true: the reservation is a VM setting, recorded in the VM's configuration and in the reconfigure task event (`config.memoryAllocation.reservation: old -> new`).
- G false: host Consumed counts pages in use, and the reservation backs none of them; it does not rise by the untouched part either.
- H false: the flat Consumed is the expected result of a reservation; the task completed, so the change applied. Repeating it changes nothing.
- I true: admission control counts a running VM's full reservation, used or not, against the host's unreserved memory.
- J false: the kernel reservation is the host/system allocation minimum, a separate reservation that stays steady whatever the VMs reserve.

## Notes
- Pair with 0442 (practical: the same fact on a VM chart and the task list). A fact gets two questions at most (design.md, section 3.9).
- No option rests on whether Reservation consumed counts the reservation as set or only the touched part (open author question Q231): D and the key read the same under both readings. No option rests on the Entitlement formula (open author question Q230); E only says Entitlement does not show the reservation.
- Distinct from 0014 (a memory reservation is backed as pages are touched, with a CPU reservation as the contrast): this question asks which counters take a reservation change.
- Evidence behind C, D, E and F: the author's lab test of 2026-11-15, one VM, the reservation set and later removed (knowledge: vm-memory-metrics, section VM reservation across counters; host-memory-metrics, section VM reservation across counters).
- Written 2026-11-15 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after approval (design.md, section 6.2).

## Metadata
```yaml
id: "0441"
title: What a VM memory reservation changes
product: [vsphere]
technology: [memory]
task: explain-mechanism
level: 300
answer_type: deterministic
input: [text]
object: [vm, esxi]
tool: [vcenter]
knowledge:
  - vsphere/technology/memory/metrics/comparisons/vm-memory-metrics
  - vsphere/technology/memory/metrics/comparisons/host-memory-metrics
  - vsphere/technology/memory/metrics/host/reservation
  - vsphere/technology/memory/metrics/virtual-motherboard/consumed
  - vsphere/architecture/resource-controls
  - vsphere/architecture/overhead
knowledge_main: vsphere/technology/memory/metrics/comparisons/vm-memory-metrics
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-15 from the author's lab test"
answer: [C, D, F, I]
misconception: [A, G]
misconception_type: [provider-vs-consumer]
pair: "0442"
status: draft
```
