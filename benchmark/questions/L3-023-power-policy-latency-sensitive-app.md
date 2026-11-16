# Host power policy for a latency-sensitive application

## Prompt
- ESXi 9.1 hosts. BIOS power management is set to OS Controlled, with C-states enabled. The ESXi power policy is Balanced.
- A market-data VM handles short bursts of messages. Between bursts, its host is almost idle.
- The application team sees latency spikes of a few hundred microseconds on the first messages after a quiet period, not during busy periods.
- They ask you to set every host in the data center to High Performance.

Which statements are correct?

- A. Balanced costs VMs performance, so High Performance belongs on every host in the data center.
- B. A host power policy changes only the power draw of the cores, not how fast an idle core starts work.
- C. Under Balanced, idle cores drop into deep C-states, which take longer to wake after a lull.
- D. For latency-sensitive work, High Performance gives the full hardware performance that Balanced can slightly reduce.
- E. With some cores idle, busy cores under Balanced reach higher Turbo Boost frequencies than under High Performance.
- F. High Performance gives up the power savings of Balanced, so the hosts draw more power.
- G. Under High Performance, ESXi does not put idle cores into deep C-states (C2 or deeper).
- H. Apply High Performance only to the hosts that run the latency-sensitive VM, such as a dedicated host group.
- I. Turning off C-states, C1E included, in the BIOS of those hosts helps a few highly latency-sensitive workloads.
- J. Turning off deep C-states in the ESXi advanced settings also turns off Turbo Boost on those hosts.
- K. Vendor guidance is to turn off all C-states in the BIOS of every host for the best performance per watt.
- L. Setting Use P States to 0 in the ESXi advanced settings keeps the cores at their base clock under load.

## Likely wrong answer
- A: "Balanced slows everything down: set High Performance everywhere."
- B: "A power setting can't add microseconds; look at the network."
- L: "Turn P-states off to hold the clock steady at base."

## Expected key points
- Answer: C, D, E, F, G, H, I.
- A is false: Balanced typically costs little or nothing, and on hosts with idle cores it can raise performance through Turbo Boost.
- B is false: a deeper C-state saves more power and takes longer to start running again, which matches spikes on the first messages after a quiet period.
- C is true: Balanced lets ESXi use deep C-states (C2 or deeper) when cores are idle, and a deeper C-state takes longer to start running again.
- D is true: the Balanced policy can slightly reduce performance of latency-sensitive workloads; High Performance uses no power-saving features.
- E is true: idle cores leave thermal room, so busy cores boost higher (about 151% of nominal under Balanced against about 130% under High Performance in the whitepaper chart).
- F is true: High Performance has no power-saving features; reducing power is what Balanced is for.
- G is true: High Performance uses no power-saving features, so ESXi stops at C1; the hardware can still deepen C1 to C1E while C1E is on in the BIOS (hence option I).
- H is true: use High Performance only where sub-second latency matters; elsewhere it costs power and can lose Turbo headroom.
- I is true: C-states including C1E can reduce the performance of a few workloads highly sensitive to latency, such as some financial platforms; deactivating them in the BIOS helps those.
- J is false: Turbo is a BIOS setting (or Power.MaxFreqPct below 100% on Intel); turning off deep C-states lowers the Turbo headroom of lightly threaded work but does not turn Turbo off.
- K is false: for the best performance per watt the advice is to activate all C-states in the BIOS and leave the choice to ESXi.
- L is false: with Use P States off, ESXi runs the cores at the highest available frequency, Turbo included. Only Power.MaxFreqPct below 100% (Intel) or the BIOS takes Turbo away.

## Notes
- Changed in the 2026-11-15 audit: hedges removed from correct options C, E, I and absolutes from wrong options A, B, K (every correct effect carried a hedge, every wrong one an absolute); L added (Use P States off read as base clock); level 300 to 400 (E, J and L need the C-state and Turbo mechanism that the rule "High Performance is fastest" gets wrong).
- Converted from judged to multiple choice (Q199 F, 2026-11-14).
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): D one fact; old G (Balanced costs most workloads little) negated A and is now the deep C-state fact (worded so that C1E, which the hardware controls, stays possible); J decidable after the power-states fix (Performance Best Practices for vSphere 9.1, p. 22; vSphere 9.1 Custom policy parameters); old L and M (Latency Sensitivity High) removed because they repeat 0112. Key changed from C, D, E, F, G, H, I, M to C, D, E, F, G, H, I.

## Metadata
```yaml
id: "0111"
title: "Host power policy for a latency-sensitive application"
product: [vsphere]
technology: [cpu]
task: judge-setting
level: 400
answer_type: deterministic
answer: [C, D, E, F, G, H, I]
misconception: [A, B, L]
input: [text]
object: [esxi]
tool: [none]
knowledge:
  - vsphere/technology/cpu/configuration/host-power-management
  - vsphere/technology/cpu/concepts/power-states
knowledge_main: vsphere/technology/cpu/configuration/host-power-management
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-12"
misconception_type: [frequency-and-hyper-threading]
status: draft
```
