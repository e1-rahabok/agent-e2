# How much a rollup dilutes a 20-second peak

## Prompt
- Last night a VM ran one 20-second burst of CPU at 100%; the rest of that hour it was idle.
- This morning you open its vCenter performance charts. vCenter keeps its default collection intervals and statistics level.

Which statements about how the burst shows in the vCenter charts are correct?

- A. In the 1 Day chart, the burst is diluted 15 times.
- B. In the 1 Week chart, the burst is diluted 90 times.
- C. In the 1 Day chart, the burst is diluted 288 times, once for each point of the day.
- D. The 1 Day chart shows the burst at full height, because each point keeps the highest sample of its 5 minutes.
- E. The burst leaves no trace in the 1 Day chart: a 5-minute point cannot carry a 20-second event.
- F. The Real-time chart still shows the burst at its 20-second height this morning.
- G. Raise the statistics level to 4 now, so the 1 Day chart shows the maximum of last night's burst.
- H. In the 1 Year chart, the burst is diluted 4,320 times.

## Likely wrong answer
C: 288 is the number of points per day, read as the dilution of one point. Or D: the chart is read as a chart of peaks.

## Expected key points
- Answer: A, B, H.
- A is true: one 1 Day point (5 minutes) averages 15 real-time samples of 20 seconds, so the burst counts for one fifteenth of the point.
- B is true: a 1 Week point (30 minutes) averages 6 points of 1 Day, so 6 × 15 = 90 samples of 20 seconds.
- C is false: 288 is how many 5-minute points a day holds; one point is built from 15 samples.
- D is false: the 1 Day chart shows averages; minimum and maximum rollups are stored only at statistics level 4.
- E is false: the over-correction. The burst lifts the point that holds it by one fifteenth of its height (a 100% burst on an otherwise idle VM gives a point of about 6.7%); it is diluted, not erased.
- F is false: the Real-time archive covers the last hour only.
- G is false: the wrong action. A statistics level applies from the moment it is set; counters that were not collected are not rebuilt, and level 4 everywhere grows the vCenter database and vpxd load.
- H is true: a 1 Year point covers one day, 86,400 / 20 = 4,320 samples.

## Notes
- Paired with the screenshot question 0432 (design.md, section 3.9).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): plural stem (was "By how much"), one fact per option, over-correction (E) and wrong action (G) added. Key changed from B to A, B, H.

## Metadata
```yaml
id: "0047"
title: "How much a rollup dilutes a 20-second peak"
product: [vsphere]
technology: [system]
task: read-metric
level: 200
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/tools/vsphere-client/vcenter-statistics
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05"
answer: [A, B, H]
misconception: [C, D]
object: [vm]
tool: [vcenter]
knowledge_main: vsphere/tools/vsphere-client/vcenter-statistics
misconception_type: [rollup-and-interval]
pair: "0432"
status: draft
```
