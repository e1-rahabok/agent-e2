# esxtop MEM overcommit average

## Prompt
- The esxtop memory panel of an ESXi 9.1 host shows `MEM overcommit avg: 0.82, 0.81, 0.80` in its header.

Which statements about this line are correct?

- A. The line compares the memory requested on the host with the memory ESXi manages, minus 1.
- B. The three values are averages over the last 1, 5 and 15 minutes.
- C. Requested memory counts each VM's configured memory, whether or not the guest has touched it.
- D. Any value above 0 shows that the host lacks the memory its VMs need right now.
- E. A value of 0.82 means that 82% of the memory ESXi manages is in use by the VMs.
- F. No level of memory overcommit, however high, can make ESXi swap the memory of a VM.
- G. Move VMs off the host with vMotion until all three values on the line read 0.
- H. Whether the overcommit slows a VM shows in that VM's memory latency, not on this line.
- I. At 0.82, the memory requested on the host is about 1.8 times the memory ESXi manages.

## Likely wrong answer
D: "Overcommit above 0, so the host is short of memory and will swap." Or E: the value read as a share of memory in use.

## Expected key points
- Answer: A, B, C, H, I.
- A true: the line is the ratio of total requested memory to managed memory, minus 1. Requested is the VMs' configured memory (or their limits), user world memory and reserved overhead.
- B true: the three values are 1-, 5- and 15-minute exponentially weighted averages.
- C true: requested is an allocation, not a use; ESXi backs a VM page only when the guest first touches it.
- D false: above 0 means requested exceeds what ESXi manages. That is fine while the VMs touch less, with sharing and ballooning as the first answers; the host state and the reclamation counters show pressure.
- E false: the value is a ratio minus 1, not a share of memory in use.
- F false: over-correction. If the VMs touch more than the host has, ESXi moves from sharing and ballooning to compression and host swapping, and swapping active pages degrades performance.
- G false: the wrong action. Overcommit above 0 is a normal, planned state; migrate on contention, not on this line.
- H true: VM memory latency (esxtop %LAT_M, VCF Operations Memory Contention) is the counter of the wait; this line is allocation.
- I true: requested / managed = 1 + 0.82, about 1.8.

## Notes
- Paired with 0399 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item D10.
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
answer: [A, B, C, H, I]
misconception: [D, E]
misconception_type: [consumption-as-contention, unit-and-normalization]
pair: "0399"
status: draft
```
