# Higher KPI, failed SLA

## Prompt
What's the difference between KPI and SLA? How can a VM has higher KPI than other VM but fail the same SLA? Provide a calculation showing clear example.

## Likely wrong answer
Treats the KPI as a raw metric averaged over time (higher is worse) and the SLA as a breach count per hour. Real SLA periods are calendar months, each 5-minute SLI is pass or fail, and the KPI is a score that reports how bad, reviewed daily.

## Expected key points
- SLA: a contract, relative to an agreed threshold. Every 5 minutes the SLI passes or fails at VM level on the 5-minute average; the SLA is the share of passed intervals over the calendar month; its target is per class of service.
- A fail is a fail: the SLI does not care how bad (just over the threshold and far over count the same).
- KPI: internal, absolute: it reports reality. A score of 0-100 (higher is better) from 20-second peaks of the worst vCPU or disk; reviewed daily (99th percentile of the day's scores); no class of service.
- SLA and KPI use different metrics, and the same metric at a different resolution. They are not mathematically related; their rankings can be opposite.
- A correct calculation: a VM that fails often but barely has the higher KPI yet fails the monthly SLA; a VM that fails rarely but severely passes the SLA with the lower KPI. The numbers use the calendar month and the 5-minute SLI.
- SLA is for the business, monthly; KPI is for the technical team, daily.

## Notes
- Author's prompt to Gemini 3.1 Pro (high effort), 2026-11-10. Gemini: overall concept right; mistake: applies an hourly SLA instead of a calendar month, and a raw-metric average as the KPI.
- Drafted by Claude 2026-11-10 from the knowledge files listed in `knowledge`. Counts only after author approval.

## Metadata
```yaml
id: "0092"
title: "Higher KPI, failed SLA"
product: [vsphere, vcf-operations]
technology: [system]
input: [text]
task: explain-mechanism
knowledge:
  - sp5-framework/performance/kpi-vs-sla
  - sp5-framework/concepts/sla-metrics
  - sp5-framework/performance/performance-kpi-design
attachments: []
origin: synthetic
source_path: "Author's prompt and Gemini 3.1 Pro exchange, 2026-11-10"
answer_type: judged
level: 300
status: draft
```
