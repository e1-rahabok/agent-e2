# Overcommit ratio: per thread or per core

## Prompt
- ESXi host: 2 sockets of 32 cores, Hyper-Threading on: 64 cores, 128 hardware threads.
- It runs 384 vCPUs of powered-on VMs.
- The capacity standard says "CPU overcommit at most 3:1". It does not say per core or per thread.
- One engineer reports the host at 3:1, another at 6:1.

Which statements are correct?

- A. 384 vCPUs on 128 threads is 3:1 and on 64 cores 6:1, so the standard needs its unit to mean anything.
- B. ESXi schedules each vCPU on a hardware thread, so up to 128 vCPUs can run at the same instant on this host, not 64.
- C. The two threads of a core give about the throughput of two cores, so 3:1 per thread and 3:1 per core mean the same capacity.
- D. When all 384 vCPUs are busy at once, each gets on average about a third of a thread, and a thread whose sibling is busy delivers less than a full core.
- E. At 6:1 per core mostly idle VMs can show low Ready, while busy VMs at 2:1 per thread can show high Ready.
- F. Ready can be estimated from the overcommit ratio: at 3:1 per thread a VM's vCPUs wait about two thirds of the time.

## Answers
A, B, D, E

## Explanation
- A is correct: 384 ÷ 128 = 3 and 384 ÷ 64 = 6; with Hyper-Threading a ratio per core is twice the ratio per thread, so a ratio needs its unit.
- B is correct: ESXi schedules a vCPU on a logical processor (a hardware thread), so 128 vCPUs can run at the same instant.
- C is wrong: two threads share one core's execution units and give a slight to significant gain, not two cores; ESXi charges the pair 1.25x one core in VM CPU Used.
- D is correct: 384 vCPUs on 128 threads is 3 per thread; with every vCPU busy each gets on average about a third of a thread's time, and a vCPU whose sibling thread is busy is charged 62.5% of the core, less than a full core.
- E is correct: the ratio is allocation; Ready depends on how many vCPUs want to run at the same time, not on how many are configured.
- F is wrong: Ready follows concurrent demand, not the configured ratio; idle vCPUs at any ratio wait for nothing.
- Misconception: C: treating a hardware thread as a full core. Or F: reading the ratio as contention.

## Notes
- Synthetic, 2026-11-12.
- Level 300 after the 2026-11-15 audit: the ratio's unit, Hyper-Threading not doubling and ratio vs contention are common rules applied to one host. The proposed Hyper-Threading Ready and 62.5% GHz options were not added: other questions already test those facts twice.
- Hyper-Threading: ESXi charges the vCPUs on a core with both threads busy 1.25 times one thread alone (each vCPU 62.5%; ESXi CPU Used still gives each thread half the core, Q-E2-225); the real gain per application varies (knowledge base, hyper-threading).

## Metadata
```yaml
id: "0234"
title: "Overcommit ratio: per thread or per core"
product: [vsphere]
technology: [system, cpu]
task: decide-capacity
level: 300
answer_type: deterministic
input: [text]
object: [esxi]
tool: [none]
knowledge:
  - sp5-framework/capacity/overcommit
  - vsphere/technology/cpu/concepts/hyper-threading
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
knowledge_main: sp5-framework/capacity/overcommit
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-12"
misconception: [C, F]
misconception_type: [frequency-and-hyper-threading, consumption-as-contention]
status: draft
```
