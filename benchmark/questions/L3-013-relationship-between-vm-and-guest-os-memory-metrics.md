# Relationship between VM and Guest OS memory metrics

## Prompt
- Two VMs on an ESXi 9.1 host, with VMware Tools installed and running on both. vCenter and VCF Operations collect their metrics.
- app-win-11, Windows Server 2022, 96 GB configured: VCF Operations shows its memory Utilization at 104% of configured memory and Guest|Physically Usable Memory at about 64 GB. Task Manager inside Windows shows 50 GB in use, 3 GB of it compressed.
- db-lnx-04, Red Hat Enterprise Linux 9, 48 GB configured: its owner plans to stop the VMware Tools service (vmtoolsd) for a day.
- The team asks whether the 104% is a data error, how ESXi can take memory back from these VMs, and whether a limit could take back the memory the guests do not use.

Which statements are correct?

- A. VCF Operations memory Utilization of a VM can read above 100% of its configured memory.
- B. The roughly 32 GB that Windows cannot use on app-win-11 count in its Utilization.
- C. The vCenter Compressed counter of app-win-11 includes the 3 GB that Task Manager shows as compressed.
- D. If VMware Tools is not installed on a Windows VM, ESXi cannot balloon it.
- E. With plenty of free memory, a Windows VM's Utilization holds a buffer of 5% of its memory.
- F. Once a guest has touched a page, ESXi has no way to take that memory back from the VM.
- G. A memory limit at the guest's In Use value is a safe way to make ESXi take back the memory the guest freed.
- H. Stopping vmtoolsd on db-lnx-04 stops ESXi from ballooning that VM.

## Likely wrong answer
C: a Guest OS counter and a VM counter with the same name read as one. Or F, the over-correction: ESXi can never take memory back.

## Expected key points
- Answer: A, B, D, E.
- A is true: VCF Operations VM memory Utilization adds guest page-in (rate × page size) and the memory the guest cannot use to Guest Needed Memory, so it can exceed 100%; the 104% of app-win-11 is not an error.
- B is true: the formula adds Memory Total Capacity minus Guest Physically Usable Memory, here 96 - 64 = 32 GB.
- C is false: Windows compresses its In Use pages inside the guest, a Guest OS counter; VM Compressed is ESXi's compression of VM pages. Different layers, different counters.
- D is true: the balloon driver is the only way for ESXi to ask the guest for memory, and on Windows it ships with VMware Tools. Without it ESXi can only compress or swap.
- E is true: Guest Needed Memory, the first term of Utilization, keeps a hardcoded buffer: Needed = physical - max(0, Unneeded - 5% of physical). With plenty of unneeded memory, 5% of the whole memory is added, whatever the guest uses.
- F is false: ESXi takes memory back by ballooning, compression and swapping. This is the over-correction of "ESXi does not see guest frees".
- G is false: the guest cannot see a limit, so it keeps using memory as if it had all of it. ESXi enforces the limit at once, ballooning first, then compressing and swapping pages it picks blind; a limit used instead of sizing the VM smaller behaves worse than a VM configured smaller.
- H is false: on Linux the balloon driver is the kernel module `vmw_balloon`, not part of open-vm-tools; ballooning goes on while vmtoolsd is stopped. "VMware Tools: Not running" reports the service, not the driver.

## Notes
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): one fact per option; F the over-correction and G the wrong action added (author approved, 2026-11-14).
- Option D was "If VMware Tools is not running, the hypervisor cannot balloon the VM". The knowledge base (ballooning; Broadcom KB 313773) says the driver is a kernel driver: on Linux `vmw_balloon` is in the kernel and not part of open-vm-tools, so a Linux VM keeps ballooning while vmtoolsd is stopped. D states the Windows case; H the Linux case.
- Review 2026-11-15: the quiz's options A (the two layers are managed independently), B (the values and patterns differ) and C (a page freed in the guest is freed in ESXi) are tested by 0095 (B, C, D, E); they are replaced by facts 0095 lacks: VCF Operations Utilization above 100% (A), unusable guest memory (B) and the two compression counters (C). D and E, the quiz's own facts, stay.
- Changed in the 2026-11-15 audit: the definition prompt became a case with two VMs (F5); B, C and H now read the case; E (Utilization falls back to Consumed without guest data, tested by the pair 0396/0397) replaced by the 5% buffer inside Needed Memory; key point G gives the limit's enforcement order (a limit balloons first).

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
  - vsphere/technology/memory/concepts/memory-limit
  - guest-os/memory/windows-memory
object: [vm, guest-os]
tool: [vcenter, vcf-operations]
knowledge_main: vsphere/technology/memory/metrics/virtual-motherboard/utilization
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > Memory > Q2 VM vs Guest OS"
answer_type: deterministic
level: 300                      # author 2026-11-05
answer: [A,B,D,E]
misconception: [C, H]
misconception_type: [layer-confusion]
status: draft
```
