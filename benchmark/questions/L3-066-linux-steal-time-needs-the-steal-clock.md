# Two Linux VMs with the steal clock option, different steal time

## Prompt
- Two Ubuntu 22.04 VMs (kernel 5.15) run the same CPU-heavy job on the same busy ESXi 9.1 host. vCenter shows CPU Readiness of about 9% per vCPU on both.
- Both VMs have `stealclock.enable = "TRUE"` in their advanced parameters.
- vm-old was never upgraded: virtual hardware version 11. vm-new is at virtual hardware version 19.
- `top` shows `st` of about 9 in vm-new and 0.0 in vm-old.

Which statements about Linux steal time on vSphere are correct?

- A. In vm-new, `st` tracks the same frozen time that vCenter reports as Ready.
- B. vm-old reports no steal because its virtual hardware is too old for the steal clock.
- C. vm-old's `st` of 0.0 shows its vCPUs were never frozen, whatever vCenter reports.
- D. Upgrading vm-old to hardware version 13 or later, option kept, lets its `st` follow Ready.
- E. A kernel without the VMware steal clock shows `st` 0 even with the option and new hardware.
- F. Steal time on ESXi also counts the time the kernel interrupted a running vCPU (Overlap).
- G. Open a support case: vCenter reports Readiness for a VM whose guest shows no steal at all.
- H. A Windows guest on the same host would show this frozen time as steal time.

## Answers
A, B, D, E

## Explanation
- A true: with the steal clock working, Linux accounts the time a vCPU waits for a physical thread as steal; it mirrors Ready.
- B true: the steal clock needs the VM option, virtual hardware version 13 or later, and a guest kernel with the VMware steal clock; vm-old misses the hardware version.
- C false: the misconception. vm-old waits as much as vm-new (Readiness about 9%); it only cannot count the wait.
- D true: with all three conditions met, `st` follows Ready.
- E true: the kernel side is needed too (mainline 5.7 or later, or a distribution backport); the option and virtual hardware version 13 or later are not enough alone.
- F false: steal time holds Ready only. ESXi counts Overlap as Run, so the guest is not told about it.
- G false: wrong action. The two layers count differently; vCenter sees the wait that vm-old's guest cannot report.
- H false: Windows has no steal time accounting.
- Misconception: C: vm-old shows `st` 0.0, so its vCPUs were never held back. Or G: the guest and vCenter disagree, so vCenter is wrong.

## Notes
- Paired with the practical question 0381 (theory and practical; design.md, section 3.9). Situation numbers differ from 0381 on purpose.
- Vendor sources for general VMs, not only Tanzu: Broadcom TechDocs, Tanzu GemFire 10.1, High CPU Steal, section VMware ESXi: "PhotonOS guests have CPU steal time tracking enabled by default. Other guest operating systems require the VM configuration option: stealclock.enable = "TRUE""; "If a VM does not support tracking CPU steal time, the steal_time counter in /proc/stat will always be 0" (https://techdocs.broadcom.com/us/en/vmware-tanzu/data-solutions/tanzu-gemfire/10-1/gf/managing-checklist-cpu-steal-high.html). Broadcom KB 376609: on VMware vSphere steal time "is not enabled automatically"; configure the VM with `stealclock.enable = "TRUE"` (https://knowledge.broadcom.com/external/article/376609). Broadcom KB 434983 (Tanzu): hardware version 13 or later. The scenario uses Ubuntu, not Photon OS, because of the Photon default.
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item D12). Counts only after author approval.
- Changed in the 2026-11-15 audit: C, D and E reworded to similar lengths (the correct options were the longest).
- Review 2026-11-15: new situation that tests the other conditions of the steal clock (virtual hardware version, kernel support), away from the default-settings story of 0381; options reworded. Key changed from A, B, E, G to A, B, D, E (new options).

## Metadata
```yaml
id: "0380"
title: "Two Linux VMs with the steal clock option, different steal time"
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
misconception: [C]
misconception_type: [layer-confusion]
pair: "0381"
status: draft
```
