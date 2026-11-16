# Memory reservation vs CPU reservation

## Prompt
- A 24 GB VM with a 16 GB memory reservation and a 6 GHz CPU reservation is powered on and sits at the BIOS screen (no OS booted).
- Its host has plenty of free CPU and memory.

Which statements are correct?

- A. While the VM sits at the BIOS, ESXi can give the untouched part of its 16 GB reservation to other VMs.
- B. CPU usage reads about 6 GHz while the VM sits at the BIOS screen.
- C. Lower the CPU reservation now: the idle VM keeps 6 GHz of cycles from the other VMs on the host.
- D. Memory Consumed reads about 24 GB, because the BIOS touches all configured memory at power-on.
- E. Once the guest has touched its reserved pages and then idles for days, ESXi hands those pages to other VMs.
- F. A CPU reservation comes into play only when VMs on the host compete for CPU.

## Likely wrong answer
- B: "Both counters show the reserved amounts: 16 GB of memory and 6 GHz of CPU."
- E: "Reserved memory goes back to the other VMs once the VM idles."

## Expected key points
- Answer: A, F.
- A is correct: a memory reservation is on demand; until the VM has touched all memory within its reservation, the VMkernel can give the untouched part to other VMs.
- B is wrong: Run, Used, Demand and Usage do not include a CPU reservation; with no OS running they are 0 or near 0.
- C is wrong: a reservation guarantees the VM runtime when it asks for it; it holds no cycles back. The other VMs run on the cycles the idle VM leaves unused, so lowering the reservation frees nothing now.
- D is wrong: Consumed grows only as the VM touches memory; a VM at the BIOS has touched little, so Consumed stays low.
- E is wrong: once a reserved page has been touched, ESXi keeps it held for the VM, even if the VM is idle for days. This is the over-correction of "reservations are on demand".
- F is correct: a CPU reservation matters only under contention; without it each VM gets its runtime with or without a reservation.

## Notes
- Tests: same name, different behaviour (CPU and memory reservations differ in nature).
- The host has free CPU and memory, so no contention is in play.
- vSphere 9.1 Resource Management, Memory reservation: a VM that has not touched its whole reservation lets the unused part go to other VMs; once it has consumed its reservation, it keeps that memory (PDF pp. 1832-1833).
- Changed in the 2026-11-15 audit: numbers differ from the knowledge-base example (16 GB VM, 10 GB, BIOS; F5). Redundancy #9 (a reservation does not raise Consumed: pair 0441/0442 holds it): old A replaced in place by the untouched-reserved-memory fact (true; Q201 settled), old B (Consumed jumps to the reservation) dropped, and old G (a throwaway: Active equals the reservation) dropped. Letters: old A -> A, C -> B, D -> C, E -> D, F -> E, H -> F. Answer A, H -> A, F; misconception B, C -> B, E. Needs a new key check.

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
answer: [A, F]
misconception: [B, E]
level: 300                      # author 2026-11-05
object: [vm]
tool: [vcenter]
knowledge_main: vsphere/architecture/resource-controls
misconception_type: [same-name-other-object]
status: draft
```
