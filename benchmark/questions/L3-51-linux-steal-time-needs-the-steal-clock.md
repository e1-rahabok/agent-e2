# Two Linux VMs, the same Ready, different steal time

## Prompt
- Two RHEL 9 VMs (kernel 5.14, virtual hardware version 21) run the same batch job on the same busy ESXi 9.1 host.
- vCenter, last hour: CPU Readiness about 12% per vCPU on both VMs.
- `top` in vm-a shows `st` about 12; `top` in vm-b shows `st` 0.0.
- The only configuration difference: vm-a has `stealclock.enable = "TRUE"` in its advanced parameters.

Which statements about Linux steal time on vSphere are correct?

- A. On ESXi, Linux steal time is the time a vCPU was ready to run but had no physical thread.
- B. Without the VM's steal clock, Linux shows `st` 0 however long its vCPUs wait in Ready.
- C. `st` 0.0 in vm-b shows that its vCPUs were never frozen.
- D. Linux cannot report steal time on ESXi at all; `st` exists only in public clouds.
- E. In vm-b, the frozen time stays in the state each vCPU was in, so its busy figures read higher than vSphere's Run.
- F. Linux steal time on ESXi also counts Overlap, the time the kernel interrupted a running vCPU.
- G. A guest kernel without the VMware steal clock shows `st` 0 even with the VM option set.
- H. Trust the guest: vm-b's Readiness in vCenter must be a collection error, since its `st` is 0.0.
- I. Windows reports the same frozen time as steal time when VMware Tools runs.

## Likely wrong answer
C: `st` is 0.0, so the hypervisor never took CPU from vm-b. Or D: Linux has no steal time on vSphere.

## Expected key points
- Answer: A, B, E, G.
- A true: steal time on ESXi mirrors Ready: the vCPU is frozen while it waits for a thread.
- B true: steal accounting on vSphere needs the VM's steal clock (`stealclock.enable = TRUE`); without it the steal counter stays 0.
- C false: the misconception. vm-b waits as much as vm-a (Readiness 12%); it only does not count the wait.
- D false: over-correction. With the steal clock, Linux on ESXi reports steal, as vm-a does.
- E true: without steal accounting Linux, like Windows, does not account the frozen time; a busy vCPU's frozen time counts as busy.
- F false: steal time holds Ready only. ESXi counts Overlap as Run, so the guest is not told about it.
- G true: the steal clock needs the VM option, hardware version 13 or later, and a guest kernel with the VMware steal clock (mainline 5.7 or later, or a backport).
- H false: wrong action. The tools count at different layers; vCenter sees the wait the guest cannot see.
- I false: Windows has no steal time accounting.

## Notes
- Paired with the practical question 0381 (theory and practical; design.md, section 3.9). Situation numbers differ from 0381 on purpose.
- Vendor sources for general VMs, not only Tanzu: Broadcom TechDocs, Tanzu GemFire 10.1, High CPU Steal, section VMware ESXi: "PhotonOS guests have CPU steal time tracking enabled by default. Other guest operating systems require the VM configuration option: stealclock.enable = "TRUE""; "If a VM does not support tracking CPU steal time, the steal_time counter in /proc/stat will always be 0" (https://techdocs.broadcom.com/us/en/vmware-tanzu/data-solutions/tanzu-gemfire/10-1/gf/managing-checklist-cpu-steal-high.html). Broadcom KB 376609: on VMware vSphere steal time "is not enabled automatically"; configure the VM with `stealclock.enable = "TRUE"` (https://knowledge.broadcom.com/external/article/376609). Broadcom KB 434983 (Tanzu): hardware version 13 or later. The scenario uses RHEL, not Photon OS, because of the Photon default.
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item D12). Counts only after author approval.

## Metadata
```yaml
id: "0380"
title: "Two Linux VMs, the same Ready, different steal time"
product: [vsphere, linux]
technology: [cpu]
task: explain-mechanism
level: 300
answer_type: deterministic
input: [text]
object: [guest-os, vm]
tool: [guest-os-tools, vcenter]
knowledge:
  - vsphere/technology/cpu/concepts/guest-os-vs-vm-cpu
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
  - vsphere/technology/cpu/metrics/virtual-motherboard/latency
knowledge_main: vsphere/technology/cpu/concepts/guest-os-vs-vm-cpu
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D12"
answer: [A, B, E, G]
misconception: [C]
misconception_type: [layer-confusion]
pair: "0381"
status: draft
```
