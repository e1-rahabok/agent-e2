# Alert definitions in VCF Operations

## Parts of an alert definition
- The alert definition editor has 4 steps: Alert, Symptoms / Conditions, Recommendations, Policies.
- Each set of symptoms or conditions is defined on an object, for example Self (the object the alert is for).
- A set is met when Any, or All, of its symptoms or conditions are true. The recommended alerts use All: every symptom must hold at the same time, which narrows the alert. The catalog row of each alert gives its match.

## Symptom and condition
- A symptom and a condition are the same thing: a test on one metric, property or event, such as a metric above a value. The two names are a VCF Operations product detail.
- A symptom definition is stored on its own and reused by many alert definitions. A condition is written inside one alert definition and cannot be reused.
- A symptom that triggers without its alert is a minor issue: it belongs to the daily health check, not to an alert ([`sp5-framework/outputs/alerts-and-insights`](../sp5-framework/outputs/alerts-and-insights.md)).
- A condition has its own wait cycle, cancel cycle and severity, as a symptom definition does. No cycle setting is lost by using conditions.
- Write an alert's tests as conditions, not as shared symptom definitions. Two reasons:
  - meaning: a symptom triggered alone is a minor issue for the daily health check; an alert's own tests are not;
  - isolation: editing a shared symptom definition changes every alert that uses it, vendor alerts included; editing a condition changes one alert.
- The threshold catalog writes a test once, by id, so code can evaluate an alert and say why it fired. That is a data model for Agent E2, not the way to build the alert in VCF Operations.

## Wait cycle
- The wait cycle is how long a condition must stay true before the alert fires. It removes short spikes and false positives, and delays the alert by the same time.
- VCF Operations collects every 5 minutes, so a wait cycle counts collection cycles: 1, 2 and 3 cycles are 5, 10 and 15 minutes.
- How long each kind of alert should wait, and why: [`sp5-framework/outputs/alert-design`](../sp5-framework/outputs/alert-design.md), section Threshold design. The wait of each recommended alert: its catalog row.

## Recommendations
- A recommendation is advice attached to an alert; it changes nothing. A remediation action runs a change.
- A generic alert has many possible causes, so its recommendation list grows long. Add conditions inside the recommendation so only the relevant advice shows, with live, clickable data instead of plain text.

## Misconceptions
- "A condition and a symptom are different things" → they are the same test. A symptom definition is reusable; a condition lives inside one alert definition.
- "Reuse symptom definitions across alerts to save work" → one edit then changes every alert that uses the symptom, vendor alerts included. Use conditions.
- "A condition has no wait or cancel cycle" → it has both, and its own severity.
- "A longer wait cycle has no cost" → the alert fires that much later: 15 minutes of wait is 15 minutes lost.
- "Any of the conditions is enough" → the recommended alerts need all their symptoms together; that is what narrows them.
- "A recommendation fixes the problem" → it is advice. A remediation action changes the environment, and is riskier.

## Metadata
```yaml
id: vcf-operations/alert-definitions
retriever_guide: how-it-works
scope: vcf-operations
technology:
- system
pillar:
- availability
- performance
- capacity
product:
- vcf-operations
internal_derive:
- sp5-framework/outputs/alert-design
related:
- sp5-framework/outputs/alerts-and-insights
- sp5-framework/observability/collection-interval
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: 'Proactive Operations > Alert > Alerts Planning > Design > Threshold Design (Wait Cycle, Conditions); Recommendation | Remediation'
corrections: []
review_notes:
- 'Section ''Parts of an alert definition'': the steps, Defined On Self and Any or All are read from the source screenshot of the Edit Alert Definition page (Pod object). Screenshot not copied.'
- 'To check: Section ''Wait cycle'': collection every 5 minutes and wait cycle counted in collection cycles (VCF Operations 9.1 documentation on symptom definitions).'
- 'To check: Section ''Symptom and condition'': a condition''s wait cycle, cancel cycle and severity are the fields waitCycles, cancelCycles and severity of the data structure alert-condition, VCF Operations API 9.1.1 (https://developer.broadcom.com/xapis/vcf-operations-api/9.1.1/data-structures/alert-condition/).'
status: draft
```
