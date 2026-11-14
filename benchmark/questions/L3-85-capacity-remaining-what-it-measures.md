# Capacity Remaining: what it measures

## Prompt
- Today is Monday, 9 November 2026. VCF Operations shows Capacity Remaining 31% for cluster prod-cl05.
- A month-end batch on 30 November roughly doubles the cluster's CPU demand for one day.
- A new project of 200 VMs is approved and will be deployed in December.
- The capacity manager asks what the 31% means.

Which statements about Capacity Remaining are correct?

- A. It is the usable capacity minus the highest projected utilization over the next 3 days.
- B. It is the capacity free right now: usable capacity minus the utilization of the last collection.
- C. A projected point above usable capacity anywhere in its window sets it to 0.
- D. The month-end batch of 30 November plays no part in today's 31%.
- E. Place the month-end batch's extra load on this cluster: 31% remaining covers it.
- F. It is the average room left over the next 3 days.
- G. Time Remaining counts down from Capacity Remaining.
- H. The approved project of 200 VMs is not counted in it.
- I. Its usable capacity is the total capacity minus the HA failover capacity and the policy buffer.
- J. For the cluster, Capacity Remaining (%) is the value of its most constrained resource.

## Likely wrong answer
B: Capacity Remaining read as free capacity now, so 31% looks like room for the month-end. Or E, the action that follows from it.

## Expected key points
- Answer: A, C, D, H, I, J.
- A true: usable capacity minus the highest projected utilization over the next 3 days: the smallest remaining capacity in the window, at its tightest point. The 3 days are fixed.
- B false: the misconception. It is a projection over the next 3 days, set by its tightest point, not the current free capacity.
- C true: projected utilization above 100% of usable capacity at any point gives 0.
- D true: the window covers the next 3 days only (to 12 November); a peak further ahead is not in Capacity Remaining.
- E false: the wrong action. The 31% does not see 30 November; read the highest values of past month-ends.
- F false: not an average over the window; the tightest point sets it.
- G false: Time Remaining comes from the projection of utilization, not from Capacity Remaining.
- H true: committed future demand (projects not yet created) is in no projection; add it on top.
- I true: usable capacity is total capacity minus what vSphere HA admission control reserves for failover, minus the policy buffer.
- J true: on a container, Capacity Remaining Percentage is the value of the most constrained resource.

## Notes
- Theory half of 0235 (pair: design.md, section 3.9). Different numbers from 0235, so one does not give away the other.
- No option rests on the risk-level mapping or the projection window of Time Remaining: both carry open review notes in vcf-operations/features/capacity-forecast.
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item B5). Counts only after author approval.

## Metadata
```yaml
id: "0430"
title: "Capacity Remaining: what it measures"
product: [vcf-operations, vsphere]
technology: [system, cpu, memory]
task: decide-capacity
level: 300
answer_type: deterministic
input: [text]
object: [cluster]
tool: [vcf-operations]
knowledge:
  - vcf-operations/features/capacity-forecast
  - sp5-framework/capacity/supply
knowledge_main: vcf-operations/features/capacity-forecast
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item B5"
answer: [A, C, D, H, I, J]
misconception: [B, E]
misconception_type: [rollup-and-interval]
pair: "0235"
status: draft
```
