# Used of the VM vs the sum of its vCPUs

## Prompt
- A 4-vCPU VM runs a busy NFS file service.
- Its ESXi host is lightly loaded. The host power policy is High Performance.
- One Real-time sample (20 seconds) from the vSphere Client advanced CPU chart:

| Instance | Run (ms) | Used (ms) |
|---|---|---|
| vCPU 0 | 12,050 | 13,840 |
| vCPU 1 | 11,980 | 13,770 |
| vCPU 2 | 12,010 | 13,800 |
| vCPU 3 | 11,960 | 13,750 |
| VM (aggregate) | 48,000 | 58,140 |

- In the same sample: System 2,900 ms, Overlap about 20 ms per vCPU, Ready and Co-stop near 0.
- The storage team says the chart is wrong: the four vCPUs add up to 55,160 ms of Used, not 58,140 ms.

Which statements are correct?

- A. The aggregate also holds work charged to the VM as a whole: System time and the VMX, MKS and helper worlds.
- B. The aggregate Used of a VM equals the sum of its vCPU instances.
- C. Each vCPU's Used is about 15% above its Run because the cores ran above their base clock (Turbo Boost).
- D. Used above Run shows the vCPUs waited for a physical CPU during the sample.
- E. System time is charged to vCPU 0, which is why vCPU 0 shows the highest Used.
- F. The gap between the aggregate and the sum grows with the IO the VM drives, so a busy file service shows a visible gap.
- G. Run of the VM equals the sum of its vCPUs because System time is not part of Run.
- H. The gap between the aggregate and the sum is the Turbo gain, counted a second time at VM level.
- I. Add a vCPU: the file service is short of CPU.

## Likely wrong answer
B: the VM row must be the sum of the vCPU rows. Or E: System time is charged to vCPU 0.

## Expected key points
- Answer: A, C, F, G.
- A: VM-level Used = Run - Overlap ± frequency and Hyper-Threading effect + System + VMX + MKS + helper worlds. Per-vCPU Used has no System part. 58,140 - 55,160 = 2,980 ms: System (2,900 ms) and the other VM worlds.
- B is wrong: same name, same object, different instance, different formula. Run has no System part, so its aggregate equals the sum; Used does not.
- C: Used counts work and converts it to ms at the base (nominal) frequency. 13,800 / 12,000 is about 1.15: the cores ran about 15% above base. Overlap is too small to matter, and the host is not busy, so Hyper-Threading does not pull Used down.
- D is wrong: waiting shows in Ready and Co-stop, which are near 0. Used above Run is faster work, not waiting.
- E is wrong: vCPU 0's Used is only 40-90 ms above the other vCPUs; 2,900 ms of System would show there, and the four vCPU rows add up to 55,160 ms, without it. System sits in the VM aggregate.
- F: the hypervisor processes the guest's storage and network IO a second time and charges it as System. IO-heavy VMs show the largest gap.
- G: Run counts only the time the vCPUs ran; the work the hypervisor does for the VM is charged to Used, not Run.
- H is wrong: the Turbo gain is already in each vCPU's Used; the 2,980 ms gap matches System (2,900 ms) plus the other VM worlds.
- I is wrong: Run is about 60% per vCPU and Ready and Co-stop are near 0; nothing shows a shortage.

## Notes
- From the author's samples: "Why does the formula state VM level, and not individual vCPU level?" and "How will Used compare with Run in general?"
- Rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): "(VM only)" removed from the stem (it told where System is charged); A no longer negates E; B one fact; H (a misreading of the gap) and I (the wrong action) added. Key unchanged, A, C, F, G (author approved, 2026-11-14).

## Metadata
```yaml
id: "0100"
title: "Used of the VM vs the sum of its vCPUs"
product: [vsphere]
technology: [cpu]
task: explain-mechanism
level: 400
answer_type: deterministic
input: [text]
object: [vm]
tool: [vcenter]
knowledge:
  - vsphere/technology/cpu/metrics/virtual-motherboard/used
  - vsphere/technology/cpu/metrics/virtual-motherboard/system
  - vsphere/architecture/kernel-worlds
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/used
attachments: []
origin: book
source_path: "Author samples (docx, 2026-11-12) > Used at VM level vs vCPU level; Used vs Run"
answer: [A, C, F, G]
misconception: [B, E]
misconception_type: [same-name-other-object, frequency-and-hyper-threading]
status: draft
```
