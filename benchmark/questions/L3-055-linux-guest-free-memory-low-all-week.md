# Linux guest free memory low all week

## Prompt
See [the VCF Operations guest memory charts](0387/vcf-operations-linux-vm-guest-memory-7-days.png) and [the terminal output from the VM](0387/linux-terminal-swap-and-pressure.png).

- A Linux VM runs nginx and serves a static file archive for a web site.
- A new monitoring rule on guest free memory has fired every day this week. The ticket it opened asks to double the VM's memory.

Which statements are correct?

- A. Free memory this low for a week means Linux has no memory left for its applications.
- B. Linux keeps file data as page cache in memory its applications leave unused, and hands it back on demand.
- C. Linux has not swapped a page in or out since it last booted.
- D. The memory pressure line shows tasks stalled on memory in the last five minutes.
- E. Guest Needed Memory stays below half of the VM's memory at every point of the week.
- F. Double the VM's memory, as the ticket asks.
- G. Cut the VM to its current Needed Memory now, since the rest of its memory holds nothing of use.
- H. Linux counts the page cache it holds in MemFree.
- I. Guest Needed Memory, not guest free memory, is the input for the VM's memory size.

## Input to supply
- Product: VCF Operations 9.1; a Linux VM (RHEL 9 or Ubuntu 22.04 or later) with open-vm-tools, 8 GB or more, running nginx (or any reader) over a file set larger than the VM's memory, so that the page cache fills memory.
- Screen 1: VCF Operations > the VM > Metrics, last 7 days, three charts stacked: Guest|Free Memory, Guest|Needed Memory and Mem|Total Capacity (KB) (all three are enabled by default in the VCF Operations 9.1 metric list). Save as `benchmark/questions/0387/vcf-operations-linux-vm-guest-memory-7-days.png`.
- Screen 2: a terminal on the VM showing, in one screen, `uptime`, `grep -E '^pswp(in|out)' /proc/vmstat` and `cat /proc/pressure/memory`. Save as `benchmark/questions/0387/linux-terminal-swap-and-pressure.png`.
- Condition the key depends on:
  - Guest|Free Memory below 5% of Mem|Total Capacity at every point of the 7 days;
  - Guest|Needed Memory between 20% and 45% of Mem|Total Capacity at every point of the 7 days;
  - `uptime` above 8 days;
  - `pswpin 0` and `pswpout 0`;
  - `/proc/pressure/memory`: `avg10`, `avg60` and `avg300` all 0.00 on both the `some` and the `full` line.
- Masking: mask every VM, host, datastore and cluster name, and the host name in the shell prompt.

## Likely wrong answer
A: "Free memory near 0 for a week, so Linux is out of memory: add memory."

## Expected key points
- Answer: B, C, E, I.
- A false: Linux fills free memory with page cache. Read the memory available to applications (MemAvailable), swap activity and memory pressure, not free memory.
- B true: page cache is given back to applications on demand; free memory near 0 with healthy other counters means no waste.
- C true: `pswpin` and `pswpout` count pages swapped in and out since boot; both are 0 and the VM has run for more than a week.
- D false: pressure stall information shows 0.00 at the 10-second, 1-minute and 5-minute averages: no task stalled on memory.
- E true: the Needed Memory chart stays below 50% of Total Capacity at every point.
- F false: the wrong action. Nothing shows a shortage; added memory would fill with more page cache and free memory would stay low.
- G false: over-correction. The page cache is in use: nginx serves files from it. The new size is the peak of Needed Memory over the business cycle plus headroom, cut in steps with a check after each.
- H false: MemFree excludes the page cache; that is why free memory is low while plenty is available.
- I true: Guest OS sizing uses Needed Memory, which keeps part of the cache, plus headroom; for memory, free is waste, not headroom.

## Notes
- Paired with 0263 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item C10.
- The swap and pressure evidence comes from the guest: the knowledge base does not state which Linux swap counters VMware Tools sends to VCF Operations.
- Review fixes 2026-11-15: new workload and request (0263 is a reporting database and +16 GB); `sar -W` replaced by the swap counters since boot and pressure stall information; screen readings added (C, E true; D false). Key B, C, D → B, C, E, I.
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
  - guest-os/system/guest-os-sizing
knowledge_main: guest-os/system/troubleshooting/linux-os-slow
attachments:
  - 0387/vcf-operations-linux-vm-guest-memory-7-days.png
  - 0387/linux-terminal-swap-and-pressure.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C10"
answer: [B, C, E, I]
misconception: [A]
misconception_type: [consumption-as-contention]
pair: "0263"
status: awaiting-input
```
