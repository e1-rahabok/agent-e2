# VMware Tools not running on a Linux VM

## Prompt
- After an OS update, the open-vm-tools service (vmtoolsd) failed to start on a Linux VM and stayed stopped for three days.
- You look at the VM in vCenter and VCF Operations for those three days.

Which of these counters still have data for those three days?

- A. VM CPU Ready.
- B. VM Memory Consumed.
- C. Guest OS CPU run queue.
- D. Guest OS disk queue length.
- E. VM virtual disk latency.
- F. Guest OS context switch rate.

## Likely wrong answer
C, D or F: counters from inside Linux, stored on the VM object, assumed to come from the hypervisor.

## Expected key points
- Answer: A, B, E.
- A, B, E are correct: the VMkernel measures them itself, from outside the guest: CPU scheduling, the memory pages it backs, and the IO the VM sends.
- C is wrong: the run queue is a Linux counter; VMware Tools collects it inside the guest. Without Tools it does not exist in vSphere.
- D is wrong: the guest disk queue is also collected inside the guest by VMware Tools; it is stored on the VM object, but the Guest OS produces it.
- F is wrong: the context switch rate is a Guest OS counter that VMware Tools collects inside the guest.

## Notes
- Options rewritten 2026-11-14 (project/question-pairing-2026-11-14.md): D (file system free space) and F (IP addresses and host name) were not in the knowledge base; replaced by two Guest OS counters that VMware Tools collects. Key unchanged.
- Ballooning is not an option here: on Linux the balloon driver (vmw_balloon) is an upstream kernel driver, not part of open-vm-tools, so it keeps working while vmtoolsd is stopped (open-vm-tools README; Broadcom KB 313773).

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
  - guest-os/cpu/metrics/context-switch
knowledge_main: vsphere/architecture/vm-vs-guest-os
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
answer: [A, B, E]
misconception: [C, D, F]
misconception_type: [layer-confusion]
status: draft
```
