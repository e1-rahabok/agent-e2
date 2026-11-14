# Memory reservation vs CPU reservation

## Prompt
- A 16 GB VM with a 10 GB memory reservation and a 4 GHz CPU reservation is powered on and sits at the BIOS screen (no OS booted).
- Its host has plenty of free CPU and memory.

Which statements are correct?

- A. Neither reservation shows in the utilization counters: Memory Consumed stays low and CPU usage stays near 0.
- B. Memory Consumed jumps to about 10 GB at power-on, the amount the reservation holds for the VM.
- C. CPU usage reads about 4 GHz, because the reserved cycles are held for the VM while it runs.
- D. Memory Consumed jumps to 10 GB while CPU usage stays near 0: memory reservation is sticky, CPU is not.
- E. Memory Consumed reads about 16 GB, because the BIOS touches all configured memory at power-on.
- F. Once the guest has touched its reserved pages and then idles for days, ESXi hands those pages to other VMs.
- G. Memory Active reads about 10 GB from the reservation, although Consumed stays low.

## Likely wrong answer
- B: "Consumed jumps to the 10 GB reservation."
- C: "Both counters show the reserved amounts: 10 GB of memory and 4 GHz of CPU."

## Expected key points
- Answer: A.
- A is true: both reservations are on demand. Untouched reserved memory is not in Consumed, and Run, Used, Demand and Usage do not include a CPU reservation; with no OS running they are 0 or near 0.
- B is false: Consumed grows only as the VM touches memory; it does not jump to the reservation.
- C is false: a CPU reservation matters only under contention and never shows in usage.
- D is false: memory reservation is also on demand at power-on; it becomes sticky only for pages the VM has touched.
- E is false: the knowledge base example is exactly this VM at the BIOS: Consumed stays low.
- F is false: once a reserved page has been touched, ESXi keeps it held for the VM, even if the VM is idle for days.
- G is false: Active is a sampled estimate of recently touched memory; a reservation adds nothing to it.

## Notes
- Tests: Same name, different behaviour (principle: CPU vs memory are different in nature).
- Prompt sharpened: the host has free CPU and memory, so no contention is in play.
- The old key point "once touched, the reserved page stays held" is tested by the false option F, to keep this a one-answer question.
- Left out of the options: whether the VMkernel can give untouched reserved memory to other VMs (open author question Q201).
- Converted from judged to multiple choice (Q199 F, 2026-11-14).

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
answer: [A]
misconception: [B, C]
level: 300                      # author 2026-11-05
object: [vm]
tool: [vcenter]
knowledge_main: vsphere/architecture/resource-controls
misconception_type: [same-name-other-object]
status: draft
```
