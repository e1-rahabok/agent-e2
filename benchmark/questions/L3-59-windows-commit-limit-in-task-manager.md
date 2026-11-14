# Windows out of memory with memory available in Task Manager

## Prompt
See [Task Manager, Memory](0393/task-manager-memory-committed-near-limit.png) and [the Virtual Memory dialog](0393/windows-virtual-memory-dialog.png).

- A Windows Server VM fails to start services at the weekly peak, and the application logs out-of-memory errors.
- The server team says memory is fine because Task Manager shows memory available. vCenter shows no ballooning, no swapping and 0% Memory Latency for the VM.

Which statements are correct?

- A. Committed memory has reached about the commit limit, so new allocations fail although memory is available.
- B. With no paging file, the commit limit is about the size of the VM's memory.
- C. The memory available in Task Manager shows room for new allocations, so the errors come from an application bug.
- D. Committed equals the memory that Windows has in use.
- E. A system-managed paging file raises the commit limit.
- F. Adding memory to the VM is the only fix for these errors.
- G. Set a memory reservation on the VM so that ESXi stops refusing its allocations.
- H. Windows runs faster with its paging file turned off.

## Input to supply
- Product: Windows Server 2022 (or 2019) VM with 8 GB or more.
- Setup: System Properties > Advanced > Performance > Virtual memory: clear "Automatically manage paging file size for all drives", select "No paging file" on every drive, reboot. Then commit memory without touching it, for example Sysinternals Testlimit `-m` (leaky, committed only), until Committed reaches 95% of the limit.
- Screen 1: Task Manager > Performance > Memory, with In use, Available, Committed (value and limit) and Cached visible. Save as `benchmark/questions/0393/task-manager-memory-committed-near-limit.png`.
- Screen 2: the Virtual Memory dialog showing "No paging file" for every drive and the total paging file size at 0. Save as `benchmark/questions/0393/windows-virtual-memory-dialog.png`.
- Condition the key depends on:
  - Committed at 95% or more of the commit limit;
  - the commit limit within 5% of the VM's configured memory;
  - Available at 1 GB or more;
  - In use at least 1 GB below Committed.
- Masking: mask every VM, host, datastore and cluster name (and the computer name if a dialog shows it).

## Likely wrong answer
C: "Over a gigabyte is available, so memory is not the problem."

## Expected key points
- Answer: A, B, E.
- A true: every committed byte must be backed by RAM or the paging file. At the commit limit a new allocation fails, whatever Available shows.
- B true: the commit limit is RAM plus the current paging file size; with no paging file it is about the RAM.
- C false: Available is physical memory free or on standby, not commit headroom.
- D false: committed memory is guaranteed in RAM or on disk, not all in RAM; Committed can rise without In use rising, as the screen shows.
- E true: the commit limit includes the paging file, and Windows grows a system-managed file when the commit charge passes 90% of the limit. Microsoft advises keeping the paging file and letting Windows manage its size.
- F false: over-correction. More memory also raises the limit, but re-enabling the paging file raises it without a change to the VM.
- G false: the wrong action. ESXi refuses nothing: vCenter shows no reclamation and no latency, and a reservation does not change the memory Windows sees. The limit is inside Windows.
- H false: with the paging file disabled, Windows slows and applications crash near the commit limit, even with memory free.

## Notes
- Paired with 0270 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item C31.
- The key holds whenever the condition of `## Input to supply` holds.
- Written 2026-11-14 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after approval (design.md, section 6.2).

## Metadata
```yaml
id: "0393"
title: "Windows out of memory with memory available in Task Manager"
product: [windows, vsphere]
technology: [memory]
task: troubleshoot
level: 300
answer_type: deterministic
input: [screenshot]
object: [guest-os, vm]
tool: [guest-os-tools, vcenter]
knowledge:
  - guest-os/memory/windows-memory
  - vsphere/technology/memory/concepts/guest-os-vs-vm-memory
knowledge_main: guest-os/memory/windows-memory
attachments:
  - 0393/task-manager-memory-committed-near-limit.png
  - 0393/windows-virtual-memory-dialog.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C31"
answer: [A, B, E]
misconception: [C]
misconception_type: [consumption-as-contention, layer-confusion]
pair: "0270"
status: awaiting-input
```
