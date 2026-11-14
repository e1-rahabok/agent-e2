# Linux steal time and Windows busy time on a busy host

## Prompt
- Two VMs with 4 vCPUs run on the same VMware ESXi host. The host is busy.
- vCenter, last hour, both VMs: CPU Ready about 10% per vCPU, Co-stop near 0.
- Linux VM (steal clock enabled in the VM's advanced settings), `top` summary line: `%Cpu(s): 58.0 us, 4.0 sy, 0.0 wa, 28.0 id, 10.0 st`.
- Windows VM, Performance Monitor: Processor(_Total) \ % Processor Time about 75%, while its VM CPU Run in vCenter is about 65%.

Which statements are correct?

- A. Linux accounts the time its vCPUs were ready but not run as steal time, so `st` mirrors Ready.
- B. Windows has no steal time: frozen time is not accounted, so Windows can show a higher busy figure than vSphere.
- C. Steal time also appears on physical servers, when the CPU waits for memory.
- D. The 10% steal is Linux's own CPU time spent on work for the hypervisor.
- E. Adding vCPUs to the Linux VM removes its steal time.
- F. Steal time also covers the slowdown from Hyper-Threading and a lower clock speed.

## Likely wrong answer
D or F: steal read as work done, or as every hypervisor effect. Or E: more vCPUs as the cure for host contention.

## Expected key points
- Answer: A, B.
- A is correct: a vCPU waiting for a physical CPU is frozen time for the guest. Linux accounts it as steal time, so `st` 10% matches Ready 10% per vCPU. On ESXi this needs the VM's steal clock (`stealclock.enable`, Broadcom KB 434983); without it Linux shows `st` 0.
- B is correct: Windows does not account frozen time; it stays in whatever state the vCPU was in, so Windows reports higher utilization than vSphere (75% against Run 65%).
- C is wrong: steal time exists only in a VM; on dedicated hardware there is nothing to steal.
- D is wrong: steal is time the vCPU did not run at all.
- E is wrong: the wait is for physical CPUs on a busy host; more vCPUs add demand, and usually more Ready.
- F is wrong: steal counts frozen time only. The guest does not see Hyper-Threading or the clock speed; those effects show in VM counters such as Usage and Latency, not in steal.

## Notes
- The Overlap angle is left out on purpose: the knowledge base says both that Linux steal time excludes Overlap and that some documents call Overlap "stolen" (author question).

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
source_path: "Drafted by Claude 2026-11-12"
answer: [A, B]
misconception: [D, E, F]
misconception_type: [layer-confusion, frequency-and-hyper-threading]
status: reviewed
```
