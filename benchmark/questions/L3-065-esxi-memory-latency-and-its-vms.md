# ESXi memory Latency and the VMs behind it

## Prompt
- An ESXi 9.1 host runs 40 VMs.
- In vCenter, the host's memory Latency (%) stays low all day, while users of one application on this host report slowness.

Which statements about host memory Latency are correct?

- A. Host memory Latency averages the memory Latency values of the VMs running on the host.
- B. A low host memory Latency shows that no VM on the host waited for memory.
- C. Host memory Latency rises above 0 only when every VM on the host waits.
- D. The VM that waits is found from the highest VM memory Latency among the host's VMs.
- E. Close the users' ticket: the host's low value rules out a memory wait on any VM.
- F. Host memory Latency is the sum of the memory Latency values of its running VMs.
- G. Memory Latency is the percentage of time a vCPU spends waiting on page faults, not a duration.

## Likely wrong answer
B: "Host memory latency is low, so no VM waits for memory."

## Expected key points
- Answer: A, D, G.
- A true: host memory Latency is a normalized average of the running VMs' memory Latency.
- B false: an average hides the VM that suffers; one VM can wait while the host value stays low.
- C false: over-correction. Any VM's wait adds to the average; it is small when one VM waits among many, not 0.
- D true: read the worst VM, the maximum VM Memory Contention across the host's VMs, not the host value.
- E false: the wrong action from B; check the VMs of that application first.
- F false: the host value is an average, not a sum: it stays a percentage of time on the same scale as one VM's.
- G true: the counter is the share of time a vCPU waits for a page fault ESXi resolves (swap-in, decompression), not latency in ns.

## Notes
- Paired with 0403 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item D13.
- The knowledge base does not say how the host value weights its VMs, so no option computes it.
- Written 2026-11-14 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after approval (design.md, section 6.2).

## Metadata
```yaml
id: "0402"
title: "ESXi memory Latency and the VMs behind it"
product: [vsphere, vcf-operations]
technology: [memory]
task: explain-mechanism
level: 300
answer_type: deterministic
input: [text]
object: [esxi, vm]
tool: [vcenter, vcf-operations]
knowledge:
  - vsphere/technology/memory/metrics/host/latency
  - vsphere/technology/memory/metrics/virtual-motherboard/latency
  - vsphere/technology/memory/metrics/comparisons/host-memory-metrics
  - sp5-framework/observability/aggregation
knowledge_main: vsphere/technology/memory/metrics/host/latency
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D13"
answer: [A, D, G]
misconception: [B]
misconception_type: [average-hides-worst]
pair: "0403"
status: draft
```
