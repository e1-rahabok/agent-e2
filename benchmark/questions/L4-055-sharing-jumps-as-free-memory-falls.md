# Page sharing jumps as free memory falls

## Prompt
- ESXi 9.1 host with 768 GB of memory, no memory tiering, default settings. It runs about 40 Windows and Linux server VMs.
- For weeks: Consumed about 700 GB; Shared about 2 GB; Shared common about 1 GB. Balloon, Compressed and Swapped all 0.
- Yesterday five large VMs were added. Since then Consumed is about 755 GB.
- Over the next two hours, Shared rose to 64 GB and Shared common to 22 GB, and Consumed fell back to about 713 GB. Balloon, Compressed and Swapped are still 0.
- No VM changed its software or contents.

Why did page sharing jump now and not before, how much memory does it save, and what does the jump tell you about the host? Which statements are correct?

- A. Sharing stayed small for weeks because the VMs' memory was backed by 2 MB pages, which ESXi does not share.
- B. With about 13 GB free, the host entered the Clear state, where ESXi breaks large pages into 4 KB pages.
- C. Page sharing saves about 42 GB: Shared minus Shared common.
- D. Page sharing saves the full 64 GB shown in Shared.
- E. Page sharing saves the 22 GB shown in Shared common.
- F. The new VMs share pages with the older VMs that run the same OS.
- G. Page sharing on this host needs Mem.ShareForceSalting set to 0 before it saves anything.
- H. Page sharing and ballooning start together, in the Soft state.
- I. With Balloon, Compressed and Swapped at 0, the jump in sharing says nothing about the state of the host.
- J. If free memory keeps falling, ballooning is the next way ESXi reclaims memory.
- K. Ballooning starts once about 90% of host memory is in use.
- L. The host returns to the High state as soon as free memory climbs back above 300% of minFree.
- M. The broken large pages cost the VMs part of the TLB benefit of 2 MB pages.
- N. Turning off 2 MB backing on the hosts, so that sharing saves memory before any pressure, is the better setting.
- O. Now that about 55 GB is free again, ESXi backs newly touched memory with 2 MB pages again.

## Likely wrong answer
- F: "The new VMs run the same OS as the old ones, so they share pages with them."
- D: "64 GB is saved."
- I: "Nothing to worry about while Balloon and Swapped are 0."

## Expected key points
- Answer: A, B, C, J, M, O.
- A true: ESXi backs guest memory with 2 MB pages whenever it can and does not share them; sharing waits until large pages are broken.
- B true: minFree for 768 GB is about 0.9 GB for the first 28 GB plus 1% of the rest, about 8.3 GB; 300% is about 25 GB, and 768 - 755 leaves about 13 GB. In Clear, ESXi stops backing new memory with large pages and breaks existing ones.
- C true: Shared counts the pages that point to a shared page, Shared common the shared pages themselves; 64 - 22 = 42 GB, and Consumed fell by the same 755 - 713 = 42 GB.
- D false: Shared is not the saving; the saving is Shared minus Shared common.
- E false: Shared common is the memory the shared pages still take, not the memory saved.
- F false: by default the salt is unique per VM, so pages are shared only within each VM, not between VMs.
- G false: sharing within a VM is active by default; the host option only extends it between VMs.
- H false: large pages are broken, and sharing starts, in Clear, far above the balloon point.
- I false: Clear is not idle: the jump shows free memory fell far enough for ESXi to start working for memory. Plan now (move VMs or add capacity).
- J true: after Clear, Soft (ballooning) comes next, then Hard (compression and swap). The jump is an early warning.
- K false: ballooning starts only after about 99% of host memory is used (Soft, at 64% of minFree).
- L false: the host leaves Clear for High only above 400% of minFree (hysteresis).
- M true: large pages reduce TLB misses; breaking them loses part of that benefit.
- N false: large pages significantly reduce TLB misses and help most workloads; a host that keeps 400% of minFree free keeps the 2 MB backing and its performance. Turning it off trades that for a saving sharing gives anyway once the host is under pressure. This is the wrong action.
- O true: with Consumed back at about 713 GB, about 55 GB of the 768 GB is free, above 400% of minFree (about 33 GB), so the host has left Clear for High, where new memory is backed by 2 MB pages again.

## Notes
- Clear entered below 300% of minFree, back to High only above 400%; large pages broken in Clear: the knowledge base, ESXi memory states. Large pages not shared, and sharing that appears only when overcommitment breaks them: Performance Best Practices for vSphere 9.1, Memory Page Sharing and Large Memory Pages. Saving = Shared - Shared common: the knowledge base, ESXi Memory Shared and Shared Common.
- minFree for 768 GB: about 0.9 GB for the first 28 GB plus 1% of the rest, about 8.3 GB (the knowledge base, ESXi memory states, minFree line).
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): one fact per option; J stated positively instead of negating I; N the wrong action added. Options G, H and K now hold facts that 0145 and 0144 no longer repeat.
- Changed in the 2026-11-15 audit: G and H reworded without absolutes; O added (back to High above 400% of minFree, from the stem's numbers).

## Metadata
```yaml
id: "0146"
title: "Page sharing jumps as free memory falls"
product: [vsphere]
technology: [memory]
task: explain-mechanism
level: 400
answer_type: deterministic
answer: [A,B,C,J,M,O]
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
source_path: "Synthetic, 2026-11-12"
misconception_type: [unit-and-normalization]
status: draft
```
