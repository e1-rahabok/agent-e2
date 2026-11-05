# Provider vs consumer metrics

## Prompt
- An ESXi host dashboard shows "CPU Ready" and "CPU Demand".

For each, is it a provider metric or a sum of the VMs' metrics? Can a physical core itself have Ready time?

## Likely wrong answer
"Both are the host's own values" — or "Demand comes from the VMs, so ESXi Demand is the sum of VM Demand".

## Expected key points
- Virtualization splits the stack into **provider** and **consumer**.
- Provider has 2 kinds of metrics: true **provider metrics** (don't exist on the consumer) and **sum of consumer** metrics.
- Ready is a consumer concept. A physical core/thread is always ready. Host-level Ready can only be an aggregate of its VMs.
- ESXi CPU Demand is a **provider metric**. It is not the sum of VM + VMkernel worlds. It is the CPU scheduler's internal value for the ideal total demand had there been no contention.
- The metric name does not say which kind it is. You must know the mechanism.
- ESXi ≠ sum of VMs + kernel. Host metrics are more complex than a sum.

## Notes
- Tests: Principle: provider vs consumer; provider metric vs sum-of-consumer metric.

## Metadata
```yaml
id: vsphere-foundations-003
title: "Provider vs consumer metrics"
scope: vsphere
product: [vsphere]
technology: [system]
area: foundations
input: text
tests: concept
knowledge:
  - vsphere/foundations/provider-consumer
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
  - vsphere/technology/cpu/metrics/host/demand
attachments: []
origin: book
source_path: "The World of Metrics > Metrics Nuances: Virtualization Impact; Architecture Complexity (VM vs ESXi; ESXi ≠ VMs + Kernel)."
format: free-text
status: draft
```
