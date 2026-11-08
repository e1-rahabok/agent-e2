# Triple See Method

## Purpose
- Thousands of metrics across a VCF private cloud are mastered by seeing what they have in common: every metric is one of three types.
- The Triple See Method: see contention, consumption and context, and verify them as one set before concluding.
- Designed for Broadcom VCF by the author, after studying the USE Method (Brendan Gregg), the RED Method (Weaveworks) and the Golden Signals (Google SRE).
- The three types are peers, each with its own purpose, and each maps to pillars of the SP5 framework (`operations-management/sp5-framework/overview`).

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

## Why contention comes first
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

- Example: Capacity Remaining (%) is primary; CPU utilization, memory usable capacity and CPU allocation are secondary.
- Example: VM Performance (%) is primary (`vsphere/object-types/vm/kpis/vm-performance`); peak vCPU Ready among the vCPUs, peak read/write latency among the virtual disks and Guest OS CPU context switch are secondary.

## Why not USE, RED or Golden Signals
- USE (utilization, saturation, errors) starts from utilization, a consumption metric. In a shared, overcommitted VCF cluster, utilization does not show who waits; contention per VM does.
- RED (rate, errors, duration) and the Golden Signals (latency, traffic, errors, saturation) are request-centric: built for services and microservices. IaaS has no request to time at the VM level; it has vCPU, memory and disk waits.
- None of the three has a context type. In VCF many questions are "it depends" questions (configuration, inventory, vMotion counts), answered only by context metrics.
- None maps its metric types to the pillars of operations, so none tells which team acts on a metric.

## Traps
- "Apply the USE Method: high utilization means a problem" → utilization is consumption, a good thing when the load is useful. Check contention first.
- "Monitor the four Golden Signals on the VMs" → they are request metrics for services. A VM has no request latency; read contention (Ready, Co-stop, memory and disk latency) per VM.
- "A metric with no threshold is useless" → context metrics have no colour; they answer "it depends".
- "CPU utilization stands for performance" → a system busy on overhead shows high utilization with falling throughput.

## Metadata
```yaml
id: operations-management/sp5-framework/triple-see-method
retriever_guide: how-it-works
scope: operations-management
technology:
- system
pillar:
- performance
- capacity
- availability
- compliance
- value
product:
- vsphere
- vcf-operations
internal_derive:
- operations-management/sp5-framework/overview
related:
- foundations/collection-interval
- foundations/aggregation
- operations-management/sp5-framework/modelling
- foundations/input-types
- foundations/metric-perspectives
- operations-management/sp5-framework/monitoring-vs-troubleshooting
- operations-management/sp5-framework/performance-vs-capacity
source:
  document: 'PART 3 - Counters.docx, Metric Mastery (author update, 2026-11-08)'
  path: Metric Mastery > Triple See Method; Primary | Secondary Metrics
corrections: []
review_notes:
- 'Author update 2026-11-08: Value Management, not Cost Management: value covers cost, price and business value (author, 2026-11-08).'
- 'Section ''Why not USE, RED or Golden Signals'': the book names the three methods and says Triple See was built from their strengths and weaknesses, but does not list them. The comparison is Claude''s reading; to confirm (Q134). Sources: brendangregg.com/usemethod.html, weave.works RED Method blog, sre.google SRE book, Monitoring Distributed Systems.'
- 'Section ''Three types of metric'': the book lists contention for performance only; availability for errors and drops follows from its Contention text.'
status: draft
```
