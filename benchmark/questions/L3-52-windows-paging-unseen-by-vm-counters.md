# Windows paging and the VM memory counters

## Prompt
- A Windows Server VM with 12 GB pages heavily to its page file during a nightly batch job.
- The ESXi host has free memory, and the VM has no memory limit.

Which statements about what the VM memory counters show in this case are correct?

- A. Page file reads and writes reach ESXi only as ordinary IO on the VM's virtual disk.
- B. VM Memory Latency counts the time Windows waits for pages from its page file.
- C. VM Swapped shows how much of the guest's memory sits in the Windows page file.
- D. The VM can show 0 balloon, 0 swap and 0% Memory Latency while Windows pages heavily.
- E. ESXi gives a paging guest extra memory from the host's free memory.
- F. VM memory counters add nothing when Windows is short of memory, since they cannot see its paging.
- G. Paging in both directions at once, while the disk queue is high, points to a memory shortage inside Windows.
- H. Set a full memory reservation on the VM, so that Windows stops paging to its page file.

## Likely wrong answer
B: "Memory Latency is 0%, so Windows is not paging." Or C: the guest page file taken for the VM swap file.

## Expected key points
- Answer: A, D, G.
- A true: the page file sits on a partition of a virtual disk; ESXi sees the guest's reads and writes, not what they are for. The Guest OS page file is an ESXi blind spot.
- B false: VM Memory Latency is the share of time a vCPU waits for a page fault that ESXi resolves (swap-in, decompression). Windows paging to its own page file is not in it.
- C false: VM Swapped is memory ESXi swapped to the VM's swap file; the guest page file is invisible to ESXi.
- D true: with free host memory and no limit, ESXi reclaims nothing and the VM does not wait on ESXi, while Windows pages inside its own memory.
- E false: the Guest OS cannot see host memory; Windows runs its configured memory as if on a physical server.
- F false: over-correction. The VM counters show what ESXi does (reclamation, and the VM's waits on ESXi), so they rule the host in or out.
- G true: high page-in and page-out with a high disk queue is the Windows sign of a memory performance problem; page-in alone also comes from binaries, mapped files and prefetch.
- H false: the wrong action. A reservation guarantees host memory behind the VM; it does not change the memory Windows sees, and the host already had memory free. The fix is more configured memory or less memory taken inside the guest.

## Notes
- Paired with 0265 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item B13.
- `knowledge_main` is guest-os-vs-vm-memory, not windows-memory as the plan proposed: the blind spot (guest page file) and the counter map (guest paging has no VM counter) that decide B, C and D are in that file.
- Written 2026-11-14 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after approval (design.md, section 6.2).

## Metadata
```yaml
id: "0383"
title: "Windows paging and the VM memory counters"
product: [windows, vsphere]
technology: [memory, storage]
task: explain-mechanism
level: 300
answer_type: deterministic
input: [text]
object: [guest-os, vm]
tool: [guest-os-tools, vcenter]
knowledge:
  - vsphere/technology/memory/concepts/guest-os-vs-vm-memory
  - guest-os/memory/windows-memory
  - vsphere/technology/memory/metrics/virtual-motherboard/latency
  - guest-os/system/troubleshooting/ms-windows-slow
  - vsphere/technology/storage/concepts/storage-layers
knowledge_main: vsphere/technology/memory/concepts/guest-os-vs-vm-memory
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item B13"
answer: [A, D, G]
misconception: [B, C]
misconception_type: [layer-confusion]
pair: "0265"
status: draft
```
