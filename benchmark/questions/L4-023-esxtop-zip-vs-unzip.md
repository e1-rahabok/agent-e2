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

- A. In this interval the vCPUs of vm-b are waiting for memory.
- B. Pages that ESXi compresses or swaps out of vm-a stall vm-a's vCPUs while they go out.
- C. vm-a's ZIP/s and SWW/s show that the host is still reclaiming memory.
- D. vm-d, with the largest SWCUR, is the VM that waits most for memory now.
- E. vm-a's compression cache (CACHEUSD) is host DRAM in use.
- F. For vm-b, a read from the compression cache costs far less than one from the swap file.
- G. vm-d's swapped pages carry no risk for vm-d's performance later.
- H. Move vm-d off the host first, to end its memory wait now.
- I. vm-a's MCTLSZ of 2,100 MB shows that its balloon is inflating in this interval.

## Answers
A, C, E, F

## Explanation
- A is correct: SWR/s and UNZIP/s bring pages back into memory. The vCPU that touched the page waits for it: memory contention.
- B is wrong: ZIP/s and SWW/s move pages out; a page that is not touched again costs the VM no wait. Only swap-in and decompression make the vCPU wait.
- C is correct: compression and swap-out are a capacity problem: the host is short of RAM and is taking pages back.
- D is wrong: SWCUR is the amount in the swap file, not activity. With SWR/s and UNZIP/s at 0, vm-d does not wait now.
- E is correct: the compression cache is host memory in use. Compression frees 2 or 3 KB of each 4 KB page (4:1 to 1 KB or 2:1 to 2 KB; a page that does not reach 2 KB is swapped instead); the compressed result stays in DRAM, inside host Consumed.
- F is correct: decompression is in DRAM and costs far less than a swap-in from disk; that is why ESXi compresses before it swaps.
- G is wrong: the more swapped, the higher the chance of a future hit; if vm-d's guest touches those pages, it waits. This is the over-correction of D.
- H is wrong: vm-d does not wait now; vm-b does. Moving vm-d first follows the misreading of SWCUR.
- I is wrong: MCTLSZ is the memory the balloon holds now; above 0 says the host reclaimed it at some point, not that it reclaims now (MCTLTGT and the host state show that). In the hard state ballooning stops inflating.
- Misconception: B: reading compression and swap-out as the VM waiting. Or D: the largest SWCUR read as the slowest VM.

## Notes
- Revised 2026-11-12: the esxtop screenshot that was to be supplied is now an esxtop excerpt typed as text.
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): one fact per option (A, B, D, E); C no longer negates B; G the over-correction and H the wrong action added. Key unchanged: A, C, E, F.
- Changed in the 2026-11-15 audit: H reworded without the "since it suffers most" reason clause; I added (MCTLSZ, a current balloon size, read as ballooning now: esxtop/memory MCTLSZ, host-memory-states Hard). Its practical half 0389 was retired, so 0068 has no pair.

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
  - vsphere/technology/memory/concepts/host-memory-states
knowledge_main: vsphere/tools/esxtop/memory
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-05"
misconception: [B, D]
misconception_type: [reclamation-as-contention, cumulative-vs-current]
status: draft
```
