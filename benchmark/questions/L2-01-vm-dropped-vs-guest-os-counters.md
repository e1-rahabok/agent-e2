# Why VM dropped packets differ from the Guest OS

## Prompt
- A VM shows Packets dropped above 0.
- The Windows network counters inside the same VM show no discarded packets.

Why can the two disagree? Choose all that apply.

- A. Received packets are dropped by ESXi before they reach the Guest OS.
- B. Transmitted packets are dropped after they leave the Guest OS.
- C. VMware Tools resets the Windows counters every 20 seconds.
- D. The Guest OS counts dropped packets in bits, the VM in bytes.

## Likely wrong answer
C or D: looking for a counter bug instead of where the drop happens.

## Expected key points
- Answer: A, B.
- The VM counter sees drops outside the Guest OS: received packets dropped before the guest, transmitted packets dropped after it. The Guest OS cannot see either.
- Tools does not modify existing Windows or Linux counters; C and D are invented.

## Notes
- Previous id: question-0039 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0039"
title: "Why VM dropped packets differ from the Guest OS"
product: [vsphere, windows, linux]
technology: [network]
task: explain-mechanism
level: 200
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/technology/network/metrics/virtual-motherboard/packets-dropped
  - vsphere/architecture/vm-vs-guest-os
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 100-200 allocation (benchmark/design.md, section 3.6)"
answer: [A, B]
misconception: [C]
status: draft
```
