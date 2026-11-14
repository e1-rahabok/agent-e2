# CPU Wait fills the chart of a quiet VM

## Prompt
- The owner of a 4-vCPU VM sends [the vSphere Client chart](0372/vcenter-vm-cpu-states-real-time.png): "CPU Wait is huge. The VM must be stuck on disk. Move it to faster storage."

Which statements are correct?

- A. Most of the Wait is Idle: the guest halted its vCPUs because it had no work.
- B. A Wait this high shows the VM is blocked on disk most of the time.
- C. In each 20-second sample, Run, Ready, Co-stop and Wait add up to about 80,000 ms for the 4 vCPUs.
- D. Each vCPU spent about 90% of the time in Wait.
- E. The part of Wait that is not Idle (Swap Wait and Other Wait) is small on this chart.
- F. Wait is the time a vCPU had work to run but no physical thread to run on.
- G. Wait holds only idle time, so a disk or memory stall can never show in it.
- H. Move the VM to a faster datastore to bring the Wait down.
- I. A vCPU in Wait keeps its physical thread, so the VM ties up most of four threads.
- J. A disk problem would show in the VM's disk latency counters, not in CPU Wait alone.

## Input to supply
- Product and version: vSphere 9.1 (vSphere Client).
- Object: one VM with 4 vCPUs, mostly idle (a guest with light background load only).
- Screen, vSphere Client > the VM > Monitor > Performance > Advanced > CPU, Chart Options: Real-time, the last hour, object the VM (not the vCPU instances), counters Wait (ms), Idle (ms), Run (ms), Ready (ms), Co-stop (ms), chart type line, with the legend table (Latest, Maximum, Average). Save as `0372/vcenter-vm-cpu-states-real-time.png`.
- How to produce it: any 4-vCPU VM with light load (for example a web server with no users) on a host that is not busy.
- Condition the key depends on: Wait about 70,000-75,000 ms per sample; Idle within 1,000 ms of Wait; Run about 5,000-10,000 ms; Ready below 400 ms; Co-stop near 0.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
B or H: Wait near its maximum means the VM waits on disk, so move it to faster storage.

## Expected key points
- Answer: A, C, D, E, J.
- A true: Idle within 1,000 ms of Wait. A halted vCPU is de-scheduled and counted in Wait.
- B false: the misconception. ESXi cannot tell an idle guest from one blocked on IO; here nearly all of Wait is Idle.
- C true: per vCPU, Run + Ready + Co-stop + Wait = 20,000 ms per sample; the VM value sums four vCPUs.
- D true: 70,000-75,000 of 80,000 ms is about 88-94%.
- E true: Wait - Idle = Swap Wait + Other Wait, under 1,000 ms here.
- F false: that is Ready.
- G false: over-correction. Wait = Idle + Swap Wait + Other Wait; a memory or IO stall shows in its non-idle part.
- H false: wrong action. The Wait is idle time; faster storage does not change it.
- I false: a halted vCPU holds no physical thread; other VMs can run there.
- J true: Wait alone proves no bottleneck; disk latency or memory contention gives the evidence.

## Reasoning path
1. Compare Wait with Idle: nearly equal.
2. Add the states: 80,000 ms per sample for 4 vCPUs.
3. The VM is quiet, not blocked.

## Notes
- Paired with the theory question 0001 (theory and practical; design.md, section 3.9).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item C9). Counts only after author approval.

## Metadata
```yaml
id: "0372"
title: "CPU Wait fills the chart of a quiet VM"
product: [vsphere]
technology: [cpu]
task: read-metric
level: 300
answer_type: deterministic
input: [screenshot]
object: [vm]
tool: [vcenter]
knowledge:
  - vsphere/technology/cpu/metrics/virtual-motherboard/wait
  - vsphere/technology/cpu/concepts/vcpu-states
  - vsphere/technology/cpu/metrics/virtual-motherboard/idle
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/wait
attachments:
  - 0372/vcenter-vm-cpu-states-real-time.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C9"
answer: [A, C, D, E, J]
misconception: [B]
misconception_type: [layer-confusion]
pair: "0001"
status: awaiting-input
```
