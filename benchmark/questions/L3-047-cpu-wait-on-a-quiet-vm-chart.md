# CPU Wait fills the chart of a quiet VM

## Prompt
- A monitoring screen flags an 8-vCPU VM: "CPU Wait critical." The service desk asks whether the VM is starved of CPU and should get more vCPUs.
- See [the vSphere Client chart](0372/vcenter-vm-cpu-states-real-time.png) of the VM.

Which statements are correct?

- A. Most of the Wait on the chart is Idle: the guest had halted its vCPUs for lack of work.
- B. The chart shows the VM waiting for physical CPU most of the time.
- C. Each 20-second sample of the chart adds up to about 160,000 ms across Run, Ready, Co-stop and Wait.
- D. On average, a vCPU spent about 90% of the time in Wait.
- E. Wait minus Idle, the part made of Swap Wait and Other Wait, stays under 1,000 ms on the chart.
- F. Ready on the chart is above 5,000 ms in most samples.
- G. Wait holds nothing but idle time, so stalls on IO or swapped memory can never appear in it.
- H. Add vCPUs so that each one waits less.
- I. A halted vCPU stays parked on its physical thread until the guest wakes it.
- J. Whether the VM is held back is read from Ready and Co-stop, which stay low here.

## Input to supply
- Product and version: vSphere 9.1 (vSphere Client).
- Object: one VM with 8 vCPUs, mostly idle (a guest with light background load only).
- Screen, vSphere Client > the VM > Monitor > Performance > Advanced > CPU, Chart Options: Real-time, the last hour, object the VM (not the vCPU instances), counters Wait (ms), Idle (ms), Run (ms), Ready (ms), Co-stop (ms), chart type line, with the legend table (Latest, Maximum, Average). Save as `0372/vcenter-vm-cpu-states-real-time.png`.
- How to produce it: any 8-vCPU VM with light load (for example an application server with no users) on a host that is not busy.
- Condition the key depends on: Wait 140,000-150,000 ms per sample; Idle within 1,000 ms of Wait; Run 10,000-20,000 ms; Ready below 800 ms; Co-stop near 0; Run + Ready + Co-stop + Wait about 160,000 ms.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
B or H: Wait near its maximum means the VM waits for CPU, so give it more vCPUs.

## Expected key points
- Answer: A, C, D, E, J.
- A true: Idle within 1,000 ms of Wait. A halted vCPU is de-scheduled and counted in Wait.
- B false: the misconception. Waiting for a physical thread is Ready, which stays below 800 ms; Wait is mostly the guest's own idle time.
- C true: per vCPU, Run + Ready + Co-stop + Wait = 20,000 ms per sample; the VM value sums eight vCPUs.
- D true: 140,000-150,000 of 160,000 ms is about 88-94% per vCPU on average.
- E true: Wait - Idle = Swap Wait + Other Wait, under 1,000 ms here.
- F false: reading. Ready stays below 800 ms per sample.
- G false: over-correction. Wait = Idle + Swap Wait + Other Wait; IO and swap stalls show in its non-idle part.
- H false: wrong action. The vCPUs are idle, not waiting for threads; more vCPUs add idle vCPUs and make the VM harder to schedule.
- I false: a halted vCPU is de-scheduled and holds no physical thread; other VMs can run there.
- J true: Ready and Co-stop are the waits for the hypervisor; both are near 0.

## Reasoning path
1. Compare Wait with Idle: nearly equal.
2. Add the states: 160,000 ms per sample for 8 vCPUs.
3. Ready and Co-stop near 0: the VM is quiet, not starved.

## Notes
- Paired with the theory question 0001 (theory and practical; design.md, section 3.9).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item C9). Counts only after author approval.
- Review 2026-11-15: an 8-vCPU VM and a new story (Wait read as waiting for CPU), away from 0001 and from the knowledge-base chart of a 4-vCPU VM; screen reading F (false) added; I reworded. Key unchanged: A, C, D, E, J.

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
