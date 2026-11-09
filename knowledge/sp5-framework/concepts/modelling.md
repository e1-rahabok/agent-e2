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

- Both assume configuration is already optimized and availability is handled separately, so the models read only contention and consumption (`sp5-framework/concepts/triple-see-method`).
- Implementations: `vsphere/object-types/vm/kpis/vm-performance`, `vsphere/object-types/cluster/kpis/cluster-performance`, `vsphere/object-types/cluster/models/cluster-risk`.

## Scale 0-100%
- 100% is the best achievable, not a theoretical perfect: disk latency is never 0, so 100.00% does not occur.
- 0% is the worst tolerated, not the slowest possible. With 40 ms as the tolerance, 40 ms scores 0% and 400 ms also scores 0%: no negative.
- A KPI is not an SLA. An SLA aims for 100%; a KPI of 75% is good.
- Four equal bands: green 75-100, yellow 50-75, orange 25-50, red 0-25. Four splits evenly (three gives 33.33 and 66.67), and yellow gives a leading indicator.
- Equal bands keep metric thresholds easy to set. Green at 95-100 would force unequal bands and harder thresholds.
- Thresholds are the hardest part. A metric whose threshold cannot be defended is left out of the KPI.
- Scoring, weights and the formula: `sp5-framework/performance/performance-kpi-design`, section Scoring. In short: five limits per metric, a straight line inside each band, and a weight that grows smoothly with a worse score, from 1 at 100 to 16 at 0.

## Three ways to combine the colours
| Question | Weighted average by colour | Weighted sum by colour | Worst colour |
|---|---|---|---|
| Rule | Every metric counts; worse counts more; average | Each metric adds by its colour; no average | KPI takes the worst colour; same-colour metrics push deeper |
| One red among greens | Shows, softened: usually reads orange | Full strength | Red |
| A metric gets worse | KPI can move the wrong way | Never the wrong way | Never the wrong way; may not move at all |
| KPI colour means | A mix: yellow can hide a red metric | A total: many yellows can make red | A fact: at least one metric is that colour |
| Ranking many clusters | Good: rarely reaches 0 or 100 | Weak: bad clusters all show the end of the scale | Ties within a colour |
| Best fit | Performance, consumption, risk: trends and ranking | A yes-or-no decision that must never go the wrong way | Availability |

- The vCommunity management pack uses the weighted average by colour for Performance, Consumption and Risk.
- Performance and capacity combine, not take the worst: contention adds up (a VM waiting for CPU, memory and disk is hurt more than one waiting for CPU); leading indicators combine (two orange risk factors bring contention closer than one); and an orange metric is a level, not a failure.
- Availability takes the worst: one failed component can take a host down. It uses two tables, partial failures component by component, and failures that alone take the host down. The score is the minimum of the two: a dead host scores as dead.
- Weights by rank (ordered weighted average, Yager 1988: worst 8x, second 4x, third 2x, fourth 1x) were considered and rejected. Ranking throws away the vSphere meaning of each colour: a second red counts half only because it is second, a fifth counts nothing.
- Known effect of the weighted average: when the KPI is already bad, a metric that gets worse can make it look better (`vsphere/object-types/cluster/models/cluster-risk`, section A worse sub-metric can lower Cluster Risk). Close for Business reads Risk at orange, so a cluster just inside orange can drop to yellow after VMs are deployed and open again.

## Setting thresholds
- Scientifically, a VM does not care what stops it (Ready, Co-stop or Overlap), so all would share one threshold. Practically, healthy production shows different scales per metric. Take the lower of the two: the goal is proactive monitoring.
- Match the thresholds to the weights, which double per band (1, 2, 4, 8 at the band limits, 16 at 0): each range limit doubles. Example: VM disk latency 20, 40, 80, 160 ms.
- Red is not an emergency: look within hours. The time to look also shows how often the value enters red and the trend.
- Single-value green: green = 0 means one dropped packet already scores yellow. Anything above 0 red: set green, yellow and orange to 0.

## Rare and rarely-green metrics
- A metric that is green almost always (dropped packets) or whose green says nothing about health (low CPU or memory utilization) would add a free 100 every cycle and hide the others.
- Implemented: skip when green. While such a metric is green it is left out of the KPI, as if it had no data; once it leaves green it counts like any other. If every metric with data was skipped, the KPI is 100.
- Missing data is left out, never counted as 0: 0 usually means perfect.
- The book's alternatives are not implemented: a fixed weight per metric (CPU 40%, memory, disk, network 20% each), a second table that overrides the KPI to red for a rare serious metric, and a multi-table KPI for many equal metrics. Weight depends only on the score. Two tables exist only in availability, as above.

## Validation
- Write the common scenarios and the value expected, then check the model gives it.
- 9 perfect green and 3 worst red (score 0, weight 16): a plain average gives 75; the weighted score is about 15.8, red.
- 8 perfect green and 1 worst red: about 33.3, orange. One red among many greens reads orange.
- 1 perfect green and 11 barely red (score 25, weight 8): about 25.8, orange; at score 24 it is about 24.8, red. Barely-red values seldom make red, so set the red limit at twice the orange limit.
- Read the score, not only the colour.
- With many objects, show the scores as a heat map: it orders them by value; most should be green.

## Limitations
- Linear mapping inside a range. Queueing delay (CPU scheduler, vSAN and NVMe queues, NUMA interconnect) grows steeply near saturation: 10% to 12% vCPU Ready hurts more than 0% to 2%. The linear map under-weights it near the limit. Kept linear: easier to read, and the fix is the same.
- Many metrics dilute each weight; mixed static and dynamic metrics. Both are solved by multiple tables.

## Traps
- "KPI at 75%, so 25% of the VMs are slow" → 75% is the top of yellow; the scale is scores, not shares.
- "Aim for a 100% KPI like an SLA" → 100% is unreachable; 75-100 is green.
- "One red metric makes the KPI red" → one worst red among 8 greens scores about 33, orange; read the score and the sub-metrics.
- "Red means drop everything" → look within hours.
- "Use the worst colour for performance, like a vCenter alarm" → contention adds up across resources; worst colour fits availability only.
- "Give the rare error metric a large weight" → weight depends only on the score; a rarely-red metric is skipped while green instead.

## Metadata
```yaml
id: sp5-framework/concepts/modelling
retriever_guide: how-it-works
scope: sp5-framework
technology:
- system
pillar:
- performance
- capacity
product:
- vcf-operations
internal_derive:
- sp5-framework/performance/performance-kpi-design
related:
- sp5-framework/concepts/triple-see-method
- sp5-framework/alerts/alerts-and-insights
- vsphere/object-types/vm/kpis/vm-performance
- vsphere/object-types/cluster/models/cluster-risk
source:
  document: 'PART 3 - Counters.docx; VCF-vCommunity-Adapter documentation, KPI Scoring Models (fetched 2026-11-08)'
  path: 'https://github.com/e1-rahabok/VCF-vCommunity-Adapter/blob/main/docs/concepts/kpi-scoring-models.md; The World of Metrics > Modelling (Actual | Potential; Calculation; Translation; Threshold; Progressive Weightage; Rare Metric; Limitation; Optional Features; Validation)'
corrections:
- 'Sections ''Three ways to combine the colours'', ''Rare and rarely-green metrics'', ''Validation'': the implementation wins over the book (author, 2026-11-08). The book weights one step per band (1, 2, 4, 8; one red = 8 greens; 9 green + 3 red = low orange); the pack weights 2^((100 - score)/25), smooth, up to 16 at 0 (issue #18), so 9 green + 3 worst red is red. The book''s per-metric weights, override table and multi-table KPI are not implemented; skip when green is.'
review_notes:
- 'Section ''Setting thresholds'': the book maps KPI colours to a timeline (red within a few hours, orange today, yellow tomorrow). The author answered Q089 that alert colours and KPI colours are not related. Kept as "look within hours" for red only (Q136).'
status: draft
```
