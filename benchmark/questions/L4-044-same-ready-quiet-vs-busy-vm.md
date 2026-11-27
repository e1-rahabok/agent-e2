# The same CPU Ready on quiet and busy VMs

## Prompt
- The team alerts when a VM's CPU Ready passes 5% (per vCPU, 20-second peak). No alert fired today.
- Between 10:00 and 11:00 the web team reported slow page loads on web-01, web-02 and web-03. The batch team reported nothing.
- At 11:00 you export the vSphere Client Real-time data (20-second samples) of every VM on the host. [The attached list](0106/vms-cpu-ready-10-to-11.csv) gives, for each VM, the sample with the highest Readiness between 10:00 and 11:00: its Readiness (%) and its Run in that same sample, converted from ms to % per vCPU.

Which VMs lose the most to CPU Ready, why did the alert not catch them, and what would you change in how the team reads Ready? Which statements are correct?

- A. The web VMs wait about 3% against about 6% of run: their work stretches to about 1.5 times.
- B. erp-app-01 waits 2.4% against 12% of run: its work takes about 1.2 times as long.
- C. batch-01 and batch-02 wait 4-5% against 94-95% of run: about 5% longer, which batch work tolerates.
- D. A flat Ready threshold ignores how much a VM runs: it nearly fires on busy VMs and misses quiet ones that suffer.
- E. For interactive VMs, the team should read Ready relative to the time the VM runs, not on its own.
- F. The 20-second peak is the right sample to keep: Ready usually lasts seconds, not minutes.
- G. No VM passed the 5% alert level in that hour, so CPU Ready cannot be the cause of the slow pages.
- H. batch-01, at 4.6%, has the highest Ready of the host and is the VM that loses the most to it.
- I. erp-db-01 likely loses more than erp-app-01 to Ready: a 16-vCPU VM is harder to schedule.
- J. The Ready of the web VMs comes from busy sibling threads on their cores (Hyper-Threading).
- K. Readiness (%) is not normalized by the vCPU count, so the values of the 8-vCPU batch VMs are overstated.
- L. More vCPUs on the web VMs would likely lower their Ready by spreading the load.

## Answers
A, B, C, D, E, F

## Explanation
- A is correct: 3.1/6.2, 2.9/5.8 and 3.0/6.5: about 1 ms of wait for every 2 ms of run. "1.5 times" takes the delayed work as equal to the run time, the reading of "2% Ready on 10% Run delays 20% of the work".
- B is correct: 2.4/12.0 = 20%.
- C is correct: 4.6/94.0 and 4.2/95.5 are about 5%.
- D is correct: Ready 5% on Run 95% is low; Ready 2% on Run 10% is very high. One threshold for both reads the wrong VMs.
- E is correct: read Ready against Run (or alert on a lower level for interactive VMs), and check whether many VMs on the host wait at once (a busy host).
- F is correct: a 5-minute value would dilute a wait that lasts seconds.
- G is wrong: the web VMs, the ones whose users complained, lose about a third of their elapsed time to Ready.
- H is wrong: batch-01 has the highest Ready in %, but only about 5% of its run; the web VMs lose ten times more relative to their work.
- I is wrong: 1.1/55 = 2%, against 20% for erp-app-01.
- J is wrong: a busy sibling thread does not put a vCPU into Ready; Ready means no physical thread was free to run it.
- K is wrong: Readiness (%) is normalized by the vCPU count; Ready (ms) is the summed value.
- L is wrong: all else equal, larger VMs show more Ready; a busy host is less likely to run many vCPUs at once.
- Misconception: G: "No VM passed 5%, so CPU Ready is not the cause." - H: "batch-01 at 4.6% is the worst VM."

## Notes
- 2026-11-16 re-review: A no longer says the web VMs "lose the most", which excluded H (batch-01 loses the most); A now states their wait against run. Key unchanged.
- Mechanism: 2% Ready on 10% Run delays about 20% of the work; the application may not notice 2% on 98% Run (knowledge base, VM CPU Ready, sections Read against Run and Guest OS sizing).
- Converted from judged to multiple choice (Q-E2-199 F, 2026-11-14).
- 2026-11-15 audit: the list is now a vCenter Real-time export (Readiness and Run of the same 20-second sample, read within the hour vCenter keeps them). The earlier VCF Operations list could not exist: VCF Operations keeps only the peak vCPU Ready of each 5-minute cycle, Net Run has no peak, and peaks of different metrics can come from different 20-second blocks (peak-20-second-metrics). CSV header changed to match; values unchanged. C, I, L reworded so hedges sit in wrong options too (truth kept).

## Metadata
```yaml
id: "0106"
title: "The same CPU Ready on quiet and busy VMs"
product: [vsphere]
technology: [cpu]
task: read-metric
level: 400
answer_type: deterministic
misconception: [G,H]
input: [table]
object: [vm]
tool: [vcenter]
knowledge:
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
  - vsphere/technology/cpu/metrics/virtual-motherboard/run
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/ready
attachments:
  - 0106/vms-cpu-ready-10-to-11.csv
origin: synthetic
source_path: "Synthetic, 2026-11-12"
misconception_type: [threshold-transplanted]
pair: "0364"
status: draft
```
