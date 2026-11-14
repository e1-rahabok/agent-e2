# esxtop: which VMs wait on swapped memory now

## Prompt
See [the esxtop memory panel](0389/esxtop-memory-panel-swap-compression.png).

- The ESXi host has been short of memory for half an hour, and users of several applications complain.
- The on-call engineer plans to tell the owner of the VM with the most memory in its swap file that their VM is the slow one, and to move that VM to another host first.

Which statements are correct?

- A. The VM with the largest SWCUR is not waiting on memory now: its SWR/s and UNZIP/s are 0.
- B. A VM with SWR/s above 0 waits now: each page read back from swap stalls the vCPU that touched it.
- C. A VM with only SWW/s or ZIP/s above 0 is not waiting: pages moved out cost it nothing until touched.
- D. The VM with the largest SWCUR is the VM that waits longest on memory right now.
- E. A VM with ZIP/s above 0 is waiting now for its compressed pages to be decompressed.
- F. The memory counted in SWCUR can no longer slow its VM, whatever the VM does next.
- G. Moving the VM with the largest SWCUR first ends the longest memory wait on the host.
- H. A page brought back by UNZIP/s costs the VM far less time than a page brought back by SWR/s.

## Input to supply
- Product: ESXi 9.1, esxtop over SSH. One host under memory pressure (state soft or hard in the header).
- Screen: esxtop, memory panel (`m`), fields added with `f`: MCTLSZ, SWCUR, SWR/s, SWW/s, ZIP/s, UNZIP/s, CACHEUSD (keep NAME and MEMSZ). Show the header lines and at least 3 VM rows, sorted by SWCUR. Save as `benchmark/questions/0389/esxtop-memory-panel-swap-compression.png`.
- Condition the key depends on, all on the one screen:
  - VM X: the largest SWCUR on the screen (1 GB or more), with SWR/s and UNZIP/s at 0.00;
  - VM Y (not X): SWR/s above 0 (1 MB/s or more);
  - VM Z (not X, not Y): SWW/s or ZIP/s above 0, with SWR/s and UNZIP/s at 0.00.
- How to produce it in a lab: overcommit a small host with VMs that touch their memory. Let VM X touch all its memory and then go idle (its pages are swapped and stay cold); let VM Y loop over all its memory (it reads swapped pages back); power on VM Z or start its load last (its pages are being moved out).
- Masking: mask every VM, host, datastore and cluster name (the NAME column and the host name).

## Likely wrong answer
D: "The VM with the most memory in swap is the slowest." Or E: compression read as the VM waiting.

## Expected key points
- Answer: A, B, C, H.
- A true: SWCUR is the amount in the swap file now, not activity. With nothing read back from swap or the compression cache, that VM does not wait now.
- B true: SWR/s brings pages back into memory; the vCPU that touched the page waits for it. That is memory contention.
- C true: SWW/s and ZIP/s move pages out: a capacity problem of the host. A page that is not touched again costs the VM no wait.
- D false: the largest amount swapped is not the largest wait; the wait is in SWR/s and UNZIP/s.
- E false: ZIP/s is compression, pages going out. UNZIP/s is the wait.
- F false: over-correction. A swapped page costs no wait until the VM touches it; then the vCPU waits for the swap-in. The more is swapped, the higher the chance.
- G false: the wrong action from D. That VM does not wait now; the VMs with SWR/s or UNZIP/s above 0 do.
- H true: decompression is in DRAM and costs far less than a swap-in from disk; that is why ESXi compresses before it swaps.

## Notes
- Paired with 0068 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item C15.
- The options name VMs by their values, not by name, because the names are masked.
- The key holds whenever the condition of `## Input to supply` holds.
- Written 2026-11-14 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after approval (design.md, section 6.2).

## Metadata
```yaml
id: "0389"
title: "esxtop: which VMs wait on swapped memory now"
product: [vsphere]
technology: [memory]
task: troubleshoot
level: 400
answer_type: deterministic
input: [screenshot]
object: [vm, esxi]
tool: [esxtop]
knowledge:
  - vsphere/tools/esxtop/memory
  - vsphere/technology/memory/concepts/swap-and-compression
  - vsphere/technology/memory/metrics/virtual-motherboard/latency
knowledge_main: vsphere/tools/esxtop/memory
attachments:
  - 0389/esxtop-memory-panel-swap-compression.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C15"
answer: [A, B, C, H]
misconception: [D]
misconception_type: [reclamation-as-contention, cumulative-vs-current]
pair: "0068"
status: awaiting-input
```
