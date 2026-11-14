# Relationship between VM and Guest OS memory metrics

## Prompt
- A Windows or Linux VM runs on ESXi 9.1. vCenter and VCF Operations collect its metrics.

Which statements about the VM memory metrics and the Guest OS memory metrics are correct?

- A. Windows and Linux run their memory as on a physical server, without seeing the host's memory.
- B. ESXi cannot tell which guest pages Windows counts as Standby (cache) or Free.
- C. When Windows or Linux frees a page, ESXi frees the matching host page within a few minutes.
- D. If VMware Tools is not installed on a Windows VM, ESXi cannot balloon it.
- E. If VMware Tools is not running, VCF Operations falls back to Consumed for the VM's memory Utilization.
- F. Once a guest has touched a page, ESXi has no way to take that memory back from the VM.
- G. A memory limit at the guest's In Use value is a safe way to make ESXi take back the memory the guest freed.

## Likely wrong answer
C: a page freed in the guest assumed to be freed in ESXi too. Or F, the over-correction: ESXi can never take memory back.

## Expected key points
- Answer: A, B, D, E.
- A is true: the two layers manage memory independently; the Guest OS cannot see the underlying host memory.
- B is true: how the Guest OS classifies its pages (In Use, Modified, Standby or cache, Free) and its page file are ESXi blind spots; ESXi sees only reads and writes.
- C is false: freeing a page only updates the guest's free list, an ordinary memory write. The hypervisor does not see it, so the ESXi page stays mapped and Consumed does not drop.
- D is true: the balloon driver is the only way for ESXi to ask the guest for memory, and on Windows it ships with VMware Tools. Without it ESXi can only compress or swap.
- E is true: VCF Operations VM memory Utilization falls back to Consumed when guest metrics from VMware Tools are not collected; Consumed holds idle and cache pages, so the value reads higher.
- F is false: ESXi takes memory back by ballooning, compression and swapping. This is the over-correction of "ESXi does not see guest frees".
- G is false: a limit does not reclaim the right pages. ESXi cannot see which pages the guest uses, so it compresses and swaps pages at random under the limit, the guest cannot see the limit, and the result is unpredictable; a limit used instead of right-sizing can cause a worse problem.

## Notes
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): A, B and E one fact each; F the over-correction and G the wrong action added. Key unchanged: A, B, D, E (author approved, 2026-11-14).
- Option D was "If VMware Tools is not running, the hypervisor cannot balloon the VM". The knowledge base (ballooning; Broadcom KB 313773) says the driver is a kernel driver: on Linux `vmw_balloon` is in the kernel and not part of open-vm-tools, so a Linux VM keeps ballooning while vmtoolsd is stopped. D now states the case both agree on (Windows without VMware Tools); the Linux case is raised as an author question (project/question-pairing-2026-11-14.md, section 1, item 5).

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
  - vsphere/technology/memory/metrics/virtual-motherboard/consumed
  - vsphere/architecture/resource-controls
  - vsphere/architecture/vm-vs-guest-os
object: [vm, guest-os]
tool: [vcenter, vcf-operations]
knowledge_main: vsphere/technology/memory/concepts/guest-os-vs-vm-memory
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
