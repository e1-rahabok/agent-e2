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
- G. VM Memory Swapped.
- H. VM Memory Ballooned.

## Answers
A, B, E, G, H

## Explanation
- A is correct: Ready is CPU scheduling time the VMkernel measures itself, outside the guest.
- B is correct: Consumed counts the host pages the VMkernel backs for the VM; no guest component takes part.
- C is wrong: the run queue is a Linux counter; VMware Tools collects it inside the guest. Without Tools it does not exist in vSphere.
- D is wrong: the guest disk queue is also collected inside the guest by VMware Tools; it is stored on the VM object, but the Guest OS produces it.
- E is correct: virtual disk latency is measured by the VMkernel on the IO the VM sends to its virtual disk.
- F is wrong: the context switch rate is a Guest OS counter that VMware Tools collects inside the guest.
- G is correct: ESXi swaps the VM's pages itself, at random and blind to guest free memory; no guest component takes part, so Swapped keeps its data.
- H is correct: Ballooned is a VMkernel counter, so it has data whatever the guest does (it would read 0 with no driver). It can stay above 0 here because on Linux the balloon driver is the kernel module `vmw_balloon`, not part of open-vm-tools, so ballooning goes on while vmtoolsd is stopped.
- Misconception: C, D or F: counters from inside Linux, stored on the VM object, assumed to come from the hypervisor. Or the over-correction: leaving out G or H, as if memory reclamation needed VMware Tools.

## Notes
- 2026-11-16 (author, Q251): level 200 to 300, as the reviewers read it. A new Level 200 basics question for the guard is still to write.
- Linux ballooning with vmtoolsd stopped: settled from the knowledge base (memory/concepts/ballooning; Q223).
- Changed in the 2026-11-15 audit: level 200 -> 300 (H needs the Linux balloon module, G is the over-correction of the layer rule); key points one bullet per option, H says first that Ballooned is a VMkernel counter. C, D and F test one fact (Guest OS counters come through VMware Tools); the reviewer's replacements for F (the VCF Operations Usage fallback, Guest Needed Memory) are facts already tested twice or the same fact again, so F stays.

## Metadata
```yaml
id: "0271"
title: "VMware Tools not running on a Linux VM"
product: [linux, vsphere]
technology: [system, memory]
task: read-metric
level: 300                      # Q251, author 2026-11-16: relabelled as written (was 200)
answer_type: deterministic
input: [text]
object: [guest-os, vm]
tool: [vcenter, vcf-operations]
knowledge:
  - vsphere/architecture/vm-vs-guest-os
  - guest-os/cpu/metrics/run-queue
  - guest-os/storage/disk-queue
  - guest-os/cpu/metrics/context-switch
  - vsphere/technology/memory/metrics/virtual-motherboard/swapped
  - vsphere/technology/memory/concepts/ballooning
knowledge_main: vsphere/architecture/vm-vs-guest-os
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
misconception: [C, D, F]
misconception_type: [layer-confusion]
status: draft
```
