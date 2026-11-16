# Host CPU Wait and thread Idle after a VDI move

## Prompt
- ESXi 9.1 host esx-12: 2 sockets of 20 cores, Hyper-Threading on (80 logical processors).
- It ran 30 server VMs (100 vCPUs). On Monday 40 VDI desktops of 2 vCPUs each, mostly idle, were moved onto it.
- vCenter, host, Real-time, mean per 20-second sample over 10:00-11:00:

| Host counter | Friday | Monday |
|---|---|---|
| Wait (ms) | 1,518,000 | 3,053,000 |
| Ready (ms) | 2,100 | 2,700 |
| Utilization (%) | 30 | 34 |

- Monday 10:20 sample, per-PCPU instances: PCPU 46 Idle 9,990 ms; PCPU 47 Idle 9,985 ms.
- A VCF Operations view of the host shows CPU Utilization for Resources|CPU Active (1 min. average) next to CPU Demand. The team plans an alert on CPU Active.
- The operations lead reads the doubled host Wait as the host waiting on storage since the desktops arrived.

Which statements are correct?

- A. Host Wait sums the Wait of its VMs, so the 80 mostly idle desktop vCPUs explain most of the rise.
- B. The doubled host Wait shows that the host's physical threads now stall on storage IO.
- C. Every VM on the host got slower on Monday, since host Wait about doubled when the desktops came.
- D. PCPU 46 was idle for almost the whole sample: a fully idle thread shows at most 10,000 ms.
- E. PCPU 46 was busy for about half of the sample, since 9,990 ms of Idle is half of 20,000 ms.
- F. With Hyper-Threading off, a fully idle core would also show at most 10,000 ms of Idle per sample.
- G. For a wait that matters on a VM, read that VM's Swap Wait and Other Wait, not the host Wait total.
- H. CPU Active (1 min. average) duplicates CPU Demand, so an alert on it adds no signal of its own.
- I. Move the desktops to another host to bring host Wait down and give the server VMs back their speed.
- J. Host Ready rising from 2,100 to 2,700 ms shows that the desktops brought CPU contention to the host.

## Answers
A, D, G, H

## Explanation
- A is correct: host Wait sums VM Wait, and a mostly idle vCPU spends most of each sample in Wait (Idle). 80 desktop vCPUs at about 19,200 ms each add about 1,536,000 ms, close to the rise of 3,053,000 − 1,518,000 = 1,535,000 ms.
- B is wrong: a physical thread runs or is halted; it does not wait. Host Wait is a sum of the VMs' Wait, mostly idle time, not an IO state of the host.
- C is wrong: host Wait grows with the number of powered-on VMs and their idle vCPUs, with no change in contention; whether VMs wait is read in their Ready and Co-stop.
- D is correct: with Hyper-Threading on, the 20,000 ms of a sample belong to the core and each thread is allotted 10,000 ms of Idle, so 9,990 ms is a nearly fully idle thread (its sibling PCPU 47, at 9,985 ms, is idle too).
- E is wrong: the thread's Idle maximum is 10,000 ms, not 20,000 ms; the misreading halves the idle share.
- F is wrong: without Hyper-Threading there is no thread-level counter and the core-level value goes up to 20,000 ms.
- G is correct: of the VM Wait parts, Swap Wait and Other Wait are the waits that matter; Idle is most of VM Wait on a VM that is not busy, and the host value mixes it in.
- H is correct: CPU Active is a legacy resource-scheduler metric that equals CPU Demand; read Demand and do not chart or alert on the legacy set.
- I is wrong: host Wait is not a performance signal; moving VMs lowers the sum without curing anything, and the readings show no contention.
- J is wrong: host Ready is the sum over 180 vCPUs: 2,700 ms / 180 = 15 ms per vCPU per 20-second sample, about 0.08%.
- Misconception: "Host Wait doubled, so the host is waiting on storage and everything got slower (B, C); and PCPU 46 is half busy, since 9,990 ms is half of 20,000 ms (E)." B, C and E are the misconceptions.

## Metadata
```yaml
id: "0445"
title: "Host CPU Wait and thread Idle after a VDI move"
product: [vsphere, vcf-operations]
technology: [cpu]
task: read-metric
level: 300
answer_type: deterministic
input: [text]
object: [esxi, vm]
tool: [vcenter, vcf-operations]
knowledge:
  - vsphere/technology/cpu/metrics/host/wait
  - vsphere/technology/cpu/metrics/host/idle
  - vsphere/technology/cpu/concepts/hyper-threading
  - vsphere/technology/cpu/metrics/host/cpu-utilization-for-resources
  - vsphere/technology/cpu/metrics/virtual-motherboard/wait
knowledge_main: vsphere/technology/cpu/metrics/host/wait
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-15, question bank audit gap: vsphere/technology/cpu/metrics/host/wait, vsphere/technology/cpu/metrics/host/idle"
misconception: [B, C, E]
misconception_type: [provider-vs-consumer, unit-and-normalization, frequency-and-hyper-threading]
status: draft
```
