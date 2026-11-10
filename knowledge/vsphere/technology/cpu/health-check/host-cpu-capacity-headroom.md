# Does this ESXi host have CPU headroom?

## Checks, in order
1. Contention first: VM Ready and Co-stop on the host's VMs, per vCPU.
2. Core Utilization (%).
3. Thread Utilization (%).
4. Usage (MHz), for performance.
5. Peak Core Usage and Imbalance.

## How to read the result
- Primary counters: Core Utilization and Thread Utilization. Complement with Usage (MHz) for performance.
- Core Utilization below 100% or Thread Utilization below 50%: physical cores are still free. New VMs can go on.
- Core Utilization at 100% (Thread Utilization at least 50%): watch Thread Utilization. Keep it around 80%-90% per host; cluster level is lower because of the HA host. Check contention.
- Drive by contention (Mark Achtemichuk).

## Example: busy host
- 40 cores, 80 threads. Demand about 130%. Usage flat at 100%.
- Core Utilization 85%: about 6 cores free, unless limits apply.
- Thread Utilization 62%: about 30 threads free.
- Host Ready peaked at 128 s with 250 vCPUs: 514 ms per vCPU, about 2.5%.
- Per VM over 7 hours: Ready about 2%, Co-stop below 0.1%. VMs average 15.29 vCPUs. Some had limits.
- Conclusion: no CPU performance problem despite Demand 130% and Usage 100%.

## Example: lightly loaded host
- Core Utilization 48%. Usage below Core Utilization: the kernel clocked cores down to save power.

## Traps
- "Demand 130% and Usage 100%, so the host is overloaded" → check Core Utilization, Thread Utilization and Ready.
- "Thread Utilization below 50% means half the capacity is free" → cores may already be busy.

## Metadata
```yaml
id: vsphere/technology/cpu/health-check/host-cpu-capacity-headroom
retriever_guide: health-check
scope: vsphere
technology:
- cpu
pillar:
- capacity
- performance
product:
- vsphere
- vcf-operations
object:
- HostSystem
internal_derive:
- vsphere/technology/cpu/metrics/comparisons/host-consumption-metrics
- vsphere/technology/cpu/concepts/hyper-threading
related:
- vsphere/technology/cpu/metrics/host/core-utilization
- vsphere/technology/cpu/metrics/host/utilization
- vsphere/technology/cpu/metrics/host/usage
- vsphere/technology/cpu/metrics/host/demand
- vsphere/technology/cpu/metrics/host/imbalance
- vsphere/technology/cpu/metrics/comparisons/host-contention-metrics
source:
  document: PART 3 - Counters.docx
  path: CPU > ESXi > Consumption Metrics > Summary > Recommendation; Real World Samples
corrections: []
review_notes:
- 'Section ''How to read the result'': the 80%-90% Thread Utilization level is field practice from the book, not a vendor threshold.'
status: draft
```
