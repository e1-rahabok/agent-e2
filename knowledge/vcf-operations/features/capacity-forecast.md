# Capacity forecast

## Projection engine (VCF Operations 9.1.1)
- 9.1.1 replaced the engine. Before: several models in parallel (linear and periodic), the best fit chosen per object. Since 9.1.1: one model, a time-decay weighted linear regression, for CPU, memory and storage. Two similar workloads now get comparable trend lines; before, each could get a different winning model.
- Time decay: recent points weigh more than old ones, so the slope follows current behaviour. A projection can look odd against the full history chart.
- Lookback: up to 90 days for capacity forecasts and Time Remaining. Workload Placement uses the last 7 days and projects about 2 hours ahead.
- Projection window: 1 year into the future. The engine reads 5-minute data and recomputes once every 24 hours; a policy change or a change of total capacity triggers an immediate recalculation.
- Range: an upper and a lower bound, each computed on its own from quantiles of the data (asymmetric), not a symmetric band around the trend line. A spike or a dip widens only its own side, so a brief burst no longer pulls Time Remaining in.
- Flat baseline (zero growth) in three cases: less than 7 days of history; data too variable for a line to fit; a downward trend. A shrinking cluster shows a flat projection, never a growing runway.
- Jump points: a step change (migration, scale-out, VM reconfiguration) is detected and the UI offers a Recommended Reset Date. Applying it drops the history before the step; trend and bounds then use only the data after it.
- Upgrade to 9.1.1 writes `/storage/log/vcops/log/capacityMetricsUpgradeChanges.csv` on the VCF Operations primary node: per object, the old and new Time Remaining and rightsizing values. Read it before sharing post-upgrade forecasts; a large delta on one object usually means a jump point.
- Usable capacity: total capacity minus what vSphere HA admission control reserves for failover, minus the policy buffer. Buffer properties: cpu|demand|bufferSetting (%), mem|demand|bufferSetting (%); default 0% ([`sp5-framework/capacity/supply`](../../sp5-framework/capacity/supply.md), section Buffer).

## Peaks in the 9.1.1 engine
- A momentary peak sits above the upper quantile and barely moves the bounds.
- A periodic peak (month-end, quarter-end) is no longer projected as a pattern: the line has no periodic term. It reaches the forecast only through the upper bound, and only if the peak points exceed the share of data the upper quantile leaves out. Example: a month-end close of 2 working days is under 7% of the days, and fewer of the 5-minute points when the peak lasts only business hours; an upper bound that leaves out the top 7% of points ignores it.
- Broadcom has not published the percentile behind each risk level. For production, check that the upper bound on the capacity chart reaches the last month-end peaks before trusting Time Remaining.
- 90 days hold one quarter-end and no year-end. A yearly peak is outside the lookback; plan it by hand ([`sp5-framework/capacity/forecasting`](../../sp5-framework/capacity/forecasting.md)).

## Risk level
- Set per policy, with a slider from Most Aggressive to Most Conservative. Each position maps to a fixed pair of upper and lower percentiles. Default: Conservative level 3.
- Conservative: the forecast uses the upper bound. Higher levels widen the bounds toward the highest historical peaks. For production and mission-critical workloads.
- Aggressive: the forecast uses the mean of the upper and lower bounds; the most aggressive level pulls both bounds close to the trend line. For non-critical workloads.

## Capacity Remaining (%)
- Usable capacity minus the highest projected utilization over the next 3 days: the smallest remaining capacity in the window, at its tightest point. The 3 days are fixed.
- Projected utilization above 100% of usable capacity at any point: Capacity Remaining is 0. It fluctuates when the load regularly touches usable capacity.
- The documentation wording "the largest difference between usable capacity and projected utilization" reads like the quietest point. The metric definition ("the maximum point") and Broadcom's description ("the minimum capacity left projected three days in the future") settle it as the tightest point.
- Capacity Remaining Percentage (%) on a container is the value of its most constrained resource.
- The 3-day window sees only the next 3 days. A periodic peak further ahead (month-end, quarter-end) is not in Capacity Remaining; it shows only in Time Remaining, and only as far as the upper bound keeps it.
- Committed future demand (projects, reservations not yet created) is not counted.
- CPU and Memory Capacity Remaining (%) appear in policies but are internal and not usable.
- The policy sets the percentage at which a Capacity Remaining alert triggers.

## Time Remaining (days)
- Days until projected utilization crosses usable capacity, within the 1-year window.
- Based on the projection of utilization, not on Capacity Remaining.
- The policy sets the warning threshold in days.

## Misconceptions
- "Conservative uses the trend line" → Conservative uses the upper bound projection; Aggressive uses the mean of the upper and lower bounds.
- "Capacity Remaining is current free capacity" → a projection over the next 3 days, set by its tightest point.
- "Capacity Remaining is the largest gap in the next 3 days" → it is the smallest remaining capacity: usable capacity minus the highest projected point.
- "Capacity Remaining is high, so the next month-end peak fits" → the 3 days may not include the peak. Read the highest values of past peaks, not daily averages, and use Conservative for production.
- "A trend line on daily averages shows when the cluster runs out" → averages hide periodic peaks; the cluster runs short at the peak first.
- "Time Remaining counts down from Capacity Remaining" → it comes from the 1-year projection of utilization.
- "Set Aggressive to get more room" → the room is the same; Aggressive lets occasional peaks count less, so the cluster can run short at those peaks.
- "Since 9.1.1 the engine projects the month-end pattern forward" → the 9.1.1 engine fits one line; a short periodic peak counts only if the upper bound's percentile reaches it.
- "Load is falling, so Time Remaining grows" → 9.1.1 flattens a downward trend to zero growth.
- "After a big migration the forecast settles by itself" → old history keeps weighing until it decays; apply the Recommended Reset Date.

## Metadata
```yaml
id: vcf-operations/features/capacity-forecast
retriever_guide: how-it-works
scope: vcf-operations
technology:
- cpu
- memory
- storage
- system
pillar:
- capacity
product:
- vcf-operations
- vsphere
object:
- ClusterComputeResource
- HostSystem
- Datastore
internal_derive:
- sp5-framework/capacity/forecasting
related:
- sp5-framework/capacity/supply
- sp5-framework/capacity/capacity-management
- vsphere/object-types/cluster/decision-tree/can-cluster-take-more-vms
source:
  document: A Smarter, More Transparent Way to Forecast Capacity in VMware Cloud Foundation 9.1.1 (VCF blog, 2026-10-20); VCF Operations 9.1 documentation (TechDocs, VCF 9.1.x, last updated 2026-11-12), How Does VCF Operations Calculate and Forecast Capacity, Capacity Analytics Generated Metrics, Policy Workspace Capacity Details; Broadcom KB 379077; VCF blog Rightsizing VMs with VMware Cloud Foundation (2025-08-12); VCF Operations 9.1.1 Capacity Engine Technical Manual (project/sources)
  path: https://blogs.vmware.com/cloud-foundation/2026/10/20/a-smarter-more-transparent-way-to-forecast-capacity-in-vcf/; https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/cost-and-capacity-management/optimizing-capacity-and-improving-performance/capacity-optimization-concepts/how-does-vmware-aria-operations-calculate-and-forecast-capacity.html; https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/infrastructure-operations/metric-property-and-alert-definitions/metrics-definitions-in-vrealize-operations-manager/calculated-metrics/capacity-metrics.html; https://knowledge.broadcom.com/external/article/379077; https://blogs.vmware.com/cloud-foundation/2025/08/12/vmware-cloud-foundation-helps-you-optimally-size-vms-and-keep-your-infrastructure-and-workloads-running-smoothly/
corrections:
- 'Section ''Risk level'': the earlier text had Aggressive as the upper band and Conservative as the trajectory; TechDocs 9.1 says Conservative uses the upper bound projection and Aggressive the mean of the upper and lower bounds.'
- 'Section ''Projection engine (VCF Operations 9.1.1)'': TechDocs 9.1 (last updated 2026-11-12) still describes the engine before 9.1.1: models chosen by best fit, linear or periodic, periodic peaks projected forward without decay. The VCF blog of 2026-10-20 describes the 9.1.1 engine: one time-decay weighted linear regression, asymmetric quantile bounds, up to 90 days of history, flat baseline rules, jump points. The newer document wins.'
- 'Section ''Capacity Remaining (%)'': the TechDocs concept page says "the largest difference between the usable capacity and the projected utilization"; the metric definition page says "the maximum point", and the VCF blog of 2025-08-12 says "the minimum capacity left projected three days in the future". The knowledge base uses the smallest remaining capacity.'
review_notes:
- 'To check: Section ''Risk level'': the mapping Conservative = upper bound, Aggressive = mean of the bounds comes from the TechDocs page that predates 9.1.1; the blog says only that slider levels map to percentiles. Check the 9.1.1 TechDocs when updated, https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/infrastructure-operations/configuring-policies/using-the-monitoring-policy-workspace/policy-workspace/policy-workspace-capacity-details.html.'
- 'To check: Section ''Peaks in the 9.1.1 engine'': that the 9.1.1 regression has no periodic term is read from the blog (one linear trendline); the percentile per risk level is not published. Check against the 9.1.1 TechDocs capacity concept page when updated.'
- 'To check: Section ''Projection engine (VCF Operations 9.1.1)'': the 1-year projection window and the 24-hour recompute come from the TechDocs page that predates 9.1.1; the technical manual in project/sources says a policy-defined window, not found in Broadcom documents.'
status: draft
```
