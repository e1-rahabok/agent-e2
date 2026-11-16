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
- B. ESXi can swap out some pages of a VM while the guest reads other swapped pages back.
- C. Swapped equals the total swapped out minus the total swapped in by this host since the VM started on it.
- D. A VM that arrives by vMotion can bring swapped pages, so Swapped can exceed what this host swapped out.
- E. The 6 GB in the swap file is the guest's working set, since ESXi swaps the pages the guest uses most.
- F. A flat Swapped total, read on its own, shows swap traffic in both directions.
- G. ESXi brings swapped pages back into memory on its own once host pressure ends.
- H. Close the memory question for this VM: a flat Swapped shows that the VM did not wait for swapped pages this hour.

## Answers
B, D

## Explanation
- A is wrong: swap out and swap in run in parallel on different pages. The swap file can keep its size while its content changes.
- B is true: in and out happen at the same time on different pages. Here about 2,000 KBps each way moves about 7 GB out and 7 GB back in this hour, with no change in the total.
- C is wrong: in and out are not one stream on one set of pages, and pages can arrive already swapped.
- D is true: Swapped is what sits in the swap file now, wherever it came from.
- E is wrong: ESXi picks pages to swap at random, without knowing what the guest uses; swapped pages are often pages the guest has not touched for a while.
- F is wrong: a flat total can also mean nothing moves at all, when the swap rates are 0; the rates tell which. This is the over-correction of A.
- G is wrong: swapped and compressed pages stay out until the guest requests them; bringing them back costs CPU. The balloon is different: it deflates when ESXi lowers the Balloon Target (host pressure ends, a limit is raised).
- H is wrong: swap-in at about 2,000 KBps is contention: each page read back is a wait for the vCPU that touched it. Check Memory Latency.
- Misconception: A: a flat Swapped read as no swap activity. Or C: Swapped read as the running difference of out and in.

## Notes
- vMotion and Swapped: the knowledge base, VM Memory Swapped, section Behaviour.
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): B states the mechanism on its own instead of negating A; F the over-correction, G a false mechanism and H the wrong action added. Key unchanged: B, D.
- Paired with 0142 (theory and practical; design.md, section 3.9).
- Changed in the 2026-11-15 audit: level 300 to 400 (C is the formula the vSphere 9.1 documentation prints, kept as a `corrections` entry in swapped; the stem's equal rates fit it arithmetically, so only the counter-start and vMotion mechanism refutes it); F worded without "always"; key point G follows the target-driven balloon deflate.

## Metadata
```yaml
id: "0143"
title: "Swapped is not Swap out minus Swap in"
product: [vsphere]
technology: [memory]
task: read-metric
level: 400
answer_type: deterministic
input: [text]
object: [vm]
tool: [vcenter]
knowledge:
  - vsphere/technology/memory/metrics/virtual-motherboard/swapped
  - vsphere/technology/memory/concepts/swap-and-compression
  - vsphere/technology/memory/metrics/virtual-motherboard/swap-out-rate
  - vsphere/technology/memory/metrics/virtual-motherboard/swap-in-rate
knowledge_main: vsphere/technology/memory/metrics/virtual-motherboard/swapped
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-12"
misconception: [A, C]
pair: "0142"
misconception_type: [cumulative-vs-current]
status: draft
```
