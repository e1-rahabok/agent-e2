# Metrics as accounting

## Definition
- A metric is an accounting of a system in operation.
- A counter records what the system did, using the system's own accounting rules.

## Consequences for metrics
- Interpreting a counter correctly requires knowing how the whole system works.
- Without the mechanism, interpretation falls back to memorising definitions. Memorised definitions fail on cases not covered by the definition.
- A threshold can only be judged once it is known how the value is calculated.
- To explain a counter value, explain the mechanism that produced it first.

## Accounting rules in vSphere counters
- VM CPU Used is a charge, not a time: the scheduler lowers it while the sibling Hyper-Threading thread runs, scales it by frequency, and adds the VMkernel work done for the VM (System) at VM level only. So VM CPU Used and VM CPU Run differ for the same vCPU ([`vsphere/technology/cpu/metrics/virtual-motherboard/used`](../../vsphere/technology/cpu/metrics/virtual-motherboard/used.md)).
- VM CPU Ready in milliseconds is a summation counter: each 20-second sample adds up the ms of every vCPU, so the same wait reads larger on a VM with more vCPUs and on a vCenter chart with a longer interval ([`sp5-framework/observability/collection-interval`](collection-interval.md), section Base of a millisecond value).
- ESXi Swap In and Swap Out are running totals to date; Swap Consumed is what sits in swap now. A running total and a current amount do not subtract into each other ([`vsphere/technology/memory/metrics/host/swap-used`](../../vsphere/technology/memory/metrics/host/swap-used.md)).
- VCF Operations counts storage, network and memory in 1024 and labels the values KB, MB, GB ([`sp5-framework/observability/units`](units.md)).

## Metadata
```yaml
id: sp5-framework/observability/metrics-as-accounting
retriever_guide: how-it-works
scope: sp5-framework
technology:
- cpu
- memory
- storage
- network
pillar:
- performance
- capacity
product:
- vsphere
- vcf-operations
internal_derive:
- vsphere/technology/cpu/metrics/virtual-motherboard/used
- sp5-framework/observability/collection-interval
- vsphere/technology/memory/metrics/host/swap-used
- sp5-framework/observability/units
related:
- sp5-framework/observability/naming-patterns
- sp5-framework/observability/thresholds
source:
  document: Knowledge base
  path: The World of Metrics > Metrics Nuances
corrections: []
review_notes: []
status: draft
```
