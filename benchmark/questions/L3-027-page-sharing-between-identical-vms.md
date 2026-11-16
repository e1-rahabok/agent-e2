# Page sharing between identical VMs

## Prompt
- A VDI cluster on ESXi 9.1. Each host runs 120 Windows 11 desktops cloned from the same image.
- Host memory Shared is small. The team expected a large saving from transparent page sharing, as they had on vSphere 5.5.
- They plan to change a setting to get the saving back.

Which statements are correct?

- A. A common `sched.mem.pshare.salt` works only after the host salting setting is changed too.
- B. With default settings, two VMs share a page only when their salt values match.
- C. By default, each VM gets a salt value of its own.
- D. The small saving shows that page sharing is broken on these hosts and needs a support case.
- E. Sharing pages between VMs is still on by default in vSphere 9.1.
- F. One host advanced setting turns on sharing between all the VMs of a host.
- G. Giving all the desktops one common salt value has no security downside.

## Likely wrong answer
D: low sharing read as a fault. Or E: the pre-6.0 default assumed to still hold.

## Expected key points
- Answer: B, C, F.
- A is wrong: the per-VM salt and the host setting are two separate ways to allow sharing between VMs; desktops given the same `sched.mem.pshare.salt` form a sharing pool with the host setting at its default.
- B is correct: since vSphere 6.0, inter-VM sharing needs the same salt value unless the host setting in F turns salting off.
- C is correct: the default salt is the VM's own `vc.uuid`, unique per VM on a host, which prevents inter-VM sharing.
- D is wrong: the behaviour is the default, not a fault.
- E is wrong: since vSphere 6.0 the default is sharing within a VM only; earlier releases shared between VMs by default.
- F is correct: `Mem.ShareForceSalting = 0` applies to all VMs on the host and restores the pre-6.0 behaviour (KB 2097593). The per-VM option `sched.mem.pshare.salt` builds smaller sharing groups.
- G is wrong: one salt for every VM makes a single sharing pool, the pre-6.0 default that was changed for security; review the security implications first (KB 2080735, 2097593). The fix taken as free.

## Notes
- Sources: Performance Best Practices for vSphere 9.1, Memory Page Sharing; Broadcom KB 2097593 and 2080735 (salting); the knowledge base, page sharing.
- Sharing within a VM (off or on by default) is tested by 0146 G; ESXi not sharing 2 MB pages by 0058 A and 0060 H, so neither is an option here.
- Changed in the 2026-11-15 audit: A (resource pools, a throwaway decided only by absence) replaced by the per-VM salt misconception; D without the support-case action tail; F without the hedge.

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
source_path: "Synthetic, 2026-11-12"
answer: [B, C, F]
misconception: [D, E]
misconception_type: [threshold-transplanted]
status: draft
```
