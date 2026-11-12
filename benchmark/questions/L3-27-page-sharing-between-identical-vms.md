# Page sharing between identical VMs

## Prompt
- A VDI cluster on ESXi 9.1. Each host runs 120 Windows 11 desktops cloned from the same image.
- Host memory Shared is small. The team expected a large saving from transparent page sharing, as they had on vSphere 5.5.
- They plan to change a setting to get the saving back.

Which statements are correct?

- A. ESXi shares pages only between VMs in the same resource pool, and these desktops sit in different pools, so little is shared.
- B. VMs share pages only when their salt matches, and each VM's salt is unique by default; a host option changes that.
- C. Sharing within each VM is also turned off by default since vSphere 6.0, which is why the host Shared counter stays small here.
- D. The small saving shows that page sharing is broken on these hosts; the fix is to open a support case and collect logs.
- E. Sharing pages between VMs has no side effect on security, which is why the default still allows it on 9.1.

## Likely wrong answer
D: low sharing read as a fault. Or E: the pre-6.0 default assumed to still hold.

## Expected key points
- Answer: B.
- A is wrong: resource pools play no part in page sharing.
- B: since vSphere 6.0, inter-VM sharing needs the same salt; the default salt is the VM's own `vc.uuid`, unique per VM. Intra-VM sharing stays on. `Mem.ShareForceSalting = 0` restores the pre-6.0 behaviour for every VM on the host; the per-VM option `sched.mem.pshare.salt` builds smaller sharing groups. The default changed because shared pages between VMs open a side channel.
- C is wrong: sharing within a VM is on by default.
- D is wrong: the behaviour is the default, not a fault.
- E is wrong: the default changed precisely because of the security risk.

## Notes
- Sources: Performance Best Practices for vSphere 9.1, Memory Page Sharing; Broadcom KB 2097593 and 2080735 (salting); the knowledge base, page sharing.

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
source_path: "Drafted by Claude 2026-11-12 for the memory slots (project/plan.md, M2)"
answer: [B]
misconception: [D, E]
misconception_type: [threshold-transplanted]
status: draft
```
