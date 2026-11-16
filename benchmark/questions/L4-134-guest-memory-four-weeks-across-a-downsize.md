# Guest memory four weeks across a downsize

## Prompt
- Two weeks ago, in the Saturday night maintenance window, the Windows Server VM erp-app-04 was cut to half its memory.
- The application owner sees guest free memory far lower than before the cut and asks for the memory back.
- I exported [the VCF Operations list view of erp-app-04](0401/vcf-operations-vm-memory-28-days.csv) for the four weeks around the cut, one row per day.

Which statements are correct?

- A. Guest Needed Memory stays below the new memory size on every day after the cut.
- B. The guest now runs short of memory, which is why its free memory figure fell.
- C. Guest page-out does not rise after the cut, judged by its highest daily value.
- D. ESXi did not make the VM wait for memory at any point of the four weeks.
- E. Needed Memory reads about 1 GB lower after the cut: its 5% buffer shrank with the VM.
- F. Needed Memory fell by about half at the cut, along with the memory size.
- G. Once ESXi shows no memory wait, the guest's own paging no longer needs checking.
- H. Restore the VM's old memory size to bring the free memory figure back.

## Likely wrong answer
B: "Free memory dropped after the downsize, so the VM is short: give the memory back."

## Expected key points
- Answer: A, C, D, E.
- A is correct: `Guest|Needed Memory (KB) (Max)` stays below 75% of the new `Memory|Total Capacity (KB) (Max)` (20,971,520 KB) on every row from November 1 to November 14: what left was memory the guest held free. Less free memory after a downsize is expected.
- B is wrong: free memory is not the measure of a shortage. `Guest|Free Memory (KB) (Max)` fell, but Needed Memory stays below the new size, page-out does not rise and contention stays 0. `Memory|Consumed (KB) (Max)` near the new size is ESXi pages the guest has touched, not guest need.
- C is correct: page-out is the guest's sign of being short; the highest daily value of `Guest|Peak Guest OS Page-out Rate within collection cycle (Max)` after the cut is lower than the highest before it.
- D is correct: `Memory|Contention (%) (Max)`, the share of time a vCPU waits on page faults ESXi resolves, is 0 on all 28 rows; a daily maximum of 0 means every 5-minute value was 0.
- E is correct: Needed Memory keeps a buffer of 5% of the VM's memory (Needed = physical - max(0, Unneeded - 5% of physical)): 2 GB at 40 GB, 1 GB at 20 GB. The mean of `Guest|Needed Memory (KB) (Max)` is about 10.7 GB before the cut and about 9.7 GB after, about 1 GB lower with the same guest load.
- F is wrong: the mean of Needed Memory after the cut is within 15% of its mean before (about 9% lower, the 5% buffer of a smaller VM), and every row after the cut is within 15% of the mean before; the guest's need did not follow the size.
- G is wrong: over-correction. Contention covers waits on ESXi only; a guest short of memory pages out with no contention at all, so guest paging is read too.
- H is wrong: the wrong action. The removed memory was unused; restoring it brings back free memory and nothing else.

## Notes
- Paired with 0400 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item D11.
- No option sets a paging threshold: windows-memory gives none. C compares page-out with its own level before the cut (judge by change).
- Metric names from the VCF Operations 9.1 Virtual Machine metric list (TechDocs, updated 2026-11-12): https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/infrastructure-operations/metric-property-and-alert-definitions/metrics-definitions-in-vrealize-operations-manager/metrics-for-vcenter-server-components/virtual-machine-metrics.html. Guest|Page Out Rate per second is disabled by default there, so page-out is read on the enabled peak metric (vcf-operations/features/peak-20-second-metrics).
- Changed in the 2026-11-15 audit: E replaced (Needed over total memory doubling, the VCF Operations Usage (%) formula, is tested by the pair 0394/0395) by the 5% buffer of Needed Memory read from the export (true by construction: buffer 2 GB before, 1 GB after; the export's means differ by 1.02 GB). Key unchanged: A, C, D, E.
- Converted to an export 2026-11-15 (project/practical-questions-as-exports-2026-11-15.md, row 0401): a seeded VCF Operations list view, daily Max, 28 rows; the cut falls between the October 31 and November 1 rows. A reworded from "every point" to "every day" (the rows are daily maxima). Consumed added as the misleading neighbour. The list view CSV format is assumed (project/tools/exportgen/README.md). The key holds for the generated export; the generator checks every condition against the rows.
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
input: [table]
object: [vm, guest-os]
tool: [vcf-operations]
knowledge:
  - sp5-framework/capacity/rightsizing
  - guest-os/system/guest-os-sizing
  - guest-os/memory/windows-memory
  - vsphere/technology/memory/metrics/virtual-motherboard/latency
  - vcf-operations/features/peak-20-second-metrics
knowledge_main: sp5-framework/capacity/rightsizing
attachments:
  - 0401/vcf-operations-vm-memory-28-days.csv
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D11"
answer: [A, C, D, E]
misconception: [B]
misconception_type: [consumption-as-contention]
pair: "0400"
status: draft
```
