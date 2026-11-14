# VM memory contention follows swap-in, not the balloon

## Prompt
See [the VCF Operations memory charts of the VM](0392/vcf-operations-vm-contention-balloon-swap-in-24h.png).

- A Windows VM runs a reporting service. Its owner reports slow reports at several times yesterday.
- The vSphere team points at the balloon on the VM and proposes to remove the balloon driver from it.

Which statements are correct?

- A. Memory Contention rises in the same intervals as Swap In Rate.
- B. Each page read back from the swap file holds the vCPU that touched it until the page arrives.
- C. Memory Contention counts the time the balloon holds part of the VM's memory.
- D. A Memory Contention value of N% means that N% of the VM's memory sits on slower media than DRAM.
- E. Memory Contention counts swap-in only, so decompression can never raise it.
- F. Remove the balloon driver so that the VM stops waiting for memory.

## Input to supply
- Product: VCF Operations 9.1; a Windows VM with VMware Tools, on a host under memory pressure for part of the day.
- Screen: VCF Operations > the VM > Metrics, last 24 hours, three charts stacked: Memory|Contention (%), the VM's balloon metric, and its Swap In Rate. Save as `benchmark/questions/0392/vcf-operations-vm-contention-balloon-swap-in-24h.png`.
- Condition the key depends on:
  - balloon above 0 (10% of the configured memory or more) for most of the 24 hours, including hours when Contention is 0;
  - Contention above 0.5% only in intervals where Swap In Rate is above 0, and below 0.1% where Swap In Rate is 0.
- How to produce it: a field VM matches more often than a lab; in a lab, overcommit a small host so this VM is ballooned, then let its guest touch more memory than is left to it for short periods, so that ESXi swaps and the guest reads pages back.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
C: "The balloon is memory the VM waits for, so it raises contention." Or D: the percentage read as a share of memory.

## Expected key points
- Answer: A, B.
- A true: on the charts, Contention rises only where Swap In Rate is above 0; with the balloon high and swap-in at 0, Contention stays at 0.
- B true: Memory Contention is the share of time a vCPU waits for a page fault ESXi resolves; a swap-in is such a fault, so the counter tracks swap-in closely.
- C false: the balloon is reclamation inside the guest; ESXi sees no fault on those pages. The counter excludes balloon activity.
- D false: the counter is a share of time, not of memory space, and not a latency in nanoseconds.
- E false: over-correction. The counter covers decompression of a compressed page too (and copy-on-write breaks); swap-in is most of it.
- F false: the wrong action. The balloon is not what the VM waits on, and without the balloon driver ESXi can only compress or swap, blind to which pages the guest uses: it can take pages the guest needs, and the VM waits when it touches them.

## Notes
- Paired with 0149 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item C27.
- The key holds whenever the condition of `## Input to supply` holds.
- Written 2026-11-14 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after approval (design.md, section 6.2).

## Metadata
```yaml
id: "0392"
title: "VM memory contention follows swap-in, not the balloon"
product: [vsphere, vcf-operations, windows]
technology: [memory]
task: read-metric
level: 300
answer_type: deterministic
input: [screenshot]
object: [vm]
tool: [vcf-operations]
knowledge:
  - vsphere/technology/memory/metrics/virtual-motherboard/latency
  - vsphere/technology/memory/concepts/ballooning
  - vsphere/technology/memory/concepts/swap-and-compression
  - vsphere/technology/memory/metrics/virtual-motherboard/swap-in-rate
knowledge_main: vsphere/technology/memory/metrics/virtual-motherboard/latency
attachments:
  - 0392/vcf-operations-vm-contention-balloon-swap-in-24h.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C27"
answer: [A, B]
misconception: [C, D]
misconception_type: [reclamation-as-contention, unit-and-normalization]
pair: "0149"
status: awaiting-input
```
