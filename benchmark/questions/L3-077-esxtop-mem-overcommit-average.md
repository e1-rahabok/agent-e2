# esxtop MEM overcommit average

## Prompt
- The esxtop memory panel of an ESXi 9.1 host shows `MEM overcommit avg: 0.82, 0.81, 0.80` in its header.
- No VM on the host has a memory limit.

Which statements about this line are correct?

- A. The line is the memory requested on the host over the memory ESXi manages, minus 1.
- B. The three values are exponentially weighted averages with 1-, 5- and 15-minute windows.
- C. Requested memory counts each VM's configured memory, whether or not the guest has touched it.
- D. Any value above 0 shows that the host lacks the memory its VMs need right now.
- E. A value of 0.82 means that 82% of the memory ESXi manages is in use by the VMs right now.
- F. Host swapping can start only once the value passes 1, when twice the managed memory is requested.
- G. Move VMs off the host with vMotion until all three values on the line read 0.
- H. Whether the overcommit slows a VM shows in that VM's memory latency, not on this line.
- I. At 0.82, the memory requested on the host is about 1.8 times the memory ESXi manages.
- J. A memory limit on a VM would leave this line unchanged, as requested counts the configured memory.

## Answers
A, B, C, H, I

## Explanation
- A is correct: the line is the ratio of total requested memory to managed memory, minus 1. Requested is the VMs' configured memory (or their limits), user world memory and reserved overhead.
- B is correct: the three values are 1-, 5- and 15-minute exponentially weighted averages.
- C is correct: requested is an allocation, not a use; ESXi backs a VM page only when the guest first touches it.
- D is wrong: above 0 means requested exceeds what ESXi manages. That is fine while the VMs touch less, with sharing and ballooning as the first answers; the host state and the reclamation counters show pressure.
- E is wrong: the value is a ratio minus 1, not a share of memory in use.
- F is wrong: over-correction. Touched memory decides, not this ratio: once the VMs touch more than the host can hold, ESXi moves from sharing and ballooning to compression and host swapping, at any overcommit above 0.
- G is wrong: the wrong action. Overcommit above 0 is a normal, planned state; migrate on contention, not on this line.
- H is correct: VM memory latency (esxtop %LAT_M, VCF Operations Memory Contention) is the counter of the wait; this line is allocation.
- I is correct: requested / managed = 1 + 0.82, about 1.8.
- J is wrong: requested counts a VM's limit in place of its configured memory, so a limit below the configured size lowers the line.
- Misconception: D: "Overcommit above 0, so the host is short of memory and will swap." Or E: the value read as a share of memory in use.

## Notes
- Paired with 0399 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item D10.
- Review fixes 2026-11-15: B reworded (exponentially weighted, with 1-, 5- and 15-minute windows); the stem states that no VM has a memory limit, so C holds (requested counts a limit in place of configured memory). Key unchanged: A, B, C, H, I.
- Changed in the 2026-11-15 audit: F (no overcommit can make ESXi swap: an absolute that was easy to reject) replaced by the over-correction that swapping waits for a value of 1, same truth; J added (a limit in the requested total).
- Written 2026-11-14 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after approval (design.md, section 6.2).

## Metadata
```yaml
id: "0398"
title: "esxtop MEM overcommit average"
product: [vsphere]
technology: [memory]
task: explain-mechanism
level: 300
answer_type: deterministic
input: [text]
object: [esxi]
tool: [esxtop]
knowledge:
  - vsphere/tools/esxtop/memory
  - vsphere/technology/memory/concepts/host-memory-states
  - vsphere/technology/memory/metrics/virtual-motherboard/latency
  - vsphere/technology/memory/metrics/virtual-motherboard/consumed
knowledge_main: vsphere/tools/esxtop/memory
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D10"
misconception: [D, E]
misconception_type: [consumption-as-contention, unit-and-normalization]
pair: "0399"
status: draft
```
