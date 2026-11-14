# Swapped and Compressed moving in opposite directions

## Prompt
- A Linux VM with 64 GB of memory runs an Oracle E-Business Suite test environment.
- The application team says batch jobs run slower than on the old physical server. The VM has had about 15 GB swapped or compressed all week.
- The ESXi host has more than 300 GB free. No other VM on the host has swapped or compressed memory.
- [The attached VCF Operations chart export](0140/vm-memory-7-days.csv) covers the VM for the last 7 days, in 1-hour samples.

Why is Consumed flat, why do Swapped and Compressed move in opposite directions, and what do you change? Which statements are correct?

- A. The VM's own memory limit is the cause: Consumed sits flat just under an Effective limit that is flat at 40.44 GB.
- B. The host is running out of memory, and ESXi is swapping this VM to free memory for the others.
- C. The two move in opposite directions: touched pages are read back (Swapped falls) while others are compressed to stay under the limit.
- D. Each fall of Swapped shows that the memory pressure on the VM has eased, and the VM is getting its pages back.
- E. Contention rises at those moments: each page read back is a wait for the vCPU that touched it.
- F. Pages swapped out make the VM wait even when the guest never touches them again, so swap-out is the slowness.
- G. Moving the VM to a host with more free memory stops the swapping and the compression of its pages.
- H. Configuring the VM with more than 64 GB stops the swapping, as the guest gets more room for its working set.
- I. Remove the limit, or raise it to what the guest needs, after finding out why it was set.
- J. Consumed flat for 7 days shows that the guest's memory demand is steady, so memory is not the problem.

## Likely wrong answer
- B: "The host is running out of memory and swaps the VM."
- G: "Move the VM to a host with more free memory."
- H: "Give the VM more than 64 GB."

## Expected key points
- Answer: A, C, E, I.
- A true: Effective limit is 40.44 GB in every sample and Consumed stays at 38.3-39.6 GB just under it; the host has over 300 GB free and no other VM is reclaimed.
- B false: with free host memory and no other VM swapped or compressed, the cause is a limit on the VM (or its pool), not the host.
- C true: in and out run at the same time on different pages; at each Compressed jump (up to 5.3 GB) Swapped drops (to as low as 10 GB).
- D false: Swapped falls because the guest asked for swapped pages (swap-in, the costly part); other pages go out at the same time to stay under the limit.
- E true: Contention jumps to 4-7% at the samples where Swapped falls and Compressed rises, and stays below 1% otherwise.
- F false: swap-out is not contention by itself; only swap-in, when the guest asks for the page, makes the vCPU wait.
- G false: the limit moves with the VM; the host was never short.
- H false: the limit, not the configured size, caps Consumed; more configured memory only adds pages to reclaim.
- I true: the limit is the cause; removing it or raising it to the guest's need is the fix.
- J false: Consumed is flat because the limit caps it; the guest keeps touching pages that ESXi swaps and compresses.

## Notes
- Not key points (they cannot be derived from the CSV alone, and 0141 tests them): the effective limit includes the VM's overhead, so Consumed stays a little below it; Granted ignores the limit and sits above it.
- An answer that also says the limit can make ESXi balloon the VM is not penalized: vSphere 9.1 Monitoring and Performance, memory troubleshooting, links high balloon or swap with a VM or pool at its resource limit (open with the author).
- From the author's samples (docx, 2026-11-12): a 64 GB VM, heavy swap and compression over 7 days, Consumed flat under the effective limit. The CSV is generated to reproduce the author's chart (Effective limit 40.44 GB, Consumed about 39.6 GB, Granted about 42.7 GB, Swapped about 14.7 GB falling when Compressed jumps, up to 5.3 GB).
- The knowledge base holds the same example: swap-and-compression, section Example: limit, swap and compress in opposite directions.
- Converted from judged to multiple choice (Q199 F, 2026-11-14). No option on ballooning under a limit (open author question Q214) or on why Consumed stays a little below the effective limit (open author question Q205).

## Metadata
```yaml
id: "0140"
title: "Swapped and Compressed moving in opposite directions"
product: [vsphere, vcf-operations, linux]
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
knowledge_main: vsphere/technology/memory/concepts/swap-and-compression
attachments:
  - 0140/vm-memory-7-days.csv
origin: book
source_path: "Author samples (docx, 2026-11-12) > Swap and compress move in opposite directions"
misconception_type: [provider-vs-consumer, cumulative-vs-current]
status: draft
```
