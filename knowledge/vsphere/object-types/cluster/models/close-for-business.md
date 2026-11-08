# Close for Business (capacity model decision, vCommunity management pack for VCF Operations)

## What it is
- The capacity model's decision for one vSphere cluster: 1 = closed for business (full: place no new VM), 0 = open.
- Published by the vCommunity management pack once per period (default every 24 hours) on every cluster, under `vCommunity|Periodic Cluster Check`.
- Built from three 0-100% scores: Cluster Performance (KPI, `vsphere/object-types/cluster/kpis/cluster-performance`), Cluster Consumption (capacity model, `vsphere/object-types/cluster/models/cluster-consumption`), Cluster Risk (risk model, `vsphere/object-types/cluster/models/cluster-risk`).
- It implements the overcommit path of the book's closure logic, with one rule for every cluster. The full decision, including the no-overcommit path and the fit of new VMs: `operations-management/capacity/health-check/can-cluster-take-more-vms`.

## Worst end of the period, not the latest value
- Each score is summarized by its worst end over the window: the value with only the Worst Percent (default 5%) of the samples worse than it.
- Cluster Performance (higher is better): the 5th percentile. Cluster Risk and Cluster Consumption (higher is worse): the 95th percentile.
- 24-hour window, 288 five-minute samples, 5%: the 14 worst samples (70 minutes) are ignored. A cluster bad for an hour a day is not fine for new VMs; one short spike does not close it.
- Worst Percent 0 = the single worst sample decides. 50 = the median; the maximum allowed.
- The percentile is computed by the pack: VCF Operations rollups have average, maximum, minimum and sum, but no percentile. An estimate from maximum and average is driven by one spike.

## The rule
- Bands, the same scale for all three scores:

| Band | Cluster Performance (higher is better) | Cluster Risk, Cluster Consumption (higher is worse) |
|---|---|---|
| Green | 75-100 | 0-25 |
| Yellow | 50-75 | 25-50 |
| Orange | 25-50 | 50-75 |
| Red | 0-25 | 75-100 |

- A value on a limit belongs to the better band: Performance of exactly 25 is orange; Risk of exactly 75 is orange.
- Closed (1) when either rule matches:
  - Rule 1: Consumption is red, or Performance is red. The cluster is full, or its VMs already suffer.
  - Rule 2: Consumption and Performance are both orange, and Risk is orange or red. Busy and slow at once, and heading the wrong way.
- Risk never closes a cluster on its own: it is a leading indicator that buys time. The pack uses orange, the lower Risk threshold of a critical cluster, for every cluster.
- Not published when one of the three scores has no data in the window.

| Worst Performance | Worst Risk | Worst Consumption | Close for Business |
|---|---|---|---|
| 20 | 10 | 30 | 1 (rule 1: Performance red) |
| 90 | 10 | 80 | 1 (rule 1: Consumption red) |
| 40 | 60 | 60 | 1 (rule 2: both orange, Risk orange) |
| 40 | 40 | 60 | 0 (both orange, Risk yellow) |
| 90 | 90 | 30 | 0 (Risk red alone does not close) |
| 40 | 90 | 40 | 0 (Consumption yellow, Risk not read) |
| 25 | 10 | 10 | 0 (25 is orange, not red) |

## Settings
- Cluster Check Period: 1, 2, 4, 6, 8, 12 or 24 hours (default 24). Each window is as long as the period.
- Cluster Check Time (UTC): when one window ends (default 00:00). No time zone setting: 02:00 in Singapore (UTC+8) is 18:00.
- Cluster Check Worst Percent: 0-50 (default 5).
- A 1-hour window has 12 samples; 5% of 12 rounds down to 0, so the single worst sample decides.
- Also published per window: Worst Cluster Performance, Worst Cluster Risk, Worst Cluster Consumption. One point per period, not every 5 minutes.

## Traps
- "Cluster Risk is red, so the cluster is closed" → Risk decides only when Performance and Consumption are both orange.
- "Close for Business uses the latest value" → it uses the worst end of the window, ignoring the worst 5% by default.
- "Performance of 25 is red" → a value on a limit takes the better band: orange.
- "Close for Business is blank, so the cluster is open" → one of the three scores had no data; the decision was not made.
- "The pack's thresholds are the book's closure thresholds" → the book closes production at Performance below 40% and non-production below 20%, with Risk at 50% and 75%; the pack uses one band set (25, 50, 75) for every cluster.

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
- vsphere/object-types/cluster/kpis/cluster-performance
- vsphere/object-types/cluster/models/cluster-consumption
- vsphere/object-types/cluster/models/cluster-risk
same_name: []
same_meaning: []
related:
- operations-management/capacity/health-check/can-cluster-take-more-vms
- vsphere/object-types/cluster/health-check/cluster-health-check
- operations-management/capacity/capacity-model
source:
  document: VCF-vCommunity-Adapter documentation, Periodic Cluster Check and Capacity Management concept (author, 2026-11-08)
  path: https://github.com/e1-rahabok/VCF-vCommunity-Adapter/blob/main/docs/reference/metrics/periodic-cluster-check.md; docs/concepts/capacity-management.md, section Closing the cluster
corrections: []
review_notes:
- 'Whole file: from the adapter documentation (author decision 2026-11-08: digest the adapter metric reference as needed). A model, not a KPI (author decision 2026-11-08).'
- 'Section Traps, last trap: the pack thresholds differ from the book closure thresholds in can-cluster-take-more-vms (Q121, Q122). Which one Agent E2 applies: Q132.'
- 'Section The rule: the adapter pages call Cluster Risk and Cluster Consumption KPIs; written as models per the author decision. Q131.'
status: draft
```
