# Triple See Method

## Purpose

- Thousands of metrics across a VCF private cloud are mastered by seeing what they have in common: every metric is one of three types.
- The Triple See Method: see contention, consumption and context, and verify them as one set before concluding.
- Designed for Broadcom VCF. Purpose-built.
- The three types are peers, each with its own purpose, and each maps to pillars of The SP5 Framework ([`sp5-framework/concepts/overview`](../concepts/overview.md)).

## Three types of metric


| Type | Measures | Primary pillar |
|---|---|---|
| Contention | Something bad | Performance; availability for errors and drops |
| Consumption | Something good, if the load is useful | Capacity, value, sustainability |
| Context | An account of inventory or configuration | Configuration, compliance, inventory |

- The knowledge base tags each metric file with its type: `metric_class: contention | consumption | context`.

### Contention

- Performance impact: contention, latency, queue. The system is up and nothing is dropped, but throughput falls.
- Availability impact: errors and drops. Most systems recover from soft errors by retrying (retransmit the packet, resend the SCSI command, rebuild the cache line). The retry is rarely observable, even in logs.

### Consumption

- High is good for the business when the load is useful (not a DDoS attack). Check that both the pattern and the value match expectation.
- Three kinds, each used by capacity:
  - utilization: actual use. No industry naming standard: IOPS, throughput, active, usage, workload. Main input to Capacity Remaining, Time Remaining and Recommended Size;
  - allocation: used when utilization is too low to be useful;
  - reservation: prevents contention, like a booked table. It can be above or below utilization at different times.

### Context

- Answers the "it depends" questions by accounting for inventory or configuration.
- Useful only to a reader who can derive insight from it. Example: the number of vMotions is high or normal only against expectation; a cluster live migration after office hours should reach the theoretical limit.

## Priority of contention

- Contention is what users feel. Consumption gets the attention because it is easier to monitor and explain.
- Many systems do not scale linearly. In a parallel database, adding nodes can lower total throughput: nodes spend more time keeping integrity, so CPU utilization rises on overhead work. Measure the overhead and the throughput, not CPU utilization.
- Utilization is not a pillar and is not managed for its own sake. It is monitored for a reason; alone it has no meaning.

## Primary and secondary metrics


| Aspect | Primary | Secondary |
|---|---|---|
| Answers | What: defines the situation | Why: possible causes of the primary value |
| Count | Usually one per use case | Many per primary metric |
| Colour | Can be colour-coded | Some can; context metrics cannot |
| Unit | Usually %, 0 bad, 100 good | Varies: GB, MHz, packets/s, ms |
| Used in | Monitoring | Troubleshooting |

- Layer the troubleshooting metrics, events and properties so a Level 1 team can use them quickly: a primary metric is 0-100%, usually a hybrid of several metrics; secondary metrics aim for 0-100% too.
- A metric that cannot be colour coded, such as VM Disk IOPS, is hard for Level 1: its meaning depends on context.
- Example: Capacity Remaining (%) is primary; CPU utilization, memory usable capacity and CPU allocation are secondary.
- Example: VM Performance (%) is primary ([`vsphere/object-types/vm/vm-performance`](../../vsphere/object-types/vm/vm-performance.md)); peak vCPU Ready among the vCPUs, peak read/write latency among the virtual disks and Guest OS CPU context switch are secondary.

## Misconceptions

- "A metric with no threshold is useless" → context metrics have no colour; they answer "it depends".
- "CPU utilization stands for performance" → a system busy on overhead shows high utilization with falling throughput.

## Metadata

```yaml
id: sp5-framework/observability/triple-see-method
retriever_guide: how-it-works
scope: sp5-framework
technology:
- system
pillar:
- performance
- capacity
- availability
- security
- value
product:
- vsphere
- vcf-operations
internal_derive:
- sp5-framework/concepts/overview
related:
- sp5-framework/observability/collection-interval
- sp5-framework/observability/aggregation
- sp5-framework/concepts/modelling
- sp5-framework/observability/input-types
- sp5-framework/observability/metric-perspectives
- sp5-framework/concepts/monitoring-vs-troubleshooting
- sp5-framework/concepts/performance-vs-capacity
source:
  document: 'Private Cloud Management by Iwan Rahabok (https://isvara.io/download), Metric Mastery'
  path: Metric Mastery > Triple See Method; Primary | Secondary Metrics
corrections: []
review_notes:
- 'Section ''Three types of metric'': the book lists contention for performance only; availability for errors and drops follows from its Contention text.'
status: draft
```
