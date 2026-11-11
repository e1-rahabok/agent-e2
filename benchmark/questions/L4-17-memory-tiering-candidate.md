# Is this host a memory tiering candidate?

## Prompt
- An ESXi 9.1 host has 1 TB of DRAM.
- Consumed memory: 800 GB. Active memory: 200 GB.
- The plan: add a 1 TB NVMe device as the memory tier (ratio 1:1) and run twice as many VMs of the same profile.

Which statements are correct? Choose all that apply.

- A. The host is a good candidate: with twice the VMs, active memory (about 400 GB) still fits within 50% of DRAM.
- B. Tiering starts when memory consumption reaches about 80% of DRAM; below that, all pages stay in DRAM.
- C. Kernel memory moves to the NVMe tier first, because it is the least active.
- D. A tiered host has a higher hypervisor memory overhead, so less memory is reservable.

## Likely wrong answer
C: assuming the kernel memory can be tiered.

## Expected key points
- Answer: A, B, D.
- Good candidates have high consumed memory and active memory below 50% of DRAM; doubling the VMs gives about 400 GB active of 1 TB DRAM.
- Tiering starts at about 80% DRAM consumption; pages are classified by recency and frequency, and cold pages move to NVMe.
- Only VM pages are tiered: kernel memory never goes to NVMe.
- Tiering raises the hypervisor overhead (about 7.96% for 512 GB DRAM + 512 GB NVMe, against about 2% for a 1 TB non-tiered host).

## Notes
- Previous id: question-0057 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0057"
title: "Is this host a memory tiering candidate?"
product: [vsphere]
technology: [memory]
task: explain-mechanism
level: 400
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/technology/memory/concepts/memory-tiering
  - vsphere/technology/memory/metrics/virtual-motherboard/active
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
answer: [A, B, D]
misconception: [C]
status: draft
```
