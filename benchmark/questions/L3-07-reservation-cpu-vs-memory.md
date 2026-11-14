# Memory reservation vs CPU reservation

## Prompt
- A 16 GB VM with a 10 GB memory reservation and a 4 GHz CPU reservation is powered on and sits at the BIOS screen (no OS booted).
- Its host has plenty of free CPU and memory.

Which statements are correct?

- A. ESXi backs the memory reservation with host pages only as the VM touches them.
- B. Memory Consumed jumps to about 10 GB at power-on, the amount the reservation holds for the VM.
- C. CPU usage reads about 4 GHz while the VM sits at the BIOS screen.
- D. Lower the CPU reservation now: the idle VM keeps 4 GHz of cycles from the other VMs on the host.
- E. Memory Consumed reads about 16 GB, because the BIOS touches all configured memory at power-on.
- F. Once the guest has touched its reserved pages and then idles for days, ESXi hands those pages to other VMs.
- G. Memory Active reports about 10 GB, the reserved amount.
- H. A CPU reservation comes into play only when VMs on the host compete for CPU.

## Likely wrong answer
- B: "Consumed jumps to the 10 GB reservation."
- C: "Both counters show the reserved amounts: 10 GB of memory and 4 GHz of CPU."

## Expected key points
- Answer: A, H.
- A is true: a memory reservation is on demand. Before the VM asks for memory, ESXi does not back the reservation with physical RAM; Consumed grows as the VM touches pages.
- B is false: Consumed grows only as the VM touches memory; it does not jump to the reservation.
- C is false: Run, Used, Demand and Usage do not include a CPU reservation; with no OS running they are 0 or near 0.
- D is false: a CPU reservation does not come into play while the VM uses no CPU or the host has CPU for every VM; the other VMs run on the cycles the idle VM does not use.
- E is false: the knowledge base example is this VM at the BIOS: Consumed stays low.
- F is false: once a reserved page has been touched, ESXi keeps it held for the VM, even if the VM is idle for days. This is the over-correction of "reservations are on demand".
- G is false: Active is a sampled estimate of recently touched memory; a reservation adds nothing to it.
- H is true: a CPU reservation matters only under contention; without it each VM gets its runtime with or without a reservation.

## Notes
- Tests: Same name, different behaviour (principle: CPU vs memory are different in nature).
- Prompt sharpened: the host has free CPU and memory, so no contention is in play.
- The old key point "once touched, the reserved page stays held" is tested by the false option F.
- Left out of the options: whether the VMkernel can give untouched reserved memory to other VMs (open author question Q201).
- Converted from judged to multiple choice (Q199 F, 2026-11-14).
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): A one fact (memory backed on touch), D the wrong action (lower the CPU reservation), H the CPU mechanism stated positively. Key changed from A to A, H (author approved, 2026-11-14).

## Metadata
```yaml
id: "0014"
title: "Memory reservation vs CPU reservation"
product: [vsphere]
technology: [system]
input: [text]
task: judge-setting
knowledge:
  - vsphere/architecture/resource-controls
  - vsphere/technology/memory/metrics/virtual-motherboard/consumed
  - vsphere/technology/memory/metrics/virtual-motherboard/active
attachments: []
origin: book
source_path: "The World of Metrics > Metrics Nuances: Resource Management."
answer_type: deterministic
answer: [A, H]
misconception: [B, C]
level: 300                      # author 2026-11-05
object: [vm]
tool: [vcenter]
knowledge_main: vsphere/architecture/resource-controls
misconception_type: [same-name-other-object]
status: draft
```
