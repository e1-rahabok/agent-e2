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

- A. vm-b is waiting for memory in this interval.
- B. Pages that ESXi compresses or swaps out of vm-a stall vm-a's vCPUs while they go out.
- C. vm-a's ZIP/s and SWW/s show that the host is still reclaiming memory.
- D. vm-d, with the largest SWCUR, is the VM that waits most for memory now.
- E. vm-a's compression cache (CACHEUSD) is host DRAM in use.
- F. For vm-b, a page read back from the compression cache costs far less time than one read from the swap file.
- G. vm-d's swapped pages carry no risk for vm-d.
- H. Move vm-d off the host first, since it suffers most.

## Likely wrong answer
B: reading compression and swap-out as the VM waiting. Or D: the largest SWCUR read as the slowest VM.

## Expected key points
- Answer: A, C, E, F.
- A is true: SWR/s and UNZIP/s bring pages back into memory. The vCPU that touched the page waits for it: memory contention.
- B is false: ZIP/s and SWW/s move pages out; a page that is not touched again costs the VM no wait. Only swap-in and decompression make the vCPU wait.
- C is true: compression and swap-out are a capacity problem: the host is short of RAM and is taking pages back.
- D is false: SWCUR is the amount in the swap file, not activity. With SWR/s and UNZIP/s at 0, vm-d does not wait now.
- E is true: the compression cache is host memory in use. Compression frees 2 or 3 KB of each 4 KB page; the compressed result stays in DRAM, inside host Consumed.
- F is true: decompression is in DRAM and costs far less than a swap-in from disk; that is why ESXi compresses before it swaps.
- G is false: the more swapped, the higher the chance of a future hit; if vm-d's guest touches those pages, it waits. This is the over-correction of D.
- H is false: vm-d does not wait now; vm-b does. Moving vm-d first follows the misreading of SWCUR.

## Notes
- Revised 2026-11-12: the esxtop screenshot that was to be supplied is now an esxtop excerpt typed as text.
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): one fact per option (A, B, D, E); C no longer negates B; G the over-correction and H the wrong action added. Key unchanged: A, C, E, F.

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
  - vsphere/technology/memory/concepts/ballooning
knowledge_main: vsphere/tools/esxtop/memory
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05"
answer: [A, C, E, F]
misconception: [B, D]
misconception_type: [reclamation-as-contention, cumulative-vs-current]
pair: "0389"
status: draft
```
