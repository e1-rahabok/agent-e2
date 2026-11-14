# Collect every metric at 20 seconds

## Prompt
Why should I not collect every metrics? What if an incident happen and I'm not able to answer why? I also need them at 20 second, not 5 minute collection interval. This is why it's essential to collect them all.

## Likely wrong answer
"Yes, collect everything at 20 seconds; storage is cheap and you never know what you will need." Or only the architecture view (database size, collection overhead, rollups), without saying which metrics are needed and why.

## Expected key points
- No: collecting everything at 20 seconds is not needed to explain incidents, and it costs a lot.
- "Everything" is two dimensions: more metrics and more often. Twice the metrics at 20 seconds instead of 5 minutes is about 30 times the data points (2 × 15); the benefit must justify it.
- Start from what can fail: for each component and service that can go down or slow, list the metrics that show it, and collect those. A metric that feeds no alert, dashboard, report or troubleshooting step is waste.
- 20-second visibility does not need 20-second collection: VCF Operations keeps the 20-second peak of each 5-minute cycle as its own metric, for the counters where bursts matter.
- Explaining an incident needs the failing component's metrics at the resolution that shows the problem, plus events, tasks and logs; not every metric.
- The cost side: storage, collection load on vCenter and the hosts, retention, and slower queries.

## Notes
- The author's own prompt to Gemini 3.1 Pro (high effort), 2026-11-10, kept in the author's words. Author: Gemini's answer is fairly good but stays at the architecture view; an operations expert works back from what can fail. Both are needed.
- Revised 2026-11-12: key points written in public words (benchmark/design.md, section 6.1).

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
object: [vm, esxi]
tool: [vcenter, vcf-operations]
knowledge_main: sp5-framework/observability/metric-volume
attachments: []
origin: real-ticket
source_path: "Author's prompt and Gemini 3.1 Pro exchange, 2026-11-10"
answer_type: judged
level: 300
misconception_type: [rollup-and-interval]
status: draft
```
