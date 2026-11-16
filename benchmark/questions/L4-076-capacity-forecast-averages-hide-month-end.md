# Capacity forecast from daily averages

## Prompt
- Cluster prod-cl03 runs the finance applications. Today is Thursday, 12 November 2026.
- The VCF Operations capacity policy for the cluster uses an aggressive risk setting and a buffer of 0%. Usable capacity is total capacity minus the HA failover capacity.
- VCF Operations shows CPU Capacity Remaining 24% and Time Remaining 210 days.
- [The attached export](0235/cluster-cpu-demand-90-days.csv) holds 90 days of cluster CPU demand, as a percentage of usable capacity: the daily average and the highest 5-minute value of each day.
- The capacity manager fitted a line to the daily averages: "Demand grows about 0.1 point a day from about 63%. We reach 100% in about a year. We can take the new 600-vCPU payroll project when it goes live next month, without buying hosts."

Which statements are correct?

- A. The capacity manager is right: 24% remaining, 210 days and a year-long trend leave room for the payroll project.
- B. At the last three month-end closes, the highest 5-minute demand reached about 93%, 96% and 98% of usable capacity.
- C. Outside the last two working days of each month, the daily highest values stay at or below about 81% of usable capacity.
- D. At the current rise of about 2 points a month, the November close is near 100% of usable capacity before the project lands.
- E. Capacity Remaining is the free capacity right now: usable capacity minus the demand measured in the last collection.
- F. Capacity Remaining looks only 3 days ahead, so on 12 November it cannot show the month-end close of November.
- G. The aggressive setting forecasts from the mean of the upper and lower bounds, so short month-end peaks weigh less.
- H. Moving the policy to aggressive gave the cluster more usable capacity, which is why the forecast shows room.
- I. For production finance, use a conservative setting, checked so that its upper bound reaches the last month-end peaks.
- J. The forecast already counts the payroll project, because VCF Operations projects committed demand from vCenter.
- K. Neither Capacity Remaining nor Time Remaining reads contention, so check VM CPU Ready and Co-stop during the last close.
- L. With three month-ends in 90 days, the 9.1.1 engine projects the month-end pattern forward as a periodic term.
- M. The project should go on this cluster only after new capacity is added or other load is moved out before the November close.
- N. Since the October close the daily highest values fell from 97.8 to about 80, so Time Remaining will grow as the trend turns down.

## Likely wrong answer
- A: "Capacity Remaining is 24% and Time Remaining is 210 days, and the trend gives a year, so there is room for the project."
- N: "Load has fallen since the close, so the runway gets longer."

## Expected key points
- Answer: B, C, D, F, G, I, K, M.
- A is wrong: the daily averages hide the month-end peaks, which already reach 98%; the project is not in any projection.
- B is correct: export, highest 5-minute values on 31 August 93.4, 30 September 95.6, 30 October 97.8.
- C is correct: every other day peaks at 80.9 or less; the risk is the periodic month-end close, not the daily trend.
- D is correct: about 2 points a month on top of 97.8 puts the November close near 100% with no project load added.
- E is wrong: Capacity Remaining is a projection over the next 3 days, set by its tightest point, not current free capacity.
- F is correct: the 3-day window is fixed; a peak further ahead is not in Capacity Remaining.
- G is correct: aggressive uses the mean of the bounds; a 2-day close is a few percent of the points and barely moves it.
- H is wrong: the room is the same; aggressive only lets occasional peaks count less, so the cluster can run short at those peaks.
- I is correct: conservative uses the upper bound; for production, check that the upper bound reaches the last month-end peaks before trusting Time Remaining.
- J is wrong: committed future demand (projects not yet created) is in no projection; add it on top.
- K is correct: both numbers read utilization against usable capacity; contention shows in VM CPU Ready and Co-stop at the peak.
- L is wrong: the 9.1.1 engine fits one time-decay weighted line with no periodic term; a periodic peak counts only through the upper bound.
- M is correct: the cluster is full at its month-end peaks before the project; place it only after new capacity or after moving load out.
- N is wrong: the fall after 30 October is the end of the periodic close, not a trend; and the 9.1.1 engine flattens a downward trend to zero growth, so a falling series never gives a growing runway.

## Notes
- Drafted 2026-11-12. Capacity Remaining looks 3 days ahead; Time Remaining reads the long projection; a conservative risk setting keeps peaks in the forecast (VCF Operations 9.1 documentation, capacity analytics). The key holds for both engines. Before 9.1.1 the engine could project the month-end pattern; the 9.1.1 engine (VCF blog, 2026-10-20) fits one time-decay weighted line to up to 90 days, the length of this export, and keeps a periodic peak only through the upper quantile bound. Capacity Remaining as the smallest remaining capacity: TechDocs 9.1 Capacity Analytics Generated Metrics ("the maximum point") and VCF blog 2025-08-12 ("the minimum capacity left").
- CSV generated by a seeded script; peaks on the last two working days of each month 88.1-97.8 (month-end days 93.4, 95.6, 97.8); all other days at most 80.9.
- Option G rests on the risk-level mapping in capacity-forecast (Conservative = upper bound, Aggressive = mean of the bounds), which has an open review note against the 9.1.1 TechDocs.
- Changed in the 2026-11-15 audit: N added (a falling load read as a growing Time Remaining: capacity-forecast, flat baseline on a downward trend).

## Metadata
```yaml
id: "0235"
title: "Capacity forecast from daily averages"
product: [vcf-operations, vsphere]
technology: [system, cpu]
task: decide-capacity
level: 400
answer_type: deterministic
answer: [B, C, D, F, G, I, K, M]
misconception: [A, N]
input: [table]
object: [cluster]
tool: [vcf-operations]
knowledge:
  - vcf-operations/features/capacity-forecast
  - sp5-framework/capacity/forecasting
  - sp5-framework/capacity/supply
knowledge_main: vcf-operations/features/capacity-forecast
attachments:
  - 0235/cluster-cpu-demand-90-days.csv
origin: synthetic
source_path: "Synthetic, 2026-11-12"
misconception_type: [rollup-and-interval, average-hides-worst]
pair: "0430"
status: draft
```
