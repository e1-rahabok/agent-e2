# A 16 GB VM under a 2 GB memory limit

## Prompt
- A Red Hat Enterprise Linux VM with 16 GB of memory runs a MySQL database.
- Someone set a memory limit of 2 GB on it by mistake.
- [The attached VCF Operations chart export](0141/vm-memory-limit-7-days.csv) covers the VM for the last 7 days, in 1-hour samples.

Which statements are correct?

- A. Consumed stays flat just above 2 GB all week: the limit caps the memory ESXi gives the VM.
- B. Granted at about 2.9 GB, above the limit, shows that ESXi does not enforce the limit on this VM at all.
- C. Granted counts every mapped VM page, shared and zero pages included, so it can sit above the limit.
- D. About 10.2 GB of the 13.5 GB Needed Memory are pages the balloon driver holds inside Linux, counted as used.
- E. Ballooned pages are counted in Consumed, and that is why Consumed stays pinned near the limit all week.

## Likely wrong answer
B: Granted above the limit read as the limit not working. Or E: ballooned memory counted in Consumed.

## Expected key points
- Answer: A, C, D.
- A: under a limit, Consumed sits at the limit and cannot grow past it.
- B is wrong: the limit caps the physical memory ESXi gives the VM, which is Consumed. Consumed stays at the limit.
- C: Granted is the VM's view of mapped pages; shared and zero pages cost little physical memory. It ignores the limit; Consumed does not.
- D: the balloon driver is a kernel driver inside Linux, so its 63.66% of 16 GB (about 10.2 GB) counts as used in the Guest OS counters. Exclude it when sizing the guest.
- E is wrong: ballooned pages have no ESXi page behind them, so they are not in Consumed.

## Notes
- From the author's samples (docx, 2026-11-12): a 16 GB MySQL VM on RHEL with a 2 GB limit (effective limit 2.12 GB); Guest Needed Memory 13.4-13.6 GB; Granted about 2.8-3.0 GB; Consumed just under 2 GB; Balloon flat at 63.66% for 7 days. The CSV is generated to reproduce those values.
- Open with the author: does a limit cause ballooning? The author's sample reads the flat balloon as proof that it does not. Vendor documents say a VM at its limit can show high balloon or swap (vSphere 9.1 Monitoring and Performance, memory troubleshooting: "high swap or balloon memory ... has reached its resource limit"; Broadcom KB 326270). 63.66% is near the Mem.CtlMaxPercent default of 65% (vSphere 9.1 documentation, advanced memory attributes). The key avoids the disputed point.
- This question also tests "ballooned pages show as In Use in the guest" (option D).

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
  - vsphere/technology/memory/metrics/virtual-motherboard/overhead
  - vsphere/technology/memory/metrics/virtual-motherboard/granted
  - vsphere/technology/memory/metrics/virtual-motherboard/consumed
knowledge_main: vsphere/technology/memory/metrics/virtual-motherboard/granted
attachments:
  - 0141/vm-memory-limit-7-days.csv
origin: book
source_path: "Author samples (docx, 2026-11-12) > Does limit result in balloon"
answer: [A, C, D]
misconception: [B, E]
misconception_type: [layer-confusion]
status: draft
```
