# A 16 GB VM under a 2 GB memory limit

## Prompt
- A Red Hat Enterprise Linux VM with 16 GB of memory runs a MySQL database.
- Someone set a memory limit of 2 GB on it by mistake.
- [The attached VCF Operations chart export](0141/vm-memory-limit-7-days.csv) covers the VM for the last 7 days, in 1-hour samples.

Which statements are correct?

- A. Memory|Effective limit reads 2.12 GB: the 2 GB limit plus the VM overhead, which the limit does not cap.
- B. Granted at about 2.9 GB, above the limit, shows that ESXi does not enforce the limit on this VM.
- C. Granted counts every mapped VM page, shared and zero pages included, so it can sit above the limit.
- D. About 10.2 GB of the 13.5 GB Needed Memory are pages the balloon driver holds inside Linux, counted as used.
- E. Consumed stays near 2 GB because the balloon's 10 GB are counted inside it.
- F. A balloon flat for 7 days cannot come from a limit, which would keep reclaiming memory.

## Answers
A, C, D

## Explanation
- A: Memory|Effective limit of a VM with a limit reads the configured limit plus the VM overhead (2.12 GB here); the limit caps Consumed, not the overhead, so Consumed stays at or just under 2 GB (1.83-1.99 GB) and the gap to 2.12 GB is not room to grow.
- B is wrong: the limit caps the physical memory ESXi gives the VM, which is Consumed. Consumed stays at the limit; Granted ignores it.
- C: Granted is the VM's view of mapped pages; shared and zero pages, once shared, cost little physical memory. It ignores the limit; Consumed does not.
- D: the balloon driver is a kernel driver inside Linux, so its 63.66% of 16 GB (about 10.2 GB) counts as used in the Guest OS counters, and Needed Memory already contains it. Guest OS sizing keeps it with no deduction; the fix for the balloon is the limit, not the guest size.
- E is wrong: ballooned pages have no ESXi page behind them, so they are not in Consumed.
- F is wrong: a limit is enforced at all times, also on a host with free memory, and ESXi reclaims the excess with the balloon first, up to its 65% default ceiling (63.66% here is just under it). Once the balloon holds what the limit requires, it stays: a flat balloon near 65% of configured memory on a limited VM is the limit at work.
- Misconception: B: Granted above the limit read as the limit not working. Or E: ballooned memory counted in Consumed. Or F: "a limit would keep squeezing the VM, so a flat balloon must come from somewhere else".

## Notes
- From the author's samples (docx, 2026-11-12): a 16 GB MySQL VM on RHEL with a 2 GB limit (effective limit 2.12 GB); Guest Needed Memory 13.4-13.6 GB; Granted about 2.8-3.0 GB; Consumed just under 2 GB; Balloon flat at 63.66% for 7 days. The CSV is generated to reproduce those values.
- A limit causes ballooning, also on a host with free memory: the balloon is first, up to the 65% default ceiling (memory-limit, Enforcement order; vSphere 9.1 Monitoring and Performance, memory troubleshooting; Broadcom KB 326270). Option F tests the sample's original reading (a flat balloon proves the limit does not balloon).
- This question also tests "ballooned pages show as In Use in the guest" (option D).
- The knowledge base does not state this CSV's values.
- Changed in the 2026-11-15 audit: A now reads the effective limit (the old A, the limit caps Consumed, is tested by the pair 0140/0291); B and E reworded without absolutes; F added (the flat balloon read as proof that a limit does not balloon).

## Metadata
```yaml
id: "0141"
title: "A 16 GB VM under a 2 GB memory limit"
product: [vsphere, vcf-operations, linux]
technology: [memory]
task: explain-mechanism
level: 400
answer_type: deterministic
input: [table]
object: [vm, guest-os]
tool: [vcf-operations]
knowledge:
  - vsphere/technology/memory/metrics/virtual-motherboard/ballooned
  - vsphere/technology/memory/concepts/ballooning
  - vsphere/technology/memory/concepts/memory-limit
  - vsphere/technology/memory/metrics/virtual-motherboard/granted
  - vsphere/technology/memory/metrics/virtual-motherboard/consumed
knowledge_main: vsphere/technology/memory/metrics/virtual-motherboard/granted
attachments:
  - 0141/vm-memory-limit-7-days.csv
origin: book
source_path: "Author samples (docx, 2026-11-12) > Does limit result in balloon"
misconception: [B, E, F]
misconception_type: [layer-confusion]
status: draft
```
