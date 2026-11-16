# The real-time sample interval

## Prompt
How often does ESXi sample its performance counters for the Real-time chart of the vSphere Client?

- A. Every 5 seconds
- B. Every 20 seconds
- C. Every 5 minutes
- D. Every 2 seconds

## Answers
B

## Explanation
- A is wrong: 5 seconds is the default refresh of esxtop, not the vCenter chart.
- B is correct: ESXi samples every 20 seconds; that is the Real-time chart.
- C is wrong: 5 minutes is the 1 Day interval, which vCenter rolls up from 15 real-time samples (then 30 minutes for 1 Week, 2 hours for 1 Month, 1 day for 1 Year).
- D is wrong: 2 seconds is the ESX Top tier of VCF Operations 9.1 and an esxtop refresh setting, not the vSphere Client Real-time chart.
- Misconception: C: 5 minutes is the 1 Day interval, built from real-time samples.

## Notes
- Synthetic, 2026-11-05, from the knowledge files listed in `knowledge`. Counts only after author approval.
- Changed in the 2026-11-15 audit: D (30 minutes, a weak distractor) replaced by 2 seconds, the VCF Operations ESX Top tier; the stem names the vSphere Client Real-time chart, so that tier is not real-time data in the sense of the question.

## Metadata
```yaml
id: "0035"
title: "The real-time sample interval"
product: [vsphere]
technology: [system]
task: read-metric
level: 100
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/tools/vsphere-client/vcenter-statistics
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-05"
misconception: [C]
object: [esxi, vm]
tool: [vcenter]
knowledge_main: vsphere/tools/vsphere-client/vcenter-statistics
misconception_type: [rollup-and-interval]
status: draft
```
