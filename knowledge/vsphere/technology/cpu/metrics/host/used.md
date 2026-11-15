# ESXi CPU Used

## Meaning by source
- ESXi (esxtop) shows Used in %.
- vCenter shows Used in ms.
- The % form is affected by CPU frequency and can exceed 100%.
- Relevance for operations: performance troubleshooting only, as the frequency-scaled time of each thread. Not for capacity, because Turbo and power saving move it: read Thread Utilization. Not for reconciling with VM CPU Used, because the two counters charge a busy Hyper-Threading core by different rules (section Mechanism).

## Reason
- ESXi is the metric source. vCenter converts or adds metrics, and formulas do not match in every case. See [`vsphere/architecture/metric-sources`](../../../../architecture/metric-sources.md).

## Notes
- CPU Used is a complex metric. Do not build conclusions on it alone.

## Mechanism
- Calculated from Non-Halted Core Cycles (NHCC), a hardware counter. Higher clock speed, more cycles: Used rises with Turbo.
- Per thread: when both threads of a core run, Used charges 10,000 ms to each, not 20,000 ms. Normalized back at host level.
- A thread running alone can reach 20,000 ms.
- VM CPU Used charges each vCPU on a busy core 62.5% of the core, while ESXi CPU Used gives each thread 50%: on a busy Hyper-Threading host the VM CPU Used of all VMs plus the kernel exceeds ESXi CPU Used ([`vsphere/technology/cpu/concepts/hyper-threading`](../../concepts/hyper-threading.md), section Hyper-Threading accounting: VM CPU Used and ESXi CPU Used).

## Misconceptions
- "Used above 100% is a data error" → the % form includes frequency effects and can exceed 100%.
- "The VM CPU Used of all VMs plus the kernel should equal ESXi CPU Used" → on a core with both threads busy, VM CPU Used carries the 1.25x Hyper-Threading charge (62.5% per vCPU) and ESXi CPU Used splits the core in half, so the VM sum is higher.

## Metadata
```yaml
id: vsphere/technology/cpu/metrics/host/used
retriever_guide: metric-meaning
scope: vsphere
technology:
- cpu
pillar:
- performance
- capacity
product:
- vsphere
object:
- HostSystem
metric_class: consumption
internal_derive:
- vsphere/architecture/metric-sources
same_name:
- vsphere/technology/cpu/metrics/virtual-motherboard/used
same_meaning: []
related:
- vsphere/technology/cpu/metrics/comparisons/consumption-metrics
- vsphere/technology/cpu/concepts/hyper-threading
- vsphere/technology/cpu/metrics/host/usage
source:
  document: Knowledge base; VMware vSphere 9.1 product documentation (PDF built 2026-11-02; the copyright page carries no revision number)
  path: The World of Metrics > Metrics Nuances > Complexity > Architecture Complexity; CPU > ESXi > Used | Usage; Core vs Thread; vSphere Monitoring and Performance > resxtop and esxtop > CPU Panel, PCPU USED(%) (p. 2153)
corrections: []
review_notes: []
status: draft
```
