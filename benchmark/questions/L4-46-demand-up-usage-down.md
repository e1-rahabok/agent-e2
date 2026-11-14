# Demand up, Usage down, Latency up

## Prompt
- A 12-vCPU VM, etl-worker-14, on hosts with a base clock of 2.1 GHz: its capacity is 25,200 MHz.
- [The attached vSphere Client export](0102/etl-worker-14-cpu-past-week-chart.csv) holds 3 days in 30-minute points: CPU Demand (MHz), Usage (%), Latency (%) and Readiness (%).
- vCenter keeps statistics level 4 for the past-week interval.
- On 10 November at about 21:30 the lines changed and stayed changed. Nobody changed the VM.

Why did Demand rise while Usage fell, why is Latency higher than Demand minus Usage, and what do you check? Which statements are correct?

- A. After 21:30, Demand rose from about 27% to about 36.5% of capacity while Usage fell from about 26.5% to about 24%.
- B. Readiness stayed below 1% in every point, before and after 21:30.
- C. The loss happens while the vCPUs run: a busy sibling thread and a lower clock speed slow them down.
- D. Usage carries the Hyper-Threading charge for a shared core; Demand does not.
- E. Latency also counts the clock-speed effect, so it sits near 28% while Demand minus Usage is about 12 points.
- F. Demand minus Usage, about 12 points, is the CPU time the VM asked for and was denied: its unmet demand.
- G. With Readiness below 1% in every point, the host cannot be what slows the VM down after 21:30.
- H. Latency rising from about 1.5% to about 28% means the vCPUs now wait about a quarter of the time to be scheduled.
- I. A CPU limit applied at 21:30 fits the pattern: a limit holds Usage down while Demand keeps rising.
- J. Adding vCPUs to etl-worker-14 would win back the throughput it lost at 21:30, since its Demand rose.
- K. Check what changed on the host at 21:30: sibling-thread load, a move to another host, the power policy and the clock speed.

## Likely wrong answer
- F: "Demand minus Usage is the unmet demand: the VM lost about 12% of its CPU."
- G: "Readiness is below 1%, so there is no CPU contention."
- J: "The VM is starved of CPU: give it more vCPUs."

## Expected key points
- Answer: A, B, C, D, E, K.
- A true: Demand averages about 6,850 MHz before and 9,200 MHz after (27.2% and 36.5% of 25,200 MHz); Usage about 26.6% before and 24.3% after.
- B true: Readiness is 0.22-0.61% in every point, before and after: the vCPUs were not waiting for a physical thread.
- C true: the vCPUs are not waiting, yet they get less done: they run slower, from Hyper-Threading and frequency.
- D true: Usage is charged 37.5% when both threads of a core run; Demand assumes the VM does not share the core. So Demand minus Usage holds only that charge.
- E true: Latency includes the Hyper-Threading effect and power saving below nominal frequency; Demand minus Usage includes only Hyper-Threading. After 21:30 Latency is 26.7-29.0% against a gap of about 12 points.
- F false: Demand minus Usage is not unmet demand; a limit, for example, leaves Demand equal to Usage. It holds only the Hyper-Threading charge.
- G false: Ready does not register Hyper-Threading or frequency; the VM loses throughput while it runs.
- H false: a rise in CPU Latency does not mean waiting: Latency also counts the sibling-thread and frequency effects, while time waiting for a physical thread shows in Readiness, which stays below 1%.
- I false: nobody changed the VM, and under a limit Demand stays at Usage; the time a limit holds back shows in Ready (Max Limited), which stays below 1%.
- J false: more vCPUs change neither the sibling-thread load nor the clock speed; the VM uses about a quarter of its capacity.
- K true: Demand rose and Usage fell at once with no change on the VM: something changed on the host it runs on.

## Notes
- From the author's samples: Demand jumped while Usage dropped, and the contention line jumped more than Demand minus Usage, because it accounts for both frequency and Hyper-Threading. In VCF Operations 8.18 and later the CPU Contention metric no longer counts frequency and Hyper-Threading, so the question uses the vSphere CPU Latency counter, which does.
- Not used from that sample: Usage above Demand at some points (Demand is smoothed over a longer window).
- Converted from judged to multiple choice (Q199 F, 2026-11-14).
- Export regenerated 2026-11-14 with new numbers and a new VM (seeded script; project/question-pairing-2026-11-14.md, decision 3): the old export equalled the Demand, Usage and Latency example of the VM CPU Demand knowledge file. Options A and B now state the reading only and D one fact: their old clauses (the extra demand was not met; the vCPUs were not waiting; the gap holds only the Hyper-Threading charge) negated F and H. Key unchanged (author approved, 2026-11-14).
- Paired with 0002 (theory and practical, design.md 3.9).

## Metadata
```yaml
id: "0102"
title: "Demand up, Usage down, Latency up"
product: [vsphere]
technology: [cpu]
task: explain-mechanism
level: 400
answer_type: deterministic
answer: [A,B,C,D,E,K]
misconception: [F,G,J]
input: [table]
object: [vm, esxi]
tool: [vcenter]
knowledge:
  - vsphere/technology/cpu/metrics/virtual-motherboard/demand
  - vsphere/technology/cpu/metrics/virtual-motherboard/latency
  - vsphere/technology/cpu/metrics/virtual-motherboard/usage
  - vsphere/technology/cpu/concepts/hyper-threading
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/demand
attachments:
  - 0102/etl-worker-14-cpu-past-week-chart.csv
origin: book
source_path: "Author samples (docx, 2026-11-12) > Demand jumped while Usage dropped; Contention above Demand - Usage"
misconception_type: [frequency-and-hyper-threading, consumption-as-contention]
pair: "0002"
status: draft
```
