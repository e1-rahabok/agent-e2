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
- Previous id: vsphere-foundations-003 (renamed 2026-11-05).
- Tests: Principle: provider vs consumer; provider metric vs sum-of-consumer metric.

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
status: draft
```
