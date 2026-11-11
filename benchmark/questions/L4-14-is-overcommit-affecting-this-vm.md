# Is memory overcommitment affecting this VM?

## Prompt
- A 32 GB VM runs on an ESXi host that is overcommitted on memory.
- Last hour, from the vCenter real-time charts:
  - Ballooned memory: 4 GB, flat.
  - Consumed memory: 28 GB. Active memory: 6 GB.
  - Swapped: 0. Compressed: 0.
  - Memory Latency: 0%.
- The application team reports no slowness.

Which statements are correct? Choose all that apply.

- A. Overcommitment is not affecting this VM now: some ballooning is normal, Consumed is above Active, and there is no host swapping, compression or latency.
- B. The VM is short of memory: ballooning above 0 means it cannot get what it asks for.
- C. Add 4 GB to the VM to cancel the balloon.
- D. If users later report slowness, check swap activity inside the Guest OS next: ballooning may then be starting to affect the guest.

## Likely wrong answer
B: reading balloon above 0 as the VM being short of memory.

## Expected key points
- Answer: A, D.
- The overcommit indicators, in order: ballooning, Consumed vs Active, host swapping and compression, Guest OS swap. Some ballooning is normal; Consumed above Active means the guest gets what it uses now; Swapped, Compressed and Latency at 0 mean no pressure on this VM.
- C is wrong: adding memory to a VM on a pressured host adds to the pressure; the balloon follows the host, not the VM size.
- Guest OS swap is the next indicator if impact appears.

## Notes
- Previous id: question-0054 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0054"
title: "Is memory overcommitment affecting this VM?"
product: [vsphere]
technology: [memory]
task: troubleshoot
level: 400
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/technology/memory/decision-tree/is-overcommit-affecting-vm
  - vsphere/technology/memory/concepts/ballooning
  - vsphere/technology/memory/metrics/virtual-motherboard/latency
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
answer: [A, D]
trap: [B]
status: draft
```
