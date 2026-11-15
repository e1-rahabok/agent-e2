# SQL Server holds its memory

## Prompt
- A SQL Server 2022 VM: Windows Server 2022, 8 vCPUs, 64 GB.
- `max server memory` is at its default (2,147,483,647 MB).
- Windows: memory In Use 61 GB (95%), Available 1.6 GB. sqlservr.exe working set 57 GB.
- vCenter, last 30 days: VM Consumed 64 GB, flat. VM Active 5-9 GB, peak 12 GB.
- The capacity team wants to cut the VM to 16 GB, based on Active. The DBA says SQL Server needs all 64 GB, because Windows shows 95% in use.

Which statements are correct?

- A. VM Active never passed 12 GB in 30 days, so 16 GB is enough and the VM can be cut to 16 GB now.
- B. Windows shows 95% in use, so SQL Server needs all of its 64 GB, and possibly more memory on top.
- C. SQL Server grows its buffer pool into the memory it is allowed and keeps it, and Windows counts all of it as in use.
- D. VM Active samples recently touched pages and cannot see how SQL Server uses its cache, so it cannot set the size.
- E. With `max server memory` at its default, SQL Server can take nearly all of the VM's memory and leave Windows little.
- F. The first change is `max server memory`: total memory minus what Windows and the other processes on the VM need.
- G. Find the size by lowering `max server memory` in steps over a business cycle, watching SQL Server counters, then resize.
- H. Cutting the VM to 16 GB in one step removes most of the database cache: more disk reads and slower queries.
- I. `max server memory` caps all of SQL Server's memory use, its thread stacks and backup buffers included.
- J. VM Consumed flat at 64 GB for 30 days shows SQL Server actively works with all 64 GB of its memory.
- K. With Lock pages in memory granted, the default `max server memory` is safe, as SQL Server gives memory back on demand.

## Likely wrong answer
- A: "Active never passed 12 GB, so 16 GB is enough: cut it now."
- B: "Windows shows 95% in use, so the VM needs more memory."

## Expected key points
- Answer: C, D, E, F, G, H.
- A false: VM Active does not see how SQL Server uses its cache; the cut removes the cache.
- B false: SQL Server grew into what `max server memory` allows, and the default allows nearly all. The setting decides the value, not the need.
- C true: SQL Server claims memory for its buffer pool up to `max server memory` and keeps it; In Use and the working set show what the buffer pool grew into.
- D true: Active is a sampled estimate for the kernel, a VM counter that cannot see the guest's cache use.
- E true: the default (2,147,483,647 MB) is no limit; Windows Available is 1.6 GB.
- F true: set `max server memory` first, leaving room for Windows, the other processes and allocations outside the buffer pool.
- G true: shrink in steps and prove each step before resizing the VM.
- H true: a cut to the Active value removes the cache SQL Server works from.
- I false: `max server memory` limits only the buffer pool; thread stacks, backup buffers, extended stored procedure DLLs and linked server providers sit outside it.
- J false: Consumed holds every page the VM has touched, even when idle; it is not demand.
- K false: with Lock pages in memory granted, Microsoft strongly recommends a set `max server memory`: without it, SQL Server can starve the rest of the system.

## Notes
- Microsoft, Server memory configuration options: subtract the memory the OS, allocations outside `max server memory`, and other applications need from total physical memory; the default `max server memory` is 2,147,483,647 MB. https://learn.microsoft.com/sql/database-engine/configure-windows/server-memory-server-configuration-options
- Option G follows guest-os-sizing; its step-down method is not on the Microsoft page and has an open review note there (field experience to confirm).
- Converted from judged to multiple choice (Q199 F, 2026-11-14).

## Metadata
```yaml
id: "0269"
title: "SQL Server holds its memory"
product: [windows, vsphere]
technology: [memory]
task: judge-setting
level: 400
answer_type: deterministic
answer: [C, D, E, F, G, H]
misconception: [A, B]
input: [text]
object: [guest-os, vm]
tool: [guest-os-tools, vcenter]
knowledge:
  - vsphere/technology/memory/concepts/guest-os-vs-vm-memory
  - vsphere/technology/memory/concepts/memory-layers
  - guest-os/system/concepts/guest-os-sizing
  - guest-os/system/concepts/guest-os-configuration-review
  - vsphere/technology/memory/metrics/virtual-motherboard/active
  - vsphere/architecture/resource-controls
knowledge_main: vsphere/technology/memory/concepts/guest-os-vs-vm-memory
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
misconception_type: [consumption-as-contention, layer-confusion]
status: draft                     # reviewed as a free-text question; converted to multiple choice 2026-11-14 (Q199): review again
```
