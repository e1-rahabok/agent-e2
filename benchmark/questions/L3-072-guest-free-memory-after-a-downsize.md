# Guest free memory after a memory downsize

## Prompt
- A Windows VM is cut from 24 GB to 12 GB of memory. In the month before, Guest|Needed Memory peaked at about 8 GB.
- After the cut, Windows Available memory falls from about 14 GB to about 4 GB.
- In the second week after the cut the host runs short of memory, and VM Memory Ballooned reads about 2 GB for two days.
- The application team watches the guest counters in the weeks after the change.

Which statements about the VM after the downsize are correct?

- A. Lower guest free memory after the cut shows that the new size is too small.
- B. Guest page-out and VM memory contention across a business cycle show if the cut went too far.
- C. VM memory contention at 0 over a business cycle proves the new size is enough.
- D. Add memory back until guest free memory returns to its level before the cut.
- E. A large cut is made in steps, with a check over a business cycle after each step.
- F. As the balloon inflates to about 2 GB, VM Consumed falls by at most about 2 GB: ESXi takes back the pages behind it.
- G. VM Consumed falling after the cut shows that the guest has enough memory.
- H. Before the next step, take the ballooned 2 GB out of Needed Memory: those pages are ESXi's request.

## Likely wrong answer
A: "Free memory dropped after the downsize, so the VM is now short: undo it." Or H: "Ballooned memory is ESXi's request, so take it out of the need before sizing."

## Expected key points
- Answer: B, E, F.
- A is wrong: free memory is not the measure of a shortage; Windows and Linux fill memory with cache.
- B is correct: after each step, check guest page-out and VM memory contention over a business cycle before the next. A guest that pages out is short; a VM with contention waits on ESXi.
- C is wrong: over-correction. Memory contention covers waits on ESXi only; a guest short of memory pages out with no contention at all, so guest page-out is read too.
- D is wrong: the wrong action from A. Free memory going back up would only bring back the unused memory.
- E is correct: cut in steps, not all at once, so a step that goes too far shows before the next.
- F is correct: the driver pins the pages it got from Windows and the VM monitor returns the ESXi pages behind them to the VMkernel, so Consumed falls at once; by less than the balloon size when some of those pages were shared.
- G is wrong: Consumed is an ESXi counter of pages the VM holds on the host; it falls because the VM is smaller, and it does not show what the guest needs.
- H is wrong: the balloon driver pins its pages inside Windows, which counts them as in use, so Needed Memory already holds them; the balloon also takes pages in use, which Windows pages out and still needs; sizing makes no deduction for the balloon, so a cut does not shrink a VM the balloon already squeezes. The balloon is a host event, fixed on the host side.

## Notes
- Paired with 0401 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item D11.
- No option sets a paging threshold: windows-memory gives none (judge paging by change and by the application's history).
- Changed in the 2026-11-15 audit: evidence in the stem (Needed Memory peak, Available before and after, a balloon episode); F replaced (it tested the VCF Operations Usage (%) formula, already tested by the pair 0394/0395) by the balloon pages inside Needed Memory (true); H added (deduct the balloon, false).
- Changed in the 2026-11-16 re-review: F (the balloon pages are inside Needed Memory) and H (take them out of Needed Memory) were near-complements; F now tests what the balloon does to VM Consumed (ballooning, Inflate and deflate, step 5; shared pages free less). Still true; the Needed Memory fact moved into the key point of H.
- Written 2026-11-14 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after approval (design.md, section 6.2).

## Metadata
```yaml
id: "0400"
title: "Guest free memory after a memory downsize"
product: [windows, vsphere, vcf-operations]
technology: [memory]
task: decide-capacity
level: 300
answer_type: deterministic
input: [text]
object: [guest-os, vm]
tool: [guest-os-tools, vcf-operations]
knowledge:
  - sp5-framework/capacity/rightsizing
  - guest-os/system/guest-os-sizing
  - guest-os/memory/windows-memory
  - vsphere/technology/memory/concepts/ballooning
  - vsphere/technology/memory/metrics/virtual-motherboard/consumed
knowledge_main: sp5-framework/capacity/rightsizing
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D11"
answer: [B, E, F]
misconception: [A, H]
misconception_type: [consumption-as-contention]
pair: "0401"
status: draft
```
