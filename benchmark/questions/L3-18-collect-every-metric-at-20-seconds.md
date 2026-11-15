# Collect every metric at 20 seconds

## Prompt
- A colleague writes: "Why should I not collect every metrics? What if an incident happen and I'm not able to answer why? I also need them at 20 second, not 5 minute collection interval. This is why it's essential to collect them all."

Which statements are correct?

- A. Collecting every metric every 20 seconds is the safe default, since any incident may turn on any metric.
- B. Collecting all metrics at 20 seconds multiplies two factors: how many metrics, and how many samples of each.
- C. Three times the metrics, collected every 20 seconds instead of every 5 minutes, gives about 45 times the data points.
- D. Build the metric list backwards: for each component that can fail or slow down, the metrics that reveal it.
- E. A metric that no alert, dashboard, report or troubleshooting step reads is a cost with no return.
- F. Seeing 20-second bursts after the fact requires collecting every metric every 20 seconds, not every 5 minutes.
- G. VCF Operations stores the highest 20-second value of each 5-minute cycle as a metric of its own.
- H. An incident is explained by the failing component's metrics at a resolution that shows the fault, plus events, tasks and logs.
- I. Raising the vCenter statistics level to 4 is the way to make VCF Operations collect more metrics from vCenter.
- J. In troubleshooting, the contention metrics, such as CPU Ready, are the ones that need data at 1-20 seconds.
- K. Capacity planning should read the 20-second peak metrics rather than the 5-minute or 15-minute averages.
- L. Collecting more often has a cost at the source too: vCenter or the host pays in performance or capacity.

## Likely wrong answer
- A: "Yes, collect everything at 20 seconds; storage is cheap and you never know what you will need."
- F: "Without 20-second collection you cannot see 20-second problems."

## Expected key points
- Answer: B, C, D, E, G, H, J, L.
- A is false: everything at 20 seconds is not needed to explain incidents, and it costs a lot; every metric collected should serve a purpose.
- B is true: more metrics and more often multiply.
- C is true: 3 × 15 = 45 times (20-second collection is 15 times the points of 5-minute collection); a jump of that size has to justify its benefit.
- D is true: begin with the end in mind and work backwards; the list is far shorter.
- E is true: input, process, output: a metric no output uses is waste.
- F is false: 20-second visibility does not need 20-second collection.
- G is true: VCF Operations stores the 20-second peak of each 5-minute cycle as a separate metric, not all 15 points.
- H is true: answering "why" depends on the right data, not all data.
- I is false: vCenter statistics levels do not apply to VCF Operations; it collects through its own policy.
- J is true: 1-20 second data is required for contention metrics; utilization and the other metrics are fine at 5 minutes.
- K is false: capacity uses about 15-minute averages, not peaks.
- L is true: the source may not produce the data, or pays a performance or capacity cost to produce it; high vCenter statistics levels raise vpxd load and database size.

## Notes
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): B, C, D, E, H paraphrased instead of copied from the knowledge file (C now asks for the arithmetic with other numbers); J restated as one fact in public words; A as one fact (author approved, 2026-11-14). Key unchanged.
- The author's own prompt to Gemini 3.1 Pro (high effort), 2026-11-10, kept in the author's words. Author: Gemini's answer is fairly good but stays at the architecture view; an operations expert works back from what can fail. Both are needed.
- Revised 2026-11-12: key points written in public words (benchmark/design.md, section 6.1).
- Converted from judged to multiple choice (Q199 F, 2026-11-14). The author's words are kept as the colleague's message.

## Metadata
```yaml
id: "0094"
title: "Collect every metric at 20 seconds"
product: [vsphere, vcf-operations]
technology: [system]
input: [text]
task: judge-setting
knowledge:
  - sp5-framework/observability/metric-volume
  - vcf-operations/features/peak-20-second-metrics
  - sp5-framework/observability/collection-interval
  - vsphere/tools/vsphere-client/vcenter-statistics
object: [vm, esxi]
tool: [vcenter, vcf-operations]
knowledge_main: sp5-framework/observability/metric-volume
attachments: []
origin: real-ticket
source_path: "Author's prompt and Gemini 3.1 Pro exchange, 2026-11-10"
answer_type: deterministic
answer: [B, C, D, E, G, H, J, L]
misconception: [A, F]
level: 300
misconception_type: [rollup-and-interval]
status: draft
```
