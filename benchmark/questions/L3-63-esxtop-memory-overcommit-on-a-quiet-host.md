# esxtop shows memory overcommit on a quiet host

## Prompt
See [the esxtop memory panel header](0399/esxtop-memory-header-overcommit.png).

- A new administrator opens esxtop on an ESXi 9.1 host and sees memory overcommit above 0.
- They raise a ticket: the host is short of memory and its VMs will soon swap. They plan to vMotion VMs off the host until the overcommit reads 0.

Which statements are correct?

- A. The memory requested on the host is about 1.3 to 1.6 times the memory ESXi manages.
- B. The host lacks the memory its running VMs need at the moment of the capture.
- C. In the memory state shown, host pressure triggers no ballooning, compression or swapping.
- D. MEMCTL, SWAP and ZIP at 0 show that nothing is ballooned, swapped or compressed now.
- E. The overcommit value is the share of the host's memory that is in use.
- F. No level of memory overcommit, however high, can make ESXi swap the memory of a VM.
- G. vMotion VMs off the host until all three overcommit values read 0.
- H. The three values close together show a steady overcommit over the last 15 minutes.

## Input to supply
- Product: ESXi 9.1, esxtop over SSH.
- Lab step: on one host, power on VMs whose configured memory adds up to 1.3-1.6 times the host's memory, with light guests (idle or small workloads), no limits and no memory tiering. Wait 20 minutes.
- Screen: esxtop, memory panel (`m`), header lines visible: MEM overcommit avg, PMEM, VMKMEM (with `state`), PSHARE, SWAP, ZIP, MEMCTL. Crop below the header, or mask the VM rows. Save as `benchmark/questions/0399/esxtop-memory-header-overcommit.png`.
- Condition the key depends on:
  - MEM overcommit avg between 0.30 and 0.60 at all three values, within 0.05 of each other;
  - VMKMEM `state` high;
  - SWAP `curr`, ZIP `zipped` and MEMCTL `curr` at 0.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
B: "Overcommit above 0 means the host is short of memory and will swap." Or E: the value read as memory in use.

## Expected key points
- Answer: A, C, D, H.
- A true: the line is requested over managed memory, minus 1; 0.30-0.60 means requested is about 1.3-1.6 times managed.
- B false: requested counts configured memory, not touched memory. The state is high and nothing is reclaimed: no shortage.
- C true: high is the state with no reclamation for host pressure; ballooning starts in soft, compression and swapping in hard.
- D true: MEMCTL, SWAP and ZIP are the host sums of ballooned, swapped and compressed VM memory; all at 0.
- E false: the value is a ratio minus 1, not a share of memory in use; PMEM shows the memory actually free.
- F false: over-correction. If the VMs touch more than the host has, ESXi moves through ballooning and compression to host swapping, which slows the VMs that touch swapped pages.
- G false: the wrong action. Overcommit above 0 is planned; migrate on contention (VM memory latency, swap-in), not on this line.
- H true: the values are 1-, 5- and 15-minute exponentially weighted averages; equal values mean a steady overcommit.

## Notes
- Paired with 0398 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item D10.
- The key holds whenever the condition of `## Input to supply` holds.
- Written 2026-11-14 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after approval (design.md, section 6.2).

## Metadata
```yaml
id: "0399"
title: "esxtop shows memory overcommit on a quiet host"
product: [vsphere]
technology: [memory]
task: read-metric
level: 300
answer_type: deterministic
input: [screenshot]
object: [esxi]
tool: [esxtop]
knowledge:
  - vsphere/tools/esxtop/memory
  - vsphere/technology/memory/concepts/host-memory-states
knowledge_main: vsphere/tools/esxtop/memory
attachments:
  - 0399/esxtop-memory-header-overcommit.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D10"
answer: [A, C, D, H]
misconception: [B, E]
misconception_type: [consumption-as-contention, unit-and-normalization]
pair: "0398"
status: awaiting-input
```
