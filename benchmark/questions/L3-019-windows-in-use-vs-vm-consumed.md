# Windows In Use vs VM Consumed

## Prompt
- A VM owner writes: "Why is Guest OS metric differ to the VM metric? Shouldn't Windows In Used map to VM Consumed since both are utilization? I see their patterns not the same, so I'm confused."

Which statements are correct?

- A. Windows In Use and VM Consumed are two views of one utilization; the gap between them is collection timing.
- B. Windows and ESXi manage the VM's memory independently.
- C. ESXi cannot see how Windows classifies its pages as In Use, Modified, Standby or Free.
- D. ESXi maps a guest page when the guest first touches it.
- E. When Windows frees memory, In Use falls while Consumed stays where it was.
- F. With VMware Tools running, ESXi reads Windows In Use and uses it to update Consumed.
- G. VM Active is the VM counter that maps to Windows In Use.
- H. ESXi sees the Windows page file and reports its use as the VM's Swapped memory.
- I. Once Windows counters are collected, VM Consumed has no use left.
- J. VM Consumed near the configured size is a reason to add memory to the VM.
- K. When Windows gives freed pages to a new process, ESXi backs them again and Consumed rises.

## Likely wrong answer
- A: "They are the same utilization seen from two sides; the patterns differ only because they are collected at different times."
- G: "Then Windows In Use must map to VM Active instead."

## Expected key points
- Answer: B, C, D, E.
- A is false: there is no mapping; the two layers count different things, so no timing fix makes them agree.
- B is true: the Guest OS cannot see host memory and runs its memory as if on a physical server; ESXi cannot see the guest's lists.
- C is true: how the guest classifies pages (Standby is Windows' cache list) and its page file are ESXi blind spots; ESXi sees only reads and writes (Active: recently touched; Consumed: touched and still backed).
- D is true: ESXi maps a guest physical page at the first touch (a fault in the second-level page tables); later freeing and reuse are ordinary memory writes that never reach ESXi.
- E is true: the ESXi page stays mapped after the guest frees it, so Consumed does not drop; Consumed is not the guest's utilization.
- F is false: Consumed is ESXi memory mapped to the VM (Granted minus sharing savings); VMware Tools plays no part in it.
- G is false: Windows In Use = VM Active is the same mistake on another counter; Active is a sampled estimate for the kernel.
- H is false: the guest page file is invisible to ESXi; Swapped is memory ESXi itself swapped out.
- I is false: Consumed is the ESXi view of the VM; it feeds host capacity and the VM's memory footprint (for example for a migration). This is the over-correction of A.
- J is false: Consumed stays high once the guest has touched its pages, cache included; that is not demand. Whether Windows needs more memory is read from Windows counters.
- K is false: freed pages are still mapped, so a new process reuses the existing mapping with no EPT violation and no ESXi work; Consumed does not move.

## Notes
- The only channel for ESXi to ask the Guest OS for memory is the balloon driver (VMware Tools on Windows; the vmw_balloon kernel module on Linux): not needed for the answer.
- Author's prompt to Gemini 3.1 Pro (high effort), 2026-11-10. A parity question: Agent E2 must at least match the frontier answer.
- The prompt is the author's own words (a real exchange); the key was drafted 2026-11-10 from the knowledge files listed in `knowledge`. The 2026-11-14 rewrite to the theory option rules was approved by the author at Level 300; the pair 0386 is the Level 400 half.
- K added in the 2026-11-15 audit (mechanism option: a new process reuses freed pages already mapped).

## Metadata
```yaml
id: "0095"
title: "Windows In Use vs VM Consumed"
product: [vsphere, windows]
technology: [memory]
input: [text]
task: explain-mechanism
object: [guest-os, vm]
tool: [guest-os-tools, vcenter]
knowledge:
  - vsphere/technology/memory/concepts/guest-os-vs-vm-memory
  - vsphere/technology/memory/metrics/virtual-motherboard/consumed
  - guest-os/memory/windows-memory
  - vsphere/technology/memory/metrics/virtual-motherboard/active
  - sp5-framework/capacity/rightsizing
  - guest-os/system/guest-os-sizing
knowledge_main: vsphere/technology/memory/concepts/guest-os-vs-vm-memory
attachments: []
origin: real-ticket
source_path: "Author's prompt and Gemini 3.1 Pro exchange, 2026-11-10"
answer_type: deterministic
answer: [B, C, D, E]
misconception: [A, G]
level: 300
misconception_type: [layer-confusion]
pair: "0386"
status: draft
```
