# Close for Business 

## Definition
- The capacity model's automatic decision for one vSphere cluster: 1 = closed for business (full: place no new VM), 0 = open.
- Built from three 0-100% scores: Cluster Performance (KPI, [`vsphere/object-types/cluster/cluster-performance`](../cluster-performance.md)), Cluster Consumption (capacity model, [`vsphere/object-types/cluster/models/cluster-consumption`](cluster-consumption.md)), Cluster Risk (risk model, [`vsphere/object-types/cluster/models/cluster-risk`](cluster-risk.md)).
- It implements the overcommit path of the cluster closure logic. The full decision, including the no-overcommit path and the fit of new VMs: [`vsphere/object-types/cluster/decision-tree/can-cluster-take-more-vms`](../decision-tree/can-cluster-take-more-vms.md).

## Logic
- It runs periodically. Ideally once a day so the full day peak is considered. 
- Each of the 3 scores is summarized by its worst end over the window: the value with only the Worst Percent (default 5%) of the samples worse than it.
- Cluster Performance (higher is better): the 5th percentile. Cluster Risk and Cluster Consumption (higher is worse): the 95th percentile.
- 24-hour window, 288 five-minute samples, 5%: the 14 worst samples (70 minutes) are ignored. A cluster bad for an hour a day is not fine for new VMs; one short spike does not close it.

## The rule
- Display bands, the same scale for all three scores (the colour the user sees on each score):

| Band | Cluster Performance (higher is better) | Cluster Risk, Cluster Consumption (higher is worse) |
|---|---|---|
| Green | 75-100 | 0-25 |
| Yellow | 50-75 | 25-50 |
| Orange | 25-50 | 50-75 |
| Red | 0-25 | 75-100 |

- Closure thresholds sit inside the display bands, not on their borders: closing a cluster needs a value that is clearly red or clearly orange, not one just across a band limit.

| Closure level | Cluster Performance | Cluster Consumption, Cluster Risk |
|---|---|---|
| Red | below 20 (display red starts below 25) | above 80 (display red starts above 75) |
| Orange | below 40 (display orange starts below 50) | above 60 (display orange starts above 50) |

- A value on a closure threshold does not reach it: Performance of exactly 20 is orange for closure; Consumption of exactly 80 is orange.
- Closed (1) when either rule matches:
  - Rule 1: Consumption is red, or Performance is red. The cluster is full, or its VMs already suffer.
  - Rule 2: Consumption and Performance are both orange, and Risk is orange or red. Busy and slow at once, and heading the wrong way.
- Risk never closes a cluster on its own: it is a leading indicator that buys time.
- Keep two settings. Production focuses on performance and closes at Risk orange. Non-production focuses on cost: it runs fuller and closes at Risk red ([`vsphere/object-types/cluster/decision-tree/can-cluster-take-more-vms`](../decision-tree/can-cluster-take-more-vms.md), step 6). With one setting for every cluster, use production: it is the more conservative.
- Not published when one of the three scores has no data in the window.

| Performance | Risk | Consumption | Close for Business |
|---|---|---|---|
| 15 | 10 | 30 | 1 (rule 1: Performance red) |
| 90 | 10 | 85 | 1 (rule 1: Consumption red) |
| 35 | 65 | 65 | 1 (rule 2: both orange, Risk orange) |
| 35 | 55 | 65 | 0 (both orange, Risk not above 60) |
| 90 | 90 | 30 | 0 (Risk red alone does not close) |
| 35 | 90 | 45 | 0 (Consumption not above 60, Risk not read) |
| 22 | 10 | 10 | 0 (22 shows red on screen; closure red is below 20) |
| 90 | 10 | 78 | 0 (78 shows red on screen; closure red is above 80) |

## Settings
- Cluster Check Period: 1, 2, 4, 6, 8, 12 or 24 hours (default 24). Each window is as long as the period.
- Cluster Check Time (UTC): when one window ends (default 00:00). No time zone setting: 02:00 in Singapore (UTC+8) is 18:00.
- Cluster Check Worst Percent: 0-50 (default 5).
- A 1-hour window has 12 samples; 5% of 12 rounds down to 0, so the single worst sample decides.
- Also published per window: Worst Cluster Performance, Worst Cluster Risk, Worst Cluster Consumption. One point per period, not every 5 minutes.

## Misconceptions
- "Cluster Risk is red, so the cluster is closed" → Risk decides only when Performance and Consumption are both orange.
- "Close for Business uses the latest value" → it uses the worst end of the window, ignoring the worst 5% by default.
- "The score shows red, so the cluster is closed" → closure needs a value clearly inside the band: Performance below 20, Consumption above 80. A Consumption of 78 shows red and leaves the cluster open.
- "Close for Business is blank, so the cluster is open" → one of the three scores had no data; the decision was not made.
- "One closure setting suits every cluster" → production closes at Risk orange. A non-production cluster focuses on cost and can run until Risk is red: keep a separate setting for it.

## Metadata
```yaml
id: vsphere/object-types/cluster/models/close-for-business
retriever_guide: metric-meaning
scope: vsphere
technology:
- cpu
- memory
- system
pillar:
- capacity
- performance
product:
- vcf-operations
object:
- ClusterComputeResource
metric_class: context
internal_derive:
- vsphere/object-types/cluster/cluster-performance
- vsphere/object-types/cluster/models/cluster-consumption
- vsphere/object-types/cluster/models/cluster-risk
same_name: []
same_meaning: []
related:
- vsphere/object-types/cluster/decision-tree/can-cluster-take-more-vms
- vsphere/object-types/cluster/cluster-health-check
- sp5-framework/capacity/supply
source:
  document: Knowledge base; Private Cloud Management by Iwan Rahabok (https://isvara.io/download) for the closure logic
  path: 'Capacity Management > Capacity Model > Cluster Closure; Logic'
corrections: []
review_notes:
status: draft
```
