# VM Memory Balloon Target

## Meaning
- Memory the hypervisor wants the balloon driver to reclaim from this VM.
- Non-zero: the hypervisor has asked the VM to give back memory.
- Balloon Target above Ballooned: the VMkernel inflates the balloon and reclaims more. Balloon Target below Ballooned: the VMkernel deflates it, and the VM can reallocate memory when needed (vSphere 9.1 documentation, p. 2104).
- The VM initiates the reallocation, so Balloon Target can be 0 while Ballooned is still above 0 (vSphere 9.1 documentation, p. 2073).
- Two causes of a non-zero target: host memory pressure, and a VM above its limit (the target covers the excess; see [`vsphere/technology/memory/concepts/memory-limit`](../../concepts/memory-limit.md)). The driver stops at its ceiling, 65% of configured memory by default; a target above it leaves the rest to compression and swap.
- Step-by-step mechanism of inflate and deflate: [`vsphere/technology/memory/concepts/ballooning`](../../concepts/ballooning.md), section Inflate and deflate, step by step.
- Relevance for operations: performance troubleshooting: a non-zero target says ESXi is reclaiming from this VM now, by host pressure or a limit. Read it with Ballooned. Not for capacity.

## Misconceptions
- "Balloon Target 0, so Ballooned must be 0" → the VM initiates the reallocation, so Ballooned can lag a target that fell to 0.
- "A Balloon Target above 0 on a host with free memory is a data error" → a limit sets the target to the excess above the limit, on a host with free memory too.

## Metadata
```yaml
id: vsphere/technology/memory/metrics/virtual-motherboard/balloon-target
retriever_guide: metric-meaning
scope: vsphere
technology:
- memory
pillar:
- performance
- capacity
product:
- vsphere
object:
- VirtualMachine
layer:
- virtual-motherboard
metric_class: context
internal_derive:
- vsphere/technology/memory/concepts/ballooning
same_name: []
same_meaning: []
related:
- vsphere/technology/memory/metrics/virtual-motherboard/ballooned
source:
  document: Knowledge base; vSphere 9.1 documentation (PDF built 2026-11-02)
  path: Memory > VM > Contention Metrics > Balloon; Monitoring and Performance, Hosts, Memory (MB), Balloon Target (p. 2073); Virtual Machines, Memory (MB), Balloon Target (p. 2104)
corrections: []
review_notes: []
status: draft
```
