# The VM swap file

## Prompt
Which file in a VM folder is the VM swap file?

- A. .vswp
- B. .vmsd
- C. .vmsn
- D. .nvram

## Likely wrong answer
C: .vmsn is the snapshot copy of the VM configuration, not swap.

## Expected key points
- Answer: A.
- .vswp is the VM swap file. It is deleted at power-off.
- .vmsd holds the snapshot metadata; .vmsn the VM configuration in a snapshot; .nvram the VM BIOS or UEFI settings.

## Notes
- Previous id: question-0033 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0033"
title: "The VM swap file"
product: [vsphere]
technology: [storage, memory]
task: read-metric
level: 100
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/technology/storage/concepts/vm-files
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 100-200 allocation (benchmark/design.md, section 3.6)"
answer: [A]
misconception: [C]
status: draft
```
