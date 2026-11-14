# Hyper-Threading and two vantage points

## Prompt
- Two single-vCPU VMs are both fully busy, running on the two hardware threads of the same physical core.
- Each VM shows CPU Usage around 62.5%, not 100%.

Which statements are correct?

- A. Both VMs have spare CPU and could be given less CPU, since they use only 62.5% of it.
- B. Core Utilization alone cannot tell whether one or both threads of a core run.
- C. The core's Usage in MHz is twice its clock speed, because two threads run on it.
- D. ESXi sees the core as fully busy: Core Utilization for that core is 100%.
- E. Each VM's CPU Run is about 100%, because Run counts time and ignores the shared core.
- F. Each VM's CPU Latency shows about 37.5%, the part lost to the shared core.
- G. Each VM gets only 62.5% of the CPU time it asks for and waits in Ready for the rest.
- H. ESXi records a core with both threads busy as 1.25 times one thread's work and charges each thread half of it.
- I. The CPU Ready of both VMs rises, because the sibling thread on the same core is busy.
- J. The 62.5% is a reporting error: a fully busy single-vCPU VM should show 100% CPU Usage.
- K. Each VM gets as much work done as it would with the core to itself.

## Likely wrong answer
- A: "The VMs are under-utilised."
- G: "Each VM only gets 62.5% of what it demands."
- J: "62.5% on a busy VM is a reporting bug."
- K: "Hyper-Threading costs a VM nothing" (the over-correction).

## Expected key points
- Answer: B, D, E, F, H.
- A is false: the VMs are fully busy (Run about 100%); the 62.5% is the charge for the shared core, not idle capacity.
- B is true: Core Utilization is 100% whether one or both threads run; only the thread-level Utilization tells which.
- C is false: ESXi records the core gain as 1.25x, not 2x; Usage (MHz) at core level reflects that Hyper-Threading benefit.
- D is true: ESXi sees the core and its 2 threads; with both threads running the core is fully busy (Usage at core level 100%, Core Utilization 100%).
- E is true: Run is unaware of Hyper-Threading and counts time only; both VMs run all the time.
- F is true: Used + Latency = 100%; with both threads running Used is 62.5% and Latency 37.5%.
- G is false: the 62.5% is an accounting charge for sharing the core, not unmet demand; Ready stays 0.
- H is true: VM Usage is Hyper-Threading aware: the core counts 1.25x, so each thread is charged 62.5% of one core, a 37.5% penalty.
- I is false: Ready does not register Hyper-Threading contention; sharing the core happens in hardware, not in the scheduler.
- J is false: not a bug; a different vantage point from the host. The VM cannot see the core or its threads; ESXi can.
- K is false: the shared core delivers about 1.25 times one thread's work in total, so each VM does about 62.5% of what it would do alone.

## Notes
- Tests: Same name, different meaning (consumer vs provider vantage point).
- Converted from judged to multiple choice (Q199 F, 2026-11-14).
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): B one fact; H states the charge without negating G; K (the over-correction) is new. Old K (each thread's Utilization about 100%) removed: it rests on open author question Q220 (Thread Utilization with both threads busy). Key changed from B, D, E, F, H, K to B, D, E, F, H (author approved, 2026-11-14).
- Paired with 0104 (theory and practical, design.md 3.9).

## Metadata
```yaml
id: "0003"
title: "Hyper-Threading and two vantage points"
product: [vsphere]
technology: [cpu]
input: [text]
task: read-metric
object: [vm, esxi]
tool: [vcenter]
knowledge:
  - vsphere/technology/cpu/metrics/virtual-motherboard/usage
  - vsphere/technology/cpu/metrics/host/usage
  - vsphere/technology/cpu/metrics/host/core-utilization
  - vsphere/technology/cpu/concepts/hyper-threading
  - vsphere/technology/cpu/metrics/virtual-motherboard/latency
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/usage
attachments: []
origin: book
source_path: "The World of Metrics > Metrics Nuances: Naming Complexity; Other Nuances (Formula)."
answer_type: deterministic
answer: [B, D, E, F, H]
misconception: [G, J, A]
level: 400                      # author 2026-11-05
misconception_type: [same-name-other-object, frequency-and-hyper-threading]
pair: "0104"
status: draft                     # reviewed as a free-text question; converted to multiple choice 2026-11-14 (Q199): review again
```
