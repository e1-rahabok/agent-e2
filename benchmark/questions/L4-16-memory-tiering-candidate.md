# Is this host a memory tiering candidate?

## Prompt
- An ESXi 9.1 host has 768 GB of DRAM, no memory tiering yet.
- Consumed memory: 620 GB. Active memory: 260 GB.
- The plan: add a 768 GB NVMe device as the memory tier (ratio 1:1) and run 1.5 times as many VMs of the same profile.

Which statements are correct?

- A. With 1.5 times the VMs, active memory reaches about 390 GB, just over half of DRAM: test and monitor the workloads.
- B. Tiering starts when memory consumption reaches about 80% of DRAM; below that, all pages stay in DRAM.
- C. Kernel memory moves to the NVMe tier first, since kernel pages are the least active pages on the host.
- D. A tiered host has a higher hypervisor memory overhead, so less of its memory is reservable for VMs.
- E. Consumed after the change, about 930 GB, exceeds DRAM, so the host will start compressing and swapping.

## Likely wrong answer
C: assuming kernel memory can be tiered. Or E: Consumed above DRAM read as pressure.

## Expected key points
- Answer: A, B, D.
- A: 260 × 1.5 = 390 GB of active memory, about 51% of 768 GB. Broadcom's guidance: 50% or lower is good; 50-75% means test and monitor; above 75%, significant loss in most cases. The plan sits at the edge.
- B: tiering starts at about 80% DRAM consumption; pages are classified by recency and frequency, and cold pages move to NVMe.
- C is wrong: only VM pages are tiered; kernel memory never goes to NVMe.
- D: tiering raises the hypervisor overhead (about 7.96% for 512 GB DRAM + 512 GB NVMe, against about 2% for a 1 TB non-tiered host).
- E is wrong: on a tiered host Consumed covers both tiers and may exceed DRAM by design. Active against DRAM decides performance, not Consumed.

## Notes
- Revised 2026-11-12 (question set 1.0): numbers changed so that A is computed (51% of DRAM), option E added, tags added. Sources: vSphere 9.1 documentation, vSphere Resource Management > Memory Tiering over NVMe (candidates, the 80% line, hypervisor overhead); Performance Best Practices for vSphere 9.1, Memory Tiering.
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
object: [esxi]
tool: [none]
knowledge_main: vsphere/technology/memory/concepts/memory-tiering
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
answer: [A, B, D]
misconception: [C, E]
misconception_type: [consumption-as-contention, threshold-transplanted]
status: draft
```
