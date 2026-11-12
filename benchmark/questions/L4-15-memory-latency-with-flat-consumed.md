# Memory latency with a flat Consumed

## Prompt
- A VM is configured with 16 GB of memory.
- Since yesterday, VCF Operations shows VM Memory Contention at about 2%, sustained.
- In the same period:
  - Swap in rate: above 0 most of the time.
  - Consumed: flat at 8 GB.
  - Ballooned: 0.
- The ESXi host has free memory and no other VM swaps.

What is the most likely cause, how do you confirm it, and what do you change?

## Likely wrong answer
"The host is short of memory: add RAM to the host or move the VM."

## Expected key points
- Most likely a memory limit of about 8 GB on the VM (or its resource pool): Latency with a flat Consumed near the limit points to the limit.
- The swap-in rate is the source of the wait: the vCPU waits for pages read back from the swap file. The host itself has free memory, so it is not host pressure.
- Confirm the limit on the VM and on every parent resource pool.
- Remove or raise the limit. A reboot in maintenance also clears the swapped pages.
- Balloon is not part of Memory Latency: Ballooned at 0 does not rule out the problem.

## Notes
- Previous id: question-0055 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0055"
title: "Memory latency with a flat Consumed"
product: [vsphere, vcf-operations]
technology: [memory]
task: troubleshoot
level: 400
answer_type: judged
input: [text]
knowledge:
  - vsphere/technology/memory/vm-memory-latency-high
  - vsphere/technology/memory/metrics/virtual-motherboard/latency
  - vsphere/technology/memory/metrics/virtual-motherboard/swap-in-rate
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
status: draft
```
