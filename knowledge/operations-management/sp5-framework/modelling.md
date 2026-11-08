# Modelling a pillar into one number

## Why model
| Reason | Effect |
|---|---|
| Persona | Level 1 operators cover wide, not deep; they cannot track many raw metrics, some of which need a specialist to read |
| Scale | One metric per object allows aggregation across thousands of objects |
| Reporting | Management relates to VM Performance (%), not CPU Throttled (ms) |
| Pattern | One value shows trends that follow business cycles or attacks |

- A model is an approximation, like a consumer price index or a yearly health check. It is better than nothing, and its movement over time carries as much meaning as its value.

## Actual and potential
| Item | Performance (%) | Risk (%) |
|---|---|---|
| Quantifies | Actual slowness: reality | Potential slowness: what may happen |
| Metric type | Contention, plus saturation (compressed, swapped) | Consumption: allocation, utilization and imbalance, reservation; count of monster VMs |
| Low value | Bad | Good |

- Both assume configuration is already optimized and availability is handled separately, so the models read only contention and consumption (`operations-management/sp5-framework/triple-see-method`).
- Implementations: `vsphere/object-types/vm/kpis/vm-performance`, `vsphere/object-types/cluster/kpis/cluster-performance`, `vsphere/object-types/cluster/models/cluster-risk`.

## Scale 0-100%
- 100% is the best achievable, not a theoretical perfect: disk latency is never 0, so 100.00% does not occur.
- 0% is the worst tolerated, not the slowest possible. With 40 ms as the tolerance, 40 ms scores 0% and 400 ms also scores 0%: no negative.
- A KPI is not an SLA. An SLA aims for 100%; a KPI of 75% is good.
- Four equal bands: green 75-100, yellow 50-75, orange 25-50, red 0-25. Four splits evenly (three gives 33.33 and 66.67), and yellow gives a leading indicator.
- Equal bands keep metric thresholds easy to set. Green at 95-100 would force unequal bands and harder thresholds.
- Thresholds are the hardest part. A metric whose threshold cannot be defended is left out of the KPI.
- Scoring, weights and the formula: `operations-management/performance/performance-kpi-design`, section Scoring.

## Setting thresholds
- Scientifically, a VM does not care what stops it (Ready, Co-stop or Overlap), so all would share one threshold. Practically, healthy production shows different scales per metric. Take the lower of the two: the goal is proactive monitoring.
- Match the thresholds to the weights 1x, 2x, 4x, 8x: each range limit doubles. Example: VM disk latency 20, 40, 80, 160 ms.
- Red is not an emergency: look within hours. The time to look also shows how often the value enters red and the trend.
- Single-value green: green = 0 means one dropped packet already scores yellow. Anything above 0 red: set green, yellow and orange to 0.

## Optional techniques
- Metric weight: a metric twice as important gets twice the weight; weights sum to 100%. Give twice the weight also to a metric twice as likely to go bad, for an earlier warning. Example: CPU 40%, memory, disk, network 20% each.
- Rare serious metric (error packets in Kubernetes): a large fixed weight is a free score while it is 0. Move it to a second table that overrides the KPI to red when it occurs.
- Multi-table KPI: many equal metrics dilute each one; one red among 21 cannot pull the KPI down. Split into tables (infrastructure and workload for a Kubernetes cluster) and combine. Not implemented; no proven need.

## Validation
- Write the common scenarios and the value expected, then check the model gives it.
- 9 perfect green and 3 worst red: a plain average gives 75; the weighted score gives low orange, close to red. Read the score, not only the colour.
- 1 perfect green and 11 barely red (near 25): the result is orange. Barely-red values rarely make red, so set the red limit at twice the orange limit.
- With many objects, show the scores as a heat map: it orders them by value; most should be green.

## Limitations
- Linear mapping inside a range. Queueing delay (CPU scheduler, vSAN and NVMe queues, NUMA interconnect) grows steeply near saturation: 10% to 12% vCPU Ready hurts more than 0% to 2%. The linear map under-weights it near the limit. Kept linear: easier to read, and the fix is the same.
- Many metrics dilute each weight; mixed static and dynamic metrics. Both are solved by multiple tables.

## Traps
- "KPI at 75%, so 25% of the VMs are slow" → 75% is the top of yellow; the scale is scores, not shares.
- "Aim for a 100% KPI like an SLA" → 100% is unreachable; 75-100 is green.
- "Only the colour matters" → 9 green and 3 worst red give low orange, near red; read the score.
- "Red means drop everything" → look within hours.
- "Give the rare error metric 40% weight" → it scores free 100 most of the time; put it in an override table.

## Metadata
```yaml
id: operations-management/sp5-framework/modelling
retriever_guide: how-it-works
scope: operations-management
technology:
- system
pillar:
- performance
- capacity
product:
- vcf-operations
internal_derive:
- operations-management/performance/performance-kpi-design
related:
- operations-management/sp5-framework/triple-see-method
- operations-management/sp5-framework/alerts-and-insights
- vsphere/object-types/vm/kpis/vm-performance
- vsphere/object-types/cluster/models/cluster-risk
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Modelling (Actual | Potential; Calculation; Translation; Threshold; Progressive Weightage; Rare Metric; Limitation; Optional Features; Validation)
corrections: []
review_notes:
- 'Section ''Setting thresholds'': the book maps KPI colours to a timeline (red within a few hours, orange today, yellow tomorrow). The author answered Q089 that alert colours and KPI colours are not related. Kept as "look within hours" for red only (Q136).'
status: draft
```
