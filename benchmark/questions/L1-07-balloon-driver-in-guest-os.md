# Where the balloon runs

## Prompt
ESXi has four memory reclamation techniques. Which one runs as a driver inside the Guest OS?

- A. Ballooning
- B. Swapping to the .vswp file
- C. Memory compression
- D. Transparent page sharing

## Likely wrong answer
C: assuming compression happens inside the guest.

## Expected key points
- Answer: A.
- The balloon is a kernel driver inside the Guest OS (part of VMware Tools). It takes instructions from the VMkernel to inflate or deflate.
- Swapping, compression and page sharing are done by the VMkernel, without the Guest OS.

## Notes
- Previous id: question-0038 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0038"
title: "Where the balloon runs"
product: [vsphere, windows, linux]
technology: [memory]
task: explain-mechanism
level: 100
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/technology/memory/concepts/ballooning
  - vsphere/technology/memory/concepts/memory-layers
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 100-200 allocation (benchmark/design.md, section 3.6)"
answer: [A]
misconception: [C]
status: draft
```
