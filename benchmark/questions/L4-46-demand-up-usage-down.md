# Demand up, Usage down, Latency up

## Prompt
- An 8-vCPU VM, app-22, on hosts with a base clock of 2.5 GHz: its capacity is 20,000 MHz.
- [The attached vSphere Client export](0102/app-22-cpu-1-week-chart.csv) holds 4 days in 30-minute points: CPU Demand (MHz), Usage (%), Latency (%) and Readiness (%).
- vCenter keeps statistics level 4 for the past-week interval.
- On 4 November at about 03:00 the lines changed and stayed changed. Nobody changed the VM.

Why did Demand rise while Usage fell, why is Latency higher than Demand minus Usage, and what do you check? Which statements are correct?

- A. After 03:00 Demand rose from about 18.5% to 25% while Usage fell from about 18% to 16%: the extra demand was not met.
- B. Readiness stayed below 1%, so the vCPUs were not waiting for a physical thread.
- C. The loss happens while the vCPUs run: a busy sibling thread and a lower clock speed slow them down.
- D. Usage carries the Hyper-Threading charge and Demand does not, so Demand minus Usage holds only that charge.
- E. Latency also counts the clock-speed effect, so it sits near 19.5% while Demand minus Usage is about 9 points.
- F. Demand minus Usage, about 9 points, is the CPU time the VM asked for and was denied: its unmet demand.
- G. With Readiness below 1% in every point, the host cannot be what slows the VM down after 03:00.
- H. Latency rising from about 2% to about 19.5% means the vCPUs now wait about a fifth of the time to be scheduled.
- I. A CPU limit applied at 03:00 fits the pattern: a limit holds Usage down while Demand keeps rising.
- J. Adding vCPUs to app-22 would win back the throughput it lost at 03:00, since its Demand rose.
- K. Check what changed on the host at 03:00: sibling-thread load, a move to another host, the power policy and the clock speed.

## Likely wrong answer
- F: "Demand minus Usage is the unmet demand: the VM lost about 9% of its CPU."
- G: "Readiness is below 1%, so there is no CPU contention."
- J: "The VM is starved of CPU: give it more vCPUs."

## Expected key points
- Answer: A, B, C, D, E, K.
- A true: Demand averages about 3,700 MHz before and 5,000 MHz after (18.6% and 25% of 20,000 MHz); Usage about 18.0% before and 16.2% after. Demand up and Usage down: the extra demand was not met.
- B true: Readiness is 0.3-0.65% in every point, before and after.
- C true: the vCPUs are not waiting, yet they get less done: they run slower, from Hyper-Threading and frequency.
- D true: Usage is charged 37.5% when both threads of a core run; Demand assumes the VM does not share the core.
- E true: Latency includes the Hyper-Threading effect and power saving below nominal frequency; Demand minus Usage includes only Hyper-Threading.
- F false: Demand minus Usage is not unmet demand; a limit, for example, leaves Demand equal to Usage. It holds only the Hyper-Threading charge.
- G false: Ready does not register Hyper-Threading or frequency; the VM loses throughput while it runs.
- H false: a rise in CPU Latency does not mean waiting; waiting shows in Ready and Co-stop, which stay low. Latency here is mostly sibling-thread and frequency effects.
- I false: nobody changed the VM, and under a limit Demand stays at Usage; the time a limit holds back shows in Ready (Max Limited), which stays below 1%.
- J false: more vCPUs change neither the sibling-thread load nor the clock speed; the VM uses about a quarter of its capacity.
- K true: Demand rose and Usage fell at once with no change on the VM: something changed on the host it runs on.

## Notes
- From the author's samples: Demand jumped while Usage dropped, and the contention line jumped more than Demand minus Usage, because it accounts for both frequency and Hyper-Threading. In VCF Operations 8.18 and later the CPU Contention metric no longer counts frequency and Hyper-Threading, so the question uses the vSphere CPU Latency counter, which does.
- Not used from that sample: Usage above Demand at some points (Demand is smoothed over a longer window).
- Converted from judged to multiple choice (Q199 F, 2026-11-14).

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
  - 0102/app-22-cpu-1-week-chart.csv
origin: book
source_path: "Author samples (docx, 2026-11-12) > Demand jumped while Usage dropped; Contention above Demand - Usage"
misconception_type: [frequency-and-hyper-threading, consumption-as-contention]
status: draft
```
