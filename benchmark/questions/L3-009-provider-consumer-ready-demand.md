# Provider vs consumer metrics

## Prompt
- esx-12 runs 41 VMs, with vSAN and NSX.
- In the vSphere Client, its real-time performance chart shows CPU Ready at about 148,000 ms per 20-second sample, and CPU Demand above CPU Usage.

Which statements are correct?

- A. Host CPU Ready is the Ready time of the host's VMs, added up at the host.
- B. Host CPU Ready measures the host's physical cores waiting for work to arrive.
- C. Host CPU Usage, like host CPU Ready, is a sum over the host's VMs.
- D. Host CPU Demand is the sum over the VMs of the CPU they would use with no contention.
- E. Host CPU Demand adds the VMkernel's actual CPU use to the demand of the VMs.
- F. A high host CPU Ready is first checked in the host's BIOS and power policy.
- G. Host CPU Usage includes kernel work such as vSAN and NSX.
- H. The name of a host counter tells whether it measures the host itself or adds up its VMs.
- I. Throughput of the host's physical NICs (vmnics) has no VM equivalent.
- J. Host CPU Demand can be read for each physical core or thread of the host.

## Likely wrong answer
- B: "Host Ready is the host's own cores waiting."
- E: "Host Demand is the host's whole load, VMs plus the VMkernel."
- C: "Host Usage adds up its VMs, like host Ready" (the over-correction).

## Expected key points
- Answer: A, D, G, I.
- A is correct: Ready is a consumer concept (a VM waiting to be scheduled); the host value adds up its VMs.
- B is wrong: a physical core or thread is always ready; Ready does not apply to ESXi itself.
- C is wrong: host Usage is summed over the physical cores and threads, not over the VMs (it also holds kernel work); only some host counters add up the VMs.
- D is correct: in vCenter, ESXi CPU Demand is the sum over the VMs, an internal value of the CPU scheduler: the demand had there been no contention.
- E is wrong: Demand is not the sum of VM worlds plus VMkernel worlds; kernel work is in Usage.
- F is wrong: host Ready is the VMs' wait, not a property of the host's cores; read the VMs, starting with the worst, and their limits, shares and size.
- G is correct: Usage counts actual use by the VMs and the kernel, vSAN and NSX included.
- H is wrong: the name does not say which kind a counter is; you must know the mechanism.
- I is correct: physical network in ESXi exists only at the host; the sum of VM network at ESXi is the counter that adds up the VMs.
- J is wrong: Demand is summed over the VMs, not over physical threads, so it has no per-core or per-thread value.

## Notes
- Tests: principle, provider vs consumer perspective; a host metric of its own vs a sum of the VMs' metric.
- For reviewers (kept out of the prompt): "A provider metric is about the ESXi host itself; a consumer-based metric is aggregated from the metrics of the VMs the host runs."
- The stem names the vSphere Client host chart: vCenter Demand, without reservations (host/demand, vCenter vs VCF Operations).
- Changed in the 2026-11-15 audit: a line of evidence in the stem (host, VMs, Ready in ms, Demand above Usage); C reworded from "Every host CPU counter" to host Usage (still false); F without "before looking at any VM" (still false, the wrong action).
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
