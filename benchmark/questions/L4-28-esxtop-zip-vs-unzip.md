# Which VMs wait for memory now?

## Prompt
The attached screenshot is the esxtop memory panel (m) of an overcommitted ESXi host, with the compression and swap columns shown.

- VM-A shows ZIP/s and SWW/s above 0, and UNZIP/s and SWR/s at 0.
- VM-B shows UNZIP/s and SWR/s above 0.

Which statements are correct? Choose all that apply.

- A. VM-B waits for memory now: its pages are read back from the compression cache and the swap file.
- B. VM-A waits for memory now, because the host compresses its pages.
- C. VM-A shows a capacity signal: the host is short of RAM and moves its pages out, which costs the VM nothing until it touches them again.
- D. SWCUR shows the swap activity of the last second.

## Input to supply
- Tool: esxtop on one ESXi 9.1 host under memory pressure, memory panel (press m), compression and swap fields added (press f).
- Must show the columns MCTLSZ, SWCUR, SWR/s, SWW/s, ZIP/s, UNZIP/s, CACHEUSD for at least 4 VMs.
- Condition for the key: one VM (label it VM-A) has ZIP/s and SWW/s above 0 with UNZIP/s and SWR/s at 0; another VM (VM-B) has UNZIP/s and SWR/s above 0.
- How to produce it: overcommit a lab host until it reaches the hard state, then start a memory load inside VM-B.
- Save as `benchmark/questions/68/esxtop-memory-compression-swap.png`.

## Likely wrong answer
B: reading ZIP/s as the VM waiting.

## Expected key points
- Answer: A, C.
- UNZIP/s and SWR/s are reads back into memory: the vCPU waits for them, so the VM has memory contention.
- ZIP/s and SWW/s move pages out: a capacity problem of the host. Unused pages that are zipped or swapped cause no contention.
- D is wrong: SWCUR is the current swapped amount, usually of inactive pages, not a rate.

## Notes
- Previous id: question-0068 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0068"
title: "Which VMs wait for memory now?"
product: [vsphere]
technology: [memory]
task: read-metric
level: 400
answer_type: deterministic
input: [screenshot]
knowledge:
  - vsphere/tools/esxtop/memory
  - vsphere/technology/memory/concepts/swap-and-compression
attachments:
  - 0068/esxtop-memory-compression-swap.png
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
answer: [A, C]
trap: [B]
status: awaiting-input
```
