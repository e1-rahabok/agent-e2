# Guest memory four weeks across a downsize

## Prompt
See [the VCF Operations guest memory charts](0401/vcf-operations-vm-guest-memory-4-weeks.png) and [the VCF Operations VM memory charts](0401/vcf-operations-vm-memory-capacity-contention-4-weeks.png).

- Two weeks ago a Windows Server VM was cut to half its memory.
- The application owner sees guest free memory far lower than before the cut and asks for the memory back.

Which statements are correct?

- A. Guest Needed Memory stays below the new memory size at every point after the cut.
- B. The guest now runs short of memory, which is why its free memory figure fell.
- C. Guest page-out does not rise after the cut.
- D. ESXi did not make the VM wait for memory at any point of the four weeks.
- E. Needed Memory as a share of the VM's total memory about doubled at the cut.
- F. Needed Memory fell by about half at the cut.
- G. Once ESXi shows no memory wait, the guest's own paging no longer needs checking.
- H. Restore the VM's old memory size to bring the free memory figure back.

## Input to supply
- Product: VCF Operations 9.1; a Windows Server VM with VMware Tools, cut to half its memory (8 GB or more removed, for example 40 GB to 20 GB; not 24 GB to 12 GB, the theory partner's numbers) two weeks before the capture.
- Screen 1: VCF Operations > the VM > Metrics, last 28 days with the cut in the middle, three charts stacked: Guest|Free Memory, Guest|Needed Memory, Guest|Peak Guest OS Page-out/rate within collection cycle (all three enabled by default in the VCF Operations 9.1 metric list). Save as `benchmark/questions/0401/vcf-operations-vm-guest-memory-4-weeks.png`.
- Screen 2: the same 28 days, two charts stacked: Mem|Total Capacity (KB) and Mem|Contention (%). Save as `benchmark/questions/0401/vcf-operations-vm-memory-capacity-contention-4-weeks.png`.
- Condition the key depends on:
  - Mem|Total Capacity halves at the cut;
  - Guest|Free Memory falls at the cut and stays lower;
  - Guest|Needed Memory below 75% of the new size at every point of the 28 days, and after the cut within 15% of its level before;
  - the highest page-out point after the cut no higher than the highest point before it;
  - Mem|Contention (%) 0 at every point of the 28 days.
- How to produce it in a lab: a VM with much unused memory and a steady workload, downsized once halfway through the window.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
B: "Free memory dropped after the downsize, so the VM is short: give the memory back."

## Expected key points
- Answer: A, C, D, E.
- A true: the Needed Memory line stays below the new Total Capacity after the cut: what left was memory the guest held free. Less free memory after a downsize is expected.
- B false: free memory is not the measure of a shortage. Needed Memory stayed below the new size, page-out did not rise, and contention stayed at 0.
- C true: page-out is the guest's sign of being short; its highest point after the cut is no higher than before.
- D true: Memory Contention, the share of time a vCPU waits on page faults ESXi resolves, is 0 at every point.
- E true: Needed Memory stayed about the same while Total Capacity halved, so its share of total memory doubled. VCF Operations VM Memory Usage (%) is that ratio, so it doubles too.
- F false: Needed Memory after the cut stays within 15% of its level before; the guest's need did not follow the size.
- G false: over-correction. Contention covers waits on ESXi only; a guest short of memory pages out with no contention at all, so guest paging is read too.
- H false: the wrong action. The removed memory was unused; restoring it brings back free memory and nothing else.

## Notes
- Paired with 0400 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item D11.
- No option sets a paging threshold: windows-memory gives none. C compares page-out with its own level before the cut (judge by change).
- Metric names from the VCF Operations 9.1 Virtual Machine metric list (TechDocs, updated 2026-11-12): https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/infrastructure-operations/metric-property-and-alert-definitions/metrics-definitions-in-vrealize-operations-manager/metrics-for-vcenter-server-components/virtual-machine-metrics.html. Guest|Page Out Rate per second is disabled by default there, so page-out is read on the enabled peak metric (vcf-operations/features/peak-20-second-metrics). Memory|Usage (%) is also disabled by default, so E reads Needed Memory against Total Capacity.
- Review fixes 2026-11-15: the reading of the free-memory fall (the negation of B) replaced by a Needed Memory reading (A); C reworded; contention 0 at every point; a false screen reading added (F); options reworded away from 0400; metric names checked against the 9.1 list. Key A, C, D, E → A, C, D, E.
- The key holds whenever the condition of `## Input to supply` holds.
- Written 2026-11-14 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after approval (design.md, section 6.2).

## Metadata
```yaml
id: "0401"
title: "Guest memory four weeks across a downsize"
product: [vcf-operations, vsphere, windows]
technology: [memory]
task: decide-capacity
level: 400
answer_type: deterministic
input: [screenshot]
object: [vm, guest-os]
tool: [vcf-operations]
knowledge:
  - sp5-framework/capacity/rightsizing
  - guest-os/system/guest-os-sizing
  - guest-os/memory/windows-memory
  - vsphere/technology/memory/metrics/virtual-motherboard/usage
  - vsphere/technology/memory/metrics/virtual-motherboard/latency
  - vcf-operations/features/peak-20-second-metrics
knowledge_main: sp5-framework/capacity/rightsizing
attachments:
  - 0401/vcf-operations-vm-guest-memory-4-weeks.png
  - 0401/vcf-operations-vm-memory-capacity-contention-4-weeks.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D11"
answer: [A, C, D, E]
misconception: [B]
misconception_type: [consumption-as-contention]
pair: "0400"
status: awaiting-input
```
