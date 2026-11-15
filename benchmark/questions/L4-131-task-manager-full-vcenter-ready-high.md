# Task Manager at 100%, vCenter shows a different picture

## Prompt
- The owner of a 4-vCPU Windows Server VM sends [the Task Manager screen](0368/task-manager-cpu-performance.png): "The CPU is maxed out. Give the VM 4 more vCPUs."
- You open [the vSphere Client CPU chart](0368/vcenter-vm-cpu-real-time.png) of the same VM for the same ten minutes. The VM has no CPU limit.

Which statements are correct?

- A. Task Manager's figure includes time its vCPUs sat frozen in Ready, because Windows cannot see that time.
- B. The chart's Readiness is the share of time each vCPU had work and no thread free.
- C. On the chart, Run stays below 64,000 ms per sample: under 80% per vCPU.
- D. Readiness on the chart stays below 5%, so the host gives the VM what it asks.
- E. Task Manager shows only one of the four processors busy: the guest runs a single thread.
- F. The two tools disagree, so one of the counters is collected wrongly.
- G. Add 4 vCPUs: the guest keeps all four busy.
- H. Task Manager is of no use on a VM: its CPU figure is simply wrong.
- I. With VMware Tools running, Windows would report the frozen time as steal time.
- J. The next checks are the VM's shares, the host's overcommit and the Ready of the other VMs.

## Input to supply
- Product and version: vSphere 9.1 (vSphere Client); Windows Server 2022 or 2025 guest with VMware Tools running.
- Object: one Windows VM with 4 vCPUs, no CPU limit, shares at Normal.
- Screen 1, Task Manager > Performance > CPU, graph changed to Logical processors (right-click the graph > Change graph to > Logical processors), after about ten minutes of load. Save as `0368/task-manager-cpu-performance.png`.
- Screen 2, vSphere Client > the VM > Monitor > Performance > Advanced > CPU, Chart Options: Real-time, the last 10-15 minutes, object the VM (not the vCPU instances), counters Readiness (%), Ready (ms), Run (ms), Co-stop (ms). Save as `0368/vcenter-vm-cpu-real-time.png`; include the legend table with Latest, Maximum, Average.
- How to produce it in a lab: run a 4-thread CPU burner in the Windows VM (for example 4 instances of a busy loop, or a stress tool set to 4 threads) on a host where other VMs also run CPU burners, so that the burning vCPUs total about 1.5-2 times the host's physical threads. No limits; default shares.
- Condition the key depends on: all four logical processors in Task Manager at 90-100% for the whole window; vSphere Readiness (%) between 22% and 35% for most of the window; Run (ms) between 40,000 and 60,000 ms per sample; Co-stop below Ready; no CPU limit on the VM. If a value falls outside its range, change the load on the other VMs and capture again.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
G: Task Manager shows the CPU maxed out, so the VM needs more vCPUs. Or F: the tools disagree, so one is wrong.

## Expected key points
- Answer: A, B, C, J.
- A true: a frozen vCPU stays in the state it was in; Windows has no steal accounting, so a busy vCPU's frozen time counts as busy.
- B true: Readiness is per vCPU: the share of each sample a vCPU had work and no physical thread.
- C true: reading. Run is 40,000-60,000 ms of the 80,000 ms that four vCPUs hold per 20-second sample (50-75% per vCPU); Ready takes a fifth or more of the time, so Run cannot reach the figure Task Manager shows.
- D false: reading. Readiness stays between 22% and 35%.
- E false: reading. All four logical processors are busy.
- F false: the misconception. The tools count at different layers: the guest kernel cannot see the time it was frozen, vSphere can.
- G false: the wrong action. The vCPUs wait for physical threads; more vCPUs on a busy host are harder to schedule and tend to raise Ready and Co-stop.
- H false: over-correction. Each layer shows its own problems (run queue, processes); read both, each at its own layer.
- I false: Windows has no steal time; VMware Tools does not change that.
- J true: with no limit, Ready comes from the VM's shares or the host's load; many VMs in Ready at once points to an overcommitted host.

## Reasoning path
1. Readiness at a fifth to a third of each sample: the vCPUs wait for physical threads.
2. Task Manager cannot see that wait, so it reads near 100% on all four processors.
3. The cure is the VM's shares or the host's load and placement, not the vCPU count.

## Notes
- Paired with the theory question 0266 (theory and practical; design.md, section 3.9).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item C1). The options hold for any capture that meets the condition above. Counts only after author approval.
- Review 2026-11-15: stem no longer quotes the value; screen readings added (C true; D, E false); J names the VM's shares as a VM-side check. Key changed from A, B, C, F, I to A, B, C, J (options relettered).

## Metadata
```yaml
id: "0368"
title: "Task Manager at 100%, vCenter shows a different picture"
product: [vsphere, windows]
technology: [cpu]
task: troubleshoot
level: 400
answer_type: deterministic
input: [screenshot]
object: [vm, guest-os, esxi]
tool: [vcenter, guest-os-tools]
knowledge:
  - vsphere/technology/cpu/concepts/guest-os-vs-vm-cpu
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
  - vsphere/technology/cpu/concepts/vcpu-states
  - vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high
knowledge_main: vsphere/technology/cpu/concepts/guest-os-vs-vm-cpu
attachments:
  - 0368/task-manager-cpu-performance.png
  - 0368/vcenter-vm-cpu-real-time.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C1"
answer: [A, B, C, J]
misconception: [F, G]
misconception_type: [layer-confusion, tool-confusion]
pair: "0266"
status: awaiting-input
```
