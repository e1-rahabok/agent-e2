# Host-wide performance tuning (dense mode)

## Purpose
- Default: ESX supports high consolidation ratios and still gives good response times for every VM and request.
- Where very high consolidation ratios are required, dense mode optimizes an individual host.
- Performance Best Practices for vSphere 9.1 says dense mode allows consolidation up to about 10% higher than without it.
- Dense mode is also called host-wide performance tuning.
- The scenario it serves: at very high consolidation, keeping average response times low matters more than keeping all response times low.

## Trigger
- When dense mode is activated, ESX monitors:
  - the number of VMs,
  - the number of vCPUs,
  - total CPU utilization.
- The dense mode optimizations are implemented only when all three conditions are met:
  - numVMs ≥ numPCPUs,
  - numVCPUs ≥ 2 × numPCPUs,
  - CPUUtil ≥ 50%.
- Variable names are as written in Performance Best Practices for vSphere 9.1, which does not define numPCPUs. In vSphere's own term a PCPU is a physical hardware execution context: a thread with Hyper-Threading on, a core with it off (vSphere 9.1 documentation, esxtop CPU panel, p. 2153). numPCPUs is read as that count, the logical processors of the host.
- Activation alone does not implement the optimizations. The consolidation ratio and CPU utilization must reach the thresholds.

## Mechanism
- The optimizations batch network packets more aggressively at several points in the hypervisor.
- Effect: lower hypervisor overhead for packet processing. More CPU resources remain for VMs.
- Benefit: when CPU utilization is high, average response time depends strongly on spare CPU resources.

## Trade-offs
- Batching increases the latency of individual requests.
- At low CPU utilization, dense mode can reduce system-wide throughput.
- The same holds when some VMs consume a disproportionately large amount of network throughput.
- Dense mode still reduces CPU utilization per unit of throughput.
- Performance Best Practices for vSphere 9.1 recommends activating dense mode only on hosts where the trade-offs are useful, not on all hosts.

## Configuration
- Advanced setting: `/Net/NetTuneHostMode`.
- Default (deactivated): `/Net/NetTuneHostMode = "default"`.
- Activated: `/Net/NetTuneHostMode = "dense"`.
- Set with the vSphere Client or esxcli.

## Misconceptions
- "Dense mode is always beneficial" → batching raises the latency of individual requests, and at low CPU utilization it can lower system-wide throughput.
- "Setting dense mode activates the optimizations" → the optimizations run only when the host meets the thresholds.

## Metadata
```yaml
id: vsphere/technology/cpu/configuration/host-wide-dense-mode
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
- vsphere/architecture/overhead
- vsphere/technology/network/configuration/rss-and-interrupt-coalescing
source:
  document: Performance Best Practices for VMware vSphere 9.1 (revision 20260624); VMware vSphere 9.1 product documentation (PDF built 2026-11-02; the copyright page carries no revision number)
  path: Host-Wide Performance Tuning (p. 54); vSphere 9.1, vSphere Monitoring and Performance > resxtop and esxtop > CPU Panel, PCPU (p. 2153)
corrections: []
review_notes: []
status: draft
```
