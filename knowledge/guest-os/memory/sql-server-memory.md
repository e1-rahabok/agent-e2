# SQL Server memory in a VM

## Memory held by SQL Server
- SQL Server takes memory for its buffer pool up to `max server memory (MB)` and keeps it, so Windows counts that memory as In Use and the sqlservr.exe working set stays near the limit, whatever the query load.
- The default of `max server memory (MB)` is 2,147,483,647 MB, which is no limit. SQL Server then takes nearly all the memory of the VM and leaves Windows little, so Windows Available is low. Microsoft recommends an upper limit in every version.
- `max server memory (MB)` limits only the buffer pool. Thread stacks, backup buffers, extended stored procedure DLLs and linked server provider allocations sit outside it, so the limit has to leave room for them, for Windows and for the other processes of the VM.
- Microsoft's starting value for one instance: total memory of the OS, minus the thread stack memory (stack size times the calculated max worker threads), minus an allowance for the allocations outside the limit. Microsoft calls the allowance a generic approximation.
- Windows In Use, the sqlservr.exe working set and VM Active do not show the memory SQL Server needs. In Use and the working set show what the buffer pool grew into. VM Active is a sample of recently touched pages and does not see how SQL Server uses its cache.
- A cut of the VM memory to the VM Active value removes the cache SQL Server works from: more reads from disk and slower queries. The first change is `max server memory (MB)`, set from the total memory minus what Windows and the other processes need.
- Finding the size: lower `max server memory (MB)` in steps, each held over a full business cycle while the SQL Server memory counters and the query times are read, and resize the VM after the last step that held (section Lowering max server memory in steps).
- In a VM, `min server memory (MB)` keeps memory pressure from the host (ballooning) from taking buffer pool memory below what the workload needs. Once SQL Server has used that much, it does not release memory below the value.
- With the Windows user right Lock pages in memory granted, Microsoft strongly recommends a set `max server memory (MB)`: without it, SQL Server can starve the rest of the system.
- SQL Server on Linux sets its memory limit with mssql-conf, setting `memory.memorylimitmb` (Microsoft, Monitor memory usage).

## Lowering max server memory in steps
- Why steps: the memory SQL Server holds shows what the limit allows, not what the workload needs. Only a lower limit, held over the workload's own cycle, shows whether the cached data was needed.
- `max server memory (MB)` takes effect at RECONFIGURE, with no restart of SQL Server (Microsoft, Server memory configuration options). A step and its undo are both immediate.
- Baseline: before the first step, record the counters below over one full business cycle at the current value. Compare each later period with the same period of the baseline (month-end with month-end), because the counters move with the load.
- Buffer Manager: Page reads/sec: physical database page reads across all databases. A rise after a step means pages that stayed in cache before now come from disk; this is the first counter to read.
- Buffer Manager: Lazy writes/sec: buffers the lazy writer flushes to make them free. A rise means the smaller buffer pool frees buffers to take in new pages.
- Buffer Manager: Free list stalls/sec: requests that waited for a free page. A rise means the pool runs out of free buffers.
- Memory Manager: Memory Grants Pending: processes waiting for workspace memory (sort, hash, index build). A rise means queries wait for memory before they run.
- Buffer Manager: Page life expectancy: seconds a page stays in the buffer pool without references. It falls with every step, because a smaller pool keeps each page for less time, so a lower level alone is expected. Sudden dips that the baseline did not have show churn: the workload no longer benefits from data already in memory (Microsoft, Monitor memory usage). On a VM with more than one vNUMA node, read Buffer Node: Page life expectancy per node.
- Query times of the application: the final test. The counters explain a change; the query times decide it.
- Buffer cache hit ratio is not a step signal: Microsoft states that after a long period of time the ratio moves very little, so a step that raises Page reads/sec can leave it nearly unchanged.
- Windows Memory: Available Bytes rises by about the size of each step: that memory is what the VM can give back.
- Step rule: a step holds when, over the full business cycle, Page reads/sec, Lazy writes/sec, Free list stalls/sec and Memory Grants Pending stay at their baseline in the same period, Page life expectancy shows no sudden dips the baseline did not have, and the query times do not lengthen.
- Step rule: a step that fails any of these is undone at once, without waiting for the end of the cycle. The size is the last value that held; a value between that one and the undone one can be tried in a further cycle.
- Step size: a choice of method, not a threshold; no Microsoft document gives one. Larger steps take fewer cycles and overshoot further; smaller steps land closer and take more cycles.
- First step: it can remove at least the low point of Memory Manager: Free Memory (KB) over the baseline cycle. That memory is committed to SQL Server and was unused at every sample of the cycle.
- Keep `min server memory (MB)` well below the value under test: Microsoft does not recommend setting min and max to the same or nearly the same value.
- Resizing the VM after the last step: the new `max server memory (MB)`, plus SQL Server memory outside it (thread stacks and the other allocations), plus Windows and the other processes. Then the memory rules of [`guest-os/system/guest-os-sizing`](../system/guest-os-sizing.md) apply: Needed Memory, read with SQL Server at its new limit, in the green band.

## Misconceptions
- "Windows shows 95% in use, so the VM needs more memory" → SQL Server grew into the memory its `max server memory (MB)` allows, and the default allows nearly all. The setting decides the value, not the need.
- "VM Active is below 12 GB, so cut the VM to 16 GB" → VM Active does not see how SQL Server uses its cache. The cut removes the cache. Set `max server memory (MB)` first and lower it in steps.

## Metadata
```yaml
id: guest-os/memory/sql-server-memory
retriever_guide: how-it-works
scope: guest-os
technology:
- memory
pillar:
- capacity
- performance
product:
- windows
- linux
layer:
- guest-os
internal_derive:
- vsphere/technology/memory/concepts/guest-os-vs-vm-memory
- guest-os/system/guest-os-sizing
related:
- guest-os/memory/windows-memory
- vsphere/technology/memory/metrics/virtual-motherboard/active
source:
  document: 'Knowledge base; Microsoft Learn, SQL Server documentation (fetched 2026-11-15): Server memory configuration options, Monitor memory usage, SQL Server Buffer Manager object, SQL Server Memory Manager object'
  path: 'Consumer Objects > Capacity: Guest OS > Guest OS Sizing (section Applications that manage their own memory)'
corrections: []
review_notes: []
status: draft
```
