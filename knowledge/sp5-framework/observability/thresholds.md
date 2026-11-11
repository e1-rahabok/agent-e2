# Thresholds and interpretation

## Definition
- What counts as a good value depends on context. There is no universal threshold.
- Tolerance varies by:
  - application,
  - use case of the same application,
  - end user, even for the same use case.

## Consequence
- Out-of-the-box universal thresholds are unreliable.
- Threshold too low → frequent red, without actual complaints.
- Threshold too high → actual problems missed.

## Layer rule
- A threshold given at one layer of the stack does not apply unchanged at a lower layer.
- Each layer above adds processing latency and queueing.
- So the threshold must be lower at each lower layer.
```text
threshold(VM layer) < threshold(Guest OS layer) < threshold(application layer)
```

## Time window rule
- "Consistently above X" must be translated into a time window.
- IO is measured per second. A 5-minute window = 300 samples.
- Observed: a 5-minute window on disk latency produces many alerts but few user complaints.

## Interval rule
- A threshold is valid only for the sample interval it was set on. The same workload reads higher at a short interval than at a long one: averaging over a longer window flattens peaks.
- Order for the same metric: 2-second (esxtop) ≥ 20-second (real-time) ≥ 5-minute ≥ 1-day values.
- Example: VM disk latency 10,370 ms at the 20-second peak vs 257 ms as the 300-second average. See `vcf-operations/features/peak-20-second-metrics`.
- So a threshold set on 20-second peaks must be higher than one set on 5-minute averages for the same tolerance. Example: VM Compressed + Swapped (5-minute samples) has a lower band than VM Memory Contention (20-second peaks), although it is the less serious signal. See `vsphere/object-types/vm/kpis/vm-performance`.
- A threshold without its interval is incomplete.

## Instance rule
- A metric with an instance breakdown (per vCPU, per virtual disk, per vNIC) has two readings: the object value (average or sum over instances) and the worst instance.
- The worst instance is always at least the average. Example: a 64-vCPU VM can show a low VM-level Readiness (%), which is normalized over its vCPUs, while one vCPU is far higher; the normalization dilutes that vCPU by 64.
- So a threshold must say which reading it applies to: "Peak CPU Ready among any vCPU" is not the same threshold as "VM CPU Ready".
- The same rule applies one level up: a cluster threshold must say whether it applies to the worst VM (depth), a percentile of VMs (breadth), or the average. See `vsphere/object-types/cluster/kpis/cluster-performance`.

## Threshold definition
```text
threshold = (metric, object, instance reading, sample interval, time window) -> band values and source
```
- Instance reading: object aggregate, worst instance, or percentile of instances.
- Sample interval: 2 s (esxtop), 20 s, 5 min, 1 day.
- Time window: how long the value must stay in the band ("consistently"), see Time window rule.

## Worked example: SQL Server disk latency
- Microsoft guidance for SQL Server: disk latency should consistently stay within 10–15 ms.
- That value is at the SQL Server layer.
- At the Windows layer the value must be lower.
- At the vSphere VM layer the value must be lower still.
- Read and write latency may require different thresholds.
- Reference: https://learn.microsoft.com/en-us/troubleshoot/sql/database-engine/performance/troubleshoot-sql-io-performance

## Misconceptions
- "The band from the 20-second chart applies to the 1-week chart" → the interval differs; longer intervals read lower.
- "VM CPU Ready is low, so no vCPU waits" → the VM value averages the vCPUs; check the worst vCPU.
- Using an application-layer threshold (e.g. 15 ms) directly as a VM-layer alert → too high.
- Treating "consistently" as a 5-minute average → many alerts, few complaints.

## Metadata
```yaml
id: sp5-framework/observability/thresholds
retriever_guide: how-it-works
scope: sp5-framework
technology:
- cpu
- memory
- storage
- network
pillar:
- performance
product:
- vsphere
- vcf-operations
internal_derive: []
related:
- sp5-framework/observability/metrics-as-accounting
- vsphere/architecture/vm-vs-guest-os
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: The World of Metrics > Metrics Nuances > Complexity > Interpretation Challenge
corrections: []
review_notes: []
status: draft
```
