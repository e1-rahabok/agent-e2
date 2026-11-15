# Relationship between VM and Guest OS memory metrics

## Prompt
- A Windows or Linux VM runs on ESXi 9.1. vCenter and VCF Operations collect its metrics.

Which statements about the VM memory metrics and the Guest OS memory metrics are correct?

- A. VCF Operations memory Utilization of a VM can read above 100% of its configured memory.
- B. When the guest can use less memory than is configured, VCF Operations counts the unusable part in the VM's memory Utilization.
- C. VM Compressed includes the pages that Windows compresses inside its own memory.
- D. If VMware Tools is not installed on a Windows VM, ESXi cannot balloon it.
- E. If VMware Tools is not running, VCF Operations falls back to Consumed for the VM's memory Utilization.
- F. Once a guest has touched a page, ESXi has no way to take that memory back from the VM.
- G. A memory limit at the guest's In Use value is a safe way to make ESXi take back the memory the guest freed.

## Likely wrong answer
C: a Guest OS counter and a VM counter with the same name read as one. Or F, the over-correction: ESXi can never take memory back.

## Expected key points
- Answer: A, B, D, E.
- A is true: VCF Operations VM memory Utilization adds guest page-in (rate × page size) and the memory the guest cannot use to Guest Needed Memory, so it can exceed 100%; that is not an error.
- B is true: the formula adds Memory Total Capacity minus Guest Physically Usable Memory, for example 22 GB on an 80 GB VM whose guest can use 58 GB.
- C is false: Windows compresses its In Use pages inside the guest, a Guest OS counter; VM Compressed is ESXi's compression of VM pages. Different layers, different counters.
- D is true: the balloon driver is the only way for ESXi to ask the guest for memory, and on Windows it ships with VMware Tools. Without it ESXi can only compress or swap.
- E is true: VCF Operations VM memory Utilization falls back to Consumed when guest metrics from VMware Tools are not collected; Consumed holds idle and cache pages, so the value reads higher.
- F is false: ESXi takes memory back by ballooning, compression and swapping. This is the over-correction of "ESXi does not see guest frees".
- G is false: the guest cannot see a limit, so it keeps using memory as if it had all of it, and the result is unpredictable; a limit used instead of right-sizing can cause a worse problem than a smaller VM.

## Notes
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): one fact per option; F the over-correction and G the wrong action added (author approved, 2026-11-14).
- Option D was "If VMware Tools is not running, the hypervisor cannot balloon the VM". The knowledge base (ballooning; Broadcom KB 313773) says the driver is a kernel driver: on Linux `vmw_balloon` is in the kernel and not part of open-vm-tools, so a Linux VM keeps ballooning while vmtoolsd is stopped. D now states the case both agree on (Windows without VMware Tools); the Linux case is raised as an author question (project/question-pairing-2026-11-14.md, section 1, item 5).
- Review 2026-11-15: the quiz's options A (the two layers are managed independently), B (the values and patterns differ) and C (a page freed in the guest is freed in ESXi) are tested by 0095 (B, C, D, E); they are replaced by facts 0095 lacks: VCF Operations Utilization above 100% (A), unusable guest memory (B) and the two compression counters (C). D and E, the quiz's own facts, stay. G's reason no longer rests on whether a limit causes ballooning (open author question Q214). Key unchanged: A, B, D, E.

## Metadata
```yaml
id: "0022"
title: "Relationship between VM and Guest OS memory metrics"
product: [vsphere, vcf-operations, windows, linux]
technology: [memory]
input: [text]
task: read-metric
knowledge:
  - vsphere/technology/memory/concepts/guest-os-vs-vm-memory
  - vsphere/technology/memory/concepts/ballooning
  - vsphere/technology/memory/metrics/virtual-motherboard/utilization
  - vsphere/technology/memory/metrics/virtual-motherboard/compressed
  - vsphere/technology/memory/metrics/virtual-motherboard/consumed
  - vsphere/architecture/resource-controls
  - vsphere/architecture/vm-vs-guest-os
object: [vm, guest-os]
tool: [vcenter, vcf-operations]
knowledge_main: vsphere/technology/memory/metrics/virtual-motherboard/utilization
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > Memory > Q2 VM vs Guest OS"
answer_type: deterministic
level: 300                      # author 2026-11-05
answer: [A,B,D,E]
misconception: [C]
misconception_type: [layer-confusion]
status: draft
```
