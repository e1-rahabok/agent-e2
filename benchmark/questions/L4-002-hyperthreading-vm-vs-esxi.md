# Hyper-Threading and two vantage points

## Prompt
- Two single-vCPU VMs are both fully busy, running on the two hardware threads of the same physical core.
- Each VM shows CPU Usage around 62.5%.

Which statements are correct?

- A. Both VMs have spare CPU and could be given less CPU, since they use only 62.5% of it.
- B. ESXi CPU Used gives each of the two threads about half of the core.
- C. The core's Usage in MHz is twice its clock speed, because two threads run on it.
- D. With the sibling thread idle, each VM's vCPU would be charged the full core, not 62.5%.
- E. Each VM's CPU Run is about 100%, because Run counts time and ignores the shared core.
- F. Latency Sensitivity High aims to give a vCPU a whole core, its sibling thread left idle.
- G. The two VMs together cannot be charged more CPU than the core's ESXi CPU Used.
- H. Each vCPU is charged 62.5% of a core: its half of a core counted at 1.25 times one thread.
- I. esxtop reports this core at 200%, that is 100% for each of its two busy threads.
- J. The 62.5% is a reporting error: a fully busy single-vCPU VM should show 100% CPU Usage.
- K. Each VM gets as much work done as it would with the whole core to itself.

## Answers
B, D, E, F, H

## Explanation
- A is wrong: the VMs are fully busy (Run about 100%); the 62.5% is the charge for the shared core, not idle capacity.
- B is correct: ESXi CPU Used accounts the core's time: with both threads running each thread (PCPU) is charged half the core, so the pair adds up to 100% of it.
- C is wrong: ESXi CPU Used gives each thread of a busy pair half the core, so the core's Usage (MHz) is its clock speed (times the frequency ratio), not twice it; the 1.25x core gain shows only in the charge to the two VMs.
- D is correct: a vCPU that has the core's execution resources to itself is charged the whole core; from each VM's vantage point an idle sibling is better.
- E is correct: Run is unaware of Hyper-Threading and counts time only; both VMs run all the time.
- F is correct: with Latency Sensitivity High the scheduler tries to give each vCPU exclusive use of a physical core; the partner thread is held idle, so the vCPU is not charged for a shared core.
- G is wrong: the two vCPUs are charged 62.5% each, 125% of the core, while ESXi CPU Used of the core is 100%; VM CPU Used carries the 1.25x and ESXi CPU Used does not.
- H is correct: VM CPU Used and VM CPU Usage count the busy core as 1.25x, so each vCPU is charged 62.5% of one core, a 37.5% penalty. ESXi CPU Used does not carry the 1.25x (B).
- I is wrong: no esxtop field adds the two threads of a core: PCPU UTIL(%) reads 100% on each thread and CORE UTIL(%) 100% for the core. 200% is a group value, such as the %RUN of a 2-vCPU VM.
- J is wrong: not a bug; a different vantage point from the host. The VM cannot see the core or its threads; ESXi can.
- K is wrong: the shared core delivers about 1.25 times one thread's work in total, so each VM does about 62.5% of what it would do alone.
- Misconception: A: "The VMs are under-utilised." - G: "The VMs cannot be charged more than the host used." - J: "62.5% on a busy VM is a reporting bug." - K: "Hyper-Threading costs a VM nothing" (the over-correction).

## Notes
- Tests: Same name, different meaning (consumer vs provider vantage point).
- Converted from judged to multiple choice (Q199 F, 2026-11-14).
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): B one fact; H states the charge without negating G; K (the over-correction) is new. Old K (each thread's Utilization about 100%) removed: it rested on open author question Q220 (Thread Utilization with both threads busy). Q220 settled 2026-11-15: each thread reads 100%; no counter adds the two threads of a core. Key changed from B, D, E, F, H, K to B, D, E, F, H (author approved, 2026-11-14).
- Paired with 0104 (theory and practical, design.md 3.9).
- Q225 settled 2026-11-15: VM CPU Used (62.5% per vCPU with both threads busy) and ESXi CPU Used (half the core per thread) are two rules; the reason for C changed from core Usage carrying the 1.25x to core Usage at the clock speed. Key unchanged.
- 2026-11-15 audit: five options replaced in place with facts of the same truth value, because their facts are tested twice elsewhere (redundancy #21-#23): B (Core Utilization cannot tell one busy thread from two) and D (Core Utilization 100%), home 0004/0012; F (Latency counts the 37.5%), home 0002/0102; G and I (Ready does not register Hyper-Threading), home 0002/0102. New: B ESXi CPU Used splits the core (true), D an idle sibling means a full-core charge (true), F Latency Sensitivity High keeps the sibling idle (true), G the VMs cannot be charged more than ESXi CPU Used (false, hyper-threading Misconceptions), I esxtop shows 200% for the core (false, hyper-threading Misconceptions). H shortened and reworded so it no longer reads as a host counter carrying the 1.25x. Stem: "not 100%" removed. Key letters unchanged.

## Metadata
```yaml
id: "0003"
title: "Hyper-Threading and two vantage points"
product: [vsphere]
technology: [cpu]
input: [text]
task: read-metric
object: [vm, esxi]
tool: [vcenter, esxtop]
knowledge:
  - vsphere/technology/cpu/metrics/virtual-motherboard/usage
  - vsphere/technology/cpu/metrics/host/usage
  - vsphere/technology/cpu/metrics/host/core-utilization
  - vsphere/technology/cpu/concepts/hyper-threading
  - vsphere/technology/cpu/configuration/latency-sensitivity
  - vsphere/tools/esxtop/cpu
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/usage
attachments: []
origin: book
source_path: "The World of Metrics > Metrics Nuances: Naming Complexity; Other Nuances (Formula)."
answer_type: deterministic
misconception: [G, J, A]
level: 400                      # author 2026-11-05
misconception_type: [same-name-other-object, frequency-and-hyper-threading]
pair: "0104"
status: draft                     # reviewed as a free-text question; converted to multiple choice 2026-11-14 (Q199): review again
```
