# Swapped is not Swap out minus Swap in

## Prompt
- A 32 GB VM, vSphere Client advanced memory chart, last hour:
  - Swapped: 6.0 GB, flat (maximum and minimum differ by less than 10 MB).
  - Swap out rate: about 2,000 KBps on average.
  - Swap in rate: about 2,000 KBps on average.
- The VM arrived on this host by vMotion three days ago.
- A colleague says: "Swapped is flat, so nothing moves in or out of the swap file. And Swapped must equal everything this host swapped out minus everything it swapped back in."

Which statements are correct?

- A. Nothing moves to or from the swap file this hour: if pages moved, the Swapped total would change.
- B. Pages move both ways: the guest reads some swapped pages back while ESXi writes others out.
- C. Swapped equals the total swapped out minus the total swapped in by this host since the VM started on it.
- D. A VM that arrives by vMotion can bring swapped pages, so Swapped can exceed what this host swapped out.
- E. The 6 GB in the swap file is the guest's working set, since ESXi swaps the pages the guest uses most.

## Likely wrong answer
A: a flat Swapped read as no swap activity. Or C: Swapped read as the running difference of out and in.

## Expected key points
- Answer: B, D.
- A is wrong: swap out and swap in run in parallel on different pages. The swap file can keep its size while its content changes.
- B: about 2,000 KBps each way moves about 7 GB out and 7 GB back in this hour, with no change in the total.
- C is wrong: in and out are not one stream on one set of pages, and pages can arrive already swapped.
- D: Swapped is what sits in the swap file now, wherever it came from.
- E is wrong: ESXi picks pages to swap without knowing what the guest uses; swapped pages are often pages the guest has not touched for a while. Active is a sampled estimate of recently touched pages.

## Notes
- vMotion and Swapped: the knowledge base, VM Memory Swapped, section Behaviour.

## Metadata
```yaml
id: "0143"
title: "Swapped is not Swap out minus Swap in"
product: [vsphere]
technology: [memory]
task: read-metric
level: 300
answer_type: deterministic
input: [text]
object: [vm]
tool: [vcenter]
knowledge:
  - vsphere/technology/memory/metrics/virtual-motherboard/swapped
  - vsphere/technology/memory/concepts/swap-and-compression
  - vsphere/technology/memory/metrics/virtual-motherboard/swap-out-rate
knowledge_main: vsphere/technology/memory/metrics/virtual-motherboard/swapped
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
answer: [B, D]
misconception: [A, C]
misconception_type: [cumulative-vs-current]
status: draft
```
