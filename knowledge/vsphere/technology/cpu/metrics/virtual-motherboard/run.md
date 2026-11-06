# VM CPU Run

## Meaning
- Static-frequency CPU utilization, from the VM vantage point.
- The ESXi equivalent is called Utilization. See `vsphere/technology/cpu/metrics/host/utilization`.
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
- See `vsphere/technology/cpu/concepts/vcpu-states` and `vsphere/technology/cpu/concepts/run-time-vs-run-quality`.

## Run vs Guest OS
- The Guest OS counts time as running when its vCPU is in Ready or Co-stop. VM Run excludes that time.
- Guest OS IO processing shows as VM Run.

## Run vs Used
- Two VMs share one core, each runs half the time, half of it overlapping: Run 50%, Used 40.625%.
- Both threads busy all the time: Run 100%, Used 62.5%.

## Not included in Run
- Interrupts (Overlap).
- System time: IO done by the hypervisor and charged back to the VM.
- Power management and frequency scaling.
- Simultaneous multithreading (Hyper-Threading).
- Run is the only consumption counter not affected by frequency scaling and Hyper-Threading.

## Instance
```text
Run (VM) = sum of Run (vCPU)
```
- In vCenter, VM-level Run can exceed 20,000 ms.

## Use
- Input for Guest OS sizing. Remove Overlap first: Net Run = Run - Overlap.
- Run higher than Used: the gap comes from power management, Hyper-Threading or both. Run cannot tell which.

## Traps
- "Run 100% means full performance" → Run is time. Throughput depends on frequency and Hyper-Threading.
- "Compare Run (ms) across VMs" → ms scales with vCPU count. Use %.
- "Run includes the hypervisor IO done for the VM" → System is not in Run.

## Metadata
```yaml
id: vsphere/technology/cpu/metrics/virtual-motherboard/run
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
layer:
- virtual-motherboard
metric_class: consumption
internal_derive:
- vsphere/foundations/provider-consumer
- vsphere/technology/cpu/concepts/vcpu-states
- vsphere/technology/cpu/concepts/run-time-vs-run-quality
same_name: []
same_meaning:
- vsphere/technology/cpu/metrics/host/utilization
related:
- vsphere/technology/cpu/metrics/comparisons/consumption-metrics
- vsphere/technology/cpu/concepts/hyper-threading
- vsphere/technology/cpu/concepts/guest-os-vs-vm-cpu
- vsphere/technology/cpu/concepts/cpu-frequency
- vcf-operations/metrics/vm/cpu-net-run
- vsphere/technology/cpu/metrics/virtual-motherboard/overlap
- vsphere/technology/cpu/diagnosis/run-vs-used-gap
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity; CPU > Architecture (pp. 52-78) > State of a VM vCPU; 2 Metrics Not 1; CPU Efficiency; CPU > VM (pp. 78-118) > Consumption Metrics > Run | Net Run
corrections: []
review_notes:
- Sections Mechanism, Run vs Guest OS, Run vs Used, and the last 2 traps: from CPU > Architecture.
- 'Sections Not included in Run, Instance, Use: from CPU > VM.'
- "Section 'Use': author (2026-11-03), Q003: Run is for Guest OS sizing. Book updated."
status: draft
```
