# Run far above Used: add vCPUs?

## Prompt
- A 4-vCPU Ubuntu VM runs an API service. The application team says it is slow and asks for 4 more vCPUs.
- Its host runs about 30 other VMs. The host power policy is Balanced.
- [The attached VCF Operations export](0104/ubuntu-api-04-cpu-7-days.csv) holds 7 days in 2-hour points, each the average of the 5-minute values: CPU Run, Used, System and Overlap in ms per 5-minute collection cycle, summed over the 4 vCPUs (1,200,000 ms is 100%), and Ready (%) and Co-stop (%).

Do you add the vCPUs, and what do you check instead? Which statements are correct?

- A. Run averages about 375,000 of 1,200,000 ms, about 31%: the 4 vCPUs are far from full.
- B. Ready below 1% and Co-stop near 0 show that the VM is not waiting for CPU.
- C. Used is about 44% of Run while System and Overlap are small: each millisecond of run completes less work.
- D. The likely causes are a clock speed lowered by power saving under Balanced, and busy sibling threads on the same cores.
- E. The checks are on the host: its power policy, its actual clock speed, and the load on sibling threads.
- F. More vCPUs change neither the clock speed nor the sharing of cores with sibling threads.
- G. Used is less than half of Run, so the VM gets less than half the CPU it needs, and the 4 extra vCPUs are justified.
- H. The gap between Run and Used is time the vCPUs spent waiting in the hypervisor to be scheduled.
- I. System and Overlap time charged to the VM explain most of the gap between Run and Used here.
- J. Run is the counter that shows how much work the vCPUs completed in each cycle.
- K. Used cannot be compared with Run, because Used is converted to milliseconds at the actual clock speed.

## Likely wrong answer
- G: "Used is less than half of Run, so the VM gets less than half the CPU it needs: add the 4 vCPUs."
- H: "The missing Used is time the VM waited."

## Expected key points
- Answer: A, B, C, D, E, F.
- A true: Run is 365,000-385,000 ms in every point; 1,200,000 ms is 100% for 4 vCPUs.
- B true: Ready 0.25-0.6%, Co-stop 0-0.04%.
- C true: Used averages about 165,000 ms against 375,000 ms of Run; System is about 3,000 ms and Overlap about 1,600 ms.
- D true: with little System and Overlap, Used below Run comes from power saving and Hyper-Threading.
- E true: power management and the actual frequency first (a setting), then the sibling-thread load, read as Thread against Core Utilization (it depends on the other VMs).
- F true: the gap is in how fast each vCPU runs, not in how many vCPUs it has; adding vCPUs to a VM at 31% Run is the wrong answer to a request for speed.
- G false: Used is a charge adjusted for a shared core, frequency and hypervisor work, not the share of CPU the VM needs.
- H false: waiting shows in Ready and Co-stop, which are near 0; the gap is in the quality of the run time.
- I false: System and Overlap together are under 5,000 ms of a gap of about 210,000 ms; System even adds to Used.
- J false: Run is time only; Used (and Usage) count the work done, adjusted for frequency and Hyper-Threading.
- K false: Used counts cycles but is converted to ms at the static (nominal) frequency, so it compares directly with Run.

## Notes
- From the author's samples: a 4-vCPU 64-bit Ubuntu VM with Used about 44% of Run, minimal System and Overlap; Used lowered by power saving and SMT; if Run is far from 100% and the team wants faster performance, the answer is not to add vCPUs. Values reproduced in the export.
- Converted from judged to multiple choice (Q199 F, 2026-11-14). Dropped from the old key: "ask for the guest's view (run queue and per-process CPU) before any size change"; the guest run queue knowledge is under open author question Q217.

## Metadata
```yaml
id: "0104"
title: "Run far above Used: add vCPUs?"
product: [vsphere, vcf-operations, linux]
technology: [cpu]
task: troubleshoot
level: 400
answer_type: deterministic
answer: [A,B,C,D,E,F]
misconception: [G,H]
input: [table]
object: [vm, esxi]
tool: [vcf-operations]
knowledge:
  - vsphere/technology/cpu/troubleshooting/run-vs-used-gap
  - vsphere/technology/cpu/metrics/virtual-motherboard/used
  - vsphere/technology/cpu/metrics/virtual-motherboard/run
  - vsphere/technology/cpu/concepts/power-states
knowledge_main: vsphere/technology/cpu/troubleshooting/run-vs-used-gap
attachments:
  - 0104/ubuntu-api-04-cpu-7-days.csv
origin: book
source_path: "Author samples (docx, 2026-11-12) > Why Run is higher than Used"
misconception_type: [frequency-and-hyper-threading]
status: draft
```
