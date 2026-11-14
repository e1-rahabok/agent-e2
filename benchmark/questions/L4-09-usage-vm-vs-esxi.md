# Memory usage: VM vs ESXi

## Prompt
- Every VM on an ESXi host shows Memory Usage below 25% in vCenter.
- The host itself shows Memory Usage at 95% in vCenter.
- The customer wants to buy more RAM.

Which statements are correct?

- A. The two values contradict each other, which points to a collection or reporting fault.
- B. VM Memory Usage in vCenter is based on the VM's Active memory.
- C. vCenter has a memory Demand counter for VMs, as it has for CPU.
- D. Host Memory Usage in vCenter is based on host Consumed.
- E. Host Memory Usage at 95% means the host needs more RAM.
- F. Cluster Memory Usage in vCenter is based on Active memory, like the VM's.
- G. Memory works as a cache, so host Consumed near 100% is the expected state of a host whose VMs have run for a while.
- H. A memory shortage on the host shows as memory Latency (contention) in its VMs.
- I. Host Memory Usage has no use in capacity management.

## Likely wrong answer
- E: "The host is nearly full, buy RAM."
- A: "The numbers are inconsistent, something is broken."

## Expected key points
- Answer: B, D, G, H.
- A is false: the same name measures different things per object (two-level memory hierarchy): VM level is what is actively used (performance), host level is what the VMs have claimed (capacity).
- B is true: vCenter VM Memory Usage (%) maps to Active.
- C is false: vCenter has no memory Demand counter (CPU has one); memory is space, not time.
- D is true: ESXi Memory Usage maps to Consumed, a capacity counter.
- E is false: the misconception and the wrong action; high Consumed is not proof of shortage, and this confusion has led customers to buy more RAM than needed.
- F is false: cluster Memory Usage maps to Consumed, with VM overhead included.
- G is true: memory is a cache; values near 100% are expected and are good use of the money spent on it.
- H is true: Memory Latency is the only counter of the wait; swap-in correlates with it. Read the worst VM, since the host's own Latency averages its VMs. Balloon is reclamation, not contention.
- I is false: host Usage maps to Consumed, which is related to capacity management; it does not decide a shortage, but it is not useless. This is the over-correction of E.

## Notes
- Tests: Same name, different formula per object (distinction).
- Converted from judged to multiple choice (Q199 F, 2026-11-14).
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md) (author approved, 2026-11-14): G and H no longer negate E; the key point of H no longer lists balloon as contention; I the over-correction added; old H (VCF Operations VM Memory Usage (%) is the vCenter value) removed, since that fact is tested by the new pair D2. Key changed from B, D, G, I to B, D, G, H (relettered; same facts).
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
answer: [B, D, G, H]
misconception: [E, A]
pair: "0151"
level: 400                      # author 2026-11-05
misconception_type: [same-name-other-object, consumption-as-contention]
status: draft
```
