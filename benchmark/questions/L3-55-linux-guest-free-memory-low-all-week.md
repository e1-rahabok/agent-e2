# Linux guest free memory low all week

## Prompt
See [the VCF Operations guest memory charts](0387/vcf-operations-linux-vm-guest-memory-7-days.png) and [the `sar -W` output of the busiest day](0387/linux-sar-swap-busiest-day.png).

- A Linux VM runs a reporting database.
- The capacity report flags it for low guest free memory all week. The capacity team asks for 50% more memory.

Which statements are correct?

- A. Guest free memory this low all week shows that Linux has run out of memory.
- B. Linux keeps page cache in memory its applications leave unused, and gives it back on demand.
- C. Swap-in and swap-out at 0 show that no page moved to or from swap on that day.
- D. Guest Needed Memory, not guest free memory, is the input for the VM's memory size.
- E. Give the VM the 50% more memory the capacity team asks for, to end its shortage.
- F. Cut the VM to its current Needed Memory value now, since the rest of its memory is unused.
- G. Linux counts the page cache it holds in its free memory figure.

## Input to supply
- Product: VCF Operations 9.1; a Linux VM (RHEL 9 or Ubuntu 22.04 or later) with open-vm-tools, 16 GB or more, running a database or a file-reading workload that fills the page cache.
- Screen 1: VCF Operations > the VM > Metrics, last 7 days, the Guest group: free memory and Needed Memory as two charts, plus the VM's configured memory (Memory|Total Capacity) so the shares can be read. Save as `benchmark/questions/0387/vcf-operations-linux-vm-guest-memory-7-days.png`.
- Screen 2: a terminal on the VM with `sar -W -f /var/log/sa/saDD` for the busiest day of the 7 (the day with the highest Needed Memory), the whole day visible with its Average line. Save as `benchmark/questions/0387/linux-sar-swap-busiest-day.png`.
- Condition the key depends on:
  - guest free memory below 3% of the configured memory for most of the 7 days;
  - Guest Needed Memory between 20% and 45% of the configured memory, its peak below 60%;
  - `pswpin/s` and `pswpout/s` at 0.00 in every sample of the day shown.
- How to produce it in a lab: read files larger than the VM's memory (for example `cat` of large files to `/dev/null` every hour) so the page cache fills memory, with the database or a small process holding its own memory well below the configured size.
- Masking: mask every VM, host, datastore and cluster name, and the host name in the shell prompt.

## Likely wrong answer
A: "Free memory near 0, so Linux has run out of memory: add memory."

## Expected key points
- Answer: B, C, D.
- A false: Linux fills free memory with page cache. Read the memory available to applications (MemAvailable), swap activity and memory pressure, not free memory.
- B true: page cache is given back to applications on demand; that is why free memory near 0 with healthy other counters means no waste.
- C true: `sar -W` shows pages swapped in and out per second; 0.00 all day means no task waited for swap on the busiest day.
- D true: Guest OS sizing uses Needed Memory, which includes part of the cache, plus headroom; free memory is waste for memory, not headroom.
- E false: the wrong action. Nothing shows a shortage; added memory would fill with more page cache and free memory would stay low.
- F false: over-correction. The new size is the peak of Needed Memory over the business cycle plus headroom, and a cut is made in steps with a check after each.
- G false: free memory excludes the page cache; that is why it is low while plenty of memory is available.

## Notes
- Paired with 0263 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item C10.
- The swap rates come from `sar -W` in the guest: the knowledge base does not state which Linux swap counters VMware Tools collects for VCF Operations.
- The key holds whenever the condition of `## Input to supply` holds.
- Written 2026-11-14 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after approval (design.md, section 6.2).

## Metadata
```yaml
id: "0387"
title: "Linux guest free memory low all week"
product: [linux, vcf-operations]
technology: [memory]
task: decide-capacity
level: 300
answer_type: deterministic
input: [screenshot]
object: [guest-os]
tool: [vcf-operations, guest-os-tools]
knowledge:
  - guest-os/system/troubleshooting/linux-os-slow
  - guest-os/system/concepts/guest-os-sizing
knowledge_main: guest-os/system/troubleshooting/linux-os-slow
attachments:
  - 0387/vcf-operations-linux-vm-guest-memory-7-days.png
  - 0387/linux-sar-swap-busiest-day.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C10"
answer: [B, C, D]
misconception: [A]
misconception_type: [consumption-as-contention]
pair: "0263"
status: awaiting-input
```
