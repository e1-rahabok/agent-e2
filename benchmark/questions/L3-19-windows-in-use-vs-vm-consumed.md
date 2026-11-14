# Windows In Use vs VM Consumed

## Prompt
- A VM owner writes: "Why is Guest OS metric differ to the VM metric? How come there is no mapping? Shouldn't Windows In Used map to VM Consumed since both are utilization? I see their patterns not the same, so I'm confused."

Which statements are correct?

- A. Windows In Use and VM Consumed are two views of one utilization; the gap between them is collection timing.
- B. Windows and ESXi manage the VM's memory independently, and neither sees the other's view fully.
- C. ESXi cannot see how Windows classifies its pages as In Use, Modified, Standby or Free.
- D. ESXi learns of a guest page when the guest first touches it; freeing the page later only updates Windows's own lists.
- E. When Windows frees memory, In Use falls while Consumed stays where it was.
- F. With VMware Tools running, ESXi reads Windows In Use and uses it to update Consumed.
- G. VM Active is the VM counter that maps to Windows In Use, not Consumed.
- H. Size the Guest OS from Guest OS counters, and read the VM counters for what ESXi does.
- I. ESXi sees the Windows page file and reports its use as the VM's Swapped memory.

## Likely wrong answer
- A: "They are the same utilization seen from two sides; the patterns differ only because they are collected at different times."
- G: "Then Windows In Use must map to VM Active instead."

## Expected key points
- Answer: B, C, D, E, H.
- A is false: there is no mapping; the two layers count different things, so no timing fix makes them agree.
- B is true: the Guest OS cannot see host memory and runs its memory as if on a physical server; ESXi cannot see the guest's lists.
- C is true: how the guest classifies pages and its page file are ESXi blind spots; ESXi sees only reads and writes (Active: recently touched; Consumed: touched and still backed).
- D is true: ESXi maps a guest physical page at the first touch (a fault in the second-level page tables); freeing and reusing pages are ordinary memory writes that never reach ESXi.
- E is true: the ESXi page stays mapped after the guest frees it, so Consumed does not drop; Consumed is not the guest's utilization.
- F is false: Consumed is ESXi memory mapped to the VM (Granted minus sharing savings); VMware Tools plays no part in it.
- G is false: Windows In Use = VM Active is the same mistake on another counter; Active is a sampled estimate for the kernel.
- H is true: you size the Guest OS from what happens inside it, and read VM counters for ESXi's memory management.
- I is false: the guest page file is invisible to ESXi; Swapped is memory ESXi itself swapped out.

## Notes
- The only channel for ESXi to ask the Guest OS for memory is the balloon driver (VMware Tools on Windows; the vmw_balloon kernel module on Linux): not needed for the answer.
- Author's prompt to Gemini 3.1 Pro (high effort), 2026-11-10. Author: Gemini's answer looks copied from the book. A parity question: Agent E2 must at least match it.
- The prompt is the author's own words (a real exchange); the key was drafted by Claude 2026-11-10 from the knowledge files listed in `knowledge`. Counts only after author approval.
- Converted from judged to multiple choice (Q199 F, 2026-11-14). The author's words are kept as the VM owner's message.

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
knowledge_main: vsphere/technology/memory/concepts/guest-os-vs-vm-memory
attachments: []
origin: real-ticket
source_path: "Author's prompt and Gemini 3.1 Pro exchange, 2026-11-10"
answer_type: deterministic
answer: [B, C, D, E, H]
misconception: [A, G]
level: 300
misconception_type: [layer-confusion]
status: draft
```
