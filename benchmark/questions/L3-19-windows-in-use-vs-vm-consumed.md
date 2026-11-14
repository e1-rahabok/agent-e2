# Windows In Use vs VM Consumed

## Prompt
Why is Guest OS metric differ to the VM metric? How come there is no mapping? Shouldn't Windows In Used map to VM Consumed since both are utilization? I see their patterns not the same, so I'm confused.

## Likely wrong answer
Maps Windows In Use to VM Consumed (or Active) as two views of the same utilization, and explains the gap as a collection or timing difference.

## Expected key points
- No mapping: the Guest OS and ESXi manage memory independently; neither sees the other fully.
- ESXi cannot see how Windows classifies pages (In Use, Modified, Cache, Free) or its page file. It sees only reads and writes: Active (recently touched) and Consumed (touched since boot and still backed).
- When Windows frees memory it updates its own lists; it does not tell the hypervisor, so Consumed does not drop while In Use does. Consumed is not the guest's utilization: it does not drop when Windows frees memory.
- Consequence: size the Guest OS from Guest OS metrics; read VM metrics for what ESXi does.

## Notes
- The only channel for ESXi to ask the Guest OS for memory is the balloon driver (VMware Tools on Windows; the vmw_balloon kernel module on Linux): not needed for the answer.
- Author's prompt to Gemini 3.1 Pro (high effort), 2026-11-10. Author: Gemini's answer looks copied from the book. A parity question: Agent E2 must at least match it.
- The prompt is the author's own words (a real exchange); the key was drafted by Claude 2026-11-10 from the knowledge files listed in `knowledge`. Counts only after author approval.

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
knowledge_main: vsphere/technology/memory/concepts/guest-os-vs-vm-memory
attachments: []
origin: real-ticket
source_path: "Author's prompt and Gemini 3.1 Pro exchange, 2026-11-10"
answer_type: judged
level: 300
misconception_type: [layer-confusion]
status: draft
```
