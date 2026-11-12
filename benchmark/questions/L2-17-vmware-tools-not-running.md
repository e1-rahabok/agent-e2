# VMware Tools not running on a Linux VM

## Prompt
- After an OS update, the open-vm-tools service (vmtoolsd) failed to start on a Linux VM and stayed stopped for three days.
- You look at the VM in vCenter and VCF Operations for those three days.

Which of these can still be read for that period, or still works?

- A. VM CPU Ready.
- B. VM Memory Consumed.
- C. Guest OS CPU run queue.
- D. Free space per Linux file system.
- E. VM virtual disk latency.
- F. The Linux IP addresses and host name in the VM's summary.

## Likely wrong answer
C, D or F: data from inside Linux assumed to come from the hypervisor.

## Expected key points
- Answer: A, B, E.
- A, B, E are correct: the VMkernel measures them itself, from outside the guest: CPU scheduling, the memory pages it backs, and the IO the VM sends.
- C is wrong: the run queue is a Linux counter; VMware Tools collects it inside the guest. Without Tools it does not exist in vSphere.
- D is wrong: file system space is also read inside the guest by VMware Tools.
- F is wrong: the IP addresses and host name are reported from inside the guest by VMware Tools. Without the service, vCenter shows them as unknown.

## Notes
- Ballooning is not an option here: on Linux the balloon driver (vmw_balloon) is an upstream kernel driver, not part of open-vm-tools, so it keeps working while vmtoolsd is stopped (open-vm-tools README; Broadcom KB 313773). The knowledge base says the opposite (author question).

## Metadata
```yaml
id: "0271"
title: "VMware Tools not running on a Linux VM"
product: [linux, vsphere]
technology: [system, memory]
task: read-metric
level: 200
answer_type: deterministic
input: [text]
object: [guest-os, vm]
tool: [vcenter, vcf-operations]
knowledge:
  - vsphere/architecture/vm-vs-guest-os
  - guest-os/cpu/metrics/run-queue
  - guest-os/storage/disk-queue
knowledge_main: vsphere/architecture/vm-vs-guest-os
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12 for the Guest OS slots (project/plan.md, M2)"
answer: [A, B, E]
misconception: [C, D, F]
misconception_type: [layer-confusion]
status: draft
```
