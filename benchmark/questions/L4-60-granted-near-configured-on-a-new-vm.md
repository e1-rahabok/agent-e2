# Granted near configured on a new VM

## Prompt
- A new Windows Server 2025 VM with 64 GB of memory was powered on this morning. Only the OS runs; the application is installed next week.
- The ESXi host is not under memory pressure: no balloon, compression or swap on any VM.
- vSphere Client, advanced memory chart of the VM, one hour after boot:
  - Granted: 61.3 GB
  - Consumed: 60.1 GB
  - Shared: 1.2 GB
  - Active: 1.9 GB
- The capacity team flags the VM: "Granted is 96% of configured. It is nearly full; add memory before go-live."

Which statements are correct?

- A. Windows zeroes its memory at boot; each page it touches gets a mapping, so Granted nears configured early.
- B. Granted near configured shows the guest needs that much memory, so add memory before go-live.
- C. At 96% Granted the VM is about to run out, and ESXi will start swapping it once Granted reaches 100%.
- D. With no host memory pressure, ESXi does not take back pages the guest touched once, so Granted stays high while the VM idles.
- E. Most granted pages were touched once at boot, not by the workload: Active is 1.9 of 61.3 GB.
- F. The 1.2 GB gap between Granted and Consumed is memory that ESXi has swapped out of the VM.

## Likely wrong answer
B or C: Granted near configured read as a VM that is full.

## Expected key points
- Answer: A, D, E.
- A: Granted counts VM pages that have an ESXi page mapped. OS initialization and memory zeroing touch most of the address space early, so Granted rises toward configured, its upper limit.
- B is wrong: Granted says which pages were ever touched, not what the guest needs. Need is read in the Guest OS once the application runs.
- C is wrong: a VM does not swap because its Granted is high; ESXi reclaims under host pressure or a limit, and there is neither.
- D: without pressure, the VMkernel does not reclaim touched pages.
- E: Active, the estimate of recently touched pages, is 1.9 GB of 61.3 GB granted: the pages were touched by the OS at boot and not since.
- F is wrong: swapped pages are not in Granted. Consumed is Granted minus what sharing saves, and that saving can be at most Shared (1.2 GB): the gap is sharing.

## Notes
- Sources: the knowledge base, VM Memory Granted (touched pages stay mapped; Granted excludes swapped pages; Consumed = Granted - sharing savings) and VM Memory Zero Pages (Windows initializes pages with zeroes).

## Metadata
```yaml
id: "0148"
title: "Granted near configured on a new VM"
product: [vsphere, windows]
technology: [memory]
task: decide-capacity
level: 400
answer_type: deterministic
input: [text]
object: [vm]
tool: [vcenter]
knowledge:
  - vsphere/technology/memory/metrics/virtual-motherboard/granted
  - vsphere/technology/memory/metrics/virtual-motherboard/zero-pages
  - vsphere/technology/memory/metrics/virtual-motherboard/consumed
knowledge_main: vsphere/technology/memory/metrics/virtual-motherboard/granted
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
answer: [A, D, E]
misconception: [B, C]
misconception_type: [consumption-as-contention]
status: draft
```
