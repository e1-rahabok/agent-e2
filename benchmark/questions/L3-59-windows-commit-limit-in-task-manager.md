# Windows build agent out of memory with memory available

## Prompt
See [Task Manager, Memory](0393/task-manager-memory-committed-near-limit.png) and [the Virtual Memory dialog](0393/windows-virtual-memory-dialog.png).

- A Windows Server VM runs a build agent. Since a template change, nightly builds fail: the compiler stops with "out of virtual memory".
- The build engineer rules out memory, because Task Manager shows memory available while the builds fail.

Which statements are correct?

- A. Committed is within 5% of its limit on the Task Manager screen.
- B. In use and Committed show the same amount on the screen.
- C. The Virtual Memory dialog shows that no drive holds a paging file.
- D. Here the limit shown next to Committed is about the VM's memory alone.
- E. Memory shown as available can be given to any new allocation, so the compiler fails for another reason.
- F. Available memory says nothing about Windows memory health; only commit counts.
- G. Turn the system-managed paging file back on, so that the commit limit grows.
- H. Set a memory reservation on the VM in vCenter, so that Windows gets more room to commit.

## Input to supply
- Product: Windows Server 2022 (or 2019) VM with 8 GB or more.
- Setup: System Properties > Advanced > Performance > Virtual memory: clear "Automatically manage paging file size for all drives", select "No paging file" on every drive, reboot. Then commit memory without touching it, for example Sysinternals Testlimit `-m` (committed, not touched), until Committed reaches 95% of the limit.
- Screen 1: Task Manager > Performance > Memory, with In use, Available, Committed (value and limit) and Cached visible. Save as `benchmark/questions/0393/task-manager-memory-committed-near-limit.png`.
- Screen 2: the Virtual Memory dialog showing "No paging file" for every drive and the total paging file size at 0. Save as `benchmark/questions/0393/windows-virtual-memory-dialog.png`.
- Condition the key depends on:
  - Committed at 95% or more of the commit limit;
  - the commit limit within 5% of the VM's configured memory;
  - Available at 1 GB or more;
  - In use at least 1 GB below Committed.
- Masking: mask every VM, host, datastore and cluster name (and the computer name if a dialog shows it).

## Likely wrong answer
E: "Task Manager shows memory available, so memory is not why the builds fail."

## Expected key points
- Answer: A, C, D, G.
- A true: the Committed value sits at 95% or more of the limit next to it. Every committed byte must be backed by RAM or the paging file, so a new allocation fails at the limit.
- B false: In use is at least 1 GB below Committed: committed memory need not be in RAM.
- C true: the dialog shows "No paging file" on every drive.
- D true: the commit limit is RAM plus the current paging file; with no paging file it is about the RAM.
- E false: Available is physical memory free or on standby, not commit headroom.
- F false: over-correction. Available is the memory Windows can use at once without saving a page first, so it shows the room left in RAM; it is only not commit headroom.
- G true: the commit limit includes the paging file, and Windows grows a system-managed file when the commit charge passes 90% of the limit. Microsoft advises keeping the paging file and letting Windows manage its size.
- H false: the wrong action. A reservation guarantees host memory behind the VM; it does not change the memory or the commit limit Windows sees. The limit is inside Windows.

## Notes
- Paired with 0270 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item C31.
- Review fixes 2026-11-15: new situation (build agent; 0270 is services failing at a weekly peak after a hardening script); the vCenter values left the stem (no screen showed them); options reworded away from 0270; screen readings added (A, C true; B false). Key A, B, E → A, C, D, G.
- The key holds whenever the condition of `## Input to supply` holds.
- Written 2026-11-14 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after approval (design.md, section 6.2).

## Metadata
```yaml
id: "0393"
title: "Windows build agent out of memory with memory available"
product: [windows]
technology: [memory]
task: troubleshoot
level: 300
answer_type: deterministic
input: [screenshot]
object: [guest-os]
tool: [guest-os-tools]
knowledge:
  - guest-os/memory/windows-memory
  - vsphere/technology/memory/concepts/guest-os-vs-vm-memory
knowledge_main: guest-os/memory/windows-memory
attachments:
  - 0393/task-manager-memory-committed-near-limit.png
  - 0393/windows-virtual-memory-dialog.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C31"
answer: [A, C, D, G]
misconception: [E]
misconception_type: [consumption-as-contention, layer-confusion]
pair: "0270"
status: awaiting-input
```
