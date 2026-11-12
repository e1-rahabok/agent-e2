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

- A. Windows hit its commit limit (RAM plus page file, here about the RAM): re-enable the page file or add memory.
- B. 1.4 GB was available, so memory was not short: the errors are an application bug.
- C. ESXi was short of memory and refused the VM's requests, though vCenter shows no reclamation.
- D. Committed Bytes is RAM in use, so 15.6 GB committed means 15.6 GB of RAM is in use.
- E. Disabling the page file made Windows faster; the errors come from the application, not from that.

## Likely wrong answer
B: Available memory read as headroom for new allocations.

## Expected key points
- Answer: A.
- A is correct: committed virtual memory must be backed by RAM or the page file. The commit limit is RAM plus page file; with no page file it is about the RAM. At 98% committed, new allocations fail even with memory available. Microsoft advises keeping the page file and letting Windows manage its size.
- B is wrong: Available is physical memory free or in standby; it is not commit headroom.
- C is wrong: ESXi shows no reclamation and no latency, and the host has free memory; the limit is inside Windows.
- D is wrong: committed memory is guaranteed in RAM or on disk, not all in RAM. Committed Bytes can rise without In Use rising.
- E is wrong: without a page file Windows slows down and applications crash near the commit limit.

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
source_path: "Drafted by Claude 2026-11-12 for the Guest OS slots (project/plan.md, M2)"
answer: [A]
misconception: [B]
misconception_type: [consumption-as-contention, layer-confusion]
status: draft
```
