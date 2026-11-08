# ESXi CPU Utilization

## Meaning
- Static-frequency CPU utilization, from the host vantage point.
- The VM equivalent is called Run. See `vsphere/technology/cpu/metrics/virtual-motherboard/run`.

## Why the names differ
- Different vantage points: provider (ESXi) and consumer (VM).

## Mechanism
- Utilization is measured per thread. Each thread has its own 100%.
- ESXi Utilization (%) = average of thread utilization.
- It is a static counter: it ignores frequency. So it suits capacity management.
- Ready and Wait do not apply at this level. A thread runs or is idle.
- See `vsphere/technology/cpu/concepts/cpu-measurement-levels`.

## The capacity reading
- Capacity is about space (quantity); performance is about speed (quality).
- Each thread can run a vCPU or a kernel world, so the thread is the unit of capacity.
- So with Hyper-Threading on, Thread Utilization is the ESXi utilization for capacity management: the share of threads in use.
- Core Utilization overstates used capacity: it counts a core as fully used when one of its two threads runs, while the other thread can still take work.
- Usage (%) is not a capacity reading either: it includes frequency (Turbo), which is speed.
- Example: Usage 100%, Core Utilization 70%, Thread Utilization 40%. For capacity the host is at 40%: about 60% of the threads are idle.

## Thread Utilization
- Read Utilization (%) as Thread Utilization (%).
- Binary per moment per thread. Averaged over the sample: 50% = running half the time.
- Ignores frequency and Hyper-Threading. Relevant only with Hyper-Threading on.
- Disregards that Hyper-Threading does not deliver 2x. Example: both threads of every core busy = 100%; one thread per core = 50%.
- Usually lower than Core Utilization. Without Hyper-Threading, equal to it.
- See `vsphere/technology/cpu/concepts/hyper-threading`.

## Traps
- "ESXi Utilization = sum of VM Run + kernel" → different vantage points. See `vsphere/technology/cpu/concepts/cpu-measurement-levels`.
- "Thread Utilization 50%, so half the host is free" → in space, yes: half the threads are free. In speed, no: every core may already run one thread, and a second thread shares the core (Hyper-Threading delivers about 1.25x per core, not 2x). Check Core Utilization for the speed effect.
- "Core Utilization is the ESXi utilization for capacity" → it counts a half-used core as full. Use Thread Utilization.

## Metadata
```yaml
id: vsphere/technology/cpu/metrics/host/utilization
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
- vsphere/architecture/provider-consumer
- vsphere/technology/cpu/concepts/cpu-measurement-levels
same_name: []
same_meaning:
- vsphere/technology/cpu/metrics/virtual-motherboard/run
related:
- vsphere/technology/cpu/metrics/host/core-utilization
- vsphere/technology/cpu/concepts/hyper-threading
- vsphere/technology/cpu/metrics/host/imbalance
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity; CPU > Architecture (pp. 52-78) > ESXi ≠ VM + Kernel; CPU > ESXi > Thread Utilization
corrections:
- 'Section ''The capacity reading'' and Traps: Thread Utilization is the ESXi utilization for capacity management (author answer Q040, 2026-11-05, and the quiz key of CPU Q1).'
review_notes:
- Sections Mechanism and Traps: from CPU > Architecture.
- 'Section Thread Utilization: from CPU > ESXi.'
status: draft
```
