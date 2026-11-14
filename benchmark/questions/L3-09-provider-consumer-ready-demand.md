# Provider vs consumer metrics

## Prompt
- An ESXi host dashboard shows "CPU Ready" and "CPU Demand".
- A provider metric is about the ESXi host itself; a consumer-based metric is aggregated from the metrics of the VMs the host runs.

Which statements are correct?

- A. Host CPU Ready is the Ready time of the host's VMs, added up at the host.
- B. Host CPU Ready measures the host's physical cores waiting for work to arrive.
- C. A physical core or thread has no Ready time of its own, because it is always ready.
- D. Host CPU Demand is the sum over the VMs of the CPU they would use with no contention.
- E. Host CPU Demand adds the VMkernel's actual CPU use to the demand of the VMs.
- F. Host CPU Demand is a provider metric of its own, unrelated to the demand of the VMs.
- G. Kernel work such as vSAN and NSX shows in host CPU Usage, not in host CPU Demand.
- H. The name of a host counter tells you whether it is a provider metric or a sum of its consumers.
- I. Throughput of the host's physical NICs (vmnics) is a provider metric with no VM equivalent.
- J. Host CPU Demand can be read for each physical core or thread of the host.

## Likely wrong answer
- B: "Host Ready is the host's own cores waiting."
- E: "Host Demand is the host's whole load, VMs plus the VMkernel."
- F: "Demand on the host is a host metric, so it has nothing to do with the VMs' demand."

## Expected key points
- Answer: A, C, D, G, I.
- A is true: Ready is a consumer concept (a VM waiting to be scheduled); the host value is a sum-of-consumers metric held at ESXi.
- B is false: a physical core or thread is always ready; Ready does not apply to ESXi itself.
- C is true: same reason; read a high host Ready by going to the VMs, starting with the worst.
- D is true: ESXi CPU Demand is a sum-of-consumers metric, an internal value of the CPU scheduler: the ideal demand had there been no contention.
- E is false: Demand is not the sum of VM worlds plus VMkernel worlds; kernel work is in Usage.
- F is false: the value at ESXi is the summation over the VMs, so it is a sum-of-consumers metric, not a provider metric.
- G is true: Usage includes the kernel (vSAN, NSX); Demand does not include kernel work, so a host figure is not VMs plus kernel by default.
- H is false: the metric name does not say which kind it is; you must know the mechanism.
- I is true: physical network in ESXi exists only at the provider; the sum of VM network at ESXi is the sum-of-consumers counterpart.
- J is false: Demand is summed over the VMs, not over physical threads, so it has no per-core or per-thread value.

## Notes
- Tests: Principle: provider vs consumer perspective; provider metric vs sum-of-consumer metric.
- Key corrected 2026-11-12. It read ESXi CPU Demand as a provider metric. The knowledge base (host/demand, provider-consumer) and the author's answer to Q009 settle it: the value at ESXi is the summation over the VMs, a sum-of-consumer metric held at the provider. A candidate that said "sum of consumers" was scored 0 against the old key in all runs of 20261112 (see project/plan.md).
- Left out of the options: whether a host with no VMs shows Demand at 0 or flat at the kernel reservation (host/demand and provider-consumer differ on it).
- Converted from judged to multiple choice (Q199 F, 2026-11-14). The definitions of provider and consumer-based metric moved from the question into the context.

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
attachments: []
origin: book
source_path: "The World of Metrics > Metrics Nuances: Virtualization Impact; Architecture Complexity (VM vs ESXi; ESXi ≠ VMs + Kernel)."
answer_type: deterministic
answer: [A, C, D, G, I]
misconception: [B, E, F]
level: 300                      # author 2026-11-05
object: [esxi, vm]
tool: [none]
knowledge_main: vsphere/architecture/provider-consumer
misconception_type: [provider-vs-consumer]
status: draft                     # reviewed as a free-text question; converted to multiple choice 2026-11-14 (Q199): review again
```
