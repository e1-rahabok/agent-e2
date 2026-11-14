# Page sharing jumps as free memory falls

## Prompt
- ESXi 9.1 host with 768 GB of memory, no memory tiering, default settings. It runs about 40 Windows and Linux server VMs.
- For weeks: Consumed about 700 GB; Shared about 2 GB; Shared common about 1 GB. Balloon, Compressed and Swapped all 0.
- Yesterday five large VMs were added. Since then Consumed is about 755 GB.
- Over the next two hours, Shared rose to 64 GB and Shared common to 22 GB, and Consumed fell back to about 713 GB. Balloon, Compressed and Swapped are still 0.
- No VM changed its software or contents.

Why did page sharing jump now and not before? How much memory does it save, and what does the jump tell you about the host?

## Likely wrong answer
"The new VMs run the same OS as the old ones, so they share pages with them: 64 GB is saved. Nothing to worry about while Balloon and Swapped are 0."

## Expected key points
- ESXi backs VM memory with 2 MB large pages whenever it can, and it does not share large pages. That is why sharing stayed tiny for weeks.
- Free memory fell below 300% of minFree (about 25 GB here, with minFree about 8 GB): the host left the high state for the clear state. In clear, ESXi stops backing new memory with large pages and breaks existing ones, so page sharing can collapse identical 4 KB pages. By default only pages within each VM are shared (salting).
- The saving is Shared minus Shared common: about 42 GB, which matches Consumed falling from about 755 to 713 GB. Shared counts the pages that point to a shared page; Shared common counts the shared pages themselves.
- The jump is a leading signal: free memory fell far enough for ESXi to start working for memory. The next steps down are ballooning (soft state), then compression and swap. Plan now (move VMs or add capacity) rather than wait for them.
- Broken large pages cost the VMs some TLB efficiency.

## Notes
- Clear entered below 300% of minFree, back to high only above 400%; large pages broken in clear: author answer Q188 (ESXi 9.1 memory reclamation manual, project/sources) and the knowledge base, ESXi memory states. Large pages not shared, and sharing that appears only when overcommitment breaks them: Performance Best Practices for vSphere 9.1, Memory Page Sharing and Large Memory Pages. Saving = Shared - Shared common: the knowledge base, ESXi Memory Shared and Shared Common.
- minFree for 768 GB: about 899 MB for the first 28 GB plus 1% of the rest, about 8.3 GB (Frank Denneman, Mem.MinFreePct sliding scale).

## Metadata
```yaml
id: "0146"
title: "Page sharing jumps as free memory falls"
product: [vsphere]
technology: [memory]
task: explain-mechanism
level: 400
answer_type: judged
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
