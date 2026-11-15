# Low average, vCPU Usage Disparity above 100%

## Prompt
- A 12-vCPU Linux appliance VM from a network monitoring vendor. Its hosts have a base clock of 2.2 GHz.
- VCF Operations shows CPU Net Run at about 8% all day, and CPU vCPU Usage Disparity at about 123%.
- The vendor says the appliance needs 12 vCPUs. Its users say reports are slow.
- The VM owner reads 8% as "mostly idle" and says the VM cannot be the bottleneck.
- [The attached metric export](0101/netmon-appl-01-cpu-5-minute.csv) holds 6 hours in 5-minute points: Net Run, vCPU Usage Disparity, and the Usage of each vCPU.

How can the average be so low while the disparity is above 100%, is the owner right, and what do you advise on the VM's size? Which statements are correct?

- A. The 8% is one fully busy vCPU out of 12: vCPU 0 runs at about 2,700 MHz while the other eleven stay near 0.
- B. vCPU 0 runs above the 2.2 GHz base clock with Turbo Boost: about 123% of base, so the spread between vCPUs passes 100%.
- C. A disparity above 100% is a data error, because the usage of one vCPU cannot pass 100% of its clock.
- D. At 8% the VM is mostly idle all day, so it cannot be the bottleneck behind the slow reports.
- E. The VM-level average hides that the one vCPU doing the work is saturated all day.
- F. vCPU Usage Disparity is the average usage of the 12 vCPUs, measured against the base clock.
- G. The export shows the vCPUs taking turns at being busy, a sign of a process moving between vCPUs.
- H. The guest likely runs its work on one CPU only, as a uniprocessor kernel or a single-threaded process would.
- I. Adding vCPUs would make the reports run faster, as the vendor's sizing for the appliance suggests.
- J. A faster clock speed would make the reports run faster on the same vCPU count.
- K. The eleven idle vCPUs can be removed without slowing the appliance, unless the vendor changes the guest to use them.
- L. Net Run follows the clock speed like Usage does, so with Turbo it can pass 100% for one vCPU.

## Likely wrong answer
- D: "8% means the VM is mostly idle, so it is not the bottleneck."
- C: "A disparity above 100% is a data error: usage cannot pass 100%."
- I: "The vendor says 12 vCPUs; give it more if the reports are slow."

## Expected key points
- Answer: A, B, E, H, J, K.
- A true: in every 5-minute point vCPU 0 is at about 2,680-2,730 MHz and the others are at 0-1.5 MHz; one busy vCPU of 12 gives about 8.3%.
- B true: 2,705 / 2,200 = about 123%; Turbo pushes one vCPU above 100% of base, and the disparity (busiest minus least busy) follows.
- C false: Turbo can push the usage of one vCPU above 100% of the base clock.
- D false: the appliance is saturated on its one working vCPU.
- E true: the average across the 12 vCPUs is low while the one vCPU that does the work is at its limit.
- F false: the disparity is built from the busiest and the least busy vCPU (Max - Min), not from the average.
- G false: vCPU 0 is the busy one in every point; the busy vCPU does not move.
- H true: the vCPUs are not used in parallel; only the guest can show why (CPU count seen by the kernel, per-CPU load). VCF Operations cannot see inside the guest.
- I false: the work runs on one CPU; more vCPUs add idle vCPUs.
- J true: a single busy vCPU is limited by its clock speed; all else equal, throughput scales with frequency.
- K true: the idle vCPUs do no work today.
- L false: Net Run is time-based and cannot pass 100%; it does not see frequency, so vCPU 0 counts as fully busy (about 8.3% for the VM) and Turbo shows only in the MHz counters.

## Notes
- From the author's samples: average utilization 12.5%, Usage Disparity above 100%; plotting each vCPU showed only the first one busy (uniprocessor kernel), and Turbo above 100%. The export keeps this pattern with its own numbers (below).
- Converted from judged to multiple choice (Q199 F, 2026-11-14). Review 2026-11-14: option L (Net Run is time-based) turned into a near miss, so fewer options are correct.
- CSV regenerated 2026-11-14 with new numbers (12 vCPUs, 2.2 GHz base clock, vCPU 0 at about 123% of base, Net Run about 8.3%) so that it no longer copies the knowledge example (project/question-pairing-2026-11-14.md, decision 3, item B14; author approved, 2026-11-14). Seeded script: the writer's scratchpad (gen_0101.py, seed 20261114). Options A, B, D, F, K and key points follow the new numbers; key unchanged: A, B, E, H, J, K. Paired with the theory question 0366.

## Metadata
```yaml
id: "0101"
title: "Low average, vCPU Usage Disparity above 100%"
product: [vsphere, vcf-operations, linux]
technology: [cpu]
task: troubleshoot
level: 400
answer_type: deterministic
answer: [A,B,E,H,J,K]
misconception: [C,D,I]
input: [table]
object: [vm, guest-os]
tool: [vcf-operations]
knowledge:
  - vsphere/technology/cpu/metrics/virtual-motherboard/usage-disparity
  - vsphere/technology/cpu/metrics/virtual-motherboard/net-run
  - vsphere/technology/cpu/concepts/cpu-frequency
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/usage-disparity
attachments:
  - 0101/netmon-appl-01-cpu-5-minute.csv
origin: book
source_path: "Author samples (docx, 2026-11-12) > Average utilization 12.5% yet Usage Disparity above 100%"
misconception_type: [average-hides-worst, frequency-and-hyper-threading]
pair: "0366"
status: draft
```
