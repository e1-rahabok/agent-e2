# Out-of-memory errors with memory available

## Prompt
- A Windows Server 2022 VM with 16 GB. A hardening script disabled the page file last month to save disk space.
- At the weekly peak, services fail to start and the application logs "out of memory" errors.
- Performance Monitor at the failure:
  - Memory \ Available MBytes: about 1,400.
  - Memory \ Committed Bytes: 15.6 GB. Memory \ Commit Limit: 15.9 GB.
  - Memory \ % Committed Bytes In Use: 98%.
- vCenter: no ballooning, no swapping, Memory Latency 0%. The host has free memory.

Which statements are correct?

- A. Windows refused new allocations because Committed Bytes reached the Commit Limit.
- B. With about 1,400 MB available, memory was not short: the errors are an application bug.
- C. ESXi was short of memory and refused the VM's requests, though vCenter shows no reclamation.
- D. 15.6 GB committed means 15.6 GB of RAM is in use.
- E. Without a page file Windows runs faster, with no side effect on its applications.
- F. Adding RAM to the VM is the only way to stop the errors.
- G. With no page file, the Commit Limit is about the size of the RAM.
- H. Re-enabling the page file raises the Commit Limit.

## Likely wrong answer
B: Available memory read as headroom for new allocations.

## Expected key points
- Answer: A, G, H.
- A is true: committed virtual memory must be backed by RAM or the page file. At 98% committed, new allocations fail even with memory available.
- B is wrong: Available is physical memory free or in standby; it is not commit headroom.
- C is wrong: ESXi shows no reclamation and no latency, and the host has free memory; the limit is inside Windows.
- D is wrong: committed memory is guaranteed in RAM or on disk, not all in RAM. Committed Bytes can rise without In Use rising.
- E is wrong: Microsoft advises not disabling the page file; with it disabled, Windows slowed and applications crashed despite over 1 GB free.
- F is wrong: re-enabling the page file also raises the limit, and Microsoft advises keeping it and letting Windows manage its size. This is the over-correction of B.
- G is true: Commit Limit = RAM + the current page file size; with no page file it is about the RAM (15.9 GB here).
- H is true: the page file adds to the Commit Limit; a system-managed page file also grows when the commit charge passes 90% of the limit.

## Notes
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): old A ("Windows hit its commit limit (RAM plus page file, here about the RAM): re-enable the page file or add memory") split into A, G and H; E one fact; F the over-correction added. Key changed from A to A, G, H.

## Metadata
```yaml
id: "0270"
title: "Out-of-memory errors with memory available"
product: [windows, vsphere]
technology: [memory]
task: troubleshoot
level: 300
answer_type: deterministic
input: [text]
object: [guest-os, vm]
tool: [guest-os-tools, vcenter]
knowledge:
  - guest-os/memory/windows-memory
  - vsphere/technology/memory/concepts/guest-os-vs-vm-memory
knowledge_main: guest-os/memory/windows-memory
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
answer: [A, G, H]
misconception: [B]
misconception_type: [consumption-as-contention, layer-confusion]
pair: "0393"
status: draft
```
