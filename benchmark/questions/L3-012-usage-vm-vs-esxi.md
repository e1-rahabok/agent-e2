# Memory usage: VM vs ESXi

## Prompt
- Every VM on an ESXi host shows Memory Usage below 25% in vCenter.
- The host itself shows Memory Usage at 95% in vCenter.
- The customer wants to buy more RAM.

Which statements are correct?

- A. The two values contradict each other, which points to a collection or reporting fault.
- B. vCenter has a memory Demand counter for VMs, as it has for CPU.
- C. Host Memory Usage in vCenter is based on host Consumed.
- D. Host Memory Usage at 95% means the host needs more RAM.
- E. Cluster Memory Usage in vCenter is based on Active memory, like the VM's.
- F. Host Consumed near 100% is the expected state once the VMs have run for a while.
- G. VMs that wait for memory the host took show it as memory Latency (Contention).
- H. Host Memory Usage has no use in capacity management.
- I. Adding up the Consumed of every VM on the host gives the host's Consumed.

## Answers
C, F, G

## Explanation
- A is false: one label, two models. vCenter VM Usage (%) is Active over configured memory, a sampled kernel estimate of recently touched pages; ESXi Usage (%) is Consumed over capacity, the pages the host holds. They do not contradict.
- B is false: vCenter has no memory Demand counter (CPU has one); memory is space, not time.
- C is true: ESXi Memory Usage maps to Consumed, a capacity counter.
- D is false: the misconception and the wrong action; near 100% is normal for a cache, and pressure shows in ballooning, compression, swapping and VM Memory Contention, not in Usage. This confusion has led customers to buy more RAM than needed.
- E is false: cluster Memory Usage maps to Consumed, with VM overhead included.
- F is true: memory is a cache; values near 100% are expected and are good use of the money spent on it.
- G is true: Memory Latency is the only counter of the wait; swap-in correlates with it. Read the worst VM, since the host's own Latency averages its VMs. Balloon is reclamation, not contention.
- H is false: host Usage maps to Consumed, which is related to capacity management; it does not decide a shortage, but it is not useless. This is the over-correction of D.
- I is false: host Consumed adds the kernel, vSAN, NSX and the VM overhead to the VMs' pages, so the sum of the VMs is lower.
- Misconception: D: "The host is nearly full, buy RAM." - A: "The numbers are inconsistent, something is broken."

## Notes
- Tests: Same name, different formula per object (distinction).
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md) (author approved, 2026-11-14): the options on host Consumed near 100% and on the Latency wait no longer negate the 95% misconception; the Latency key point no longer lists balloon as contention; the over-correction (no use in capacity management) added; the option that VCF Operations VM Memory Usage (%) is the vCenter value removed, since the pair 0394/0395 tests it.
- Review 2026-11-15: the Latency option reworded to the wait of the VMs whose memory the host took.
- Changed in the 2026-11-15 audit: level 400 to 300 (one same-name fact on two objects); old B (vCenter VM Usage is Active) dropped, as the redundancy cap keeps that fact in the pair 0394/0395; I added (the sum of the VMs' Consumed read as host Consumed, host/consumed misconception); G trimmed. Letters: old C to I are now B to H; answer B, D, G, H became C, F, G; misconception E, A became D, A. Key point A no longer uses a word from the Words to avoid table.
- Paired with 0151 (theory and practical; design.md, section 3.9).

## Metadata
```yaml
id: "0020"
title: "Memory usage: VM vs ESXi"
product: [vsphere]
technology: [memory]
input: [text]
task: read-metric
knowledge:
  - vsphere/technology/memory/metrics/virtual-motherboard/usage
  - vsphere/technology/memory/metrics/host/usage
  - vsphere/technology/memory/metrics/host/consumed
  - sp5-framework/observability/resource-nature
  - vsphere/technology/memory/metrics/cluster/usage
  - vsphere/technology/memory/metrics/comparisons/vm-memory-metrics
  - vsphere/technology/memory/metrics/virtual-motherboard/latency
  - vsphere/technology/memory/metrics/host/latency
object: [vm, esxi]
tool: [vcenter]
knowledge_main: vsphere/technology/memory/metrics/virtual-motherboard/usage
attachments: []
origin: book
source_path: "The World of Metrics > Metrics Nuances: Naming Complexity; Architecture Complexity (Memory)."
answer_type: deterministic
misconception: [D, A]
pair: "0151"
level: 300
misconception_type: [same-name-other-object, consumption-as-contention]
status: draft
```
