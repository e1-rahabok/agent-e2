# CPU Contention and CPU Latency disagree

## Prompt
- Three VMs, the same busy 5-minute interval. CPU Contention is from VCF Operations 9.1; the other counters are from the vSphere Client Past day chart, converted to % per vCPU.

| VM | CPU Contention | CPU Latency | Ready | Max Limited | Co-stop | Overlap |
|---|---|---|---|---|---|---|
| db-11 (8 vCPUs) | 9% | 10% | 8.5% | 0% | 0.4% | 0.1% |
| app-31 (4 vCPUs) | 0.8% | 38% | 0.5% | 0% | 0.1% | 0.2% |
| web-07 (8 vCPUs) | 15.4% | 0.9% | 15% | 14.7% | 0.3% | 0.1% |

- app-31's host: power policy Balanced, Utilization (per thread) 88%. The esxtop power panel shows %A/MPERF about 90. db-11 and app-31 have no CPU limit.
- Inside app-31 the run queue is short.

Which statements are correct?

- A. Most of db-11's 9% CPU Contention is Ready: its vCPUs waited for a physical thread.
- B. app-31's 0.8% CPU Contention shows its vCPUs rarely waited to be scheduled.
- C. VCF Operations 9.1 CPU Contention counts the loss from a busy sibling thread and a slow clock.
- D. The two tools disagree on app-31, so one of them reports wrong data.
- E. CPU Contention counts the time a CPU limit holds a vCPU back.
- F. Raise app-31's CPU shares above its neighbours' to bring its CPU Latency down.
- G. CPU Contention counts Swap Wait, the time a vCPU waits for a page to come in from ESXi swap.
- H. web-07's CPU Latency below 1% shows its vCPUs rarely waited for CPU.

## Answers
A, B, E

## Explanation
- A is correct: Ready (8.5%) makes up most of db-11's 9% (Ready + Co-stop + Overlap = 9.0%). db-11 has no limit (Max Limited 0%), so its vCPUs waited for a physical thread or behind higher shares; shares and host load are the next checks.
- B is correct: since Aria Operations 8.18 (July 2024), CPU Contention = Ready (with the time a limit holds back) + Co-stop + Overlap + Other Wait when below 1%. app-31's parts are low, so it barely waited.
- C is wrong: that was CPU Contention before Aria Operations 8.18, when it mapped to CPU Latency. Now it counts only time the vCPU does not run; frequency does not apply to a vCPU that is not running.
- D is wrong: two counters with two formulas. Each is right for what it counts.
- E is correct: Contention includes Ready caused by a limit, so it shows the VM's contention whatever the cause. web-07's 15.4% is its Ready (almost all Max Limited) plus Co-stop and Overlap.
- F is wrong: app-31's 38% is the busy sibling thread (Utilization per thread 88%) and a clock at about 90% of nominal, which CPU Latency counts and Ready does not. Shares decide who runs first when vCPUs wait in Ready; app-31 is not waiting, and shares change neither the sibling load nor the clock.
- G is wrong: Swap Wait belongs to memory contention, not to CPU Contention.
- H is wrong: CPU Latency leaves out Max Limited. web-07's Ready of 15%, nearly all of it Max Limited, is time its limit held the vCPUs back; Latency near 0% with Ready above 15% is the sign of a limit.
- Misconception: C: CPU Contention read as the old Latency-based counter. Or D: one tool must be wrong. Or H: low CPU Latency read as no waiting on a VM that a limit holds back.

## Notes
- Revised 2026-11-12: the earlier key said VCF Operations CPU Contention counts frequency and Hyper-Threading. That was true before Aria Operations 8.18 (Contention mapped to CPU Latency); in 9.1 it is false. The question now tests the difference between the two counters.
- Hint moved out of the prompt (author, 2026-11-14: a hint helps the frontier model, not the local model), for reviewers: ": the cores run below the base clock" (after %A/MPERF about 90).
- Trimmed 2026-11-14 to what CPU Contention counts (project/question-pairing-2026-11-14.md, decision 4): the options on CPU Latency counting frequency and Hyper-Threading (old B, C, E) were removed, because 0002 and 0102 test that fact; C, E and G are new single facts on Contention. Key changed from A, C, E to A, B, E.
- 2026-11-15 audit: the stem now gives one 5-minute interval (VCF Operations has no 20-second peak of Contention; peak-20-second-metrics) and a third VM, web-07, held back by a limit, so E is read from the table and H tests "Latency 0% means no contention" (latency, Misconceptions; the second question on that fact, with 0002 G).

## Metadata
```yaml
id: "0059"
title: "CPU Contention and CPU Latency disagree"
product: [vsphere, vcf-operations]
technology: [cpu]
task: troubleshoot
level: 400
answer_type: deterministic
input: [text]
object: [vm, esxi]
tool: [vcf-operations, vcenter]
knowledge:
  - vsphere/technology/cpu/metrics/virtual-motherboard/contention
  - vsphere/technology/cpu/metrics/virtual-motherboard/latency
  - vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high
  - vsphere/technology/cpu/concepts/hyper-threading
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/contention
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-05; revised 2026-11-12"
misconception: [C, D, H]
misconception_type: [tool-confusion, frequency-and-hyper-threading]
status: draft
```
