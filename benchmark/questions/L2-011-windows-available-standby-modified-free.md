# Windows Available, Standby, Modified and Free

## Prompt
- Windows Resource Monitor, Memory tab, splits the memory of a Windows Server VM into In Use, Modified, Standby and Free, and shows Available and Cached below the bar.
- The monitoring tool raises an alert whenever Free falls below 500 MB.

Which statements about these Windows memory counters are correct?

- A. Available is the sum of the Standby and Free pages that Windows holds.
- B. Modified pages are written to disk before Windows can reuse them.
- C. Standby pages hold cached data that Windows can hand to a process at once.
- D. Cached is the sum of the Standby and Modified pages that Windows holds.
- E. Free that stays low all day shows that Windows is running out of memory.
- F. In Use is the least memory that Windows and its applications can run with.
- G. No Windows counter can show that the guest is short of memory.
- H. Modified pages are part of Available: Windows can hand them to a process at once.

## Likely wrong answer
E: "Free is almost 0 and the alert fires all day, so Windows is out of memory."

## Expected key points
- Answer: A, B, C, D.
- A true: Available is the memory Windows can use at once without saving a page first: Standby plus Free.
- B true: Modified pages hold changed data no process uses now; Windows writes them to disk, in batches, before it reuses them, so they are not Available.
- C true: Standby is cache; Windows hands those pages out at once, so low Free with high Standby is normal and means no waste.
- D true: Cached is Standby plus Modified.
- E false: Windows fills memory with Standby cache, and Free can touch 0 for a moment. Read Available, paging together with the disk queue, and % Committed.
- F false: In Use is not a minimum: Windows compresses In Use pages it does not use, even with plenty of memory free.
- G false: over-correction. Low Free alone is not a shortage, but page-in and page-out together with a high disk queue are the Windows sign of a memory performance problem.
- H false: Modified pages hold changed data that must be written to disk before reuse, so they are in Cached, not in Available (Standby plus Free).

## Notes
- Paired with 0264 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item B2.
- Changed in the 2026-11-15 audit: H (a second copy of E's belief) replaced by a false definition, so not every definition is true and not every judgment false. A true judgment ("low Free with high Standby wastes no memory") was not added: the Free memory row of the threshold catalog scores that state as poor (knowledge-base issue 3 of the review).
- Written 2026-11-14 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after approval (design.md, section 6.2).

## Metadata
```yaml
id: "0382"
title: "Windows Available, Standby, Modified and Free"
product: [windows]
technology: [memory]
task: explain-mechanism
level: 200
answer_type: deterministic
input: [text]
object: [guest-os]
tool: [guest-os-tools]
knowledge:
  - guest-os/memory/windows-memory
knowledge_main: guest-os/memory/windows-memory
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item B2"
answer: [A, B, C, D]
misconception: [E]
misconception_type: [consumption-as-contention]
pair: "0264"
status: draft
```
