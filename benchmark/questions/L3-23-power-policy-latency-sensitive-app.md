# Host power policy for a latency-sensitive application

## Prompt
- ESXi 9.1 hosts. BIOS power management is set to OS Controlled, with C-states enabled. The ESXi power policy is Balanced.
- A market-data VM handles short bursts of messages. Between bursts, its host is almost idle.
- The application team sees latency spikes of a few hundred microseconds on the first messages after a quiet period, not during busy periods.
- They ask you to set every host in the data center to High Performance.

Should you? What in the Balanced policy can cause this, what does High Performance change, and what does it cost?

## Likely wrong answer
"Balanced always slows VMs down: set High Performance on every host." Or: "A power policy cannot add microseconds; look at the network."

## Expected key points
- Under Balanced, idle cores enter deeper sleep states (C-states) and can run at a lower frequency. A deeper state takes longer to wake, so the first work after a quiet period starts late.
- High Performance turns those power-saving features off: steadier, lower latency for latency-sensitive work.
- Cost: more power and heat. And when some cores are idle, Balanced can let the busy cores reach higher Turbo Boost frequencies than High Performance allows, so some workloads lose peak speed.
- For most workloads Balanced costs little or nothing. Apply High Performance to the hosts that run the latency-sensitive VM (a dedicated cluster or host group), not to every host.
- If that is not enough: deeper measures for that host or VM, such as C-states (including C1E) off in the BIOS, or Latency Sensitivity High on the VM with full reservations.

## Metadata
```yaml
id: "0111"
title: "Host power policy for a latency-sensitive application"
product: [vsphere]
technology: [cpu]
task: judge-setting
level: 300
answer_type: judged
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
source_path: "Drafted by Claude 2026-11-12 for the CPU slots (project/plan.md, M2)"
misconception_type: [frequency-and-hyper-threading]
status: draft
```
