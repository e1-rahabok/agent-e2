# Swapped and Compressed moving in opposite directions

## Prompt
- A Windows Server VM with 24 GB of memory runs SQL Server for the nightly reports.
- The report team says the reports, which run every night from 01:00 to 03:00, take twice as long as on the old cluster.
- The ESXi host has more than 200 GB free. No other VM on the host has swapped or compressed memory.
- The VM carries `sched.mem.maxmemctl = 0` from an old hardening template. VCF Operations shows its Memory|Balloon at 0 for the same 3 days.
- [The attached VCF Operations export](0140/vm-memory-3-days.csv) covers the VM for the last 3 days, in 30-minute samples.

Why do the reports slow down, and what do you change? Which statements are correct?

- A. A memory limit on the VM or on its resource pool caps the VM's memory.
- B. The host is short of memory, and ESXi swaps this VM to free memory for the others.
- C. During each report run, the guest reads swapped pages back while ESXi compresses other pages to stay under the cap.
- D. Each fall of Swapped shows that the memory pressure on the VM has eased.
- E. A compressed page the guest touches costs its vCPU a shorter wait than a swapped page does.
- F. Pages swapped out make the VM wait even when the guest never touches them again.
- G. Moving the VM to a host with more free memory stops the swapping and the compression of its pages.
- H. Configuring the VM with more than 24 GB stops the swapping.
- I. Remove the limit, or raise it to what the guest needs, after finding out why it was set.
- J. A Consumed value that stays flat for 3 days shows that memory is not the cause of the slow reports.
- K. With the cap in place, the VM waits for memory all day, not only during the runs.
- L. Memory|Balloon at 0 in every sample rules out a limit, since a limit always balloons first.
- M. The gap of about 0.4 GB between Consumed and Memory|Effective limit is room the VM can still grow into.

## Likely wrong answer
- B: "The host is running out of memory and swaps the VM."
- G: "Move the VM to a host with more free memory."
- H: "Give the VM more memory."
- L: "No balloon, so no limit: a limit balloons first."

## Expected key points
- Answer: A, C, E, I.
- A true: Consumed stays flat at 15.66-15.83 GB, just under a limit of about 16 GB (Memory|Effective limit, 16.19 GB, is the limit plus the VM overhead), while the host has over 200 GB free and no other VM is reclaimed: the cause is a limit on the VM or its pool, not the host.
- B false: with free host memory and no other VM swapped or compressed, the host is not short.
- C true: in and out run at the same time on different pages; in each run Swapped falls (about 6.12 to 4.86, 4.85 to 3.79 and 3.80 to 2.99 GB) while Compressed rises (about 0.24 to 0.80, 0.80 to 1.28 and 1.28 to 1.65 GB), and Consumed stays flat.
- D false: Swapped falls because the guest asked for swapped pages (swap-in, the costly part); other pages go out at the same time to stay under the limit.
- E true: decompression latency is much smaller than swap-in latency; both are waits for the vCPU that touched the page, and they show as the Contention of about 3.2-6.2% in the samples of 01:00 to 02:30.
- F false: swap-out is not contention by itself; only swap-in, when the guest asks for the page, makes the vCPU wait.
- G false: the limit moves with the VM; the host was never short.
- H false: the limit, not the configured size, caps Consumed; more configured memory changes nothing while the limit stays.
- I true: the limit is the cause; removing it or raising it to the guest's need is the fix.
- J false: Consumed is flat because the limit caps it; the guest keeps touching pages that ESXi swaps and compresses.
- K false: outside the runs Contention stays at 0.05% or less, mostly 0; swapped pages the guest does not touch cost no wait. This is the over-correction of A: a limit read as a wait at every moment.
- L false: the balloon goes first under a limit only when the driver runs; `sched.mem.maxmemctl = 0` switches it off, so ESXi compresses and swaps instead.
- M false: the configured limit caps Consumed; Memory|Effective limit adds the VM overhead, which the limit does not cap, so the gap is not room to grow.

## Notes
- Practical half of 0291 (project/question-pairing-2026-11-14.md, pair A14). CSV from a seeded script (seed 14020261114, 3 days, 30-minute samples); the old 64 GB scenario, a near-copy of the knowledge example in swap-and-compression, is in project/archive/benchmark-questions/attachments.
- A VM limit caps Consumed, and Memory|Effective limit is the configured limit plus the VM overhead (memory-limit, Signs in the counters). The CSV fits it: Consumed stays under 16 GB while the effective limit reads 16.19 GB.
- Under a limit the balloon goes first when the driver runs (memory-limit, Enforcement order). The CSV has Granted + Swapped + Compressed near 24 GB and no balloon, so the stem gives the driver switched off (`sched.mem.maxmemctl = 0`) and Memory|Balloon 0.
- From the author's samples (docx, 2026-11-12): a 64 GB VM, heavy swap and compression over 7 days, Consumed flat under the effective limit; the knowledge base keeps that example.
- Changed in the 2026-11-15 audit: stem gives the balloon setting and Balloon 0; E (Contention is the swap-in wait, redundancy #37, homed in 0149/0392) replaced by the decompression-vs-swap-in fact; L and M added.

## Metadata
```yaml
id: "0140"
title: "Swapped and Compressed moving in opposite directions"
product: [vsphere, vcf-operations, windows]
technology: [memory]
task: troubleshoot
level: 400
answer_type: deterministic
answer: [A,C,E,I]
misconception: [B,G,H,L]
input: [table]
object: [vm]
tool: [vcf-operations]
knowledge:
  - vsphere/technology/memory/concepts/swap-and-compression
  - vsphere/technology/memory/concepts/memory-limit
  - vsphere/technology/memory/vm-memory-latency-high
  - vsphere/technology/memory/metrics/virtual-motherboard/granted
  - vsphere/technology/memory/metrics/virtual-motherboard/overhead
  - vsphere/architecture/resource-controls
  - vsphere/technology/memory/metrics/virtual-motherboard/swap-in-rate
  - vsphere/technology/memory/metrics/virtual-motherboard/compressed
knowledge_main: vsphere/technology/memory/concepts/swap-and-compression
attachments:
  - 0140/vm-memory-3-days.csv
origin: book
source_path: "Author samples (docx, 2026-11-12) > Swap and compress move in opposite directions"
misconception_type: [provider-vs-consumer, cumulative-vs-current]
pair: "0291"
status: draft
```
