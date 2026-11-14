# Swapped and Compressed moving in opposite directions

## Prompt
- A Windows Server VM with 24 GB of memory runs SQL Server for the nightly reports.
- The report team says the reports, which run every night from 01:00 to 03:00, take twice as long as on the old cluster.
- The ESXi host has more than 200 GB free. No other VM on the host has swapped or compressed memory.
- [The attached VCF Operations export](0140/vm-memory-3-days.csv) covers the VM for the last 3 days, in 30-minute samples.

Why do the reports slow down, and what do you change? Which statements are correct?

- A. A memory limit on the VM or on its resource pool caps the VM's memory.
- B. The host is short of memory, and ESXi swaps this VM to free memory for the others.
- C. During each report run, the guest reads swapped pages back while ESXi compresses other pages to stay under the cap.
- D. Each fall of Swapped shows that the memory pressure on the VM has eased.
- E. The Contention during the runs is the wait for pages being brought back into memory.
- F. Pages swapped out make the VM wait even when the guest never touches them again.
- G. Moving the VM to a host with more free memory stops the swapping and the compression of its pages.
- H. Configuring the VM with more than 24 GB stops the swapping.
- I. Remove the limit, or raise it to what the guest needs, after finding out why it was set.
- J. A Consumed value that stays flat for 3 days shows that memory is not the cause of the slow reports.
- K. With the cap in place, the VM waits for memory all day, not only during the runs.

## Likely wrong answer
- B: "The host is running out of memory and swaps the VM."
- G: "Move the VM to a host with more free memory."
- H: "Give the VM more memory."

## Expected key points
- Answer: A, C, E, I.
- A true: Consumed stays flat (15.66-15.83 GB) just below the Effective limit (16.19 GB in every sample), while the host has over 200 GB free and no other VM is reclaimed: the cause is a limit on the VM or its pool, not the host.
- B false: with free host memory and no other VM swapped or compressed, the host is not short.
- C true: in and out run at the same time on different pages; in each run Swapped falls (about 6.12 to 4.86, 4.86 to 3.78 and 3.80 to 2.98 GB) while Compressed rises (about 0.24 to 0.80, 0.80 to 1.27 and 1.28 to 1.66 GB), and Consumed stays flat.
- D false: Swapped falls because the guest asked for swapped pages (swap-in, the costly part); other pages go out at the same time to stay under the limit.
- E true: Contention is about 3.4-6.2% in the samples of 01:00 to 02:30 and at most 0.5% at other times: each page read back is a wait for the vCPU that touched it.
- F false: swap-out is not contention by itself; only swap-in, when the guest asks for the page, makes the vCPU wait.
- G false: the limit moves with the VM; the host was never short.
- H false: the limit, not the configured size, caps Consumed; more configured memory changes nothing while the limit stays.
- I true: the limit is the cause; removing it or raising it to the guest's need is the fix.
- J false: Consumed is flat because the limit caps it; the guest keeps touching pages that ESXi swaps and compresses.
- K false: outside the runs Contention stays at 0.5% or less; swapped pages the guest does not touch cost no wait. This is the over-correction of A: a limit read as a wait at every moment.

## Notes
- Rewritten 2026-11-14 (project/question-pairing-2026-11-14.md, pair A14) (author approved, 2026-11-14): the old scenario (a 64 GB Linux VM, Oracle E-Business Suite, 7 days in 1-hour samples, an effective limit of 40.44 GB) was a near-copy of the knowledge example in swap-and-compression, section Example: limit, swap and compress in opposite directions. New scenario: a 24 GB Windows SQL Server VM whose nightly reports read swapped pages back; a new CSV from a seeded script (seed 14020261114, 3 days, 30-minute samples). The old CSV is in project/archive/benchmark-questions/attachments.
- Old option A ("Consumed stays flat below an Effective limit that reads 40.44 GB in every sample") is replaced by a statement of the cause alone: no option reads the gap between Consumed and the effective limit, or what the effective limit adds to the configured limit (open author question Q205). Granted, which ignores the limit and sits above it, is not an option either.
- No option on ballooning under a limit (open author question Q214).
- K, the over-correction, is added. Key unchanged: A, C, E, I.
- From the author's samples (docx, 2026-11-12): a 64 GB VM, heavy swap and compression over 7 days, Consumed flat under the effective limit; the knowledge base keeps that example.
- Converted from judged to multiple choice (Q199 F, 2026-11-14).

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
misconception: [B,G,H]
input: [table]
object: [vm]
tool: [vcf-operations]
knowledge:
  - vsphere/technology/memory/concepts/swap-and-compression
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
