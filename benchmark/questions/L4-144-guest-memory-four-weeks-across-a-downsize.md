# Guest memory four weeks across a downsize

## Prompt
See [the VCF Operations guest memory charts](0401/vcf-operations-vm-guest-memory-4-weeks.png) and [the VCF Operations VM memory charts](0401/vcf-operations-vm-memory-usage-contention-4-weeks.png).

- Two weeks ago a Windows Server VM was cut to half its memory.
- The application owner sees guest free memory far lower than before the cut and asks for the memory back.

Which statements are correct?

- A. The fall in guest free memory at the cut is the unused memory that was removed.
- B. The lower guest free memory shows that the VM is now short of memory.
- C. Guest page-out after the cut stays at the level of the weeks before it.
- D. Memory Contention near 0 after the cut shows that ESXi did not make the VM wait.
- E. Memory Usage (%) about doubled at the cut while Guest Needed Memory stayed about the same.
- F. With Memory Contention at 0, the new size is right whatever the guest's paging does.
- G. Give the VM its memory back so that guest free memory returns to its old level.

## Input to supply
- Product: VCF Operations 9.1; a Windows Server VM with VMware Tools, cut to half its memory (8 GB or more removed, for example 32 GB to 16 GB) two weeks before the capture.
- Screen 1: VCF Operations > the VM > Metrics, last 28 days with the cut in the middle, four charts stacked: Guest free memory, Guest|Needed Memory, Guest|Page In Rate per second, Guest|Page Out Rate per second. Save as `benchmark/questions/0401/vcf-operations-vm-guest-memory-4-weeks.png`.
- Screen 2: the same 28 days, three charts stacked: Memory|Total Capacity, Memory|Usage (%), Memory|Contention (%). Save as `benchmark/questions/0401/vcf-operations-vm-memory-usage-contention-4-weeks.png`.
- Condition the key depends on:
  - guest free memory falls at the cut and stays lower;
  - the peak of Guest Needed Memory before the cut below 75% of the new size, and its level after the cut within 15% of its level before;
  - the highest page-out peak after the cut no higher than 1.2 times the highest peak before it;
  - Memory|Usage (%) after the cut 1.7 to 2.3 times its level before;
  - Memory|Contention below 0.5% for the whole 28 days.
- How to produce it in a lab: a VM with much unused memory and a steady workload, downsized once halfway through the window.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
B: "Free memory dropped after the downsize, so the VM is short: give the memory back."

## Expected key points
- Answer: A, C, D, E.
- A true: the guest's need (Needed Memory) stayed below the new size; what left was memory the guest held free. Less free memory after a downsize is expected.
- B false: free memory is not the measure of a shortage. Needed Memory stayed below the new size, page-out did not rise, and contention stayed at 0.
- C true: page-out is the guest's sign of being short; it did not rise after the cut.
- D true: Memory Contention is the share of time a vCPU waits on page faults ESXi resolves; near 0 throughout.
- E true: Usage (%) is Guest Needed Memory over total memory; the same need over half the total reads about twice as high.
- F false: over-correction. Contention covers ESXi only; a guest short of memory pages out with no contention at all, so guest paging is read too.
- G false: the wrong action. The removed memory was unused; adding it back brings back free memory and nothing else.

## Notes
- Paired with 0400 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item D11.
- No option sets a paging threshold: windows-memory gives none. C compares page-out with its own level before the cut (judge by change).
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
  - guest-os/system/concepts/guest-os-sizing
  - guest-os/memory/windows-memory
  - vsphere/technology/memory/metrics/virtual-motherboard/usage
  - vsphere/technology/memory/metrics/virtual-motherboard/latency
knowledge_main: sp5-framework/capacity/rightsizing
attachments:
  - 0401/vcf-operations-vm-guest-memory-4-weeks.png
  - 0401/vcf-operations-vm-memory-usage-contention-4-weeks.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D11"
answer: [A, C, D, E]
misconception: [B]
misconception_type: [consumption-as-contention]
pair: "0400"
status: awaiting-input
```
