# Is this host a memory tiering candidate?

## Prompt
- An ESXi 9.1 host has 768 GB of DRAM, no memory tiering yet.
- Consumed memory: 620 GB. Active memory: 290 GB.
- The plan: add a 768 GB NVMe device as the memory tier (ratio 1:1) and run 1.5 times as many VMs of the same profile.

Which statements are correct?

- A. With 1.5 times the VMs, active memory lands in the band where Broadcom advises testing and monitoring the workloads.
- B. No VM page moves to the NVMe tier until about 80% of the host DRAM is consumed.
- C. Kernel memory moves to the NVMe tier first, since kernel pages are the least active pages on the host.
- D. Adding the NVMe tier raises the memory the hypervisor itself needs, which leaves less memory for VM reservations.
- E. Once Consumed passes the 768 GB of DRAM, the host starts compressing and swapping.
- F. The NVMe device of the memory tier can still give part of its capacity to vSAN.

## Likely wrong answer
C: assuming kernel memory can be tiered. Or E: Consumed above DRAM read as pressure.

## Expected key points
- Answer: A, B, D.
- A is correct: 290 × 1.5 = 435 GB of active memory, about 57% of 768 GB. Broadcom's guidance: 50% or lower is good; 50-75% means test and monitor; above 75%, significant loss in most cases.
- B is correct: tiering starts at about 80% DRAM consumption; pages are classified by recency and frequency, and cold pages move to NVMe.
- C is wrong: only VM pages are tiered; kernel memory never goes to NVMe.
- D is correct: tiering raises the hypervisor overhead (about 7.96% for 512 GB DRAM + 512 GB NVMe, against about 2% for a 1 TB non-tiered host).
- E is wrong: on a tiered host Consumed covers both tiers and may exceed DRAM by design (about 930 GB here); new pages come from the NVMe tier once DRAM passes about 80%. Active against DRAM decides performance, not Consumed.
- F is wrong: an NVMe device used for tiering is not available to vSAN; the lost vSAN capacity counts in the cluster sizing.

## Notes
- Sources: vSphere 9.1 documentation, vSphere Resource Management > Memory Tiering over NVMe (candidates, the 80% line, hypervisor overhead, the device not available to vSAN); Performance Best Practices for vSphere 9.1, Memory Tiering.
- Synthetic, from the knowledge files listed in `knowledge`. Counts only after author approval.
- F added in the 2026-11-15 audit (memory-tiering, Capacity and Misconceptions: a tiering device is taken out of vSAN capacity).

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
source_path: "Synthetic, 2026-11-05"
answer: [A, B, D]
misconception: [C, E]
misconception_type: [consumption-as-contention, threshold-transplanted]
status: draft
```
