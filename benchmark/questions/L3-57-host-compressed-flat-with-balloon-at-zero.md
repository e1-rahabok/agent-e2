# Host compressed memory flat for months with balloon at 0

## Prompt
See [the VCF Operations memory charts of the host](0391/vcf-operations-host-memory-90-days.png).

- A new team member reviews an ESXi 9.1 host over the last 90 days and finds compressed memory on it, but no balloon.
- She asks whether that compressed memory still costs the VMs anything, and whether some VMs should move to another host.

Which statements are correct?

- A. Compressed memory above 0 with the balloon at 0 shows a counter fault.
- B. ESXi leaves compressed pages in the compression cache until a VM touches them again.
- C. With usage below 90% all quarter, free memory stayed far above the level at which ESXi balloons.
- D. The flat compressed line shows ESXi compressing pages at a steady rate.
- E. No VM had a measurable wait on a compressed page during the quarter.
- F. Pages still held in the compression cache can no longer slow any VM.
- G. Move VMs off the host to stop ESXi from compressing their memory.
- H. The compressed amount at the end of the quarter is less than half of what it was at the start.

## Input to supply
- Product: VCF Operations 9.1; one ESXi host that compressed memory at some point and has had compressed memory since.
- Screen: VCF Operations > the host > Metrics, last 90 days, four charts stacked, with the names of the VCF Operations 9.1 host metric list: Mem|Usage (%), Mem|Balloon (KB), Mem|Compressed (KB), Mem|Decompression Rate (KBps). Save as `benchmark/questions/0391/vcf-operations-host-memory-90-days.png`.
- Condition the key depends on, at every point of the 90 days:
  - Mem|Compressed (KB) flat (within 10% of its first value) and at 500 MB or more, and not between 4.5 and 5.5 GB (the knowledge-base example);
  - Mem|Balloon (KB) 0;
  - Mem|Usage (%) below 90%;
  - Mem|Decompression Rate (KBps) 0.
- How to produce it: a host from the field matches more often than a lab; in a lab, push the host into the hard state with memory-touching VMs, then power off the extra load and leave the compressed VMs idle.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
A: "Ballooning comes before compression, so compressed memory without a balloon must be a fault." Or D: the flat amount read as compression going on now.

## Expected key points
- Answer: B, C, E.
- A false: Compressed is an amount held now, from compression in the past. The order balloon, then compression applies while pressure rises; with usage below 90% there is no host pressure to balloon now.
- B true: compressed and swapped data stays out until the guest asks for it, because bringing it back costs CPU.
- C true: ballooning from host pressure starts at about 99% of host memory used; below 90% the host is far from it.
- D false: the line is an amount, not a rate; Compression Rate shows activity.
- E true: a VM waits only when it touches a compressed page and ESXi decompresses it; Decompression Rate is 0 at every point of the quarter.
- F false: over-correction. A VM that touches one of those pages waits for the decompression; the risk stays while the pages stay compressed.
- G false: the wrong action. Nothing is being compressed now and nothing waits; moving VMs changes neither.
- H false: the compressed line stays within 10% of its first value for the whole quarter.

## Notes
- Paired with 0025 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item C17.
- Metric names from the VCF Operations 9.1 Host System metric list (TechDocs, updated 2026-11-12): https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/infrastructure-operations/metric-property-and-alert-definitions/metrics-definitions-in-vrealize-operations-manager/metrics-for-vcenter-server-components/host-system-metrics.html
- No option says what caused the compression (host pressure or a limit), and none rests on how fast a balloon deflates: ballooning (deflates when pressure ends) and ballooned (pages stay ballooned while idle) read differently on that point.
- Review fixes 2026-11-15: new situation; A made one fact; the option on balloon deflation dropped (it rested on that difference); E now reads 0 at every point; a false screen reading added (H). Key B, C, E, H → B, C, E.
- The key holds whenever the condition of `## Input to supply` holds.
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
  - vsphere/technology/memory/concepts/host-memory-states
knowledge_main: vsphere/technology/memory/concepts/swap-and-compression
attachments:
  - 0391/vcf-operations-host-memory-90-days.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C17"
answer: [B, C, E]
misconception: [A, D]
misconception_type: [cumulative-vs-current, reclamation-as-contention]
pair: "0025"
status: awaiting-input
```
