---
id: vsphere/cpu/distinctions
type: distinction
scope: vsphere
resources: [cpu]
objects: [vcpu, vm, esxi, guest-os]
related:
  - foundations/naming-patterns
  - vsphere/foundations/provider-consumer
  - vsphere/foundations/metric-sources
  - vsphere/foundations/kernel-worlds
  - vsphere/foundations/resource-management
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity
corrections:
  - "2026-11-02: CPU Usage (%) VM vs ESXi block rewritten from author. Uploaded document sentence is truncated."
  - "2026-11-02: ESXi CPU Usage is artificially capped at 100%: accounting decision error, documented in an official VMware KB. Uploaded document describes it as normal behaviour."
  - "2026-11-02: Removed: 'VM Used HT penalty 37.5% vs ESXi Used HT penalty 50%'. Author: CPU Used metric is buggy."
review_notes:
  - "KB article number for the ESXi CPU Usage 100% cap not yet provided."
status: draft
---

# CPU distinctions

Language rule: a vCPU is a thread in the ESXi CPU scheduler. It demands runtime. The kernel decides how much runtime it gets.

## CPU Used: vCPU level vs VM level
- pattern: same-name-same-object-different-formula
- vCPU level: excludes System time.
- VM level: includes System time.
- why: System time is charged at VM level. It does not exist at vCPU level.
- src: Naming Complexity

## CPU Usage (%): VM vs ESXi (Hyper-Threading) [author-correction 2026-11-02]
- pattern: same-name-different-meaning
- Scenario: two vCPUs run on the two threads of the same physical core at the same time.
- VM: VM Usage is HT-aware. When both threads run, the VM is charged a 37.5% penalty, so it shows ~62.5%.
- ESXi: sees the core as fully busy (100%).
- why: ESXi can see both the core and its 2 threads. A VM cannot.
- ESXi values for that core:

| ESXi metric (core level) | Value |
|---|---|
| Usage (%) | 100% |
| Usage (MHz) | Reflects the Hyper-Threading benefit |
| Core Utilization | 100% |
| Thread Utilization | 100% |

- trap: "VM shows 62.5%, so the metric is wrong" → wrong. Different vantage point.
- src: Naming Complexity

## CPU Usage cap: VM vs ESXi [author-correction 2026-11-02]
- pattern: same-name-different-behaviour
- VM: CPU Usage (MHz) is not capped.
- ESXi: CPU Usage is artificially capped at 100%. Usage (MHz) does not exceed total capacity.
- why: accounting decision error in ESXi. Known issue, documented in an official VMware KB.
- trap: "ESXi CPU Usage = 100% means maximum possible work" → the value is capped, not measured beyond 100%.
- src: Naming Complexity

## CPU Latency vs Disk Latency and Memory Latency
- pattern: same-name-different-meaning
- Disk Latency and Memory Latency: indicate a performance problem. They are the primary counters for how well the VM is served by the underlying infrastructure.
- CPU Latency: does not always indicate a performance problem.
- why: CPU Latency is affected by CPU frequency, which goes up or down. At lower frequency the VM runs slower but is not waiting to be served. Equivalent to running on an older CPU.
- trap: "CPU Latency rose, so the VM has CPU contention" → check whether CPU frequency changed. Waiting shows in unmet-demand metrics (Ready, Co-Stop; see `vsphere/foundations/visibility-layers` area D).
- src: Naming Complexity

## Linux Steal Time vs VM CPU Latency
- pattern: same-name-same-purpose-different-formula
- Linux Steal Time: includes only CPU Ready.
- VM CPU Latency ("stolen time" from the VM view): includes many factors, including CPU frequency.
- trap: expecting Steal Time inside Linux to equal VM CPU Latency.
- src: Naming Complexity

## CPU Wait (VM)
- pattern: confusing-name
- VM CPU Wait includes idle time.
- Most VMs do not run at 100%, so CPU Wait is naturally high.
- why the name is still correct: from the kernel scheduler's vantage point, an idle vCPU is waiting to be used.
- trap: "High CPU Wait means the VM waits for disk or memory" → wrong. Mostly idle time.
- src: Naming Complexity

## Run (VM) vs Utilization (ESXi)
- pattern: same-purpose-different-name
- Both measure static-frequency CPU utilization.
- VM calls it Run. ESXi calls it Utilization.
- why: different vantage points.
- src: Naming Complexity

## Logical Processor (vCenter) vs Physical CPU (esxtop)
- pattern: same-purpose-different-name
- vSphere Client label "Logical Processor" = esxtop label "Physical CPU".
- Clearer pairing: virtual vs physical.
- src: Naming Complexity

## Consumed (%) vs Usage (%) for ESXi CPU in vCenter
- pattern: same-purpose-different-name
- vCenter uses both names for the same ESXi CPU utilization.
- src: Naming Complexity

## ESXi Core Utilization vs Thread Utilization
- pattern: confusing-name
- Core Utilization reports 100% when 1 thread of the core runs.
- Core Utilization also reports 100% when both threads run.
- To tell which case applies, check Thread Utilization.
- src: Other Nuances

## ESXi CPU Idle (ms)
- pattern: confusing-name
- Includes low activities, not only true idle.
- Considers CPU frequency, not simply whether the CPU is running.
- src: Other Nuances

## CPU Ready above 100%
- VM CPU Ready can exceed 100%.
- Many VM-level values in esxtop exceed 100%.
- why: summation, not average.
- src: Other Nuances

## Rollup: 20,000 ms vs 10,000 ms
- vCenter real-time interval is 20,000 ms.
- With Hyper-Threading enabled, the maximum value for a completely idle thread is 10,000 ms.
- why: 20,000 ms is set at core level. A core has 2 threads, each allocated 10,000 ms.
- src: Other Nuances

## Ready: VM vs ESXi
- Ready applies to a VM (consumer). It does not apply to ESXi: a physical core or thread is always ready.
- See `vsphere/foundations/provider-consumer`.

## Demand: ESXi [author-correction 2026-11-02]
- ESXi CPU Demand is a provider metric, not the sum of VM + VMkernel worlds.
- See `vsphere/foundations/provider-consumer`.

## Consumption metric choices
- VM CPU has 5 "consumption" metrics: Run, Used, Usage, Usage (MHz), Demand.
- ESXi CPU has 7 "consumption" metrics: Core Utilization, Utilization, Used, Usage, Usage (MHz), Consumed, Demand.
- src: Other Nuances

## Source: ESXi vs vCenter
- ESXi provides Run (ms), Used (ms), Demand (MHz). vCenter adds Usage (MHz) and Usage (%).
- ESXi Used (%) vs vCenter Used (ms): the % form is affected by frequency and can exceed 100%.
- See `vsphere/foundations/metric-sources`.

## Reservation and limit effects on CPU metrics
- CPU reservation is on demand. It is not included in Run, Used, Demand or Usage.
- CPU limit impacts CPU Ready.
- See `vsphere/foundations/resource-management`.

## GHz across hardware
- 1 GHz is not comparable across CPU generations, architectures, or model variants.
- See `foundations/resource-nature`.
