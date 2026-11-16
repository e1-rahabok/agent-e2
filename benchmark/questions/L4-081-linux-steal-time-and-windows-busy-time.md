# Linux steal time and Windows busy time on a busy host

## Prompt
- Two VMs with 4 vCPUs run on the same VMware ESXi host. Host CPU Utilization is about 92%.
- vCenter, last hour, both VMs: CPU Ready about 10% per vCPU, Co-stop near 0.
- Linux VM, `top` summary line: `%Cpu(s): 58.0 us, 4.0 sy, 0.0 wa, 28.0 id, 10.0 st`.
- Windows VM, Performance Monitor: Processor(_Total) \ % Processor Time about 75%, while its VM CPU Run in vCenter is about 65%.

Which statements are correct?

- A. The Linux `us` and `sy` count the time the vCPUs ran, not the speed they ran at.
- B. Windows counts the frozen time in the state the vCPU was in, so its busy figure exceeds Run.
- C. Windows' % Processor Time maps one to one onto a single vCenter CPU counter of the VM.
- D. The 10% steal is Linux's own CPU time spent on work for the hypervisor.
- E. Adding vCPUs to the Linux VM spreads the work and removes its steal time.
- F. Steal time also covers the slowdown from Hyper-Threading and a lower clock speed.

## Likely wrong answer
D or F: steal read as work done, or as every hypervisor effect. Or E: more vCPUs as the cure for host contention. C looks for one VM counter that equals the Windows figure.

## Expected key points
- Answer: A, B.
- A is correct: Linux `top` usage figures count time spent, not the speed of the run. The guest does not see Hyper-Threading, and in many versions not the clock either, so `us` and `sy` count a second on a shared or slower core the same as a second alone at full clock.
- B is correct: Windows does not account frozen time; it stays in whatever state the vCPU was in, so Windows reads above vSphere: 75% is about Run 65% plus Ready 10%.
- C is wrong: two kernels count independently, and none of vCenter's VM CPU utilization metrics maps directly onto Windows or Linux utilization; here the Windows figure sits near Run plus Ready, two counters.
- D is wrong: steal is time the vCPU did not run at all, frozen because no physical thread was free. `st` 10% matches Ready 10% per vCPU because this VM's steal clock works.
- E is wrong: the wait is for physical CPUs on a busy host; more vCPUs add demand, and usually more Ready.
- F is wrong: steal counts frozen time only. The guest does not see Hyper-Threading or the clock speed; those effects show in VM counters such as Usage and Latency, not in steal.

## Notes
- Overlap (not in Linux steal time: latency, Contrast with Linux Steal Time) is tested in 0380 F, not here.
- "`st` follows Ready with the steal clock" is tested by 0380 and 0381; this question no longer tests it (cap of two questions per fact).
- Changed 2026-11-16 (re-review, minimal change): C (the gap as hidden guest work) was the rival explanation of B's gap; C now tests the one-to-one mapping misconception (guest-os-vs-vm-cpu, Layers and Misconceptions), still false.
- Changed in the 2026-11-15 audit: A replaced (was "`st` mirrors Ready", over the cap of two) by the time-only fact of Linux `us` and `sy`; throwaway C replaced by the Windows-gap misconception; B and E reworded for length and hedge cues; the stem gives host Utilization instead of "busy" and no longer states the steal clock setting; needs the author's review.

## Metadata
```yaml
id: "0266"
title: "Linux steal time and Windows busy time on a busy host"
product: [linux, windows, vsphere]
technology: [cpu]
task: explain-mechanism
level: 400
answer_type: deterministic
input: [text]
object: [guest-os, vm, esxi]
tool: [guest-os-tools, vcenter]
knowledge:
  - vsphere/technology/cpu/concepts/guest-os-vs-vm-cpu
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
  - vsphere/technology/cpu/metrics/virtual-motherboard/latency
knowledge_main: vsphere/technology/cpu/concepts/guest-os-vs-vm-cpu
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-12"
answer: [A, B]
misconception: [D, E, F]
misconception_type: [layer-confusion, frequency-and-hyper-threading]
pair: "0368"
status: draft
```
