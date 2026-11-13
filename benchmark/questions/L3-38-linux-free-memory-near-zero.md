# Linux free memory near zero

## Prompt
- A Linux VM with 32 GB runs a reporting database. `free -m` today:

```text
               total        used        free      shared  buff/cache   available
Mem:           32000        9100         310         120       23490       22900
Swap:           4095        1210        2885
```

- `sar -W` for the last 7 days: `pswpin/s` and `pswpout/s` are 0.00 in every sample.
- `/proc/pressure/memory`: `some avg10=0.00 avg60=0.00 avg300=0.00`.
- The capacity team flags the VM: free memory below 1% and swap in use. They request 16 GB more.

Which statements are correct?

- A. Add 16 GB: free memory below 1% means Linux has run out of RAM.
- B. Keep 32 GB: `available` includes cache Linux can drop, and no page moved to or from swap this week.
- C. Add memory: 1.2 GB of swap used shows that the VM is swapping now.
- D. Add memory: the database cannot use `buff/cache`, so only 310 MB is left for it.
- E. Turn off swap, so Linux keeps all its pages in RAM and frees the 1.2 GB.

## Likely wrong answer
A or C: free memory near 0, or swap in use, read as a current shortage.

## Expected key points
- Answer: B.
- A is wrong: Linux fills free memory with page cache. Read `available` (MemAvailable), swap activity and memory pressure, not `free`.
- B is correct: about 22.9 GB is available; swap-in and swap-out were 0 for a week and memory pressure is 0, so no task waited for memory. The 1.2 GB in swap are pages moved out earlier and not touched since.
- C is wrong: swap used is an amount left by past activity. Pages stay in swap until they are touched again; a current shortage shows as swap-in and swap-out rates and memory pressure.
- D is wrong: page cache is given back to applications on demand; that is why it counts in `available`.
- E is wrong: it forces the 1.2 GB back into RAM for nothing, and removes the safety net for a real peak.

## Notes
- Paired with the Windows free memory question (0264): the same concept on another Guest OS (benchmark/design.md, section 5).
- `free` columns (procps-ng free(1)): `available` estimates memory available for new applications without swapping, including reclaimable page cache. https://man7.org/linux/man-pages/man1/free.1.html

## Metadata
```yaml
id: "0263"
title: "Linux free memory near zero"
product: [linux]
technology: [memory]
task: decide-capacity
level: 300
answer_type: deterministic
input: [text]
object: [guest-os]
tool: [guest-os-tools]
knowledge:
  - guest-os/system/troubleshooting/linux-os-slow
  - guest-os/system/concepts/guest-os-sizing
knowledge_main: guest-os/system/troubleshooting/linux-os-slow
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12 for the Guest OS slots (project/plan.md, M2)"
answer: [B]
misconception: [A, C]
misconception_type: [consumption-as-contention, reclamation-as-contention]
status: draft
```
