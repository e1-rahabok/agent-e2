# Run far above Used: add vCPUs?

## Prompt
- A 4-vCPU Ubuntu VM runs an API service. The application team says it is slow and asks for 4 more vCPUs.
- Its host runs about 30 other VMs. The host power policy is Balanced.
- [The attached VCF Operations export](0104/ubuntu-api-04-cpu-7-days.csv) holds 7 days in 2-hour points, each the average of the 5-minute values: CPU Run, Used, System and Overlap in ms for the VM as a whole (not per vCPU), and Ready (%) and Co-stop (%).

Do you add the vCPUs, and what do you check instead? Which statements are correct?

- A. The vCPUs are far from full: no 2-hour point puts Run above a third of the time the 4 vCPUs have.
- B. Ready below 1% and Co-stop near 0 show that the VM is not waiting for CPU.
- C. Used averages about 44% of Run: each millisecond of run did less work than a millisecond at base clock.
- D. Likely causes: power saving under Balanced and busy sibling threads on the same cores.
- E. The checks are on the host: its power policy, its actual clock speed, and the load on sibling threads.
- F. More vCPUs change neither the clock speed nor the sharing of cores with sibling threads.
- G. Used is less than half of Run, so the VM gets less than half the CPU it needs, and the 4 extra vCPUs are justified.
- H. The gap between Run and Used is time the vCPUs spent waiting in the hypervisor to be scheduled.
- I. System and Overlap charged to the VM likely explain most of the gap between Run and Used.
- J. Run is the counter that shows how much work the vCPUs completed in each cycle.
- K. Used cannot be compared with Run, because Used is converted to milliseconds at the actual clock speed.
- L. Against the 1,200,000 ms of 5 minutes for 4 vCPUs, Run of about 25,000 ms is 2%: the VM is nearly idle.

## Answers
A, B, C, D, E, F

## Explanation
- A is correct: Run is about 24,300-25,700 ms in every point, 30-32% of 80,000 ms. A VCF Operations 5-minute ms value is the average of the 15 20-second values, so 100% is 20,000 ms per vCPU, 80,000 ms for 4 vCPUs; the 2-hour points average the 5-minute values and keep that base. Read against 1,200,000 ms (the vCenter Past Day sum), Run would look like 2%.
- B is correct: Ready 0.25-0.6%, Co-stop 0-0.04%.
- C is correct: Used averages about 11,000 ms against 25,000 ms of Run; Used counts the work done and converts it to ms at the base (nominal) frequency, so a ratio of 0.44 is less work per millisecond of run. System (about 200 ms) and Overlap (about 110 ms) are too small to move it.
- D is correct: with little System and Overlap, Used below Run comes from power saving and Hyper-Threading.
- E is correct: power management and the actual frequency first (a setting), then the sibling-thread load, read as Thread against Core Utilization (it depends on the other VMs).
- F is correct: the gap is in how fast each vCPU runs, not in how many vCPUs it has; adding vCPUs to a VM at 31% Run is the wrong answer to a request for speed.
- G is wrong: Used is a charge adjusted for a shared core, frequency and hypervisor work, not the share of CPU the VM needs.
- H is wrong: waiting shows in Ready and Co-stop, which are near 0; the gap is in the quality of the run time.
- I is wrong: System and Overlap together are under 400 ms of a gap of about 14,000 ms; System even adds to Used.
- J is wrong: Run is time only; Used (and Usage) count the work done, adjusted for frequency and Hyper-Threading.
- K is wrong: Used counts cycles but is converted to ms at the static (nominal) frequency, so it compares directly with Run.
- L is wrong: 1,200,000 ms is the base of a vCenter Past Day point, which sums its 15 samples. VCF Operations stores their average, so its 100% is 80,000 ms for 4 vCPUs and Run is about 31%.
- Misconception: G: "Used is less than half of Run, so the VM gets less than half the CPU it needs: add the 4 vCPUs." - H: "The missing Used is time the VM waited." - L: "A 5-minute point of 4 vCPUs is 1,200,000 ms, so 25,000 ms is next to nothing."

## Notes
- From the author's samples: a 4-vCPU 64-bit Ubuntu VM with Used about 44% of Run, minimal System and Overlap; Used lowered by power saving and SMT; if Run is far from 100% and the team wants faster performance, the answer is not to add vCPUs. Values reproduced in the export.
- Converted from judged to multiple choice (Q199 F, 2026-11-14). Dropped from the old key: "ask for the guest's view (run queue and per-process CPU) before any size change"; the guest run queue knowledge is in guest-os/cpu/metrics/run-queue (Q217 settled 2026-11-15).
- Leak closed 2026-11-14 on the knowledge side (project/question-pairing-2026-11-14.md, decision 3): the example row of run-vs-used-gap no longer gives this VM's numbers.
- Export rescaled 2026-11-15 (Q224): a VCF Operations 5-minute ms value averages the 15 20-second values, so 100% is 20,000 ms per vCPU (Broadcom KB 315941; KB 444403 for VCF Operations 9.x). Every ms value is divided by 15; ratios, Ready (%), Co-stop (%) and the key are unchanged. The base line (1,200,000 ms) left the stem, so option A now needs the base. Old export: project/archive/benchmark-questions/attachments/0104-ubuntu-api-04-cpu-7-days-before-2026-11-15.csv.
- Paired with 0003 (theory and practical, design.md 3.9).
- 2026-11-16 re-review: A/L and C/I were near-negations. A no longer states "about 31%" (the 2% of L is not ruled out by the words, only by the base); C no longer says System and Overlap are small (I tests that). Truth kept; key unchanged.
- 2026-11-15 audit: L added (the vCenter sum base applied to a VCF Operations value; collection-interval, Misconceptions). This is the one question that tests the VCF Operations ms base as an option (0105's proposed H/I were not added). D shortened; I carries a hedge (truth kept).

## Metadata
```yaml
id: "0104"
title: "Run far above Used: add vCPUs?"
product: [vsphere, vcf-operations, linux]
technology: [cpu]
task: troubleshoot
level: 400
answer_type: deterministic
misconception: [G,H,L]
input: [table]
object: [vm, esxi]
tool: [vcf-operations]
knowledge:
  - vsphere/technology/cpu/troubleshooting/run-vs-used-gap
  - vsphere/technology/cpu/metrics/virtual-motherboard/used
  - vsphere/technology/cpu/metrics/virtual-motherboard/run
  - vsphere/technology/cpu/concepts/power-states
  - sp5-framework/observability/collection-interval
knowledge_main: vsphere/technology/cpu/troubleshooting/run-vs-used-gap
attachments:
  - 0104/ubuntu-api-04-cpu-7-days.csv
origin: book
source_path: "Author samples (docx, 2026-11-12) > Why Run is higher than Used"
misconception_type: [frequency-and-hyper-threading, unit-and-normalization, tool-confusion]
pair: "0003"
status: draft
```
