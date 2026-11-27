# Demand above the base clock, Usage above 100%: is the host full?

## Prompt
- An ESXi 9.1 host has 48 cores at a 2.2 GHz base clock (105,600 MHz at base clock) and 96 threads (Hyper-Threading on).
- From 09:00 to 14:00 on a weekday, in the vSphere Client:
  - CPU Demand: about 150,000 MHz.
  - CPU Usage: about 112%.
  - Core Utilization: 80%. Utilization (per thread): 55%.
  - Per VM: Ready about 1.5%, Co-stop below 0.2%.
- The operations manager wants to stop placing VMs on this host because it is overloaded.

Which statements about this host are correct?

- A. Ready about 1.5% and Co-stop below 0.2% per VM show the VMs get the run time they ask for now.
- B. Demand about 40% above the base-clock total and Usage above 100% mean the host is out of CPU, so stop placing VMs.
- C. Usage of 112% on a Core Utilization of 80% means the busy cores run about 40% above the base clock.
- D. ESXi 9.1 caps Usage at 100%, so a reading of 112% points to a counter or collection error.
- E. Demand of 150,000 MHz means the VMs were refused about 44,000 MHz of the CPU they asked for.
- F. A second thread starting on a busy core raises its thread Utilization but not that core's Usage.
- G. Demand is summed over the VMs, so vCenter gives no Demand value per core or per thread.
- H. Core Utilization of 80% means that 80% of the host's CPU capacity is already in use.
- I. An idle thread on a busy core gives a new vCPU the same speed as a whole free core.
- J. Demand reads higher than Usage once VMs share cores with Hyper-Threading.

## Answers
A, C, F, G, J

## Explanation
- A is correct: Ready and Co-stop per VM are the contention reading; at about 1.5% and below 0.2% there is no CPU performance problem now.
- B is wrong: neither counter shows overload on its own. Usage above 100% is Turbo against the base clock, and Demand runs above Usage once threads share cores; read Core Utilization, Thread Utilization and VM contention.
- C is correct: ESXi Usage is based on Core Utilization, adjusted for frequency: 112 / 80 is about 1.4, so while busy the cores run about 40% above base (All-Core Turbo).
- D is wrong: the cap of older releases is removed in vCenter (since 8.0 Update 3, Broadcom KB 417702) and in VCF Operations (since Aria Operations 8.18).
- E is wrong: vCenter's Demand is the scheduler's estimate of what the VMs would use with no contention, with no reservations in it; it runs above Usage once threads share cores. It is not work the host refused: Ready of about 1.5% shows the VMs got nearly all they asked for.
- F is correct: Usage counts a core with one or two busy threads once, so a second thread on a busy core doubles that core's Thread Utilization and leaves its Usage unchanged.
- G is correct: ESXi Demand is a sum over the VMs, not over physical threads, so it has no value per core or thread.
- H is wrong: Core Utilization counts a core as fully used when one of its two threads runs. For capacity (space) count threads: Thread Utilization.
- I is wrong: a second thread shares the core; Hyper-Threading delivers about 1.25 times per core, not 2 times, so a vCPU on a shared core runs slower than on a free core.
- J is correct: Demand is the scheduler's view of what the VMs would use with no contention; with Hyper-Threading it is higher than Usage.
- Misconception: B: "Demand well above the host's GHz and Usage above 100% mean the host is out of CPU. Stop placing VMs."

## Notes
- Changed in the 2026-11-15 audit: new host figures and window (the old ones were the knowledge base's own example); Demand and Usage given as separate numbers; base clock no longer called capacity; options that repeated facts homed elsewhere replaced in place: C (Usage above 100% is Turbo) by the Usage-over-Core-Utilization arithmetic, F (free cores) by the second-thread Usage fact, G (free threads) by the Demand-per-core fact; old J (keep placing while Ready is low) dropped, old K re-lettered J; key point E corrected to vCenter's Demand (no reservations); misconception type label-read-as-model added.
- Revised 2026-11-12: ESXi 9.1 no longer caps host CPU Usage at 100% (the older example this question came from showed a flat 100%); task moved from troubleshoot to decide-capacity, since the question is whether to keep placing VMs.
- Converted from judged to multiple choice (Q-E2-199 F, 2026-11-14). Knowledge added: host CPU Demand (Demand above Usage once cores are shared; not work the host refuses).

## Metadata
```yaml
id: "0058"
title: "Demand above the base clock, Usage above 100%: is the host full?"
product: [vsphere]
technology: [cpu]
task: decide-capacity
level: 400
answer_type: deterministic
misconception: [B]
input: [text]
object: [esxi, vm]
tool: [vcenter]
knowledge:
  - vsphere/technology/cpu/decision-tree/host-cpu-capacity-headroom
  - vsphere/technology/cpu/metrics/host/utilization
  - vsphere/technology/cpu/metrics/host/core-utilization
  - vsphere/technology/cpu/metrics/host/usage
  - vsphere/technology/cpu/metrics/host/demand
knowledge_main: vsphere/technology/cpu/decision-tree/host-cpu-capacity-headroom
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-05; revised 2026-11-12"
misconception_type: [consumption-as-contention, frequency-and-hyper-threading, label-read-as-model]
pair: "0374"
status: draft
```
