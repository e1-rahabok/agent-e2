# Host memory usage high all week without balloon

## Prompt
See [the vCenter memory chart of the host](0385/vcenter-host-memory-usage-balloon-past-week.png) and [the VCF Operations list of its VMs](0385/vcf-operations-host-vms-memory-contention-7-days.png).

- The capacity team flags an ESXi 9.1 host for high memory usage all week.
- They ask to move VMs off it now, before ballooning starts and the VMs slow down.

Which statements are correct?

- A. Host Memory Usage here is Consumed as a share of the host's total memory.
- B. ESXi starts to inflate balloons once host memory usage passes about 90%.
- C. At this usage, free memory stayed above the level at which ESXi starts to balloon.
- D. No VM waited on memory for more than 0.5% of any 5-minute interval this week.
- E. The VMs wait for memory now, because a host above 90% usage delays the pages they touch.
- F. Once ballooning starts on this host, its VMs begin to wait for memory.
- G. If free memory kept falling, ESXi would compress and swap pages before it inflated any balloon.
- H. No level of host memory usage, even 100%, can make the VMs wait for memory.
- I. Move VMs off the host now, so that they do not slow down once ballooning starts.

## Input to supply
- Product: vSphere Client 9.1 and VCF Operations 9.1. One ESXi host with 256 GB of memory or more, no memory tiering.
- Screen 1: vSphere Client > the host > Monitor > Performance > Advanced > Memory. Chart Options: timespan Past week; counters Usage (%) and Balloon (KB); target the host. Save as `benchmark/questions/0385/vcenter-host-memory-usage-balloon-past-week.png`.
- Screen 2: VCF Operations > the host > its VMs (a list or a Top-N view of the host's VMs), column Memory|Contention (%) with the maximum over the last 7 days, sorted from the highest. Save as `benchmark/questions/0385/vcf-operations-host-vms-memory-contention-7-days.png`.
- Condition the key depends on:
  - Usage (%) between 94% and 97% for the whole week, never above 97%;
  - Balloon 0 for the whole week;
  - every VM on the host with a 7-day maximum Memory|Contention below 0.5%.
- How to produce it in a lab: fill the host with VMs whose guests touch most of their memory (a memory load tool or a database cache) until host Consumed reaches 94-97%, with no limits, and leave it a week.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
B or E: "The host is at 95%: ballooning is about to start and the VMs will slow down."

## Expected key points
- Answer: A, C, D.
- A true: host Memory Usage is Consumed against total capacity: what the VMs and the kernel hold, a capacity counter. Memory is a cache, so values near 100% are expected.
- B false: ballooning from host pressure starts in the soft state, at 64% of minFree, which is about 99% of host memory in use (99.3% on 512 GB to 1.5 TB hosts).
- C true: at 97% or less used, free memory stays above the soft-state level, so ESXi has no reason to balloon.
- D true: the list shows every VM's worst 5-minute Memory Contention below 0.5% in the week. Contention, not Usage, shows a wait.
- E false: Usage is consumption, not contention. A VM waits only when it touches a page ESXi swapped or compressed; the contention list shows no such wait.
- F false: ballooning is reclamation inside the guest, not a wait; the guest gives up free and cache pages first. The wait shows in Memory Contention.
- G false: the order runs the other way. Ballooning starts in the soft state; compression and host swapping start in the hard state, at 32% of minFree.
- H false: over-correction. In the hard and low states ESXi compresses and swaps pages, and a VM that touches one waits for it.
- I false: the wrong action from E. Nothing on the screens shows a VM waiting; the host is using its memory as intended.

## Notes
- Paired with 0144 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item C3.
- The key holds whenever the condition of `## Input to supply` holds. The options do not compute the state from minFree, so the host size only needs to be 256 GB or more (soft state at 99.2% used or above).
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
misconception: [B, E]
misconception_type: [consumption-as-contention, threshold-transplanted]
pair: "0144"
status: awaiting-input
```
