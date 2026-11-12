# SQL Server holds its memory

## Prompt
- A SQL Server 2022 VM: Windows Server 2022, 8 vCPUs, 64 GB.
- `max server memory` is at its default (2,147,483,647 MB).
- Windows: memory In Use 61 GB (95%), Available 1.6 GB. sqlservr.exe working set 57 GB.
- vCenter, last 30 days: VM Consumed 64 GB, flat. VM Active 5-9 GB, peak 12 GB.
- The capacity team wants to cut the VM to 16 GB, based on Active. The DBA says SQL Server needs all 64 GB, because Windows shows 95% in use.

Who is right? What do you advise, and which setting do you change first?

## Likely wrong answer
"Active never passed 12 GB, so 16 GB is enough: cut it now." Or: "Windows shows 95% in use, so the VM needs more memory."

## Expected key points
- Neither number shows what SQL Server needs.
- SQL Server manages its own memory: its buffer pool grows into the RAM it is allowed and keeps it as cache. Windows counts all of it as in use.
- VM Active is a VM counter: a sample of recently touched pages. It does not see how SQL Server uses its cache, so it is no basis for the size.
- With `max server memory` at its default, SQL Server can take almost all RAM and leave Windows little (Available 1.6 GB). Set `max server memory` first: total memory minus what Windows and the other processes on the VM need.
- To find the right size, shrink in steps: lower `max server memory`, then watch SQL Server's own memory counters and the query times over a full business cycle; resize the VM only after that.
- Cutting to 16 GB in one step removes most of the database cache: more disk reads and slower queries.

## Notes
- Microsoft, Server memory configuration options: subtract the memory the OS, allocations outside `max server memory`, and other applications need from total physical memory; the default `max server memory` is 2,147,483,647 MB. https://learn.microsoft.com/sql/database-engine/configure-windows/server-memory-server-configuration-options

## Metadata
```yaml
id: "0269"
title: "SQL Server holds its memory"
product: [windows, vsphere]
technology: [memory]
task: judge-setting
level: 400
answer_type: judged
input: [text]
object: [guest-os, vm]
tool: [guest-os-tools, vcenter]
knowledge:
  - vsphere/technology/memory/concepts/guest-os-vs-vm-memory
  - vsphere/technology/memory/concepts/memory-layers
  - guest-os/system/concepts/guest-os-sizing
  - guest-os/system/concepts/guest-os-configuration-review
  - vsphere/technology/memory/metrics/virtual-motherboard/active
knowledge_main: vsphere/technology/memory/concepts/guest-os-vs-vm-memory
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12 for the Guest OS slots (project/plan.md, M2)"
misconception_type: [consumption-as-contention, layer-confusion]
status: draft
```
