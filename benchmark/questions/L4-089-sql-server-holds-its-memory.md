# SQL Server holds its memory

## Prompt
- A SQL Server 2022 VM: Windows Server 2022, 12 vCPUs, 96 GB.
- `max server memory` is at its default (2,147,483,647 MB).
- Windows: memory In Use 90 GB (94%), Available 3.1 GB. sqlservr.exe working set 85 GB.
- vCenter, last 30 days: VM Consumed 96 GB, flat. VM Active 7-13 GB, peak 17 GB.
- The capacity team wants to cut the VM to 24 GB, based on Active. The DBA says SQL Server needs all 96 GB, because Windows shows 94% in use.

Which statements are correct?

- A. Page life expectancy settling at a lower level after the first step shows that step failed and must be undone.
- B. Windows shows 94% in use, so SQL Server needs all of its 96 GB, and possibly more memory on top.
- C. SQL Server grows its buffer pool into the memory it is allowed and keeps it, and Windows counts all of it as in use.
- D. A change of `max server memory` takes effect at RECONFIGURE, without a restart, so a failed step is undone at once.
- E. With `max server memory` at its default, SQL Server can take nearly all of the VM's memory and leave Windows little.
- F. The first change is `max server memory`: total memory minus what Windows and the other processes on the VM need.
- G. Find the size by lowering `max server memory` in steps over a business cycle, watching SQL Server counters, then resize.
- H. Cutting the VM to 24 GB in one step removes most of the database cache: more disk reads and slower queries.
- I. `max server memory` caps all of SQL Server's memory use, its thread stacks and backup buffers included.
- J. VM Consumed flat at 96 GB for 30 days shows SQL Server actively works with all 96 GB of its memory.
- K. With Lock pages in memory granted, the default `max server memory` is safe, as SQL Server gives memory back on demand.

## Likely wrong answer
- A: "Page life expectancy dropped after the first step, so the step failed: undo it."
- B: "Windows shows 94% in use, so the VM needs more memory."

## Expected key points
- Answer: C, D, E, F, G, H.
- A false: a smaller buffer pool keeps each page for less time, so Page life expectancy falls with every step and a lower level alone is expected; only sudden dips the baseline did not have show churn. The step is judged on Page reads/sec, Lazy writes/sec, Free list stalls/sec, Memory Grants Pending and the query times.
- B false: SQL Server grew into what `max server memory` allows, and the default allows nearly all. The setting decides the value, not the need.
- C true: SQL Server takes memory for its buffer pool up to `max server memory` and keeps it; In Use and the working set show what the buffer pool grew into.
- D true: `max server memory` takes effect at RECONFIGURE with no restart of SQL Server, so a step and its undo are both immediate.
- E true: the default (2,147,483,647 MB) is no limit; Windows Available is 3.1 GB.
- F true: set `max server memory` first, leaving room for Windows, the other processes and allocations outside the buffer pool.
- G true: each step is held over a full business cycle and compared with a baseline of the same period (Page reads/sec, Lazy writes/sec, Free list stalls/sec, Memory Grants Pending, query times); a failing step is undone at once, and the VM is resized after the last step that held.
- H true: VM Active, a sample of recently touched pages, does not see how SQL Server uses its cache; a cut to about the Active value removes the cache SQL Server works from.
- I false: `max server memory` limits only the buffer pool; thread stacks, backup buffers, extended stored procedure DLLs and linked server providers sit outside it.
- J false: Consumed holds every page the VM has touched, even when idle; it is not demand.
- K false: with Lock pages in memory granted, Microsoft strongly recommends a set `max server memory`: without it, SQL Server can starve the rest of the system.

## Notes
- Microsoft, Server memory configuration options: subtract the memory the OS, allocations outside `max server memory`, and other applications need from total physical memory; the default `max server memory` is 2,147,483,647 MB; the setting takes effect at RECONFIGURE. https://learn.microsoft.com/sql/database-engine/configure-windows/server-memory-server-configuration-options
- Microsoft, Monitor memory usage: Page life expectancy and its sudden dips; Buffer Manager and Memory Manager objects. https://learn.microsoft.com/sql/relational-databases/performance-monitor/monitor-memory-usage
- Changed in the 2026-11-15 audit: stem numbers moved off the knowledge base's misconception example; A (cut on Active, a fact homed in 0021/0079) replaced by the Page life expectancy misconception; D (Active cannot see the cache, same cluster) replaced by the RECONFIGURE fact; the Active fact stays in H's key point.

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
  - guest-os/system/guest-os-sizing
  - guest-os/memory/sql-server-memory
  - guest-os/system/guest-os-configuration-review
  - vsphere/technology/memory/metrics/virtual-motherboard/active
  - vsphere/architecture/resource-controls
knowledge_main: guest-os/memory/sql-server-memory
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-12"
misconception_type: [consumption-as-contention, layer-confusion]
status: draft                     # reviewed as a free-text question; converted to multiple choice 2026-11-14 (Q199): review again
```
