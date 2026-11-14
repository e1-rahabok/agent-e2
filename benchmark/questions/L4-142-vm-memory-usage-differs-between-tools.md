# VM Memory Usage differs between vCenter and VCF Operations

## Prompt
See [the vCenter memory chart of the VM](0395/vcenter-vm-memory-usage-active-consumed-past-day.png) and [the VCF Operations memory charts of the same VM](0395/vcf-operations-vm-memory-usage-needed-24h.png).

- A Windows Server VM with VMware Tools running.
- The owner's capacity report, from VCF Operations, shows the VM's memory usage far higher than the vCenter chart the vSphere team reads. The owner asks which tool is wrong.
- The vSphere team proposes to cut the VM's memory to what vCenter shows it uses.

Which statements are correct?

- A. vCenter Usage (%) here is about Active divided by the VM's configured memory.
- B. VCF Operations Usage (%) here is about Guest Needed Memory divided by Total Capacity.
- C. One tool reports wrongly: the same counter cannot read so differently over the same day.
- D. The gap comes from VCF Operations averaging 20-second samples into 5-minute points.
- E. Memory Contention near 0 shows that the VM did not wait on ESXi for memory during the day.
- F. Cut the VM to about its Active memory, since that is what Windows uses.
- G. Size the guest from the peak of Guest Needed Memory plus headroom.
- H. Consumed near the configured size shows that Windows uses all of its memory.
- I. Both tools compute Usage (%) from ESXi counters, so neither shows what Windows needs.

## Input to supply
- Product: vSphere Client 9.1 and VCF Operations 9.1; a Windows Server VM with VMware Tools, 8 GB or more, running a workload that keeps a large cache (a database or a file server).
- Screen 1: vSphere Client > the VM > Monitor > Performance > Advanced > Memory. Chart Options: timespan Past day; counters Usage (%), Active (KB) and Consumed (KB); target the VM. Save as `benchmark/questions/0395/vcenter-vm-memory-usage-active-consumed-past-day.png`.
- Screen 2: VCF Operations > the VM > Metrics, the same 24 hours, four charts stacked: Memory|Usage (%), Guest|Needed Memory (KB), Memory|Total Capacity (KB), Memory|Contention (%). Save as `benchmark/questions/0395/vcf-operations-vm-memory-usage-needed-24h.png`.
- Condition the key depends on:
  - vCenter Usage (%) at 15% or less for most of the day, and within 2 points of Active / configured memory;
  - Consumed at 85% or more of the configured memory;
  - VCF Operations Usage (%) at 60% or more, and within 2 points of Guest Needed Memory / Total Capacity;
  - Memory|Contention (%) below 0.5% for the whole day.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
C: "The same counter cannot read so differently on the same day: one tool is wrong." Or F: Active taken as what Windows uses.

## Expected key points
- Answer: A, B, E, G.
- A true: vCenter VM Memory Usage (%) maps to Active; the chart's Usage line matches Active against the configured memory.
- B true: VCF Operations VM Memory Usage (%) = Guest OS Needed Memory / VM Memory Total Capacity × 100; the charts agree within a point or two.
- C false: one name, two formulas. Both tools report correctly; they read different layers.
- D false: vCenter's past-day chart holds 5-minute averages too, and averaging cannot turn Active into Needed Memory.
- E true: Memory Contention is the share of time a vCPU waits on page faults ESXi resolves; near 0 all day, ESXi did not make the VM wait.
- F false: the wrong action. Active is a sampled kernel estimate of recently touched pages; a cut to it removes the cache Windows works from.
- G true: Guest OS sizing uses the peak of Needed Memory over the business cycle plus headroom, so the result lands below 100%.
- H false: Consumed counts pages the VM has touched since power-on and ESXi still backs; it is not what Windows uses now.
- I false: over-correction. VCF Operations Usage (%) reads Guest Needed Memory, which VMware Tools collects inside the guest.

## Notes
- Paired with 0394 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item D2.
- Kept to the difference between the tools; the fallback without guest data is pair D8 (0396, 0397). No option rests on memory Demand (open author question Q221).
- The key holds whenever the condition of `## Input to supply` holds.
- Written 2026-11-14 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after approval (design.md, section 6.2).

## Metadata
```yaml
id: "0395"
title: "VM Memory Usage differs between vCenter and VCF Operations"
product: [vsphere, vcf-operations, windows]
technology: [memory]
task: read-metric
level: 400
answer_type: deterministic
input: [screenshot]
object: [vm]
tool: [vcenter, vcf-operations]
knowledge:
  - vsphere/technology/memory/metrics/virtual-motherboard/usage
  - vsphere/technology/memory/metrics/virtual-motherboard/active
  - vsphere/technology/memory/metrics/virtual-motherboard/consumed
  - vsphere/technology/memory/metrics/virtual-motherboard/latency
  - guest-os/system/concepts/guest-os-sizing
  - sp5-framework/observability/collection-interval
knowledge_main: vsphere/technology/memory/metrics/virtual-motherboard/usage
attachments:
  - 0395/vcenter-vm-memory-usage-active-consumed-past-day.png
  - 0395/vcf-operations-vm-memory-usage-needed-24h.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D2"
answer: [A, B, E, G]
misconception: [C]
misconception_type: [tool-confusion, rollup-and-interval]
pair: "0394"
status: awaiting-input
```
