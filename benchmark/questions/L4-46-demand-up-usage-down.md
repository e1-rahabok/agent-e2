# Demand up, Usage down, Latency up

## Prompt
- An 8-vCPU VM, app-22, on hosts with a base clock of 2.5 GHz: its capacity is 20,000 MHz.
- [The attached vSphere Client export](0102/app-22-cpu-1-week-chart.csv) holds 4 days in 30-minute points: CPU Demand (MHz), Usage (%), Latency (%) and Readiness (%).
- vCenter keeps statistics level 4 for the past-week interval.
- On 4 November at about 03:00 the lines changed and stayed changed. Nobody changed the VM.

Explain the change. Why did Demand rise while Usage fell, and why is Latency higher than Demand minus Usage? Is the VM short of CPU, and what do you check?

## Likely wrong answer
"Demand minus Usage is the unmet demand: the VM lost about 9% of its CPU. Readiness is below 1%, so there is no CPU contention." Or: "The VM is starved of CPU."

## Expected key points
- The VM asked for more CPU (Demand from about 18.5% to 25% of its capacity) and got less work done (Usage from about 18% to 16%): its extra demand was not met.
- Readiness stayed below 1%: the vCPUs were not waiting for a physical thread. The loss happens while they run: a busy sibling thread (Hyper-Threading) and a lower clock speed slow them down.
- Usage carries the Hyper-Threading charge and Demand does not, so Demand minus Usage (about 9 points) holds only the Hyper-Threading part.
- Latency also counts the frequency effect, so it is higher (about 19.5%) than Demand minus Usage. Demand minus Usage is not the unmet demand.
- Check what changed on the host at 03:00: new load on the sibling threads (host Utilization against Core Utilization), a move to a busier host, the power policy and the actual frequency.

## Notes
- From the author's samples: Demand jumped while Usage dropped, and the contention line jumped more than Demand minus Usage, because it accounts for both frequency and Hyper-Threading. In VCF Operations 8.18 and later the CPU Contention metric no longer counts frequency and Hyper-Threading, so the question uses the vSphere CPU Latency counter, which does.
- Not used from that sample: Usage above Demand at some points (Demand is smoothed over a longer window).

## Metadata
```yaml
id: "0102"
title: "Demand up, Usage down, Latency up"
product: [vsphere]
technology: [cpu]
task: explain-mechanism
level: 400
answer_type: judged
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
