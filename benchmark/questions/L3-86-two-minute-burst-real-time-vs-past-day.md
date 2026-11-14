# A two-minute burst: Real-time vs past day

## Prompt
- A VM owner reports that his VM ran at full CPU for a couple of minutes this morning. He sends [the Real-time CPU chart](0432/vcenter-vm-cpu-usage-real-time.png).
- An hour later you open [the past-day CPU chart](0432/vcenter-vm-cpu-usage-past-day.png) of the same VM. The owner says the second chart is wrong, because it never shows the full peak.

Which statements are correct?

- A. The past-day chart is wrong: it should show the same peak as the Real-time chart.
- B. Each past-day point is the average of the 15 Real-time samples of its 5 minutes, busy and idle ones together.
- C. The Real-time chart shows the VM busy at close to its full CPU for about 2 minutes.
- D. The past-day chart shows that the VM ran at that lower level for the whole 5 minutes.
- E. Open a support case: vCenter dropped the peak samples during the rollup.
- F. A burst shorter than 5 minutes leaves no mark at all in the past-day chart.

## Input to supply
- Product and version: vSphere 9.1 (vSphere Client), vCenter at the default collection intervals and statistics level.
- Object: one VM with 2 or 4 vCPUs, otherwise idle.
- How to produce it: run a CPU burner on all vCPUs of the VM for 120 seconds (Linux: `stress-ng --cpu 0 --timeout 120s`; Windows: a stress tool with one busy thread per vCPU), starting 1 minute after a 5-minute mark (for example at 10:01:00), so that the whole burst falls inside one 5-minute point.
- Screen 1: the VM > Monitor > Performance > Advanced > CPU, Chart Options: Real-time, counter Usage (%), object the VM; capture within the hour, with the legend table (Latest, Maximum, Average). Save as `0432/vcenter-vm-cpu-usage-real-time.png`.
- Screen 2: the same chart with the period Last day, after the rollup has run (about 30 minutes later), zoomed or hovered so the point that holds the burst is readable. Save as `0432/vcenter-vm-cpu-usage-past-day.png`.
- Condition the key depends on: Real-time shows 5-7 consecutive samples at 90% or more, with the samples before and after below 10%; the past-day point that holds the burst reads between 30% and 50%, its neighbours below 10%.
- Masking: mask every VM, host, datastore and cluster name, including names in chart titles and legends.

## Likely wrong answer
A: the past-day chart is expected to keep the peak, so it is called wrong; E, the action that follows from it.

## Expected key points
- Answer: B, C.
- A false: the misconception. The 1 Day interval stores averages; a 20-second peak is diluted 15 times in a 5-minute point.
- B true: one 5-minute point is built from 15 Real-time samples of 20 seconds; about 6 busy samples at about 100% and 9 idle ones average to about 40%.
- C true: the Real-time samples show the burst: about 6 consecutive samples of 20 seconds near 100%.
- D false: a 5-minute average says nothing about how the load was spread inside the 5 minutes; the Real-time chart shows a short burst at full height, not a steady lower level.
- E false: the wrong action. The rollup averages by design; nothing was dropped.
- F false: the over-correction. The burst lifts the point that holds it by its share of the 15 samples; it is diluted, not erased.

## Notes
- Practical half of 0047 (pair: design.md, section 3.9).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item C8). The options hold for any capture that meets the condition above. Counts only after author approval.

## Metadata
```yaml
id: "0432"
title: "A two-minute burst: Real-time vs past day"
product: [vsphere]
technology: [cpu, system]
task: read-metric
level: 300
answer_type: deterministic
input: [screenshot]
object: [vm]
tool: [vcenter]
knowledge:
  - vsphere/tools/vsphere-client/vcenter-statistics
  - sp5-framework/observability/real-time-metrics
knowledge_main: vsphere/tools/vsphere-client/vcenter-statistics
attachments:
  - 0432/vcenter-vm-cpu-usage-real-time.png
  - 0432/vcenter-vm-cpu-usage-past-day.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C8"
answer: [B, C]
misconception: [A, E]
misconception_type: [rollup-and-interval]
pair: "0047"
status: awaiting-input
```
