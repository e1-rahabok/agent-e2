# VM CPU Run

## Meaning
- Static-frequency CPU utilization, from the VM vantage point.
- The ESXi equivalent is called Utilization. See `vsphere/cpu/metrics/host/utilization`.
- Source: ESXi provides Run in ms.

## Reservation
- CPU reservation is on demand. It is not included in Run.

## Mechanism
- Run measures how long the vCPU runs. Unit: ms, not GHz.
- Run is binary: it counts whether the vCPU runs, not how much work it completes.
- Run does not see CPU frequency or Hyper-Threading.
- Run is one of 4 states: Run + Ready + Co-stop + Wait = 100%, per vCPU.
- vCenter: 20,000 ms = 100% per vCPU. The VM value in ms is the sum over its vCPUs.
- Use Run for capacity (Run Time). Use throughput in MHz for performance (Run Quality).
- See `vsphere/cpu/concepts/vcpu-states` and `vsphere/cpu/concepts/run-time-vs-run-quality`.

## Run vs Guest OS
- The Guest OS counts time as running when its vCPU is in Ready or Co-stop. VM Run excludes that time.
- Guest OS IO processing shows as VM Run.

## Run vs Used
- Two VMs share one core, each runs half the time, half of it overlapping: Run 50%, Used 40.625%.
- Both threads busy all the time: Run 100%, Used 62.5%.

## Traps
- "Run 100% means full performance" → Run is time. Throughput depends on frequency and Hyper-Threading.
- "Compare Run (ms) across VMs" → ms scales with vCPU count. Use %.

## Metadata
```yaml
id: vsphere/cpu/metrics/virtual-machine/run
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
- VirtualMachine
metric_class: consumption
internal_derive:
- vsphere/foundations/provider-consumer
- vsphere/cpu/concepts/vcpu-states
- vsphere/cpu/concepts/run-time-vs-run-quality
same_name: []
same_meaning:
- vsphere/cpu/metrics/host/utilization
related:
- vsphere/cpu/metrics/comparisons/consumption-metrics
- vsphere/cpu/concepts/cpu-efficiency
- vsphere/cpu/concepts/guest-os-vs-vm-cpu
- vsphere/cpu/concepts/frequency-and-ht-impact-on-vm
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity; CPU > Architecture (pp. 52-78) > State of a VM vCPU; 2 Metrics Not 1; CPU Efficiency
corrections: []
review_notes:
- Sections Mechanism, Run vs Guest OS, Run vs Used, and the last 2 traps: from CPU > Architecture.
status: draft
```
