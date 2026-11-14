# Memory usage: VM vs ESXi

## Prompt
- Every VM on an ESXi host shows Memory Usage below 25% in vCenter.
- The host itself shows Memory Usage at 95% in vCenter.
- The customer wants to buy more RAM.

Which statements are correct?

- A. The two values are inconsistent, which points to a collection or reporting fault.
- B. VM Memory Usage in vCenter reads the VM's Active memory.
- C. A memory Demand counter, like CPU Demand, would show whether the VMs need more memory.
- D. Host Memory Usage reads Consumed: the memory the VMs have claimed on the host.
- E. Host Memory Usage at 95% shows the host is short of memory, so more RAM is needed.
- F. Cluster Memory Usage in vCenter reads Active memory, like the VM.
- G. Memory works as a cache, so host Consumed near 100% is expected and is not proof of a shortage.
- H. In VCF Operations, VM Memory Usage (%) is the same as in vCenter: Active memory against configured memory.
- I. Whether the host is short of memory is read from contention counters, not from Usage.

## Likely wrong answer
- E: "The host is nearly full, buy RAM."
- A: "The numbers are inconsistent, something is broken."

## Expected key points
- Answer: B, D, G, I.
- A is false: the same name measures different things per object (two-level memory hierarchy): VM level is what is actively used (performance), host level is what the VMs have claimed (capacity).
- B is true: vCenter VM Memory Usage (%) maps to Active.
- C is false: vCenter has no memory Demand counter; memory is space, not time.
- D is true: ESXi Memory Usage maps to Consumed, a capacity counter.
- E is false: the misconception; high Consumed is not proof of shortage, and this confusion has led customers to buy more RAM than needed.
- F is false: cluster Memory Usage maps to Consumed, with VM overhead included.
- G is true: memory is a cache; near 100% is expected and is good use of the money spent on it.
- H is false: VCF Operations computes VM Memory Usage (%) from Guest OS Needed Memory and falls back to Active only when guest data is missing.
- I is true: check contention (memory latency, swap-in, balloon), not Usage, to decide.

## Notes
- Tests: Same name, different formula per object (distinction).
- Converted from judged to multiple choice (Q199 F, 2026-11-14).

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
object: [vm, esxi]
tool: [vcenter]
knowledge_main: vsphere/technology/memory/metrics/virtual-motherboard/usage
attachments: []
origin: book
source_path: "The World of Metrics > Metrics Nuances: Naming Complexity; Architecture Complexity (Memory)."
answer_type: deterministic
answer: [B, D, G, I]
misconception: [E, A]
level: 400                      # author 2026-11-05
misconception_type: [same-name-other-object, consumption-as-contention]
status: draft
```
