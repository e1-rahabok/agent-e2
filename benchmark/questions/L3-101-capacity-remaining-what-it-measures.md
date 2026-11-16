# Capacity Remaining: what it measures

## Prompt
- Today is Monday, 9 November 2026. VCF Operations shows Capacity Remaining 31% for cluster prod-cl05.
- A month-end batch on 30 November roughly doubles the cluster's CPU demand for one day.
- A new project of 200 VMs is approved and will be deployed in December.
- The capacity manager asks what the 31% means.

Which statements about Capacity Remaining are correct?

- A. It swings from day to day on a cluster whose load regularly reaches usable capacity.
- B. 31% means 69% of usable capacity is in use at this moment.
- C. A projected point above usable capacity anywhere in its window sets it to 0.
- D. 30 November lies outside the window that sets today's 31%.
- E. The month-end batch fits on this cluster without more capacity: 31% covers it.
- F. It is the average room left between usable capacity and utilization over the next 3 days.
- G. Time Remaining counts down from Capacity Remaining as the days pass.
- H. The approved project of 200 VMs, due in December, is not counted in it.
- I. Its usable capacity is total capacity minus HA failover capacity and the policy buffer.
- J. For the cluster, it is the value of its most constrained resource.
- K. It is the largest gap between usable capacity and projected utilization in the next 3 days.

## Answers
A, C, D, H, I, J

## Explanation
- A is correct: it is set by the tightest projected point of the next 3 days, so it fluctuates when the load regularly touches usable capacity (and drops to 0 when a projected point passes it).
- B is wrong: the misconception. Capacity Remaining is a projection over the next 3 days, set by its tightest point, not the share of usable capacity in use now.
- C is correct: projected utilization above 100% of usable capacity at any point gives 0.
- D is correct: the window is the next 3 days (9 to 12 November); a peak further ahead is not in Capacity Remaining.
- E is wrong: the wrong decision. The 31% does not see 30 November; read the highest values of past month-ends.
- F is wrong: not an average over the window; the tightest point sets it.
- G is wrong: Time Remaining comes from the projection of utilization, not from Capacity Remaining.
- H is correct: committed future demand (projects not yet created) is in no projection; add it on top.
- I is correct: usable capacity is total capacity minus what vSphere HA admission control reserves for failover, minus the policy buffer.
- J is correct: on a container, Capacity Remaining Percentage is the value of the most constrained resource.
- K is wrong: it is the smallest remaining capacity, usable capacity minus the highest projected point; the largest gap would be the quietest point of the window.
- Misconception: B: Capacity Remaining read as free capacity now, so 31% looks like room for the month-end. Or E, the decision that follows from it. Or K: the documentation wording "the largest difference between usable capacity and projected utilization" read literally.

## Notes
- Review 2026-11-15: B, D and E reworded away from the options of 0235. Key unchanged.
- Theory half of 0235 (pair: design.md, section 3.9). Different numbers from 0235, so one does not give away the other.
- No option rests on the risk-level mapping or the projection window of Time Remaining: both carry open review notes in vcf-operations/features/capacity-forecast.
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item B5). Counts only after author approval.
- I is at risk from a knowledge-base contradiction: knowledge/glossary.md (Usable capacity) adds hypervisor overhead, which vcf-operations/features/capacity-forecast and sp5-framework/capacity/supply leave out. The key follows capacity-forecast; fix the glossary line.
- Changed in the 2026-11-15 audit: K added (the largest-gap reading of the documentation wording); E reworded from an imperative to a statement.
- Changed 2026-11-16: A reworded. The old A (usable capacity minus the highest projected utilization) and K (the largest gap) were two readings of one definition, one the negation of the other. A now tests that the value fluctuates near usable capacity; the definition is still tested through F and K, and K keeps the documented trap.

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
misconception: [B, E, K]
misconception_type: [rollup-and-interval]
pair: "0235"
status: draft
```
