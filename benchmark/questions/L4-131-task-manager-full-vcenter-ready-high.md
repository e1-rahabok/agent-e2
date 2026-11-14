# Task Manager at 100%, vCenter shows a different picture

## Prompt
- The owner of a 4-vCPU Windows Server VM sends [the Task Manager screen](0368/task-manager-cpu-performance.png): "CPU has been at 100% for ten minutes. Give the VM 4 more vCPUs."
- You open [the vSphere Client CPU chart](0368/vcenter-vm-cpu-real-time.png) of the same VM for the same ten minutes. The VM has no CPU limit.

Which statements are correct?

- A. Windows does not know when its vCPUs were frozen, so it counts that time as busy and reads higher than vSphere.
- B. Readiness of about 25-40% means each vCPU spent that share of the time with work to run and no physical thread free.
- C. With Readiness at 25-40%, the vCPUs ran at most about 60-75% of the time in vSphere's accounting.
- D. The two tools disagree, so one of the counters is collected wrongly.
- E. Add 4 vCPUs: the guest keeps all 4 busy at about 100%.
- F. On this busy host, more vCPUs would add demand and tend to raise the VM's Ready.
- G. Task Manager is of no use on a VM: its CPU figure is simply wrong.
- H. With VMware Tools running, Windows would report the frozen time as steal time.
- I. The next checks are on the host side: the VM's shares, the host's overcommit and the Ready of the other VMs.

## Input to supply
- Product and version: vSphere 9.1 (vSphere Client); Windows Server 2022 or 2025 guest with VMware Tools running.
- Object: one Windows VM with 4 vCPUs, no CPU limit, shares at Normal.
- Screen 1, Task Manager > Performance > CPU, the utilization graph after about ten minutes of load (right-click the graph > Change graph to > Logical processors is optional). Save as `0368/task-manager-cpu-performance.png`.
- Screen 2, vSphere Client > the VM > Monitor > Performance > Advanced > CPU, Chart Options: Real-time, the last 10-15 minutes, object the VM (not the vCPU instances), counters Readiness (%), Ready (ms), Run (ms), Co-stop (ms). Save as `0368/vcenter-vm-cpu-real-time.png`; include the legend table with Latest, Maximum, Average.
- How to produce it in a lab: run a 4-thread CPU burner in the Windows VM (for example 4 instances of a busy loop, or a stress tool set to 4 threads) on a host where other VMs also run CPU burners, so that the burning vCPUs total about 1.5-2 times the host's physical threads. No limits; default shares.
- Condition the key depends on: Task Manager CPU at 95-100% for the whole window; vSphere Readiness (%) between 25% and 40% for most of the window; Co-stop below Ready; no CPU limit on the VM. If Readiness falls outside 25-40%, change the load on the other VMs and capture again.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
E: Task Manager shows 100%, so the VM needs more vCPUs. Or D: the tools disagree, so one is wrong.

## Expected key points
- Answer: A, B, C, F, I.
- A true: a frozen vCPU stays in the state it was in; Windows has no steal accounting, so time spent in Ready counts as busy for a busy vCPU.
- B true: Readiness is per vCPU; Ready is demanded run time the kernel could not give.
- C true: per vCPU, Run + Ready + Co-stop + Wait fills each 20-second sample; with 25-40% in Ready, Run is at most 60-75%.
- D false: the misconception. The tools count at different layers: the guest kernel cannot see the time it was frozen, vSphere can.
- E false: the wrong action. The vCPUs wait for physical threads; Task Manager's 100% includes the frozen time.
- F true: more vCPUs on a busy host are harder to schedule and tend to raise Ready and Co-stop.
- G false: over-correction. Each layer shows its own problems (run queue, processes); read both, each at its own layer.
- H false: Windows has no steal time; VMware Tools does not change that.
- I true: with no limit, Ready comes from shares or host load; many VMs with Ready at once points to an overcommitted host.

## Reasoning path
1. Readiness 25-40% per vCPU: the vCPUs wait for physical threads.
2. Task Manager cannot see that wait, so it reads near 100%.
3. The cure is on the host side (load, placement, shares), not the vCPU count.

## Notes
- Paired with the theory question 0266 (theory and practical; design.md, section 3.9).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item C1). The options hold for any capture that meets the condition above. Counts only after author approval.

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
answer: [A, B, C, F, I]
misconception: [D, E]
misconception_type: [layer-confusion, tool-confusion]
pair: "0266"
status: awaiting-input
```
