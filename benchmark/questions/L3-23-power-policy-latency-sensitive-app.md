# Host power policy for a latency-sensitive application

## Prompt
- ESXi 9.1 hosts. BIOS power management is set to OS Controlled, with C-states enabled. The ESXi power policy is Balanced.
- A market-data VM handles short bursts of messages. Between bursts, its host is almost idle.
- The application team sees latency spikes of a few hundred microseconds on the first messages after a quiet period, not during busy periods.
- They ask you to set every host in the data center to High Performance.

Which statements are correct?

- A. Balanced always slows VMs down, so High Performance belongs on every host in the data center, not only these.
- B. A host power policy cannot add microseconds of latency, so the cause must be in the network.
- C. Under Balanced, idle cores can drop into deeper C-states that take longer to wake, delaying the first work after a lull.
- D. High Performance turns off the power-saving features, giving steadier, lower latency to latency-sensitive work.
- E. When some cores are idle, Balanced can let the busy cores reach higher Turbo Boost frequencies than High Performance allows.
- F. High Performance gives up the power savings of Balanced, so the hosts draw more power.
- G. For most workloads, the Balanced policy costs little or no performance.
- H. Apply High Performance to the hosts that run the latency-sensitive VM, such as a dedicated cluster or host group.
- I. If High Performance is not enough, turning off C-states, C1E included, in the BIOS of those hosts can help.
- J. Turning off deep C-states in the ESXi settings also turns off Turbo Boost on those hosts.
- K. Turning off all C-states in the BIOS is the vendor's advice for every host, for the best performance per watt.
- L. Latency Sensitivity High on the VM is free: the physical cores it uses stay available to other VMs.
- M. Latency Sensitivity High on the market-data VM, with full reservations, can further cut its network latency and jitter.

## Likely wrong answer
- A: "Balanced slows everything down: set High Performance everywhere."
- B: "A power setting can't add microseconds; look at the network."

## Expected key points
- Answer: C, D, E, F, G, H, I, M.
- A is false: Balanced typically costs little or nothing, and on hosts with idle cores it can raise performance through Turbo Boost.
- B is false: a deeper C-state takes longer to start running again, which matches spikes on the first messages after a quiet period.
- C is true: Balanced lets ESXi use deep C-states (C2 or deeper) when cores are idle; High Performance stops at C1.
- D is true: High Performance uses no power-saving features; the Balanced policy can slightly reduce performance of latency-sensitive workloads.
- E is true: idle cores leave thermal room, so busy cores boost higher (about 151% of nominal under Balanced against about 130% under High Performance in the whitepaper chart).
- F is true: High Performance has no power-saving features; reducing power is what Balanced is for.
- G is true: Balanced typically gives little or no performance reduction.
- H is true: use High Performance only where sub-second latency matters; elsewhere it costs power and can lose Turbo headroom.
- I is true: C-states including C1E can reduce the performance of a few workloads highly sensitive to latency; deactivating them in the BIOS can help those.
- J is false: firmware thermal management still sets each core's frequency; turning off deep C-states does not turn off Turbo.
- K is false: for the best performance per watt the advice is to activate all C-states in the BIOS and leave the choice to ESXi.
- L is false: Latency Sensitivity High removes the assigned physical cores from the pool for other VMs and VMkernel worlds, and it needs full reservations.
- M is true: with Latency Sensitivity High the scheduler tries to give each vCPU a physical core of its own, and network latency and jitter drop greatly; it needs a full memory reservation and, from virtual hardware 14, a full CPU reservation.

## Notes
- Converted from judged to multiple choice (Q199 F, 2026-11-14).
- Review 2026-11-14: option M added, so the old key point "Latency Sensitivity High on the VM with full reservations" as a further measure survives as a true option; L tests its cost.

## Metadata
```yaml
id: "0111"
title: "Host power policy for a latency-sensitive application"
product: [vsphere]
technology: [cpu]
task: judge-setting
level: 300
answer_type: deterministic
answer: [C, D, E, F, G, H, I, M]
misconception: [A, B]
input: [text]
object: [esxi]
tool: [none]
knowledge:
  - vsphere/technology/cpu/configuration/host-power-management
  - vsphere/technology/cpu/concepts/power-states
  - vsphere/technology/cpu/configuration/latency-sensitivity
knowledge_main: vsphere/technology/cpu/configuration/host-power-management
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
misconception_type: [frequency-and-hyper-threading]
status: draft
```
