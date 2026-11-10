# Collect every metric at 20 seconds

## Prompt
Why should I not collect every metrics? What if an incident happen and I'm not able to answer why? I also need them at 20 second, not 5 minute collection interval. This is why it's essential to collect them all.

## Likely wrong answer
Only the architecture view: database and collection overhead, maximum rollups, application monitoring. Misses the operations view: work backwards from what can go wrong, and 20-second peaks without 20-second collection.

## Expected key points
- Names the premise: "collect everything" means two dimensions, more metrics and more often. 2x the metrics at 20 seconds instead of 5 minutes is 30x the data points; a jump that size must justify its benefit.
- Begin with the end in mind: for each hardware, software, product and service that can go down or slow, list the metrics needed; work backwards. The list is far shorter and each metric serves a purpose.
- Input, Process, Output: a metric is an input; with no output (alert, dashboard, report, troubleshooting step) that uses it, collecting it is waste.
- 20-second visibility without 20-second collection: VCF Operations keeps the 20-second peak of each 5-minute cycle as its own metric.
- Answering "why" needs the right data, not all data: the failing component's metrics at the resolution that shows it, plus events, tasks and logs.
- Cost of the alternative: storage, collection load, retention.

## Notes
- Author's prompt to Gemini 3.1 Pro (high effort), 2026-11-10. Author: Gemini's answer is fairly good but focuses on architecture; the author's is an operations expert's view. Both are needed.
- Drafted by Claude 2026-11-10 from the knowledge files listed in `knowledge`. Counts only after author approval.

## Metadata
```yaml
id: "0094"
title: "Collect every metric at 20 seconds"
product: [vsphere, vcf-operations]
technology: [system]
input: [text]
task: judge-setting
knowledge:
  - observability/metric-volume
  - vcf-operations/features/peak-20-second-metrics
  - observability/collection-interval
attachments: []
origin: synthetic
source_path: "Author's prompt and Gemini 3.1 Pro exchange, 2026-11-10"
answer_type: judged
level: 300
status: draft
```
