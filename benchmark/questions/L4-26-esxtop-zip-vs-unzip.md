# Which VMs wait for memory now?

## Prompt
- An ESXi 9.1 host has been in the hard memory state for 20 minutes.
- esxtop, memory panel (m) with the balloon, compression and swap fields added, MB and MB/s:

```text
NAME      MEMSZ   MCTLSZ  SWCUR  SWR/s  SWW/s  ZIP/s  UNZIP/s  CACHEUSD
vm-a      32768   2100    3400   0.00   18.40  6.20   0.00     610
vm-b      16384   900     2800   9.60   0.00   0.00   4.10     420
vm-c      65536   0       0      0.00   0.00   0.00   0.00     0
vm-d      8192    1500    6100   0.00   0.00   0.00   0.00     0
```

Which statements are correct?

- A. vm-b waits for memory now: it reads pages back from its swap file and from its compression cache.
- B. vm-a waits for memory now: ESXi compresses and swaps its pages out, and each page written out stalls a vCPU.
- C. vm-a shows the host short of memory: its pages go out, which costs vm-a no wait until it touches them again.
- D. vm-d is the slowest VM on the host: it holds the most memory in its swap file, 6,100 MB of its 8 GB.
- E. vm-a's compressed pages still take host memory: CACHEUSD sits in DRAM, each page at a quarter or half its size.
- F. For vm-b, a page read back from the compression cache costs far less time than one read from the swap file.

## Likely wrong answer
B: reading compression and swap-out as the VM waiting. Or D: the largest SWCUR read as the slowest VM.

## Expected key points
- Answer: A, C, E, F.
- A: SWR/s and UNZIP/s bring pages back into memory. The vCPU that touched the page waits for it: memory contention.
- B is wrong and C is right: ZIP/s and SWW/s move pages out. That is the host's capacity problem; a page that is not touched again costs the VM no wait.
- D is wrong: SWCUR is the amount in the swap file, not activity. With SWR/s and UNZIP/s at 0, vm-d does not wait now.
- E: the compression cache is host memory in use. Compression frees 2 or 3 KB of each 4 KB page; the compressed result stays in DRAM, inside host Consumed.
- F: decompression is in DRAM and costs far less than a swap-in from disk; that is why ESXi compresses before it swaps.

## Notes
- Revised 2026-11-12 (question set 1.0): the esxtop screenshot that was to be supplied is now an esxtop excerpt typed as text.

## Metadata
```yaml
id: "0068"
title: "Which VMs wait for memory now?"
product: [vsphere]
technology: [memory]
task: read-metric
level: 400
answer_type: deterministic
input: [text]
object: [vm, esxi]
tool: [esxtop]
knowledge:
  - vsphere/tools/esxtop/memory
  - vsphere/technology/memory/concepts/swap-and-compression
  - vsphere/technology/memory/metrics/host/compressed
knowledge_main: vsphere/tools/esxtop/memory
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
answer: [A, C, E, F]
misconception: [B, D]
misconception_type: [reclamation-as-contention, cumulative-vs-current]
status: draft
```
