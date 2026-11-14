# Modelling a pillar into one number

## Reasons to model
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

- Both assume configuration is already optimized and availability is handled separately, so the models read only contention and consumption ([`sp5-framework/observability/triple-see-method`](../observability/triple-see-method.md)).
- Implementations: [`vsphere/object-types/vm/vm-performance`](../../vsphere/object-types/vm/vm-performance.md), [`vsphere/object-types/cluster/cluster-performance`](../../vsphere/object-types/cluster/cluster-performance.md), [`vsphere/object-types/cluster/models/cluster-risk`](../../vsphere/object-types/cluster/models/cluster-risk.md).

## Scale 0-100%
- 100% is the best achievable, not a theoretical perfect: disk latency is never 0, so 100.00% does not occur.
- 0% is the worst tolerated, not the slowest possible. With 40 ms as the tolerance, 40 ms scores 0% and 400 ms also scores 0%: no negative.
- A KPI is not a contract: it does not aim for 100%; a KPI of 75% is good.
- Four equal bands: green 75-100, yellow 50-75, orange 25-50, red 0-25. Four splits evenly (three gives 33.33 and 66.67), and yellow gives a leading indicator.
- Equal bands keep metric thresholds easy to set. Green at 95-100 would force unequal bands and harder thresholds.
- Thresholds are the hardest part. A metric whose threshold cannot be defended is left out of the KPI.
- Scoring, weights and the formula: [`sp5-framework/performance/performance-kpi-design`](../performance/performance-kpi-design.md), section Scoring. In short: five limits per metric, a straight line inside each band, and a weight that grows smoothly with a worse score, from 1 at 100 to 16 at 0.

## Three ways to combine the colours
| Question | Weighted average by colour | Weighted sum by colour | Worst colour |
|---|---|---|---|
| Rule | Every metric counts; worse counts more; average | Each metric adds by its colour; no average | KPI takes the worst colour; same-colour metrics push deeper |
| One red among greens | Shows, softened: usually reads orange | Full strength | Red |
| A metric gets worse | KPI can move the wrong way | Never the wrong way | Never the wrong way; may not move at all |
| KPI colour means | A mix: yellow can hide a red metric | A total: many yellows can make red | A fact: at least one metric is that colour |
| Ranking many clusters | Good: rarely reaches 0 or 100 | Weak: bad clusters all show the end of the scale | Ties within a colour |
| Best fit | Performance, consumption, risk: trends and ranking | A yes-or-no decision that must never go the wrong way | Availability |

- Performance, Consumption and Risk use the weighted average by colour.
- Performance and capacity combine, not take the worst: contention adds up (a VM waiting for CPU, memory and disk is hurt more than one waiting for CPU); leading indicators combine (two orange risk factors bring contention closer than one); and an orange metric is a level, not a failure.
- Availability takes the worst: one failed component can take a host down. It uses two tables, partial failures component by component, and failures that alone take the host down. The score is the minimum of the two: a dead host scores as dead.
- Weights by rank (ordered weighted average, Yager 1988: worst 8x, second 4x, third 2x, fourth 1x) were considered and rejected. Ranking throws away the vSphere meaning of each colour: a second red counts half only because it is second, a fifth counts nothing.
- Known effect of the weighted average: when the KPI is already bad, a metric that gets worse can make it look better ([`vsphere/object-types/cluster/models/cluster-risk`](../../vsphere/object-types/cluster/models/cluster-risk.md), section Sub-metric weight in Cluster Risk). Close for Business reads Risk at orange, so a cluster just inside orange can drop to yellow after VMs are deployed and open again.

## Setting thresholds
- Scientifically, a VM does not care what stops it (Ready, Co-stop or Overlap), so all would share one threshold. Practically, healthy production shows different scales per metric. Take the lower of the two: the goal is proactive monitoring.
- Match the thresholds to the weights, which double per band (1, 2, 4, 8 at the band limits, 16 at 0): each range limit doubles. Example: VM disk latency 20, 40, 80, 160 ms.
- A KPI or model colour is severity: how bad, not by when. A worse KPI usually means more urgency, but there is no fixed link: KPI red is not a red alert and does not mean act today. The daily health check reads red first, then orange, then how often a value enters red and its trend.
- The colour depends on where the metric is shown. The same metric can carry different colour thresholds in an alert, a NOC live screen, a daily report and a dashboard, as each channel has its own urgency ([`sp5-framework/outputs/system-engagement`](../outputs/system-engagement.md)).
- Four bands need five numbers per metric: where it scores 100, and where green, yellow and orange end, and where it scores 0. Vendor guidance with three zones (good, potential issue, impact) is not enough: convert it, do not copy it. Example: NVMe read latency, Broadcom's good below 200 µs and impact above 400 µs become 100, 200, 400 and 800 µs, with red from 400.
- Score the what, never filter it by the why. A reading is not discarded because its cause looks harmless (a device waking from a power-saving state): the consumer waited all the same. The cause belongs to troubleshooting.
- A metric that cannot be quantified into its bands ([grey], green, yellow, orange, red) is not used. Real-world data is not reliable because it is real: check its quality first, then collect enough of it to rule out outliers.
- Single-value green: green = 0 means one dropped packet already scores yellow. Anything above 0 red: set green, yellow and orange to 0.

## Rare and rarely-green metrics
- A metric that is green almost always (dropped packets) or whose green says nothing about health (low CPU or memory utilization) would add a free 100 every cycle and hide the others.
- So such a metric is skipped while green and counts once it leaves green; missing data is left out, never counted as 0. The rules: [`sp5-framework/performance/performance-kpi-design`](../performance/performance-kpi-design.md), section Scoring.
- Alternatives not implemented: a fixed weight per metric (CPU 40%, memory, disk, network 20% each), a second table that overrides the KPI to red for a rare serious metric, and a multi-table KPI for many equal metrics. Weight depends only on the score. Two tables exist only in availability, as above.

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

## Misconceptions
- "KPI at 75%, so 25% of the VMs are slow" → 75% is the top of yellow; the scale is scores, not shares.
- "Aim for a 100% KPI" → 100% is unreachable; 75-100 is green.
- "One red metric makes the KPI red" → one worst red among 8 greens scores about 33, orange; read the score and the sub-metrics.
- "KPI red: act today, like a red alert" → a KPI colour is severity, not a deadline. The alert carries the deadline, with its own values.
- "A metric has one colour scale everywhere" → its colour thresholds depend on the channel: alert, NOC live screen, daily report, dashboard.
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
- sp5-framework/observability/triple-see-method
- sp5-framework/outputs/alerts-and-insights
- vsphere/object-types/vm/vm-performance
- vsphere/object-types/cluster/models/cluster-risk
source:
  document: Knowledge base
  path: 'The World of Metrics > Modelling (Actual | Potential; Calculation; Translation; Threshold; Progressive Weightage; Rare Metric; Limitation; Optional Features; Validation)'
corrections: []
review_notes: []
status: draft
```
