# Host compressed memory flat for months with balloon at 0

## Prompt
See [the VCF Operations memory charts of the host](0391/vcf-operations-host-memory-90-days.png).

- An administrator reviews an ESXi 9.1 host over the last 90 days and finds compressed memory on it but no balloon.
- The ticket reads: "ESXi balloons before it compresses, so this cannot be right. Is it a bug, and should we move VMs off the host?"

Which statements are correct?

- A. Compressed memory above 0 with the balloon at 0 cannot happen, because ESXi balloons before it compresses.
- B. ESXi leaves compressed pages in the compression cache until a VM touches them again.
- C. With usage below 90% all quarter, free memory stayed far above the level at which ESXi balloons.
- D. The flat compressed line shows ESXi compressing pages at a steady rate.
- E. Decompression at 0 shows that no VM waited on a compressed page in the period.
- F. Pages left in the compression cache can no longer slow any VM.
- G. Move VMs off the host to stop ESXi from compressing their memory.
- H. ESXi deflates its balloons once the memory pressure that inflated them has passed.

## Input to supply
- Product: VCF Operations 9.1; one ESXi host that compressed memory at some point and has had compressed memory since.
- Screen: VCF Operations > the host > Metrics, last 90 days, four charts stacked: Memory|Usage (%), the host's balloon metric, its compressed memory metric, and its decompression rate. Save as `benchmark/questions/0391/vcf-operations-host-memory-90-days.png`.
- Condition the key depends on, for the whole 90 days:
  - compressed memory flat (within 10%) and at 500 MB or more;
  - balloon 0;
  - Usage (%) below 90%;
  - decompression rate 0 (below 1 KBps).
- How to produce it: a host from the field matches more often than a lab; in a lab, push the host into the hard state with memory-touching VMs, then power off the extra load and leave the compressed VMs idle.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
A: "Ballooning comes first, so compressed without balloon is impossible." Or D: the flat amount read as compression going on now.

## Expected key points
- Answer: B, C, E, H.
- A false: the order applies while pressure rises. Compressed is an amount held now, from compression in the past; the balloon is gone and the compressed pages stayed.
- B true: compressed and swapped data stays out until the guest asks for it, because bringing it back costs CPU.
- C true: ballooning from host pressure starts at about 99% of host memory used; below 90% the host is far from it.
- D false: the line is an amount, not a rate. A rate counter (compression rate) shows activity.
- E true: a VM waits only when it touches a compressed page and ESXi decompresses it; a decompression rate of 0 means no such wait.
- F false: over-correction. A VM that touches one of those pages waits for the decompression; the risk stays while the pages stay compressed.
- G false: the wrong action. Nothing is compressed now and nothing waits; moving VMs changes neither.
- H true: the balloon deflates when the pressure ends, while compressed pages stay where they are until requested. That is why the balloon can be 0 while compressed memory is above 0.

## Notes
- Paired with 0025 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item C17.
- Fixed to compressed memory, not "compressed or swapped" as the plan proposed, so that one rate counter (decompression) decides E.
- The key holds whenever the condition of `## Input to supply` holds. No option says what caused the compression (host pressure or a limit).
- Written 2026-11-14 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after approval (design.md, section 6.2).

## Metadata
```yaml
id: "0391"
title: "Host compressed memory flat for months with balloon at 0"
product: [vsphere, vcf-operations]
technology: [memory]
task: troubleshoot
level: 300
answer_type: deterministic
input: [screenshot]
object: [esxi]
tool: [vcf-operations]
knowledge:
  - vsphere/technology/memory/concepts/swap-and-compression
  - vsphere/technology/memory/metrics/host/compressed
  - vsphere/technology/memory/metrics/host/ballooned
  - vsphere/technology/memory/concepts/ballooning
  - vsphere/technology/memory/concepts/host-memory-states
knowledge_main: vsphere/technology/memory/concepts/swap-and-compression
attachments:
  - 0391/vcf-operations-host-memory-90-days.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C17"
answer: [B, C, E, H]
misconception: [A, D]
misconception_type: [cumulative-vs-current, reclamation-as-contention]
pair: "0025"
status: awaiting-input
```
