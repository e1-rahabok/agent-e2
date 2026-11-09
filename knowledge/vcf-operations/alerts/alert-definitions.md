# Alert definitions in VCF Operations

## Parts of an alert definition
- The alert definition editor has 4 steps: Alert, Symptoms / Conditions, Recommendations, Policies.
- Each set of symptoms or conditions is defined on an object, for example Self (the object the alert is for).
- A set is met when Any, or All, of its symptoms or conditions are true. The per-resource alerts in this knowledge base use All: every condition must hold at the same time.

## Conditions, not symptoms
- Build alerts from conditions, not from symptom definitions.
- In the author's design a symptom is a light, small problem that does not warrant an alert, like a mild body ache that goes away with rest. Symptoms belong to the daily health check (`sp5-framework/alerts/alerts-and-insights`).
- A condition is a test written inside the alert definition, such as a metric above a value.

## Wait cycle
- The wait cycle is how long a condition must stay true before the alert fires. It removes short spikes and false positives, and delays the alert by the same time.
- Values in the author's set:
  - contention: 5 minutes; 10 minutes where the metric tends to give false positives;
  - consumption: 15 minutes.
- VCF Operations collects every 5 minutes, so 5, 10 and 15 minutes are 1, 2 and 3 collection cycles.
- Wait cycle and threshold together: a 20-second peak above 4x the 5-minute threshold, plus the 5-minute average above the threshold, catches an issue that is both acute and sustained (`sp5-framework/alerts/alert-design`).

## Recommendations
- A recommendation is advice attached to an alert; it changes nothing. A remediation action runs a change.
- A generic alert has many possible causes, so its recommendation list grows long. Add conditions inside the recommendation so only the relevant advice shows, with live, clickable data instead of plain text.

## Traps
- "Reuse symptom definitions to build alerts" → in this design symptoms are minor issues for the daily check. Alerts are built from conditions.
- "A longer wait cycle has no cost" → the alert fires that much later: 15 minutes of wait is 15 minutes lost.
- "Any of the conditions is enough" → the per-resource alerts need all conditions together; that is what narrows them.
- "A recommendation fixes the problem" → it is advice. A remediation action changes the environment, and is riskier.

## Metadata
```yaml
id: vcf-operations/alerts/alert-definitions
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
- sp5-framework/alerts/alert-design
related:
- sp5-framework/alerts/alerts-and-insights
- observability/collection-interval
source:
  document: PART 2 - Consumption for Agent E2.docx
  path: 'Proactive Operations > Alert > Alerts Planning > Design > Threshold Design (Wait Cycle, Conditions); Recommendation | Remediation (pp. 15-16)'
corrections: []
review_notes:
- 'Section ''Parts of an alert definition'': the steps, Defined On Self and Any or All are read from the source screenshot of the Edit Alert Definition page (Pod object). Screenshot not copied.'
- 'Section ''Wait cycle'': collection every 5 minutes and wait cycle counted in collection cycles are Claude''s knowledge of VCF Operations; check against the VCF Operations 9.1 documentation on symptom definitions.'
- 'Section ''Conditions, not symptoms'': the definition of a condition (a test written inside the alert definition) is Claude''s reading of the screenshot, where Conditions and Symptoms are two tabs. Q143.'
status: draft
```
