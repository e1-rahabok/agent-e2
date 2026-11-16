# Compressed memory and the Consumed drop

## Prompt
- erp-app-11 is a vendor appliance VM on Linux with 64 GB of memory configured, no reservation and no limit. The vendor image blacklists the vmw_balloon module.
- At 14:10 an HA failover restarted several VMs on its host, esx-15. The esxtop memory state of esx-15 was hard from 14:10 to 14:30, then high again.
- vCenter, Real-time chart of erp-app-11:

| Counter | 14:05 | 14:35 |
|---|---|---|
| Consumed | 61.0 GB | 54.6 GB |
| Compressed | 0 | 2.0 GB |
| Memory saved by zipping | 0 | 5.6 GB |
| Swapped | 0 | 0.8 GB |
| Ballooned memory | 0 | 0 |

- The appliance's load is steady all afternoon. Swap in rate and Decompression rate stay at 0 from 14:05 to 14:35.
- The capacity manager puts "compression saved 2.0 GB on erp-app-11" on a slide. An administrator replies: "Consumed fell by 6.4 GB, but only 2.8 GB was compressed or swapped. The counters disagree."

Which statements are correct?

- A. Compression freed about 5.6 GB of host memory from erp-app-11.
- B. The 2.0 GB shown as Compressed is the memory that compression freed.
- C. About 7.6 GB of the VM's memory went into compression.
- D. The 2.0 GB compressed result is still counted in the VM's Consumed.
- E. Compression freed nothing, because compressed pages stay in host DRAM and count in Consumed at their full size.
- F. Consumed fell by 6.4 GB: the 5.6 GB saved by compression plus the 0.8 GB swapped out.
- G. The 0.8 GB swapped shows that the VM's compression cache was full.
- H. Nearly all compressed pages shrank to 1 KB: at 2 KB each, 7.6 GB of pages would leave about 3.8 GB.
- I. The pages that went into compression still count in the VM's Granted.
- J. Report the 5.6 GB on the slide as savings next to page sharing, since compression frees memory the same way.

## Likely wrong answer
B: "Compressed is the memory compression saved." The administrator's reading that the counters disagree also rests on B.

## Expected key points
- Answer: A, C, D, F, H.
- A is correct: Memory saved by zipping (`mem.zipSaved`) is the memory compression freed.
- B is wrong: the misconception of ESXi Memory Compressed ("Compressed is the memory freed by compression"). Compressed is the result kept in the compression cache in DRAM; the freed amount is `mem.zipSaved`.
- C is correct: the pages before compression are the result plus the saving: 2.0 + 5.6 = 7.6 GB.
- D is correct: the compressed result stays in Consumed; only the freed part leaves (a 4 KB page compressed to 1 KB keeps 1 KB in Consumed).
- E is wrong: over-correction. The pages stay in DRAM at their compressed size, so the saving left Consumed.
- F is correct: Consumed excludes swapped memory and the memory compression freed: 61.0 - 54.6 = 6.4 GB = 5.6 + 0.8. With no swap in and no decompression, nothing came back in the window.
- G is wrong: the compression cache of a VM is capped by Mem.MemZipMaxPct, 10% of its memory by default: 6.4 GB for 64 GB. 2.0 GB is below it. Pages that do not compress to 2 KB or smaller are swapped instead.
- H is correct: ESXi keeps a page compressed at 4:1 (1 KB) or 2:1 (2 KB). At 2:1 throughout, 7.6 GB gives 3.8 GB; at 4:1 throughout, 1.9 GB. 2.0 GB is close to 1.9 GB.
- I is wrong: Granted excludes ballooned, swapped, compressed and host-cache pages: a compressed page is not directly accessible.
- J is wrong: the wrong action. Compression is not counted as savings, because decompression costs performance; page sharing is.

## Notes
- Sources: the knowledge base, ESXi Memory Compressed (result, not savings; `mem.zipSaved`; Mem.MemZipMaxPct), VM Memory Consumed (compressed result stays in Consumed), Swap and compression (4:1 and 2:1, swap when a page does not reach 2 KB), VM Memory Granted (excludes compressed pages), VM Memory Shared (compression not counted as savings).
- "Memory saved by zipping" is the vSphere Client label of `mem.zipSaved`. The VM has no balloon driver, so a hard state reclaims by compression and swap only.

## Metadata
```yaml
id: "0452"
title: Compressed memory and the Consumed drop
product: [vsphere, linux]
technology: [memory]
task: read-metric
level: 400
answer_type: deterministic
input: [text]
object: [vm, esxi]
tool: [vcenter, esxtop]
knowledge:
  - vsphere/technology/memory/metrics/host/compressed
  - vsphere/technology/memory/metrics/virtual-motherboard/consumed
  - vsphere/technology/memory/metrics/virtual-motherboard/compressed
  - vsphere/technology/memory/concepts/swap-and-compression
  - vsphere/technology/memory/metrics/virtual-motherboard/granted
  - vsphere/technology/memory/metrics/virtual-motherboard/shared
knowledge_main: vsphere/technology/memory/metrics/host/compressed
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-15, question bank audit gap: vsphere/technology/memory/metrics/host/compressed"
answer: [A, C, D, F, H]
misconception: [B]
misconception_type: [label-read-as-model, unit-and-normalization]
status: draft
```
