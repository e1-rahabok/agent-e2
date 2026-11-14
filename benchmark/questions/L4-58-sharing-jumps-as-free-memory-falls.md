# Page sharing jumps as free memory falls

## Prompt
- ESXi 9.1 host with 768 GB of memory, no memory tiering, default settings. It runs about 40 Windows and Linux server VMs.
- For weeks: Consumed about 700 GB; Shared about 2 GB; Shared common about 1 GB. Balloon, Compressed and Swapped all 0.
- Yesterday five large VMs were added. Since then Consumed is about 755 GB.
- Over the next two hours, Shared rose to 64 GB and Shared common to 22 GB, and Consumed fell back to about 713 GB. Balloon, Compressed and Swapped are still 0.
- No VM changed its software or contents.

Why did page sharing jump now and not before, how much memory does it save, and what does the jump tell you about the host? Which statements are correct?

- A. Sharing stayed tiny for weeks because ESXi backed VM memory with 2 MB pages, which it does not share.
- B. With about 13 GB free, below 300% of minimum free memory (about 25 GB), the host entered Clear and began breaking large pages.
- C. The saving is Shared minus Shared common, about 42 GB, which matches the fall of Consumed from about 755 to 713 GB.
- D. The saving is the full 64 GB shown in Shared, the memory that sharing gave back.
- E. The saving is the 22 GB shown in Shared common, the pages that sharing removed.
- F. The new VMs share pages with the older VMs that run the same OS, which made Shared jump.
- G. Page sharing on this host works only once Mem.ShareForceSalting is set to 0 on the host.
- H. Page sharing starts only in the Soft state, at the same time as ballooning inflates.
- I. With Balloon, Compressed and Swapped at 0, the jump in sharing says nothing about the state of the host.
- J. The jump is an early warning: as free memory keeps falling, ballooning comes next, then compression and swap.
- K. Ballooning starts at about 90% of host memory, so at about 98% Consumed it should already be active.
- L. The host returns to the High state as soon as free memory climbs back above 300% of its minimum free memory.
- M. The broken large pages cost the VMs some of the TLB efficiency that 2 MB pages gave them.

## Likely wrong answer
- F: "The new VMs run the same OS as the old ones, so they share pages with them."
- D: "64 GB is saved."
- I: "Nothing to worry about while Balloon and Swapped are 0."

## Expected key points
- Answer: A, B, C, J, M.
- A true: ESXi backs guest memory with 2 MB pages whenever it can and does not share them; sharing waits until large pages are broken.
- B true: minFree for 768 GB is about 0.9 GB for the first 28 GB plus 1% of the rest, about 8.3 GB; 300% is about 25 GB, and 768 - 755 leaves about 13 GB. In Clear, ESXi stops backing new memory with large pages and breaks existing ones.
- C true: Shared counts the pages that point to a shared page, Shared common the shared pages themselves; 64 - 22 = 42 GB, and 755 - 713 = 42 GB.
- D false: Shared is not the saving; the saving is Shared minus Shared common.
- E false: Shared common is the memory the shared pages still take, not the memory saved.
- F false: by default the salt is unique per VM, so pages are shared only within each VM, not between VMs.
- G false: sharing within a VM is active by default; the host option only extends it between VMs.
- H false: large pages are broken, and sharing starts, in Clear, far above the balloon point.
- I false: Clear is not idle: the jump shows free memory fell far enough for ESXi to start working for memory. Plan now (move VMs or add capacity).
- J true: Soft (ballooning) comes next, then Hard (compression and swap).
- K false: ballooning starts only after about 99% of host memory is used.
- L false: the host leaves Clear for High only above 400% of minFree (hysteresis).
- M true: large pages reduce TLB misses; breaking them loses part of that benefit.

## Notes
- Clear entered below 300% of minFree, back to high only above 400%; large pages broken in clear: author answer Q188 (ESXi 9.1 memory reclamation manual, project/sources) and the knowledge base, ESXi memory states. Large pages not shared, and sharing that appears only when overcommitment breaks them: Performance Best Practices for vSphere 9.1, Memory Page Sharing and Large Memory Pages. Saving = Shared - Shared common: the knowledge base, ESXi Memory Shared and Shared Common.
- minFree for 768 GB: about 899 MB for the first 28 GB plus 1% of the rest, about 8.3 GB (Frank Denneman, Mem.MinFreePct sliding scale).
- Converted from judged to multiple choice (Q199 F, 2026-11-14).

## Metadata
```yaml
id: "0146"
title: "Page sharing jumps as free memory falls"
product: [vsphere]
technology: [memory]
task: explain-mechanism
level: 400
answer_type: deterministic
answer: [A,B,C,J,M]
misconception: [D,F,I]
input: [text]
object: [esxi]
tool: [vcenter]
knowledge:
  - vsphere/technology/memory/concepts/large-memory-pages
  - vsphere/technology/memory/metrics/host/shared
  - vsphere/technology/memory/concepts/page-sharing
  - vsphere/technology/memory/concepts/host-memory-states
knowledge_main: vsphere/technology/memory/metrics/host/shared
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
misconception_type: [unit-and-normalization]
status: draft
```
