# Page sharing between identical VMs

## Prompt
- A VDI cluster on ESXi 9.1. Each host runs 120 Windows 11 desktops cloned from the same image.
- Host memory Shared is small. The team expected a large saving from transparent page sharing, as they had on vSphere 5.5.
- They plan to change a setting to get the saving back.

Which statements are correct?

- A. ESXi shares pages only between VMs in the same resource pool.
- B. Two VMs share a page only when their salt values match.
- C. By default, each VM gets a salt value of its own.
- D. The small saving shows that page sharing is broken on these hosts: open a support case and collect logs.
- E. Sharing pages between VMs is still on by default in vSphere 9.1.
- F. One host advanced setting can let every VM on the host share pages with the others.
- G. Giving all the desktops one common salt value has no security downside.

## Likely wrong answer
D: low sharing read as a fault. Or E: the pre-6.0 default assumed to still hold.

## Expected key points
- Answer: B, C, F.
- A is false: resource pools play no part in page sharing.
- B is true: since vSphere 6.0, inter-VM sharing needs the same salt value.
- C is true: the default salt is the VM's own `vc.uuid`, unique per VM on a host, which prevents inter-VM sharing.
- D is false: the behaviour is the default, not a fault.
- E is false: since vSphere 6.0 the default is sharing within a VM only; earlier releases shared between VMs by default.
- F is true: `Mem.ShareForceSalting = 0` applies to all VMs on the host and restores the pre-6.0 behaviour (KB 2097593). The per-VM option `sched.mem.pshare.salt` builds smaller sharing groups.
- G is false: one salt for every VM makes a single sharing pool, the pre-6.0 default that was changed for security; review the security implications first (KB 2080735, 2097593). This is the over-correction: the fix taken as free.

## Notes
- Sources: Performance Best Practices for vSphere 9.1, Memory Page Sharing; Broadcom KB 2097593 and 2080735 (salting); the knowledge base, page sharing.
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): A no longer adds a case fact the stem does not give (desktops in different pools); old B split into B, C and F; E one fact; G the over-correction added. Old C (sharing within a VM is off by default) removed: the same fact is option G of 0146. Key changed from B to B, C, F.

## Metadata
```yaml
id: "0145"
title: "Page sharing between identical VMs"
product: [vsphere, windows]
technology: [memory]
task: judge-setting
level: 300
answer_type: deterministic
input: [text]
object: [esxi, vm]
tool: [none]
knowledge:
  - vsphere/technology/memory/concepts/page-sharing
  - vsphere/technology/memory/concepts/large-memory-pages
knowledge_main: vsphere/technology/memory/concepts/page-sharing
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
answer: [B, C, F]
misconception: [D, E]
misconception_type: [threshold-transplanted]
status: draft
```
