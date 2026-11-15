# Host memory usage high all week without balloon

## Prompt
See [the vCenter memory chart of the host](0385/vcenter-host-memory-usage-balloon-past-week.png) and [the VCF Operations list of its VMs](0385/vcf-operations-host-vms-memory-contention-7-days.png).

- The capacity team flags an ESXi 9.1 host for high memory usage all week.
- They ask to move VMs off it now, before ballooning starts and the VMs slow down.

Which statements are correct?

- A. Host Memory Usage here is Consumed as a share of the host's total memory.
- B. The balloon rose above 0 on at least one day of the week.
- C. At this usage, free memory stayed above the level at which ESXi starts to balloon.
- D. No VM on the host waited on memory at any point of the week.
- E. The VMs wait for memory now, because a host above 90% usage delays the pages they touch.
- F. Memory that ESXi takes back through the balloon is memory the VMs then wait for.
- G. No level of host memory usage, even 100%, can make the VMs wait for memory.
- H. Move VMs off the host now, so that they do not slow down once ballooning starts.

## Input to supply
- Product: vSphere Client 9.1 and VCF Operations 9.1. One ESXi host with 256 GB of memory or more, no memory tiering.
- Screen 1: vSphere Client > the host > Monitor > Performance > Advanced > Memory. Chart Options: timespan Past week; counters Usage (%) and Balloon (KB); target the host. Save as `benchmark/questions/0385/vcenter-host-memory-usage-balloon-past-week.png`.
- Screen 2: VCF Operations > the host > its VMs (a list or a Top-N view of the host's VMs), column Mem|Contention (%) with the maximum over the last 7 days, sorted from the highest. Save as `benchmark/questions/0385/vcf-operations-host-vms-memory-contention-7-days.png`.
- Condition the key depends on:
  - Usage (%) between 94% and 97% at every point of the week;
  - Balloon 0 at every point of the week;
  - Mem|Contention (%) 0 at every point of the week for every VM on the host (the 7-day maximum of every row is 0);
  - no VM moved onto or off the host during the week.
- How to produce it in a lab: fill the host with VMs whose guests touch most of their memory (a memory load tool or a database cache) until host Consumed reaches 94-97%, with no limits and DRS set so that no VM moves, and leave it a week.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
E: "The host is above 90%, so its VMs are already waiting for memory: move some off."

## Expected key points
- Answer: A, C, D.
- A true: host Memory Usage is Consumed against total capacity: what the VMs and the kernel hold, a capacity counter. Memory is a cache, so values near 100% are expected.
- B false: the balloon line reads 0 at every point of the week.
- C true: ballooning from host pressure starts in the soft state, at about 99% of host memory in use; at 97% or less, free memory stays above that level, so ESXi has no reason to balloon.
- D true: every VM's 7-day maximum Memory Contention is 0. Contention, not Usage, shows a wait.
- E false: Usage is consumption, not contention. A VM waits only when it touches a page ESXi swapped or compressed; the contention list shows no such wait.
- F false: ballooning is reclamation inside the guest, not a wait; the guest gives up free and cache pages first. The wait shows in Memory Contention.
- G false: over-correction. In the hard and low states ESXi compresses and swaps pages, and a VM that touches one waits for it.
- H false: the wrong action from E. Nothing on the screens shows a VM waiting; the host is using its memory as intended.

## Notes
- Paired with 0144 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item C3.
- The options do not compute the memory state from minFree, so the host size only needs to be 256 GB or more (soft state at 99.2% used or above).
- Review fixes 2026-11-15: the 90% balloon option and the order of reclamation were removed (they repeated 0146 K and J, and the 0144 rewrite dropped that fact on purpose); a false screen reading (B) added; the condition now reads 0 at every point and fixes the VM list. Key A, C, D → A, C, D (relettered).
- The key holds whenever the condition of `## Input to supply` holds.
- Written 2026-11-14 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after approval (design.md, section 6.2).

## Metadata
```yaml
id: "0385"
title: "Host memory usage high all week without balloon"
product: [vsphere, vcf-operations]
technology: [memory]
task: read-metric
level: 300
answer_type: deterministic
input: [screenshot]
object: [esxi, vm]
tool: [vcenter, vcf-operations]
knowledge:
  - vsphere/technology/memory/concepts/host-memory-states
  - vsphere/technology/memory/metrics/host/usage
  - vsphere/technology/memory/metrics/host/ballooned
  - vsphere/technology/memory/metrics/virtual-motherboard/latency
  - vsphere/technology/memory/concepts/ballooning
knowledge_main: vsphere/technology/memory/concepts/host-memory-states
attachments:
  - 0385/vcenter-host-memory-usage-balloon-past-week.png
  - 0385/vcf-operations-host-vms-memory-contention-7-days.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C3"
answer: [A, C, D]
misconception: [E]
misconception_type: [consumption-as-contention, reclamation-as-contention]
pair: "0144"
status: awaiting-input
```
