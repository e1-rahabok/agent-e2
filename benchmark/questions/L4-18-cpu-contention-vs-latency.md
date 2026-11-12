# CPU Contention and CPU Latency disagree

## Prompt
- Two VMs, one hour, 20-second peaks, normalized by vCPU count. CPU Contention is from VCF Operations 9.1; the other counters are from the vSphere Client.

| VM | CPU Contention | CPU Latency | Ready | Co-stop | Overlap |
|---|---|---|---|---|---|
| db-11 (8 vCPUs) | 9% | 10% | 8.5% | 0.4% | 0.1% |
| app-31 (4 vCPUs) | 0.8% | 38% | 0.5% | 0.1% | 0.2% |

- app-31's host: power policy Balanced, Utilization (per thread) 88%. The esxtop power panel shows %A/MPERF about 90: the cores run below the base clock. Neither VM has a CPU limit.
- Inside app-31 the run queue is short.

Which statements are correct?

- A. db-11 waits for a physical thread: Ready is counted in both Contention and Latency, so the two agree.
- B. app-31 is starved of CPU: a Latency above 37.5% means the host cannot serve it.
- C. app-31 loses speed to Hyper-Threading and a lower clock: CPU Latency counts both, and Contention counts neither.
- D. The two tools disagree on app-31, so one of them reports wrong data.
- E. Setting app-31's host to High Performance removes the frequency part of its Latency; the Hyper-Threading part stays while sibling threads are busy.
- F. Raising app-31's CPU shares lowers its Latency.

## Likely wrong answer
B: a CPU Latency above 37.5% read as starvation. Or D: one tool must be wrong.

## Expected key points
- Answer: A, C, E.
- A: Ready (8.5%) is part of both counters; db-11 waits for a thread. Its host or placement is the next check.
- B is wrong: Ready, Co-stop and Overlap are low and the guest run queue is short; Hyper-Threading alone can cost up to 37.5%, and a lower clock adds to it.
- C: from VCF Operations 8.18, CPU Contention = Ready (with the time a limit holds back) + Co-stop + Overlap + Other Wait. CPU Latency counts Ready without the limit part, Co-stop, Overlap, the Hyper-Threading effect and power saving below the base clock.
- D is wrong: two counters with two formulas. Each is right for what it counts.
- E: High Performance stops power saving below the base clock (%A/MPERF about 90 shows it now). A busy sibling thread still slows the vCPU.
- F is wrong: shares decide who runs first when vCPUs wait in Ready; app-31 is not waiting.

## Notes
- Previous id: question-0059 (renamed 2026-11-05).
- Revised 2026-11-12: the earlier key said VCF Operations CPU Contention counts frequency and Hyper-Threading. That was true before VCF Operations 8.18 (Contention mapped to CPU Latency); in 9.1 it is false. The question now tests the difference between the two counters.

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
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6); revised 2026-11-12"
answer: [A, C, E]
misconception: [B, D]
misconception_type: [tool-confusion, frequency-and-hyper-threading]
status: draft
```
