# Granted near configured on a new VM

## Prompt
- A new Windows Server 2025 VM with 64 GB of memory was powered on this morning. Only the OS runs; the application is installed next week.
- The ESXi host is not under memory pressure: no balloon, compression or swap on any VM.
- vSphere Client, advanced memory chart of the VM, one hour after boot:
  - Granted: 61.3 GB
  - Consumed: 61.2 GB
  - Shared: 0.1 GB
  - Active: 1.9 GB
- The capacity team flags the VM: "Granted is 96% of configured. It is nearly full; add memory before go-live."

Which statements are correct?

- A. Windows zeroes its memory at boot, so each page gets a mapping and Granted nears configured early.
- B. Granted near configured shows the guest needs that much memory, so add memory before go-live.
- C. Once Granted reaches 100% of configured memory, ESXi will start swapping this VM.
- D. With no host memory pressure, ESXi does not take back pages the guest touched, so Granted stays high.
- E. Most granted pages were touched once at boot, not by the workload: Active is 1.9 of 61.3 GB.
- F. The 0.1 GB gap between Granted and Consumed is memory that ESXi has swapped out of the VM.
- G. Consumed, about 61.2 GB, is the host memory to plan for if this VM moves to another host.
- H. The zeroed pages cost almost no host memory as long as the host stays in the High state.

## Answers
A, D, E, G

## Explanation
- A: Granted counts VM pages that have an ESXi page mapped. OS initialization and memory zeroing touch most of the address space early, so Granted rises toward configured, its upper limit.
- B is wrong: Granted says which pages were ever touched, not what the guest needs. Need is read in the Guest OS once the application runs.
- C is wrong: a VM does not swap because its Granted is high; Granted cannot pass configured memory, and ESXi reclaims under host pressure or a limit, and there is neither.
- D: without pressure, the VMkernel does not reclaim touched pages.
- E: Active, the estimate of recently touched pages, is 1.9 GB of 61.3 GB granted: the pages were touched by the OS at boot and not since.
- F is wrong: swapped pages are not in Granted. Consumed is Granted minus what sharing saves, and that saving can be at most Shared (0.1 GB): the gap is sharing.
- G is true: VM Consumed is the VM's footprint on ESXi, the figure for migration and host capacity; it is not the guest's need.
- H is wrong: ESXi backs VM memory with 2 MB pages and does not share them; a zeroed 4 KB page inside a large page keeps its host memory until the host breaks large pages, from the Clear state. Here Consumed is close to Granted: the zeroed pages cost real memory.
- Misconception: B or C: Granted near configured read as a VM that is full. H: "Windows zeroes its memory, and zero pages are shared, so they cost nothing."

## Notes
- Sources: the knowledge base, VM Memory Granted (touched pages stay mapped; Granted excludes swapped pages; Consumed = Granted - sharing savings), VM Memory Zero Pages (Windows initializes pages with zeroes; zero pages inside 2 MB pages keep their RAM until Clear) and VM Memory Consumed (the VM's footprint on ESXi).
- Changed in the 2026-11-15 audit: Shared lowered from 1.2 to 0.1 GB and Consumed raised from 60.1 to 61.2 GB (with 2 MB backing and a host in High, an hour-old VM shares almost nothing); C keeps one claim; G (Consumed as the host-side figure) and H (zero pages inside large pages) added.

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
source_path: "Synthetic, 2026-11-12"
misconception: [B, C, H]
misconception_type: [consumption-as-contention]
status: draft
```
