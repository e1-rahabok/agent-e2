# Provider vs consumer metrics

## Prompt
- An ESXi host dashboard shows "CPU Ready" and "CPU Demand".

For each, is it a provider's perspective (meaning the raw data is about the ESXi host itself) or is it a consumer's perspective (meaning it's aggregated from the ESXi running VMs' metrics)? 
Can a physical core itself have Ready time?

## Likely wrong answer
"Both are the host's own measurements": Ready as the host's cores waiting for work, and Demand as the host's load including the VMkernel. Or: "Demand is a provider metric, so it is not related to the VMs' demand."

## Expected key points
- Virtualization splits the stack into **provider** and **consumer**. A provider has 2 kinds of metrics: a true **provider metric** (it has no consumer equivalent) and a **sum-of-consumer metric** (the provider adds up what its consumers report).
- Both are sum-of-consumer's perspective metrics, held at ESXi. Neither is a provider perspective metric.
- Ready is a consumer concept: a VM waits to be scheduled. A physical core or thread is always ready, so a core itself has no Ready time. Host-level Ready is only the VMs' Ready added up.
- ESXi CPU Demand is the sum over the VMs of the demand they would have with no contention, an internal value of the CPU scheduler. It is not the sum of VM worlds plus VMkernel worlds: kernel work is in Usage, not in Demand (a host with no VMs shows Demand flat at 0 while Usage is not 0).
- The metric name does not say which kind it is. You must know the mechanism.
- Do not read a host figure as VMs plus kernel by default: Usage includes the kernel, Demand does not.

## Notes
- Tests: Principle: provider vs consumer perspective; provider metric vs sum-of-consumer metric.
- Key corrected 2026-11-12. It read ESXi CPU Demand as a provider metric. The knowledge base (host/demand, provider-consumer) and the author's answer to Q009 settle it: the value at ESXi is the summation over the VMs, a sum-of-consumer metric held at the provider. A candidate that said "sum of consumers" was scored 0 against the old key in all runs of 20261112 (see project/plan.md).

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
answer_type: judged
level: 300                      # author 2026-11-05
object: [esxi, vm]
tool: [none]
knowledge_main: vsphere/architecture/provider-consumer
misconception_type: [provider-vs-consumer]
status: reviewed
```
