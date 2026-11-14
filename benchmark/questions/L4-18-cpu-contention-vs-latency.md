# CPU Contention and CPU Latency disagree

## Prompt
- Two VMs, one hour, 20-second peaks, normalized by vCPU count. CPU Contention is from VCF Operations 9.1; the other counters are from the vSphere Client.

| VM | CPU Contention | CPU Latency | Ready | Co-stop | Overlap |
|---|---|---|---|---|---|
| db-11 (8 vCPUs) | 9% | 10% | 8.5% | 0.4% | 0.1% |
| app-31 (4 vCPUs) | 0.8% | 38% | 0.5% | 0.1% | 0.2% |

- app-31's host: power policy Balanced, Utilization (per thread) 88%. The esxtop power panel shows %A/MPERF about 90. Neither VM has a CPU limit.
- Inside app-31 the run queue is short.

Which statements are correct?

- A. Most of db-11's 9% CPU Contention is Ready: its vCPUs waited for a physical thread.
- B. app-31's 0.8% CPU Contention shows its vCPUs rarely waited to be scheduled.
- C. In VCF Operations 9.1, CPU Contention counts the throughput a vCPU loses to a busy sibling thread and to a clock below nominal.
- D. The two tools disagree on app-31, so one of them reports wrong data.
- E. CPU Contention counts the time a CPU limit holds a vCPU back.
- F. Raise app-31's CPU shares to bring its Latency down.
- G. CPU Contention counts Swap Wait, the time a vCPU waits for a page to come in from ESXi swap.

## Likely wrong answer
C: CPU Contention read as the old Latency-based counter. Or D: one tool must be wrong.

## Expected key points
- Answer: A, B, E.
- A: Ready (8.5%) makes up most of db-11's 9% (Ready + Co-stop + Overlap = 9.0%); db-11 waits for a thread. Its limits, shares and host load are the next checks.
- B: from VCF Operations 8.18, CPU Contention = Ready (with the time a limit holds back) + Co-stop + Overlap + Other Wait when below 1%. app-31's parts are low, so it barely waited.
- C is wrong: that was CPU Contention before VCF Operations 8.18, when it mapped to CPU Latency. Now it counts only time the vCPU does not run; frequency does not apply to a vCPU that is not running.
- D is wrong: two counters with two formulas. Each is right for what it counts.
- E: Contention includes Ready caused by a limit, so it shows the VM's contention whatever the cause; CPU Latency leaves that time out.
- F is wrong: shares decide who runs first when vCPUs wait in Ready; app-31 is not waiting.
- G is wrong: Swap Wait belongs to memory contention, not to CPU Contention.

## Notes
- Revised 2026-11-12: the earlier key said VCF Operations CPU Contention counts frequency and Hyper-Threading. That was true before VCF Operations 8.18 (Contention mapped to CPU Latency); in 9.1 it is false. The question now tests the difference between the two counters.
- Hint moved out of the prompt (author, 2026-11-14: a hint helps the frontier model, not the local model), for reviewers: ": the cores run below the base clock" (after %A/MPERF about 90).
- Trimmed 2026-11-14 to what CPU Contention counts (project/question-pairing-2026-11-14.md, decision 4): the options on CPU Latency counting frequency and Hyper-Threading (old B, C, E) were removed, because 0002 and 0102 test that fact; C, E and G are new single facts on Contention. Key changed from A, C, E to A, B, E.

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
source_path: "Drafted by Claude 2026-11-05; revised 2026-11-12"
answer: [A, B, E]
misconception: [C, D]
misconception_type: [tool-confusion, frequency-and-hyper-threading]
status: draft
```
