# Demand above capacity, Usage above 100%: is the host full?

## Prompt
- An ESXi 9.1 host has 40 cores at a 2.0 GHz base clock (80,000 MHz of capacity) and 80 threads (Hyper-Threading on).
- Over 7 hours, in the vSphere Client:
  - CPU Demand: about 104,000 MHz against 80,000 MHz of capacity. CPU Usage: about 104%.
  - Core Utilization: 85%. Utilization (per thread): 62%.
  - Per VM: Ready about 2%, Co-stop below 0.1%.
- The operations manager wants to stop placing VMs on this host because it is overloaded.

Which statements about this host are correct?

- A. Ready about 2% and Co-stop below 0.1% per VM show the VMs get the run time they ask for now.
- B. Demand at 130% of capacity and Usage above 100% mean the host is out of CPU, so stop placing VMs.
- C. Usage above 100% is Turbo Boost: Usage is measured against the 2.0 GHz base clock.
- D. ESXi 9.1 caps Usage at 100%, so a reading of 104% points to a counter error.
- E. Demand of 104,000 MHz means the VMs were refused about 24,000 MHz of the CPU they asked for.
- F. Core Utilization of 85% means about 6 of the 40 cores run no thread at all.
- G. Thread Utilization of 62% leaves about 30 of the 80 threads idle.
- H. Core Utilization of 85% means that 85% of the host's capacity is in use.
- I. An idle thread on a busy core gives a new vCPU the same speed as a whole free core.
- J. Keep placing VMs while per-VM Ready and Co-stop stay low, watching Thread Utilization against its ceiling.
- K. Demand reads higher than Usage once VMs share cores with Hyper-Threading.

## Likely wrong answer
- B: "Demand at 130% of capacity and Usage above 100% mean the host is out of CPU. Stop placing VMs."

## Expected key points
- Answer: A, C, F, G, J, K.
- A true: no CPU performance problem now; the VMs get their run time.
- B false: neither counter shows overload on its own. Read Core Utilization, Thread Utilization and VM contention.
- C true: Usage is not capped in vSphere 9.1; above 100% means cores run above base frequency (Broadcom KB 417702).
- D false: the cap of older releases is removed in vCenter (since 8.0 Update 3) and in VCF Operations (since Aria Operations 8.18).
- E false: Demand sums VM demand and reservations and runs higher than Usage once cores are shared; it is not work the host refuses. Ready of about 2% shows the VMs got nearly all they asked for.
- F true: 15% of 40 cores is about 6 cores with no thread running.
- G true: 38% of 80 threads is about 30 threads free.
- H false: Core Utilization counts a core as fully used when one of its two threads runs. For capacity (space) count threads: Thread Utilization.
- I false: a second thread shares the core; Hyper-Threading delivers about 1.25 times per core, not 2 times, so a vCPU on a shared core runs slower than on a free core.
- J true: decide by contention as VMs are added. The planned ceiling for Thread Utilization is set per host, and lower at cluster level because of the HA host.
- K true: Demand is the scheduler's view of what the VMs would use with no contention; with Hyper-Threading it is higher than Usage.

## Notes
- Revised 2026-11-12: ESXi 9.1 no longer caps host CPU Usage at 100% (the book's example was an older release with a flat 100%); task moved from troubleshoot to decide-capacity, since the question is whether to keep placing VMs.
- Converted from judged to multiple choice (Q199 F, 2026-11-14). Knowledge added: host CPU Demand (Demand above Usage once cores are shared; not work the host refuses).

## Metadata
```yaml
id: "0058"
title: "Demand above capacity, Usage above 100%: is the host full?"
product: [vsphere]
technology: [cpu]
task: decide-capacity
level: 400
answer_type: deterministic
answer: [A,C,F,G,J,K]
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
source_path: "Drafted by Claude 2026-11-05; revised 2026-11-12"
misconception_type: [consumption-as-contention, frequency-and-hyper-threading]
status: draft
```
