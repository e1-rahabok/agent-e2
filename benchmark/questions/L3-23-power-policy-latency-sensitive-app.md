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
- D. For latency-sensitive work, High Performance gives the full hardware performance that Balanced can slightly reduce.
- E. When some cores are idle, Balanced can let the busy cores reach higher Turbo Boost frequencies than High Performance allows.
- F. High Performance gives up the power savings of Balanced, so the hosts draw more power.
- G. Under High Performance, an idle core goes no deeper than C1.
- H. Apply High Performance to the hosts that run the latency-sensitive VM, such as a dedicated cluster or host group.
- I. If High Performance is not enough, turning off C-states, C1E included, in the BIOS of those hosts can help.
- J. Turning off deep C-states in the ESXi advanced settings also turns off Turbo Boost on those hosts.
- K. Turning off all C-states in the BIOS is the vendor's advice for every host, for the best performance per watt.

## Likely wrong answer
- A: "Balanced slows everything down: set High Performance everywhere."
- B: "A power setting can't add microseconds; look at the network."

## Expected key points
- Answer: C, D, E, F, G, H, I.
- A is false: Balanced typically costs little or nothing, and on hosts with idle cores it can raise performance through Turbo Boost.
- B is false: a deeper C-state takes longer to start running again, which matches spikes on the first messages after a quiet period.
- C is true: Balanced lets ESXi use deep C-states (C2 or deeper) when cores are idle.
- D is true: the Balanced policy can slightly reduce performance of latency-sensitive workloads; High Performance uses no power-saving features.
- E is true: idle cores leave thermal room, so busy cores boost higher (about 151% of nominal under Balanced against about 130% under High Performance in the whitepaper chart).
- F is true: High Performance has no power-saving features; reducing power is what Balanced is for.
- G is true: policies that do not use deep C-states stop at C1, so an idle core returns to work almost at once.
- H is true: use High Performance only where sub-second latency matters; elsewhere it costs power and can lose Turbo headroom.
- I is true: C-states including C1E can reduce the performance of a few workloads highly sensitive to latency; deactivating them in the BIOS can help those.
- J is false: Turbo is a BIOS setting (or Power.MaxFreqPct below 100% on Intel); turning off deep C-states lowers the Turbo headroom of lightly threaded work but does not turn Turbo off.
- K is false: for the best performance per watt the advice is to activate all C-states in the BIOS and leave the choice to ESXi.

## Notes
- Converted from judged to multiple choice (Q199 F, 2026-11-14).
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): D one fact; old G (Balanced costs most workloads little) negated A and is now the C1 fact; J decidable after the power-states fix (Performance Best Practices for vSphere 9.1, p. 22; vSphere 9.1 Custom policy parameters); old L and M (Latency Sensitivity High) removed because they repeat 0112. Key changed from C, D, E, F, G, H, I, M to C, D, E, F, G, H, I.

## Metadata
```yaml
id: "0111"
title: "Host power policy for a latency-sensitive application"
product: [vsphere]
technology: [cpu]
task: judge-setting
level: 300
answer_type: deterministic
answer: [C, D, E, F, G, H, I]
misconception: [A, B]
input: [text]
object: [esxi]
tool: [none]
knowledge:
  - vsphere/technology/cpu/configuration/host-power-management
  - vsphere/technology/cpu/concepts/power-states
knowledge_main: vsphere/technology/cpu/configuration/host-power-management
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
misconception_type: [frequency-and-hyper-threading]
status: draft
```
