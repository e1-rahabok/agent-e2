# BIOS and power settings on new hosts

## Prompt
- Four new ESXi 9.1 hosts: 2 × Intel Xeon 6, base clock 2.4 GHz, 1 TB of memory each.
- The server team applied the BIOS factory defaults, then set Node Interleaving to Enabled "so every VM sees the same memory latency" and power management to OS Controlled.
- The performance team wants repeatable benchmark results. They set the ESXi power policy to Custom with Use P States = 0 (Use C States left at 1), expecting the cores to stay at 2.4 GHz.
- During the benchmark, esxtop:
  - power panel: busy cores at 3.3-3.5 GHz;
  - memory panel: one NUMA node on each two-socket host.

Which statements are correct?

- A. With Use P States = 0, busy cores run at the highest frequency available, Turbo included.
- B. Cores above 2.4 GHz show that the policy change did not take effect, so the hosts need a reboot.
- C. Setting Use C States = 0 as well would keep the busy cores at the 2.4 GHz base clock.
- D. To keep the cores at or below base clock from ESXi, set Power.MaxFreqPct below 100.
- E. Use P States = 0 also keeps the idle cores out of deep C-states, so they wake faster.
- F. One NUMA node per two-socket host shows that interleaving hides the NUMA layout from ESXi.
- G. Performance Best Practices advises node interleaving on most hosts, because it evens out memory latency.
- H. The BIOS factory defaults suit an ESXi host, so the rest of the BIOS needs no review.
- I. With EPT turned off in the BIOS, ESXi 9.1 would fall back to software MMU virtualization.

## Likely wrong answer
"Use C States = 0 would pin the clock at base (C); interleaving gives every VM even memory latency, which is good (G); and the factory defaults are fine (H)." C, G and H are the misconceptions.

## Expected key points
- Answer: A, D, F.
- A is correct: Use P States disabled makes ESXi use the highest available frequency, Turbo included; Turbo stays on while the BIOS enables it.
- B is wrong: the readings are what the setting does; a reboot changes nothing.
- C is wrong: Use C States controls deep C-states on idle cores; disabling it does not disable Turbo, and firmware thermal management still sets each core's frequency.
- D is correct: on Intel processors, Power.MaxFreqPct below 100% keeps the cores at or below base clock, which turns Turbo off; the other way is to turn Turbo off in the BIOS.
- E is wrong: deep C-states are the job of Use C States, still 1 here; with Use C States 1 and Use P States 0, idle cores sleep and busy cores run at the highest frequency.
- F is correct: node interleaving deactivates NUMA as ESXi sees it, so its NUMA scheduler cannot keep a VM's memory on the VM's node; Performance Best Practices says the best performance in most cases comes from leaving NUMA active.
- G is wrong: Performance Best Practices for vSphere 9.1 says to deactivate node interleaving in most cases.
- H is wrong: Performance Best Practices for vSphere 9.1 says default BIOS settings might not be the best for performance and lists the settings to check on a new server.
- I is wrong: ESXi 6.7 and later support neither software CPU nor software MMU virtualization; VT-x and EPT must be on in the BIOS.

## Metadata
```yaml
id: "0448"
title: "BIOS and power settings on new hosts"
product: [vsphere]
technology: [cpu, memory]
task: judge-setting
level: 300
answer_type: deterministic
input: [text]
object: [esxi]
tool: [esxtop]
knowledge:
  - vsphere/object-types/esxi/configuration/bios-settings
  - vsphere/technology/cpu/concepts/power-states
  - vsphere/technology/cpu/concepts/cpu-frequency
  - vsphere/technology/cpu/concepts/hardware-assisted-virtualization
knowledge_main: vsphere/object-types/esxi/configuration/bios-settings
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-15, question bank audit gap: vsphere/object-types/esxi/configuration/bios-settings, vsphere/technology/cpu/concepts/hardware-assisted-virtualization"
answer: [A, D, F]
misconception: [C, G, H]
misconception_type: [frequency-and-hyper-threading]
status: draft
```
