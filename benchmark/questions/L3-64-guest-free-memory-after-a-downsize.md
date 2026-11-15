# Guest free memory after a memory downsize

## Prompt
- A Windows VM is cut from 24 GB to 12 GB of memory after a month of low use.
- The application team watches the guest counters in the weeks after the change.

Which statements about the VM after the downsize are correct?

- A. Lower guest free memory after the cut shows that the new size is too small.
- B. Pages the guest writes out, and VM memory contention, over a full business cycle show if the cut went too far.
- C. VM memory contention at 0 over a business cycle proves the new size is enough.
- D. Add memory back until guest free memory returns to its level before the cut.
- E. A large cut is made in steps, with a check over a business cycle after each step.
- F. VM Memory Usage (%) in VCF Operations rises after the cut even if Needed Memory stays the same.
- G. VM Consumed falling after the cut shows that the guest has enough memory.

## Likely wrong answer
A: "Free memory dropped after the downsize, so the VM is now short: undo it."
## Expected key points
- Answer: B, E, F.
- A false: free memory is not the measure of a shortage; Windows and Linux fill memory with cache.
- B true: after each step, check guest page-out and VM memory contention over a business cycle before the next. A guest that pages out is short; a VM with contention waits on ESXi.
- C false: over-correction. Memory contention covers waits on ESXi only; a guest short of memory pages out with no contention at all, so guest page-out is read too.
- D false: the wrong action from A. Free memory going back up would only bring back the unused memory.
- E true: cut in steps, not all at once, so a step that goes too far shows before the next.
- F true: Usage (%) is Guest Needed Memory divided by the VM's total memory; the same need over a smaller total reads higher.
- G false: Consumed is an ESXi counter of pages the VM holds on the host; it falls because the VM is smaller, and it does not show what the guest needs.

## Notes
- Paired with 0401 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item D11.
- No option sets a paging threshold: windows-memory gives none (judge paging by change and by the application's history).
- Review fixes 2026-11-15: the option stating the expected fall of free memory was dropped, since it was the negation of the misconception (T2); the over-correction is now that contention at 0 proves the size (one fact, not the negation of B). Key A, C, F, G → B, E, F (relettered).
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
  - guest-os/system/concepts/guest-os-sizing
  - guest-os/memory/windows-memory
  - vsphere/technology/memory/metrics/virtual-motherboard/usage
  - vsphere/technology/memory/metrics/virtual-motherboard/consumed
knowledge_main: sp5-framework/capacity/rightsizing
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D11"
answer: [B, E, F]
misconception: [A]
misconception_type: [consumption-as-contention]
pair: "0401"
status: draft
```
