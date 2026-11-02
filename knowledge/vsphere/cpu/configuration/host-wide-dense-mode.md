---
id: vsphere/cpu/configuration/host-wide-dense-mode
retriever_guide: what-to-set
scope: vsphere
technology:
- cpu
- network
pillar:
- capacity
- performance
product:
- vsphere
object:
- HostSystem
internal_derive: []
related:
- vsphere/cpu/concepts/virtualization-overhead
- vsphere/network/configuration/rss-and-interrupt-coalescing
source:
  document: Performance Best Practices for VMware vSphere 9.1 (revision 20260624)
  path: Host-Wide Performance Tuning (p. 54)
corrections: []
review_notes:
- Checked against 9.1 (revision 20260624). Page 54 unchanged. Page reference updated.
- 'Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-9-1-performance-best-practices'
- The source gives the dense mode thresholds in one line. The exact comparison of CPU utilization (50%) is as written in the source.
status: draft
---

# Host-wide performance tuning (dense mode)

## Purpose
- Default: ESX supports high consolidation ratios and still gives good response times for every VM and request.
- Where very high consolidation ratios are needed, dense mode optimizes an individual host.
- The source says dense mode allows consolidation up to about 10% higher than without it.
- Dense mode is also called host-wide performance tuning.
- Source priority for very high consolidation: keeping average response times low matters more than keeping all response times low.

## Trigger
- When dense mode is activated, ESX monitors:
  - the number of VMs,
  - the number of vCPUs,
  - total CPU utilization.
- The dense mode optimizations are implemented only when all three conditions are met:
  - numVMs ≥ numPCPUs,
  - numVCPUs ≥ 2 × numPCPUs,
  - CPUUtil ≥ 50%.
- Variable names are as written in the source. The source does not define numPCPUs. It is read here as the number of physical CPUs on the host.
- The source notes that activation alone does not implement the optimizations. The consolidation ratio and CPU utilization must reach the thresholds.

## Mechanism
- The optimizations batch network packets more aggressively at several points in the hypervisor.
- Effect: lower hypervisor overhead for packet processing. More CPU resources remain for VMs.
- Benefit: when CPU utilization is high, average response time depends strongly on spare CPU resources.

## Trade-offs
- Batching increases the latency of individual requests.
- At low CPU utilization, dense mode can reduce system-wide throughput.
- The same holds when some VMs consume a disproportionately large amount of network throughput.
- Dense mode still reduces CPU utilization per unit of throughput.
- The source recommends activating dense mode only on hosts where the trade-offs are useful, not on all hosts.

## Configuration
- Advanced setting: `/Net/NetTuneHostMode`.
- Default (deactivated): `/Net/NetTuneHostMode = "default"`.
- Activated: `/Net/NetTuneHostMode = "dense"`.
- Set with the vSphere Client or esxcli.

## Traps
- "Dense mode is always beneficial" → the source warns about higher individual latency, and lower system-wide throughput at low CPU utilization.
- "Setting dense mode activates the optimizations" → the optimizations run only when the host meets the thresholds.
