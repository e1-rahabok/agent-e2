# Provider vs consumer metrics

## Prompt
- In the vSphere Client, the performance chart of an ESXi host shows CPU Ready and CPU Demand.

Which statements are correct?

- A. Host CPU Ready is the Ready time of the host's VMs, added up at the host.
- B. Host CPU Ready measures the host's physical cores waiting for work to arrive.
- C. Every host CPU counter is a sum over the host's VMs.
- D. Host CPU Demand is the sum over the VMs of the CPU they would use with no contention.
- E. Host CPU Demand adds the VMkernel's actual CPU use to the demand of the VMs.
- F. A high host CPU Ready calls for tuning the host itself (BIOS, power policy) before looking at any VM.
- G. Host CPU Usage includes kernel work such as vSAN and NSX.
- H. The name of a host counter tells whether it measures the host itself or adds up its VMs.
- I. Throughput of the host's physical NICs (vmnics) has no VM equivalent.
- J. Host CPU Demand can be read for each physical core or thread of the host.

## Likely wrong answer
- B: "Host Ready is the host's own cores waiting."
- E: "Host Demand is the host's whole load, VMs plus the VMkernel."
- C: "A host counter is always the sum of its VMs" (the over-correction).

## Expected key points
- Answer: A, D, G, I.
- A is true: Ready is a consumer concept (a VM waiting to be scheduled); the host value adds up its VMs.
- B is false: a physical core or thread is always ready; Ready does not apply to ESXi itself.
- C is false: Usage and Utilization are summed over the physical cores and threads, and vmnic throughput exists only at the host; only some host counters add up the VMs.
- D is true: in vCenter, ESXi CPU Demand is the sum over the VMs, an internal value of the CPU scheduler: the demand had there been no contention.
- E is false: Demand is not the sum of VM worlds plus VMkernel worlds; kernel work is in Usage.
- F is false: host Ready is the VMs' wait; read the VMs, starting with the worst, and their limits, shares and size.
- G is true: Usage counts actual use by the VMs and the kernel, vSAN and NSX included.
- H is false: the name does not say which kind a counter is; you must know the mechanism.
- I is true: physical network in ESXi exists only at the host; the sum of VM network at ESXi is the counter that adds up the VMs.
- J is false: Demand is summed over the VMs, not over physical threads, so it has no per-core or per-thread value.

## Notes
- Tests: Principle: provider vs consumer perspective; a host metric of its own vs a sum of the VMs' metric.
- Key corrected 2026-11-12. It read ESXi CPU Demand as a provider metric. The knowledge base (host/demand, provider-consumer) and the author's answer to Q009 settle it: the value at ESXi is the summation over the VMs, a sum-of-consumer metric held at the provider. A candidate that said "sum of consumers" was scored 0 against the old key in all runs of 20261112 (see project/plan.md).
- Converted from judged to multiple choice (Q199 F, 2026-11-14). The definitions of provider and consumer-based metric moved from the question into the context.
- Hint moved out of the prompt (author, 2026-11-14: a hint helps the frontier model, not the local model), for reviewers: "A provider metric is about the ESXi host itself; a consumer-based metric is aggregated from the metrics of the VMs the host runs."
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): the stem names the vSphere Client host chart (vCenter Demand, without reservations); old C (a core has no Ready) negated B, old F negated D, and old G's clause negated E; C is now the over-correction, F the wrong action, G one fact; knowledge-base terms removed from the options. Key changed from A, C, D, G, I to A, D, G, I (author approved, 2026-11-14).
- Paired with 0115 (theory and practical, design.md 3.9).

## Metadata
```yaml
id: "0016"
title: "Provider vs consumer metrics"
product: [vsphere]
technology: [system]
input: [text]
task: read-metric
knowledge:
  - vsphere/architecture/provider-consumer
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
  - vsphere/technology/cpu/metrics/host/demand
  - vsphere/technology/cpu/metrics/host/usage
attachments: []
origin: book
source_path: "The World of Metrics > Metrics Nuances: Virtualization Impact; Architecture Complexity (VM vs ESXi; ESXi ≠ VMs + Kernel)."
answer_type: deterministic
answer: [A, D, G, I]
misconception: [B, E]
level: 300                      # author 2026-11-05
object: [esxi, vm]
tool: [vcenter]
knowledge_main: vsphere/architecture/provider-consumer
misconception_type: [provider-vs-consumer]
pair: "0115"
status: draft                     # reviewed as a free-text question; converted to multiple choice 2026-11-14 (Q199): review again
```
