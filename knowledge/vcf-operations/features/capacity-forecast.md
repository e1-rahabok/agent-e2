# Capacity forecast

## Projection engine
- The capacity engine projects future utilization as a range: an upper bound and a lower bound projection. The range covers 90% of the future data points.
- Projection window: 1 year into the future.
- Uses 6+ months of history when available. Recent data weighs more (exponential decay), so a projection can look visually odd.
- Momentary one-off peaks barely affect the projection. Sustained non-periodic peaks fade over time. Periodic peaks (hourly, daily, weekly, month-end, overlapping) are detected; 5-minute data is required as input.
- Usable capacity in the engine: total capacity minus what vSphere HA admission control reserves for failover, minus the buffer set in the policy. Buffer properties: cpu|demand|bufferSetting (%), mem|demand|bufferSetting (%); default 0% ([`sp5-framework/capacity/supply`](../../sp5-framework/capacity/supply.md), section Buffer).

## Risk level
- Set per policy.
- Conservative: the upper bound projection. For production and mission-critical workloads; the projection keeps every peak, regular or occasional, found in the history.
- Aggressive: the mean of the upper and lower bound projections. For non-critical workloads.

## Capacity Remaining (%)
- The largest difference between usable capacity and projected utilization, from now to 3 days ahead. The 3 days are fixed.
- Projected utilization above 100% of usable capacity: Capacity Remaining is 0. It fluctuates when the load regularly touches usable capacity.
- Read the documentation's "largest difference" together with the 0 rule: one projected point above usable capacity sets the value to 0, so the value follows the tightest point of the 3 days (the highest projected utilization), not the quietest.
- The 3-day window sees only the next 3 days. A periodic peak further ahead (month-end, quarter-end) is not in Capacity Remaining; it shows only in Time Remaining, and only as far as the risk level keeps it.
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
- "Capacity Remaining is high, so the next month-end peak fits" → the 3 days may not include the peak. Read the highest values of past peaks, not daily averages, and use Conservative for production.
- "A trend line on daily averages shows when the cluster runs out" → averages hide periodic peaks; the cluster runs short at the peak first.
- "Time Remaining counts down from Capacity Remaining" → it comes from the 1-year projection of utilization.
- "Set Aggressive to get more room" → the room is the same; Aggressive lets occasional peaks count less, so the cluster can run short at those peaks.

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
  document: VCF Operations 9.1 documentation (TechDocs, VCF 9.1.x), How Does VCF Operations Calculate and Forecast Capacity; Policy Workspace Capacity Details; Policy Time Remaining Element; Policy Capacity Remaining Element (read 2026-11-11); Private Cloud Management by Iwan Rahabok (https://isvara.io/download), Provider Objects > Capacity > Projected Metrics
  path: https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/cost-and-capacity-management/optimizing-capacity-and-improving-performance/capacity-optimization-concepts/how-does-vmware-aria-operations-calculate-and-forecast-capacity.html; .../9-1/infrastructure-operations/configuring-policies/using-the-monitoring-policy-workspace/policy-workspace/policy-workspace-capacity-details.html
corrections:
- 'Section ''Risk level'': the earlier text had Aggressive as the upper band and Conservative as the trajectory; TechDocs 9.1 says Conservative uses the upper bound projection and Aggressive the mean of the upper and lower bounds.'
review_notes:
- 'To check: Section ''Capacity Remaining (%)'': the documentation says "the largest difference between the usable capacity and the projected utilization between now and 3 days into the future"; the reading as the tightest point rests on the 0 rule on the same page, https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/cost-and-capacity-management/optimizing-capacity-and-improving-performance/capacity-optimization-concepts/how-does-vmware-aria-operations-calculate-and-forecast-capacity.html.'
- 'To check: Section ''Projection engine'': 6+ months of history, exponential decay and the peak handling come from the book; not found on the 9.1 pages read.'
- 'To check: Section ''Projection engine'': the docs define usable capacity as total minus the HA admission control reserve; buffer taken from the policy buffer setting (book).'
status: draft
```
