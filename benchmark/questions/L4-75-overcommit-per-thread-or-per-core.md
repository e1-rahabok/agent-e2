# Overcommit ratio: per thread or per core

## Prompt
- ESXi host: 2 sockets of 32 cores, Hyper-Threading on: 64 cores, 128 hardware threads.
- It runs 384 vCPUs of powered-on VMs.
- The capacity standard says "CPU overcommit at most 3:1". It does not say per core or per thread.
- One engineer reports the host at 3:1, another at 6:1.

Which statements are correct?

- A. Both numbers describe the same host: 384 vCPUs on 128 threads is 3:1; on 64 cores it is 6:1. The standard is ambiguous by a factor of 2.
- B. ESXi schedules each vCPU on a hardware thread, so up to 128 vCPUs can run at the same instant on this host, not 64.
- C. The two threads of a core give about the throughput of two cores, so 3:1 per thread and 3:1 per core mean the same capacity.
- D. When all 384 vCPUs are busy at once, each gets on average about a third of a thread, and a thread whose sibling is busy delivers less than a full core.
- E. The ratio alone does not show contention: at 6:1 per core with mostly idle VMs Ready can stay low, while 2:1 per thread with busy VMs can show high Ready.
- F. Ready rises in proportion to the overcommit ratio, so the ratio is a direct measure of how long the VMs wait.

## Likely wrong answer
C: treating a hardware thread as a full core. Or F: reading the ratio as contention.

## Expected key points
- Answer: A, B, D, E.
- A: the arithmetic: 384 ÷ 128 = 3, 384 ÷ 64 = 6. A ratio needs its unit.
- B: a vCPU runs on a logical processor (a hardware thread).
- C is wrong: two threads share one core's execution units; together they give much less than two cores (ESXi accounts about 1.25 times one core).
- D: 384 vCPUs on 128 threads is 3 per thread; with every vCPU busy, each gets on average about a third of a thread's time, and less than a core's worth when the sibling thread is busy.
- E: the ratio is allocation; contention depends on how many vCPUs are busy at the same time.
- F is wrong: Ready follows concurrent demand, not the configured ratio.

## Notes
- Drafted 2026-11-12 for the System slots (question set 1.0, plan M2).
- Hyper-Threading: ESXi accounts a core with both threads busy as 1.25 times one thread alone (each thread 62.5%); the real gain per application varies (knowledge base, hyper-threading).

## Metadata
```yaml
id: "0234"
title: "Overcommit ratio: per thread or per core"
product: [vsphere]
technology: [system, cpu]
task: decide-capacity
level: 400
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
source_path: "Drafted by Claude 2026-11-12 for the System slots (question set 1.0)"
answer: [A, B, D, E]
misconception: [C, F]
misconception_type: [frequency-and-hyper-threading, consumption-as-contention]
status: draft
```
