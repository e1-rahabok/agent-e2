# Linux shows no steal, vCenter shows Ready

## Prompt
- A Linux administrator says: "`top` shows no steal all afternoon, so the hypervisor takes no CPU from this VM. The slowness must be elsewhere."
- The VM runs RHEL 9 (kernel 5.14) with 4 vCPUs, virtual hardware version 21. It was deployed from a template with default VM settings; nobody changed its advanced parameters.
- See [the top screen](0381/linux-top-summary.png) and [the vSphere Client CPU chart](0381/vcenter-vm-cpu-real-time.png) for the same 10 minutes.

Which statements are correct?

- A. `st` 0.0 shows the vCPUs were never held off a physical thread.
- B. The chart's Readiness is the share of each sample a vCPU had work and no thread free.
- C. Readiness on the chart stays below 2%.
- D. vCenter's Readiness must be a collection error, since the guest sees no steal.
- E. With this VM's default settings the steal clock is off, so the guest has no counter for the frozen time.
- F. With `stealclock.enable = "TRUE"` set on this VM, `st` would follow its Ready.
- G. The us and sy figures in `top` include time the vCPUs were frozen.
- H. `top` shows `wa` above 10%, so the guest is waiting on storage.
- I. Add 2 vCPUs to the VM to absorb the wait.

## Input to supply
- Product and version: vSphere 9.1 (vSphere Client); RHEL 9 guest (kernel 5.14), virtual hardware version 21.
- Object: one Linux VM with 4 vCPUs, no CPU limit, and no `stealclock.enable` entry in VM > Edit Settings > Advanced Parameters (check it before the capture). Not Photon OS: Photon tracks steal time by default.
- Screen 1, `top` in the guest during the load, the summary lines visible (the `%Cpu(s)` line with us, sy, id, wa, st). Save as `0381/linux-top-summary.png`.
- Screen 2, vSphere Client > the VM > Monitor > Performance > Advanced > CPU, Chart Options: Real-time, the same 10 minutes, object the VM, counters Readiness (%), Ready (ms), Run (ms), with the legend table. Save as `0381/vcenter-vm-cpu-real-time.png`.
- How to produce it in a lab: run a 4-thread CPU burner in the VM (for example `stress-ng --cpu 4`) on a host where other VMs also run CPU burners, so that the burning vCPUs total about 1.5-2 times the host's physical threads.
- Condition the key depends on: `st` 0.0 on the screen; us + sy at 60% or more; wa below 2; Readiness 14-28% for most of the window; no CPU limit.
- Masking: mask every VM, host, datastore and cluster name; mask the guest's host name in the `top` screen if it shows.

## Likely wrong answer
A: `st` is 0.0, so the hypervisor takes nothing from this VM. Or D: the tools disagree, so vCenter is wrong.

## Expected key points
- Answer: B, E, F, G.
- A false: the misconception. Without the steal clock `st` cannot show the wait at all; the chart's Readiness shows it.
- B true: Readiness is per vCPU: the share of each sample a vCPU had demand and no physical thread.
- C false: reading. Readiness stays at 14-28%.
- D false: the tools count at different layers. The guest kernel is not told about the frozen time; vCenter counts it.
- E true: on vSphere, steal accounting needs the VM's steal clock (`stealclock.enable`); default settings leave it off, so the steal counter stays 0.
- F true: RHEL 9's kernel 5.14 has the VMware steal clock (mainline 5.7 or later) and hardware version 21 is above 13; with the option, `st` follows Ready.
- G true: reading and mechanism. A frozen vCPU stays in the state it was in, so a busy vCPU's frozen time counts as us or sy, which reach 60% or more.
- H false: reading. `wa` stays below 2.
- I false: wrong action. The vCPUs wait for physical threads on a busy host; more vCPUs add demand and tend to raise Ready.

## Reasoning path
1. vCenter: Readiness of 14-28%: the vCPUs wait.
2. `top`: `st` 0.0 with defaults: the guest does not count the wait.
3. The wait is real; enable the steal clock to see it in the guest, and fix the host load or placement.

## Notes
- Paired with the theory question 0380 (theory and practical; design.md, section 3.9).
- Vendor sources for general VMs: Broadcom TechDocs, Tanzu GemFire 10.1, High CPU Steal, section VMware ESXi (steal time needs `stealclock.enable = "TRUE"` except on Photon OS; without it `/proc/stat` steal stays 0), https://techdocs.broadcom.com/us/en/vmware-tanzu/data-solutions/tanzu-gemfire/10-1/gf/managing-checklist-cpu-steal-high.html; Broadcom KB 376609, https://knowledge.broadcom.com/external/article/376609; Broadcom KB 434983 (hardware version 13 or later).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item D12). Counts only after author approval.
- Review 2026-11-15: kernel 5.14 in the stem (F needs it); B without the range; screen readings C and H (false) added; options reworded away from 0380. Key changed from B, D, E, G to B, E, F, G (options relettered).

## Metadata
```yaml
id: "0381"
title: "Linux shows no steal, vCenter shows Ready"
product: [vsphere, linux]
technology: [cpu]
task: troubleshoot
level: 400
answer_type: deterministic
input: [screenshot]
object: [guest-os, vm]
tool: [guest-os-tools, vcenter]
knowledge:
  - vsphere/technology/cpu/concepts/guest-os-vs-vm-cpu
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
  - vsphere/technology/cpu/metrics/virtual-motherboard/latency
knowledge_main: vsphere/technology/cpu/concepts/guest-os-vs-vm-cpu
attachments:
  - 0381/linux-top-summary.png
  - 0381/vcenter-vm-cpu-real-time.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D12"
answer: [B, E, F, G]
misconception: [A, D]
misconception_type: [layer-confusion, tool-confusion]
pair: "0380"
status: awaiting-input
```
