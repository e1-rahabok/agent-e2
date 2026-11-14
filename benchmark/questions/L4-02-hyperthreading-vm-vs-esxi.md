# Hyper-Threading and two vantage points

## Prompt
- Two single-vCPU VMs are both fully busy, running on the two hardware threads of the same physical core.
- Each VM shows CPU Usage around 62.5%, not 100%.

Which statements are correct?

- A. Both VMs have spare CPU and could be given less CPU, since they use only 62.5% of it.
- B. ESXi Utilization, read per thread, shows whether one or both threads run; Core Utilization does not.
- C. The core's Usage in MHz is twice its clock speed, because two threads run on it.
- D. ESXi sees the core as fully busy: Core Utilization for that core is 100%.
- E. Each VM's CPU Run is about 100%, because Run counts time and ignores the shared core.
- F. Each VM's CPU Latency shows about 37.5%, the part lost to the shared core.
- G. Each VM gets only 62.5% of the CPU time it asks for and waits in Ready for the rest.
- H. The 62.5% is the charge for sharing a core with a busy sibling thread, not unmet demand.
- I. The CPU Ready of both VMs rises, because the sibling thread on the same core is busy.
- J. The 62.5% is a reporting error: a fully busy single-vCPU VM should show 100% CPU Usage.
- K. Utilization (%) of each of the two threads of that core is about 100%, as each runs all the time.

## Likely wrong answer
- A: "The VMs are under-utilised."
- G: "Each VM only gets 62.5% of what it demands."
- J: "62.5% on a busy VM is a reporting bug."

## Expected key points
- Answer: B, D, E, F, H, K.
- A is false: the VMs are fully busy (Run about 100%); the 62.5% is the charge for the shared core, not idle capacity.
- B is true: Core Utilization is 100% whether 1 or 2 threads run; Utilization (thread level) tells which.
- C is false: ESXi records the core gain as 1.25x, not 2x; Usage (MHz) at core level reflects that Hyper-Threading benefit.
- D is true: ESXi sees the core and its 2 threads; with both threads running the core is fully busy (Usage at core level 100%, Core Utilization 100%).
- E is true: Run is unaware of Hyper-Threading and counts time only; both VMs run all the time.
- F is true: Used + Latency = 100%; with both threads running Used is 62.5% and Latency 37.5%.
- G is false: the 62.5% is an accounting charge for sharing the core, not unmet demand; Ready stays 0.
- H is true: VM Usage is Hyper-Threading aware; when both threads run each VM is charged a 37.5% penalty, so it shows about 62.5%.
- I is false: Ready does not register Hyper-Threading contention; sharing the core happens in hardware, not in the scheduler.
- J is false: not a bug; a different vantage point from the host. The VM cannot see the core or its threads; ESXi can.
- K is true: Thread Utilization counts the time a thread runs, whatever its sibling does; both threads run all the time, so each shows 100% (esxtop adds the two to 200% for the core).

## Notes
- Tests: Same name, different meaning (consumer vs provider vantage point).
- Converted from judged to multiple choice (Q199 F, 2026-11-14). Option K keeps the reviewed key point Thread Utilization = 100%.

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
answer: [B, D, E, F, H, K]
misconception: [G, J, A]
level: 400                      # author 2026-11-05
misconception_type: [same-name-other-object, frequency-and-hyper-threading]
status: draft                     # reviewed as a free-text question; converted to multiple choice 2026-11-14 (Q199): review again
```
